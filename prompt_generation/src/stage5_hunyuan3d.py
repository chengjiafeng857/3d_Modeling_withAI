# stage5_hunyuan3d.py - Stage 5: Hunyuan 3D Model Generation
#
# Pipeline Stage: Text Spec → 2D Prompts → T-pose Images → [HUNYUAN 3D API]
#                                                          ^^^^^^^^^^^^^^^
#                                                          THIS STAGE
#
# This module orchestrates the Hunyuan 3D API workflow:
#   1. Submit a job (with prompt OR image OR image_url)
#   2. Poll for completion with timeout and backoff
#   3. Download results (ZIP with .obj, .mtl, textures)
#   4. Extract and identify the main .obj file
#   5. Write metadata.json with job info
#
# REQUIRES:
#   - TENCENT_SECRET_ID: Tencent Cloud SecretId
#   - TENCENT_SECRET_KEY: Tencent Cloud SecretKey
#   - TENCENT_COS_BUCKET: COS bucket for image uploads (optional)
#   - TENCENT_COS_REGION: COS region (optional)

import json
import os
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from .providers import (
    RawHttpHunyuan3DProvider,
    SDKHunyuan3DProvider,
    TencentCOSUploader,
    SDKCOSUploader,
    get_cos_uploader,
    Hunyuan3DJobResult,
    Hunyuan3DAPIError,
    JobStatus,
    ViewImage,
    VALID_VIEW_TYPES,
    TENCENT_SECRET_ID_ENV,
    TENCENT_SECRET_KEY_ENV,
    TENCENT_COS_BUCKET_ENV,
    TENCENT_COS_REGION_ENV,
    get_provider,
    is_sdk_available,
    get_sdk_install_instructions,
)

# Re-export env var names for convenience
__all__ = [
    "generate_3d_model",
    "generate_3d_from_prompt",
    "generate_3d_from_image",
    "generate_3d_from_url",
    "check_required_env_vars",
    "get_env_var_help",
    "Hunyuan3DResult",
    "Hunyuan3DMetadata",
    "TENCENT_SECRET_ID_ENV",
    "TENCENT_SECRET_KEY_ENV",
    # Provider selection
    "VALID_PROVIDERS",
    "is_sdk_available",
    # Multi-view support
    "ViewImage",
    "VALID_VIEW_TYPES",
]

# Valid provider types
VALID_PROVIDERS = ("http", "sdk")


# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------

# Polling configuration
DEFAULT_POLL_INTERVAL = 10  # seconds between polls
DEFAULT_TIMEOUT = 600  # 10 minutes total timeout
MAX_POLL_INTERVAL = 60  # max backoff interval

# File patterns for identifying main model
OBJ_EXTENSION = ".obj"
MTL_EXTENSION = ".mtl"
TEXTURE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tga", ".bmp")


# -----------------------------------------------------------------------------
# DATA CLASSES
# -----------------------------------------------------------------------------

@dataclass
class Hunyuan3DResult:
    """
    Result of a Hunyuan 3D generation job.
    
    Attributes:
        job_id: The Hunyuan job ID
        status: Final job status (DONE or FAIL)
        obj_path: Path to the main .obj file (if successful)
        all_files: List of all downloaded files
        metadata_path: Path to the metadata.json file
        error_message: Error message (if failed)
        elapsed_seconds: Total time taken
    """
    job_id: str
    status: str
    obj_path: Optional[Path] = None
    all_files: list[Path] = None
    metadata_path: Optional[Path] = None
    error_message: Optional[str] = None
    elapsed_seconds: float = 0.0
    
    def __post_init__(self):
        if self.all_files is None:
            self.all_files = []


