#!/usr/bin/env python3
# generate_prompts.py - Main CLI Entry Point
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                      AI CHARACTER PROMPT PIPELINE                            │
# │                                                                              │
# │   TEXT SPEC  →  BASE PROMPTS  →  LLM REFINE  →  CHECKLIST  →  IMAGE GEN    │
# │   (YAML/JSON)    (Stage 1)       (Stage 2)      (Stage 3)     (Stage 4)    │
# │                                                                              │
# │   Stage 2: Uses OpenAI GPT (with web search) to refine prompts              │
# │   Stage 4: Generates T-pose images using Gemini API                         │
# │   Then manually: Upload to Hunyuan.3D → Download .fbx/.obj                  │
# └─────────────────────────────────────────────────────────────────────────────┘
#
# Usage:
#   uv run generate_prompts.py prompts -i configs/aethel.yaml   # Static prompts
#   uv run generate_prompts.py refine -i configs/aethel.yaml    # LLM-refined prompts
#   uv run generate_prompts.py images -i configs/aethel.yaml    # Generate images
#   uv run generate_prompts.py all -i configs/aethel.yaml       # Full pipeline
#
# This file is the THIN CLI LAYER that ties everything together.
# All the actual logic lives in the src/ modules.

from pathlib import Path
from typing import Annotated, Optional
from datetime import datetime
import sys
import os

# Load environment variables from .env file (if it exists)
# This allows storing API keys in a .env file instead of exporting them manually
from dotenv import load_dotenv
load_dotenv()  # Loads .env from current directory or parent directories

import typer

# -----------------------------------------------------------------------------
# IMPORTS FROM OUR MODULES
# -----------------------------------------------------------------------------
# We import from the src package, which contains all our pipeline logic.
# Each module handles one part of the pipeline.

# models.py: Character specification data model and file loading
from src.models import CharacterSpec, load_character_spec

# stage*_*.py: Prompt generators for each pipeline stage
from src.stage1_base_prompts import generate_base_prompts      # Stage 1: Base prompts
from src.stage2_gemini_prompts import generate_gemini_prompts  # Stage 2a: Gemini meta-prompts
from src.stage2_llm_refiner import (                           # Stage 2b: LLM refinement
    refine_prompts_to_dict,
    preview_llm_requests,
    OPENAI_API_KEY_ENV,
)
from src.stage3_common_prompts import generate_common_prompts  # Stage 3: Checklist/Notes
from src.stage4_image_generation import (                       # Stage 4: Image Gen
    generate_tpose_images,
    generate_image_prompts_only,
    save_generated_images,
    GEMINI_API_KEY_ENV,
)

# file_utils.py: File output utilities
from src.file_utils import write_prompts, print_prompts_to_stdout


# -----------------------------------------------------------------------------
# TIMESTAMPED OUTPUT FOLDER
# -----------------------------------------------------------------------------

def create_timestamped_output_dir(base_dir: Path) -> Path:
    """
    Create a timestamped output directory inside the base directory.
    
    Each run gets its own folder named with the current timestamp.
    Format: YYYY-MM-DD_HH-MM-SS
    
    Example: output/2024-12-09_15-30-45/
    
    Args:
        base_dir: The base output directory (e.g., Path("output"))
        
    Returns:
        Path to the new timestamped directory
    """
    # Generate timestamp string: 2024-12-09_15-30-45
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create the timestamped directory path
    timestamped_dir = base_dir / timestamp
    
    # Create the directory (and parents if needed)
    timestamped_dir.mkdir(parents=True, exist_ok=True)
    
    return timestamped_dir


# -----------------------------------------------------------------------------
# CLI APPLICATION SETUP
# -----------------------------------------------------------------------------
# Typer is a modern Python CLI framework built on Click.
# It uses type hints to automatically generate CLI argument parsing.

app = typer.Typer(
    # Name shown in help text
    name="generate_prompts",
    
    # Description shown when user runs --help
    help="Generate AI character prompts and images for the 2D → 3D pipeline.",
    
    # Disable shell completion script generation (simplifies the CLI)
    add_completion=False,
)


# -----------------------------------------------------------------------------
# PROMPT GENERATION FUNCTION
# -----------------------------------------------------------------------------