@dataclass
class Hunyuan3DMetadata:
    """
    Metadata about a Hunyuan 3D job for the metadata.json file.
    
    Attributes:
        job_id: Hunyuan job ID
        status: Final status
        input_type: Type of input (prompt, image, image_url)
        input_value: The actual input value
        created_at: ISO timestamp of job creation
        completed_at: ISO timestamp of job completion
        elapsed_seconds: Time taken
        files: List of generated file names
        main_obj: Name of the main .obj file
    """
    job_id: str
    status: str
    input_type: str
    input_value: str
    created_at: str
    completed_at: str
    elapsed_seconds: float
    files: list[str]
    main_obj: Optional[str] = None
    error_message: Optional[str] = None


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def _find_largest_obj(files: list[Path]) -> Optional[Path]:
    """
    Find the largest .obj file in a list of files.
    
    The largest .obj file is typically the main model,
    as smaller .obj files might be accessories or LOD versions.
    
    Args:
        files: List of file paths
        
    Returns:
        Path to the largest .obj file, or None if no .obj found
    """
    obj_files = [f for f in files if f.suffix.lower() == OBJ_EXTENSION]
    
    if not obj_files:
        return None
    
    # Sort by file size descending and return the largest
    return max(obj_files, key=lambda f: f.stat().st_size if f.exists() else 0)


def _validate_inputs(
    prompt: Optional[str],
    image: Optional[Path],
    image_url: Optional[str],
) -> tuple[str, str]:
    """
    Validate that exactly one input is provided.
    
    Args:
        prompt: Text prompt
        image: Local image path
        image_url: Remote image URL
        
    Returns:
        Tuple of (input_type, input_value)
        
    Raises:
        ValueError: If not exactly one input is provided
    """
    inputs = [
        ("prompt", prompt),
        ("image", str(image) if image else None),
        ("image_url", image_url),
    ]
    
    provided = [(t, v) for t, v in inputs if v]
    
    if len(provided) == 0:
        raise ValueError(
            "Must provide exactly one of: prompt, image, or image_url"
        )
    
    if len(provided) > 1:
        types = [t for t, v in provided]
        raise ValueError(
            f"Provide only ONE input. Got: {', '.join(types)}"
        )
    
    return provided[0]


# -----------------------------------------------------------------------------
# MAIN ORCHESTRATION FUNCTION
# -----------------------------------------------------------------------------

def generate_3d_model(
    *,
    prompt: Optional[str] = None,
    image: Optional[Path] = None,
    image_url: Optional[str] = None,
    left_view: Optional[Path] = None,
    right_view: Optional[Path] = None,
    back_view: Optional[Path] = None,
    output_dir: Path,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    timeout: int = DEFAULT_TIMEOUT,
    verbose: bool = True,
    provider_type: str = "http",
) -> Hunyuan3DResult:
    """
    Generate a 3D model using the Hunyuan 3D API.
    
    This is the main orchestration function that:
    1. Validates inputs (exactly one of prompt/image/image_url)
    2. Uploads local image(s) to COS if needed
    3. Submits the job to Hunyuan 3D (with optional multi-view images)
    4. Polls for completion with exponential backoff
    5. Downloads and extracts results
    6. Writes metadata.json
    
    Args:
        prompt: Text description to generate 3D model from
        image: Path to local image to convert to 3D (front view)
        image_url: URL of image to convert to 3D
        left_view: Optional path to left view image
        right_view: Optional path to right view image
        back_view: Optional path to back view image
        output_dir: Directory to save results
        poll_interval: Initial seconds between status polls
        timeout: Maximum seconds to wait for completion
        verbose: Print progress messages
        provider_type: "http" (default, no SDK) or "sdk" (requires SDK)
        
    Returns:
        Hunyuan3DResult with paths to downloaded files
        
    Raises:
        ValueError: If inputs are invalid
        Hunyuan3DAPIError: If the API returns an error
        TimeoutError: If job doesn't complete within timeout
        ImportError: If SDK provider requested but SDK not installed
        
    Example:
        result = generate_3d_model(
            prompt="A cute panda figurine",
            output_dir=Path("output/hunyuan3d/2024-01-01_12-00-00"),
        )
        print(f"Main OBJ: {result.obj_path}")
        
        # With multi-view images for better 3D reconstruction
        result = generate_3d_model(
            image=Path("front.png"),
            left_view=Path("left.png"),
            right_view=Path("right.png"),
            back_view=Path("back.png"),
            output_dir=Path("output"),
        )
    """
    start_time = time.time()
    created_at = datetime.now().isoformat()
    
    # Validate provider type
    if provider_type not in VALID_PROVIDERS:
        raise ValueError(
            f"Invalid provider_type: {provider_type}. "
            f"Valid options: {', '.join(VALID_PROVIDERS)}"
        )
    
    # Step 1: Validate inputs
    input_type, input_value = _validate_inputs(prompt, image, image_url)
    
    if verbose:
        print(f"Input: {input_type} = {input_value[:50]}..." if len(input_value) > 50 else f"Input: {input_type} = {input_value}")
        print(f"Provider: {provider_type}")
    
    # Step 2: Upload local images to COS if needed
    final_image_url = image_url
    multi_view_images: list[ViewImage] = []
    
    # Use SDK-based COS uploader (more reliable than raw HTTP)
    uploader = None
    if image or left_view or right_view or back_view:
        uploader = get_cos_uploader(use_sdk=True)
    
    # Upload main/front image
    if image:
        if verbose:
            print(f"Uploading front image to Tencent COS...")
        final_image_url = uploader.upload_file(Path(image))
        if verbose:
            print(f"  ✓ Front: {final_image_url[:60]}...")
    
    # Upload multi-view images
    view_uploads = [
        ("left", left_view),
        ("right", right_view),
        ("back", back_view),
    ]
    
    for view_name, view_path in view_uploads:
        if view_path:
            if verbose:
                print(f"Uploading {view_name} view to Tencent COS...")
            view_url = uploader.upload_file(Path(view_path))
            multi_view_images.append(ViewImage(view=view_name, image_url=view_url))
            if verbose:
                print(f"  ✓ {view_name.capitalize()}: {view_url[:60]}...")
    
    # Step 3: Create provider and submit job
    if verbose:
        print("Submitting job to Hunyuan 3D API...")
        if multi_view_images:
            print(f"  (with {len(multi_view_images)} additional view(s))")
    
    # Get provider class based on type
    provider_class = get_provider(provider_type)
    provider = provider_class()
    
    job_id = provider.submit(
        prompt=prompt,
        image_url=final_image_url,
        multi_view_images=multi_view_images if multi_view_images else None,
    )
    
    if verbose:
        print(f"  ✓ Job ID: {job_id}")
    
    # Step 4: Poll for completion with exponential backoff
    if verbose:
        print(f"Polling for completion (timeout: {timeout}s)...")
    
    current_interval = poll_interval
    elapsed = 0
    result: Optional[Hunyuan3DJobResult] = None
    
    while elapsed < timeout:
        time.sleep(current_interval)
        elapsed = time.time() - start_time
        
        result = provider.poll(job_id)
        
        if verbose:
            print(f"  [{int(elapsed)}s] Status: {result.status.value}")
        
        if result.status == JobStatus.DONE:
            break
        elif result.status == JobStatus.FAIL:
            error_msg = result.error_message or "Unknown error"
            return Hunyuan3DResult(
                job_id=job_id,
                status="FAIL",
                error_message=error_msg,
                elapsed_seconds=elapsed,
            )
        
        # Exponential backoff with cap
        current_interval = min(current_interval * 1.5, MAX_POLL_INTERVAL)
    
    if result is None or result.status not in (JobStatus.DONE, JobStatus.FAIL):
        raise TimeoutError(
            f"Job {job_id} did not complete within {timeout} seconds"
        )
    
    # Step 5: Download and extract results
    if verbose:
        print("Downloading results...")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded_files = provider.download_result(result, output_dir)
    
    if verbose:
        print(f"  ✓ Downloaded {len(downloaded_files)} files")
        for f in downloaded_files:
            print(f"    - {f.name}")
    
    # Step 6: Find the main .obj file
    main_obj = _find_largest_obj(downloaded_files)
    
    if verbose and main_obj:
        print(f"  ✓ Main OBJ: {main_obj.name}")
    
    # Step 7: Write metadata.json
    completed_at = datetime.now().isoformat()
    total_elapsed = time.time() - start_time
    
    metadata = Hunyuan3DMetadata(
        job_id=job_id,
        status="DONE",
        input_type=input_type,
        input_value=input_value,
        created_at=created_at,
        completed_at=completed_at,
        elapsed_seconds=total_elapsed,
        files=[f.name for f in downloaded_files],
        main_obj=main_obj.name if main_obj else None,
    )
    
    metadata_path = output_dir / "metadata.json"
    metadata_path.write_text(
        json.dumps(asdict(metadata), indent=2),
        encoding="utf-8",
    )
    
    if verbose:
        print(f"  ✓ Metadata: {metadata_path.name}")
    
    return Hunyuan3DResult(
        job_id=job_id,
        status="DONE",
        obj_path=main_obj,
        all_files=downloaded_files,
        metadata_path=metadata_path,
        elapsed_seconds=total_elapsed,
    )