def generate_all_prompts(spec: CharacterSpec) -> dict[str, str]:
    """
    Generate all prompts for all pipeline stages (1-3).
    
    This function calls each stage's generator and merges the results
    into a single dictionary.
    
    Pipeline stages:
        Stage 1 (stage1_base_prompts.py):   Base 2D concept prompts
        Stage 2 (stage2_gemini_prompts.py): Gemini T-pose meta-prompts
        Stage 3 (stage3_common_prompts.py): Checklist and design notes
    
    Args:
        spec: The character specification
        
    Returns:
        A dictionary containing all prompts from all stages.
        Keys are like: "base_2d_full_body", "gemini_tpose_prompt", etc.
    """
    # Create an empty dictionary to hold all prompts
    all_prompts: dict[str, str] = {}
    
    # Stage 1: Generate base 2D prompts
    base_prompts = generate_base_prompts(spec)
    all_prompts.update(base_prompts)
    
    # Stage 2: Generate Gemini meta-prompts
    gemini_prompts = generate_gemini_prompts(spec)
    all_prompts.update(gemini_prompts)
    
    # Stage 3: Generate common documents
    common_prompts = generate_common_prompts(spec)
    all_prompts.update(common_prompts)
    
    return all_prompts


# -----------------------------------------------------------------------------
# COMMAND: prompts (Stages 1-3)
# -----------------------------------------------------------------------------