# -----------------------------------------------------------------------------
# CONVENIENCE FUNCTIONS
# -----------------------------------------------------------------------------

def generate_3d_from_prompt(
    prompt: str,
    output_dir: Path,
    **kwargs,
) -> Hunyuan3DResult:
    """
    Generate a 3D model from a text prompt.
    
    Convenience wrapper around generate_3d_model().
    
    Args:
        prompt: Text description of the 3D model
        output_dir: Directory to save results
        **kwargs: Additional arguments passed to generate_3d_model()
        
    Returns:
        Hunyuan3DResult with paths to files
    """
    return generate_3d_model(prompt=prompt, output_dir=output_dir, **kwargs)


def generate_3d_from_image(
    image: Path,
    output_dir: Path,
    **kwargs,
) -> Hunyuan3DResult:
    """
    Generate a 3D model from a local image.
    
    The image will be uploaded to Tencent COS first.
    
    Args:
        image: Path to local image file
        output_dir: Directory to save results
        **kwargs: Additional arguments passed to generate_3d_model()
        
    Returns:
        Hunyuan3DResult with paths to files
    """
    return generate_3d_model(image=image, output_dir=output_dir, **kwargs)


def generate_3d_from_url(
    image_url: str,
    output_dir: Path,
    **kwargs,
) -> Hunyuan3DResult:
    """
    Generate a 3D model from an image URL.
    
    Args:
        image_url: URL of the image to convert
        output_dir: Directory to save results
        **kwargs: Additional arguments passed to generate_3d_model()
        
    Returns:
        Hunyuan3DResult with paths to files
    """
    return generate_3d_model(image_url=image_url, output_dir=output_dir, **kwargs)


# -----------------------------------------------------------------------------
# ENVIRONMENT VARIABLE CHECKERS
# -----------------------------------------------------------------------------

def check_required_env_vars(include_cos: bool = False) -> list[str]:
    """
    Check if required environment variables are set.
    
    Args:
        include_cos: Also check COS variables (for image uploads)
        
    Returns:
        List of missing environment variable names
    """
    required = [TENCENT_SECRET_ID_ENV, TENCENT_SECRET_KEY_ENV]
    
    if include_cos:
        required.extend([TENCENT_COS_BUCKET_ENV, TENCENT_COS_REGION_ENV])
    
    return [var for var in required if not os.environ.get(var)]


def get_env_var_help() -> str:
    """
    Get help text for setting up environment variables.
    
    Returns:
        Help text string
    """
    return f"""
Required environment variables for Hunyuan 3D:

  {TENCENT_SECRET_ID_ENV}   - Tencent Cloud SecretId
  {TENCENT_SECRET_KEY_ENV}  - Tencent Cloud SecretKey

For image uploads (--image option), also set:

  {TENCENT_COS_BUCKET_ENV}  - COS bucket name (e.g., "mybucket-1250000000")
  {TENCENT_COS_REGION_ENV}  - COS region (e.g., "ap-guangzhou")

Get credentials at: https://console.cloud.tencent.com/cam/capi

Add to your .env file:
  {TENCENT_SECRET_ID_ENV}=your-secret-id
  {TENCENT_SECRET_KEY_ENV}=your-secret-key
  {TENCENT_COS_BUCKET_ENV}=your-bucket-name
  {TENCENT_COS_REGION_ENV}=ap-guangzhou
"""