@app.command("prompts")
def generate_prompts_command(
    input_file: Annotated[
        Path,
        typer.Option(
            "--input", "-i",
            help="Path to character spec file (YAML or JSON)",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir", "-o",
            help="Base output directory for generated prompts",
        ),
    ] = Path("output"),
    version: Annotated[
        str,
        typer.Option(
            "--version", "-v",
            help="Version string suffix for filenames (e.g., v1, v2)",
        ),
    ] = "v1",
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Print prompts to stdout instead of writing files",
        ),
    ] = False,
) -> None:
    """
    Generate text prompts (Stages 1-3).
    
    Creates base 2D prompts, Gemini meta-prompts, checklist, and design notes.
    
    \b
    Example:
      uv run generate_prompts.py prompts -i configs/aethel.yaml -o prompts -v v1
    """
    # Step 1: Load the character specification
    print(f"Loading character spec from: {input_file}")
    
    try:
        spec = load_character_spec(input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        raise typer.Exit(code=1)
    
    print(f"Character: {spec.name} ({spec.role})")
    
    # Step 2: Generate all prompts
    print(f"Generating prompts (version: {version})...")
    prompts = generate_all_prompts(spec)
    
    # Step 3: Output
    if dry_run:
        print("\n[DRY RUN] Printing prompts to stdout:\n")
        print_prompts_to_stdout(prompts)
    else:
        # Create timestamped output directory
        run_output_dir = create_timestamped_output_dir(output_dir)
        print(f"Writing prompts to: {run_output_dir}/")
        
        written_paths = write_prompts(prompts, spec, run_output_dir, version)
        
        print(f"\nGenerated {len(written_paths)} files:")
        for path in written_paths:
            print(f"  ✓ {path}")
    
    print("\nDone!")


# -----------------------------------------------------------------------------
# COMMAND: refine (Stage 2b - LLM Refinement)
# -----------------------------------------------------------------------------

@app.command("refine")
def refine_prompts_command(
    input_file: Annotated[
        Path,
        typer.Option(
            "--input", "-i",
            help="Path to character spec file (YAML or JSON)",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir", "-o",
            help="Base output directory for refined prompts",
        ),
    ] = Path("output"),
    version: Annotated[
        str,
        typer.Option(
            "--version", "-v",
            help="Version string suffix for filenames (e.g., v1, v2)",
        ),
    ] = "v1",
    model: Annotated[
        str,
        typer.Option(
            "--model", "-m",
            help="OpenAI model to use (gpt-5, gpt-5-mini, gpt-4.1, etc.)",
        ),
    ] = "gpt-5",
    web_search: Annotated[
        bool,
        typer.Option(
            "--web-search",
            help="Enable web search for current AI art trends",
        ),
    ] = False,
    api_key: Annotated[
        Optional[str],
        typer.Option(
            "--api-key",
            help=f"OpenAI API key (or set {OPENAI_API_KEY_ENV} env var)",
            envvar=OPENAI_API_KEY_ENV,
        ),
    ] = None,
    preview_only: Annotated[
        bool,
        typer.Option(
            "--preview",
            help="Preview requests without making API calls",
        ),
    ] = False,
) -> None:
    """
    Refine prompts using OpenAI GPT (Stage 2b).
    
    Uses LLM to transform character specs into optimized image prompts.
    The refined prompts are ready to use directly in image generators.
    
    \b
    Example:
      export OPENAI_API_KEY='your-api-key'
      uv run generate_prompts.py refine -i configs/aethel.yaml -v v1
      
    \b
    With web search (for current AI art trends):
      uv run generate_prompts.py refine -i configs/aethel.yaml --web-search
      
    \b
    Preview mode (no API calls):
      uv run generate_prompts.py refine -i configs/aethel.yaml --preview
    """
    # Step 1: Load the character specification
    print(f"Loading character spec from: {input_file}")
    
    try:
        spec = load_character_spec(input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        raise typer.Exit(code=1)
    
    print(f"Character: {spec.name} ({spec.role})")
    
    # Step 2: Preview or refine
    if preview_only:
        # Preview mode: show what would be sent to the LLM
        print("\n[PREVIEW] Requests that would be sent to LLM:\n")
        requests = preview_llm_requests(spec)
        
        for key, request in requests.items():
            print(f"{'='*60}")
            print(f"=== {key} ===")
            print(f"{'='*60}\n")
            print(request)
            print()
        
        print("Done! (No API calls made)")
        
    else:
        # Full refinement mode
        print(f"\nRefining prompts with LLM (version: {version})...")
        
        # Check for API key
        if not api_key:
            api_key = os.environ.get(OPENAI_API_KEY_ENV)
        
        if not api_key:
            print(f"\nError: OpenAI API key required.", file=sys.stderr)
            print(f"Set the {OPENAI_API_KEY_ENV} environment variable:", file=sys.stderr)
            print(f"  export {OPENAI_API_KEY_ENV}='your-api-key'", file=sys.stderr)
            print(f"\nOr use the --api-key option:", file=sys.stderr)
            print(f"  --api-key 'your-api-key'", file=sys.stderr)
            print(f"\nOr use --preview to just see the requests.", file=sys.stderr)
            raise typer.Exit(code=1)
        
        try:
            # Refine prompts using LLM
            refined_prompts = refine_prompts_to_dict(
                spec=spec,
                api_key=api_key,
                model=model,
                use_web_search=web_search,
            )
            
            # Create timestamped output directory
            run_output_dir = create_timestamped_output_dir(output_dir)
            
            # Save refined prompts
            print(f"\nWriting refined prompts to: {run_output_dir}/")
            written_paths = write_prompts(refined_prompts, spec, run_output_dir, version)
            
            print(f"\nGenerated {len(written_paths)} refined prompt files:")
            for path in written_paths:
                print(f"  ✓ {path}")
            
        except ImportError as e:
            print(f"\nError: {e}", file=sys.stderr)
            raise typer.Exit(code=1)
            
        except Exception as e:
            print(f"\nError refining prompts: {e}", file=sys.stderr)
            raise typer.Exit(code=1)
    
    print("\nDone!")


# -----------------------------------------------------------------------------
# COMMAND: images (Stage 4)
# -----------------------------------------------------------------------------

@app.command("images")
def generate_images_command(
    input_file: Annotated[
        Path,
        typer.Option(
            "--input", "-i",
            help="Path to character spec file (YAML or JSON)",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir", "-o",
            help="Output directory for generated images",
        ),
    ] = Path("output/images"),
    version: Annotated[
        str,
        typer.Option(
            "--version", "-v",
            help="Version string suffix for filenames (e.g., v1, v2)",
        ),
    ] = "v1",
    views: Annotated[
        str,
        typer.Option(
            "--views",
            help="Comma-separated views to generate (front,side,back)",
        ),
    ] = "front,side,back",
    api_key: Annotated[
        Optional[str],
        typer.Option(
            "--api-key",
            help=f"Gemini API key (or set {GEMINI_API_KEY_ENV} env var)",
            envvar=GEMINI_API_KEY_ENV,
        ),
    ] = None,
    prompts_only: Annotated[
        bool,
        typer.Option(
            "--prompts-only",
            help="Only generate image prompts, don't call API",
        ),
    ] = False,
) -> None:
    """
    Generate T-pose images using Gemini API (Stage 4).
    
    Generates 3-view T-pose images (front, side, back) for 3D modeling.
    Requires GEMINI_API_KEY environment variable or --api-key option.
    
    \b
    Example:
      export GEMINI_API_KEY='your-api-key'
      uv run generate_prompts.py images -i configs/aethel.yaml -o output -v v1
      
    \b
    Prompts-only mode (no API calls):
      uv run generate_prompts.py images -i configs/aethel.yaml --prompts-only
    """
    # Step 1: Load the character specification
    print(f"Loading character spec from: {input_file}")
    
    try:
        spec = load_character_spec(input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        raise typer.Exit(code=1)
    
    print(f"Character: {spec.name} ({spec.role})")
    
    # Parse views
    view_list = [v.strip().lower() for v in views.split(",")]
    valid_views = ["front", "side", "back"]
    for v in view_list:
        if v not in valid_views:
            print(f"Error: Invalid view '{v}'. Valid views: {valid_views}", file=sys.stderr)
            raise typer.Exit(code=1)
    
    print(f"Views to generate: {', '.join(view_list)}")
    
    # Step 2: Generate images or prompts
    if prompts_only:
        # Prompts-only mode: just show the prompts that would be used
        print("\n[PROMPTS ONLY] Image generation prompts:\n")
        image_prompts = generate_image_prompts_only(spec, view_list)
        
        for key, prompt in image_prompts.items():
            print(f"{'='*60}")
            print(f"=== {key} ===")
            print(f"{'='*60}\n")
            print(prompt)
            print()
        
        print("Done! (No API calls made)")
        
    else:
        # Full image generation mode
        print(f"\nGenerating T-pose images (version: {version})...")
        
        # Check for API key
        if not api_key:
            api_key = os.environ.get(GEMINI_API_KEY_ENV)
        
        if not api_key:
            print(f"\nError: Gemini API key required.", file=sys.stderr)
            print(f"Set the {GEMINI_API_KEY_ENV} environment variable:", file=sys.stderr)
            print(f"  export {GEMINI_API_KEY_ENV}='your-api-key'", file=sys.stderr)
            print(f"\nOr use the --api-key option:", file=sys.stderr)
            print(f"  --api-key 'your-api-key'", file=sys.stderr)
            print(f"\nOr use --prompts-only to just see the prompts.", file=sys.stderr)
            raise typer.Exit(code=1)
        
        try:
            # Generate images
            images = generate_tpose_images(
                spec=spec,
                version=version,
                api_key=api_key,
                views=view_list,
            )
            
            # Create timestamped output directory
            run_output_dir = create_timestamped_output_dir(output_dir)
            
            # Save images
            print(f"\nSaving images to: {run_output_dir}/")
            saved_paths = save_generated_images(images, spec, run_output_dir, version)
            
            print(f"\nGenerated {len(saved_paths)} images:")
            for path in saved_paths:
                print(f"  ✓ {path}")
            
        except ImportError as e:
            print(f"\nError: {e}", file=sys.stderr)
            raise typer.Exit(code=1)
            
        except Exception as e:
            print(f"\nError generating images: {e}", file=sys.stderr)
            raise typer.Exit(code=1)
    
    print("\nDone!")


# -----------------------------------------------------------------------------
# COMMAND: all (Full pipeline)
# -----------------------------------------------------------------------------

@app.command("all")
def generate_all_command(
    input_file: Annotated[
        Path,
        typer.Option(
            "--input", "-i",
            help="Path to character spec file (YAML or JSON)",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir", "-o",
            help="Base output directory for all generated files",
        ),
    ] = Path("output"),
    version: Annotated[
        str,
        typer.Option(
            "--version", "-v",
            help="Version string suffix for filenames",
        ),
    ] = "v1",
    skip_refine: Annotated[
        bool,
        typer.Option(
            "--skip-refine",
            help="Skip LLM refinement (use static prompts only)",
        ),
    ] = False,
    web_search: Annotated[
        bool,
        typer.Option(
            "--web-search",
            help="Enable web search for LLM refinement",
        ),
    ] = False,
    skip_images: Annotated[
        bool,
        typer.Option(
            "--skip-images",
            help="Skip image generation (only generate prompts)",
        ),
    ] = False,
) -> None:
    """
    Run the full pipeline (Stages 1-4).
    
    Generates static prompts, refines with LLM, and creates T-pose images.
    
    \b
    Required API keys:
      - OPENAI_API_KEY: For LLM refinement (Stage 2)
      - GEMINI_API_KEY: For image generation (Stage 4)
    
    \b
    Example (full pipeline):
      export OPENAI_API_KEY='your-openai-key'
      export GEMINI_API_KEY='your-gemini-key'
      uv run generate_prompts.py all -i configs/aethel.yaml -v v1
    
    \b
    Example (skip refinement):
      uv run generate_prompts.py all -i configs/aethel.yaml --skip-refine
    """
    # Step 1: Load spec
    print(f"Loading character spec from: {input_file}")
    
    try:
        spec = load_character_spec(input_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        raise typer.Exit(code=1)
    
    print(f"Character: {spec.name} ({spec.role})")
    
    # Create timestamped output directory for this run
    run_output_dir = create_timestamped_output_dir(output_dir)
    print(f"\nOutput directory: {run_output_dir}/")
    
    # Step 2: Generate static prompts (Stages 1, 2a, 3)
    print(f"\n{'='*60}")
    print("STAGE 1 & 3: Generating static prompts...")
    print(f"{'='*60}")
    
    prompts = generate_all_prompts(spec)
    written_prompt_paths = write_prompts(prompts, spec, run_output_dir, version)
    
    print(f"Generated {len(written_prompt_paths)} static prompt files")
    
    # Step 3: LLM Refinement (Stage 2b)
    if not skip_refine:
        print(f"\n{'='*60}")
        print("STAGE 2: Refining prompts with LLM...")
        print(f"{'='*60}")
        
        openai_key = os.environ.get(OPENAI_API_KEY_ENV)
        
        if not openai_key:
            print(f"\nWarning: {OPENAI_API_KEY_ENV} not set. Skipping LLM refinement.")
            print("Set the environment variable to enable LLM refinement.")
        else:
            try:
                refined_prompts = refine_prompts_to_dict(
                    spec=spec,
                    api_key=openai_key,
                    use_web_search=web_search,
                )
                refined_paths = write_prompts(refined_prompts, spec, run_output_dir, version)
                print(f"Generated {len(refined_paths)} refined prompt files")
            except Exception as e:
                print(f"Warning: LLM refinement failed: {e}")
                print("Static prompts were still generated successfully.")
    else:
        print("\n(LLM refinement skipped)")
    
    # Step 4: Generate images (Stage 4)
    if not skip_images:
        print(f"\n{'='*60}")
        print("STAGE 4: Generating T-pose images...")
        print(f"{'='*60}")
        
        gemini_key = os.environ.get(GEMINI_API_KEY_ENV)
        images_dir = run_output_dir / "images"
        
        if not gemini_key:
            print(f"\nWarning: {GEMINI_API_KEY_ENV} not set. Skipping image generation.")
            print("Set the environment variable to enable image generation.")
        else:
            try:
                images = generate_tpose_images(spec, version, gemini_key)
                saved_image_paths = save_generated_images(images, spec, images_dir, version)
                print(f"Generated {len(saved_image_paths)} images")
            except Exception as e:
                print(f"Warning: Image generation failed: {e}")
                print("Prompts were still generated successfully.")
    else:
        print("\n(Image generation skipped)")
    
    print(f"\n{'='*60}")
    print("PIPELINE COMPLETE!")
    print(f"{'='*60}")
    print(f"  Output: {run_output_dir}/")
    print("\nDone!")


# -----------------------------------------------------------------------------
# SCRIPT ENTRY POINT
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app()
