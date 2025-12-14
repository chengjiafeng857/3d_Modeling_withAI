# AI Character Prompt Pipeline - Teaching Guide

> A comprehensive guide to understanding the codebase architecture, design patterns, and Python concepts demonstrated in this project.

**🔗 Related Documentation:**
- [README.md](./README.md) - Project overview and quick start
- [COURSE_MATERIALS_GUIDE.md](./COURSE_MATERIALS_GUIDE.md) - **Full teaching materials** (slides, tutorials, assessments, video scripts)
- [prompt_generation/README.md](./prompt_generation/README.md) - CLI usage documentation

---

## 📚 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture & Data Flow](#2-architecture--data-flow)
3. [Module Deep Dive](#3-module-deep-dive)
4. [Python Concepts Demonstrated](#4-python-concepts-demonstrated)
5. [API Integration Patterns](#5-api-integration-patterns)
6. [Design Patterns Used](#6-design-patterns-used)
7. [Code Walkthrough](#7-code-walkthrough)
8. [Extension Points](#8-extension-points)

---

## 1. Project Overview

### 1.1 What This Project Does

This is a **7-stage AI pipeline** that transforms a simple text description of a game character into a playable, animated 3D character in Unreal Engine.

**Currently Implemented (Stages 1-3):**
1. Optimized text prompts for AI image generators
2. Actual T-pose images ready for 3D modeling

**Planned (Stages 4-7):**
3. 3D mesh from Hunyuan.3D
4. Auto-rigged animations from MexMiao
5. Quality assessment with Eval3D
6. Game-ready character in Unreal Engine 5

### 1.2 The Pipeline Stages

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AI-DRIVEN CHARACTER ASSET PIPELINE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐         │
│   │  Stage 1  │ →  │  Stage 2  │ →  │  Stage 3  │ →  │  Stage 4  │         │
│   │ Character │    │  Prompt   │    │    2D     │    │    3D     │         │
│   │   Spec    │    │ Refine    │    │  T-Pose   │    │  Model    │         │
│   │  (YAML)   │    │  (GPT-5)  │    │ (Gemini)  │    │(Hunyuan)  │         │
│   └───────────┘    └───────────┘    └───────────┘    └───────────┘         │
│        │                │                │                │                 │
│        ▼                ▼                ▼                ▼                 │
│   Character         Optimized        Front/Side/       Rigged             │
│   Definition        Prompts          Back Images       .fbx/.obj          │
│                                                                              │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐                          │
│   │  Stage 5  │ →  │  Stage 6  │ →  │  Stage 7  │                          │
│   │   Rig +   │    │  Eval3D   │    │  Unreal   │                          │
│   │ Animation │    │Assessment │    │Integration│                          │
│   │(MexMiao)  │    │ Pipeline  │    │   (UE5)   │                          │
│   └───────────┘    └───────────┘    └───────────┘                          │
│                                                                              │
│   ✅ Implemented: Stages 1-3 (this codebase)                                │
│   🔜 Planned: Stages 4-7                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Technology Stack

| Stage | Tool | Purpose | API/Interface |
|-------|------|---------|---------------|
| 1-2 | **Python + Typer** | Character spec → prompts | CLI |
| 2 | **OpenAI GPT-5** | Prompt refinement | REST API |
| 3 | **Gemini 3 Pro** | T-pose image generation | REST API |
| 4 | **Tencent Hunyuan.3D** | 2D → 3D conversion | Web UI |
| 5 | **Meshy / MexMiao** | Auto-rigging + animation | Web UI |
| 6 | **Eval3D Pipeline** | Quality assessment | CLI |
| 7 | **Unreal Engine 5** | Game integration | Editor |

---

## 2. Architecture & Data Flow

### 2.1 Directory Structure

```
prompt_generation/
├── generate_prompts.py          # 🎯 CLI Entry Point (thin layer)
├── src/                         # 📦 Core Logic Package
│   ├── __init__.py              #    Package exports
│   ├── models.py                #    Data models (CharacterSpec)
│   ├── stage1_base_prompts.py   #    Static prompt templates
│   ├── stage2_gemini_prompts.py #    Meta-prompts for Gemini
│   ├── stage2_llm_refiner.py    #    OpenAI GPT integration
│   ├── stage3_common_prompts.py #    Human documents (checklists)
│   ├── stage4_image_generation.py #  Gemini image generation
│   └── file_utils.py            #    File I/O utilities
├── configs/                     # 📝 Character Specifications
│   ├── _template.yaml           #    Template with documentation
│   └── aethel.yaml              #    Example character
└── output/                      # 📁 Generated Outputs
    └── {timestamp}/             #    Each run in separate folder
```

### 2.2 Data Flow Diagram

```
┌──────────────────┐
│  configs/*.yaml  │  ← Human writes character spec
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    models.py     │  ← Parse YAML → CharacterSpec dataclass
│  CharacterSpec   │
└────────┬─────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Stage 1│ │Stage 2│ │Stage 3│ │Stage 4│
│ Base  │ │  LLM  │ │Common │ │ Image │
│Prompts│ │Refiner│ │ Docs  │ │  Gen  │
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │         │         │
    ▼         ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│ .txt  │ │ .txt  │ │ .txt  │ │ .jpg  │
│ files │ │ files │ │ files │ │ files │
└───────┘ └───────┘ └───────┘ └───────┘
```

### 2.3 Module Dependencies

```
generate_prompts.py (CLI)
        │
        ├── src/models.py           (CharacterSpec, load_character_spec)
        ├── src/stage1_base_prompts.py  (generate_base_prompts)
        ├── src/stage2_gemini_prompts.py (generate_gemini_prompts)
        ├── src/stage2_llm_refiner.py   (refine_prompts_to_dict)
        ├── src/stage3_common_prompts.py (generate_common_prompts)
        ├── src/stage4_image_generation.py (generate_tpose_images)
        └── src/file_utils.py       (write_prompts)

Internal dependencies:
  stage1 ← models (uses CharacterSpec)
  stage2_gemini ← models, stage1 (reuses helper functions)
  stage2_llm ← models, stage1 (reuses helper functions)
  stage3 ← models, stage1 (reuses helper functions)
  stage4 ← models, stage1 (reuses helper functions)
  file_utils ← models (uses CharacterSpec for filenames)
```

---

## 3. Module Deep Dive

### 3.1 `models.py` - Data Models

**Purpose:** Define the core data structure and file loading logic.

**Key Concepts:**
- `@dataclass` decorator for automatic `__init__`, `__repr__`
- `field(default_factory=list)` for mutable defaults
- `Optional[str]` for nullable fields
- YAML/JSON parsing with error handling

```python
@dataclass
class CharacterSpec:
    """Data model for a character specification."""
    
    # Required field (no default)
    name: str
    
    # Optional fields with defaults
    role: str = ""
    game_style: str = ""
    silhouette: str = ""
    
    # Mutable defaults MUST use default_factory
    # Using = [] would share the same list across ALL instances!
    color_palette: list[str] = field(default_factory=list)
    key_props: list[str] = field(default_factory=list)
    animation_focus: list[str] = field(default_factory=list)
    
    # Nullable field
    extra_notes: Optional[str] = None
```

**Why `default_factory=list`?**
```python
# ❌ WRONG - All instances share the same list!
class Bad:
    items: list[str] = []

# ✅ CORRECT - Each instance gets a new list
class Good:
    items: list[str] = field(default_factory=list)
```

---

### 3.2 `stage1_base_prompts.py` - Static Templates

**Purpose:** Generate base prompts using simple string formatting.

**Key Concepts:**
- Helper functions for formatting (DRY principle)
- f-strings for template interpolation
- Dictionary return type for multiple outputs

```python
def format_key_props(props: list[str]) -> str:
    """Format props into natural English phrase."""
    if not props:
        return "no specific props"
    if len(props) == 1:
        return f"a {props[0]}"
    if len(props) == 2:
        return f"a {props[0]} and a {props[1]}"
    # Oxford comma for 3+ items
    items = [f"a {prop}" for prop in props[:-1]]
    return ", ".join(items) + f", and a {props[-1]}"

# Example:
# format_key_props(["sword", "shield", "helmet"])
# → "a sword, a shield, and a helmet"
```

**Main Export Pattern:**
```python
def generate_base_prompts(spec: CharacterSpec) -> dict[str, str]:
    """Main function other modules should call."""
    return {
        "base_2d_full_body": generate_base_2d_full_body(spec),
        "base_2d_sheet": generate_base_2d_sheet(spec),
    }
```

---

### 3.3 `stage2_llm_refiner.py` - OpenAI Integration

**Purpose:** Use GPT-5 to transform specs into optimized prompts.

**Key Concepts:**
- Environment variable handling
- API client initialization
- System prompts vs user prompts
- Responses API with web_search tool

**Architecture:**
```
┌─────────────────────┐
│   System Prompt     │  ← Defines AI's role & rules
│   (Expert Engineer) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   User Request      │  ← Character spec + instructions
│   (Character Spec)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   OpenAI GPT-5      │  ← Responses API
│   + web_search tool │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Refined Prompt    │  ← Ready to use in image gen
└─────────────────────┘
```

**API Call Pattern:**
```python
def call_openai_responses_api(
    user_message: str,
    api_key: str,
    model: str = "gpt-5",
    use_web_search: bool = False,
) -> str:
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key)
    
    # Build full input with system context
    full_input = f"{SYSTEM_PROMPT}\n\n---\n\n{user_message}"
    
    # Configure web search tool if enabled
    tools = [{"type": "web_search"}] if use_web_search else None
    
    # Make API call
    response = client.responses.create(
        model=model,
        input=full_input,
        tools=tools,
    )
    
    return response.output_text.strip()
```

---

### 3.4 `stage4_image_generation.py` - Gemini API

**Purpose:** Generate actual T-pose images using Gemini 3 Pro.

**Key Concepts:**
- Google Genai SDK
- Configuration objects (types.GenerateContentConfig)
- Binary data handling (image bytes)
- Response parsing with multiple part types

**Model Configuration:**
```python
# Model: gemini-3-pro-image-preview (Nano Banana Pro)
# Features:
#   - 1K, 2K, 4K resolutions
#   - Up to 14 reference images
#   - Thinking mode (enabled by default)

IMAGE_MODEL = "gemini-3-pro-image-preview"
IMAGE_ASPECT_RATIO = "1:1"  # Square for character refs
IMAGE_SIZE = "2K"           # 2048x2048 pixels
```

**API Call Pattern:**
```python
def generate_image_with_gemini(
    prompt: str,
    api_key: str,
    aspect_ratio: str = "1:1",
    image_size: str = "2K",
) -> bytes:
    from google import genai
    from google.genai import types
    
    # Create client
    client = genai.Client(api_key=api_key)
    
    # Configure image generation
    config = types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        ),
    )
    
    # Generate
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[prompt],
        config=config,
    )
    
    # Extract image bytes
    for part in response.parts:
        if part.inline_data is not None:
            return part.inline_data.data
    
    raise Exception("No image generated")
```

---

### 3.5 `file_utils.py` - File I/O

**Purpose:** Handle all file operations with a clean mapping system.

**Key Concepts:**
- Path manipulation with `pathlib.Path`
- Filename sanitization
- Directory structure mapping
- Parent directory creation

**File Mapping Pattern:**
```python
# Maps prompt keys to (subdirectory, filename_template)
PROMPT_FILE_MAP: dict[str, tuple[str, str]] = {
    "base_2d_full_body": ("base", "{name}_2d_base_{version}.txt"),
    "refined_concept": ("refined", "{name}_refined_concept_{version}.txt"),
    "common_design_notes": ("common", "{name}_design_notes_{version}.txt"),
}

def resolve_output_path(base_dir: Path, spec: CharacterSpec, version: str, key: str) -> Path:
    subdir, template = PROMPT_FILE_MAP[key]
    name_safe = spec.name.lower().replace(" ", "_")
    filename = template.format(name=name_safe, version=version)
    return base_dir / subdir / filename

# Example:
# resolve_output_path(Path("output"), spec, "v1", "base_2d_full_body")
# → output/base/aethel_2d_base_v1.txt
```

---

### 3.6 `generate_prompts.py` - CLI Layer

**Purpose:** Thin CLI layer that ties all modules together.

**Key Concepts:**
- Typer for CLI framework
- Type annotations for automatic argument parsing
- Timestamped output directories
- Environment variable loading with dotenv

**Command Structure:**
```python
app = typer.Typer(name="generate_prompts")

@app.command("prompts")   # Stage 1 + 2a + 3
@app.command("refine")    # Stage 2b (LLM)
@app.command("images")    # Stage 4
@app.command("all")       # Full pipeline

if __name__ == "__main__":
    app()
```

**Typer Argument Pattern:**
```python
@app.command("images")
def generate_images_command(
    input_file: Annotated[
        Path,
        typer.Option(
            "--input", "-i",
            help="Path to character spec file",
            exists=True,      # File must exist
            file_okay=True,   # Can be a file
            dir_okay=False,   # Cannot be a directory
            readable=True,    # Must be readable
        ),
    ],
    version: Annotated[
        str,
        typer.Option("--version", "-v", help="Version suffix"),
    ] = "v1",
) -> None:
    """Generate T-pose images using Gemini API."""
    ...
```

---

## 4. Python Concepts Demonstrated

### 4.1 Type Hints

```python
# Basic types
def process(name: str, count: int) -> bool: ...

# Generic types
def get_colors() -> list[str]: ...
def get_prompts() -> dict[str, str]: ...

# Optional (can be None)
def parse(notes: Optional[str]) -> str: ...

# Type aliases
from typing import Annotated
InputPath = Annotated[Path, typer.Option(...)]
```

### 4.2 Dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class Character:
    name: str                                    # Required
    role: str = ""                               # Optional with default
    props: list[str] = field(default_factory=list)  # Mutable default
    
    def get_summary(self) -> str:                # Instance method
        return f"{self.name} ({self.role})"
```

### 4.3 Path Operations

```python
from pathlib import Path

# Create path
path = Path("output") / "images" / "file.png"

# Check existence
if path.exists(): ...

# Read/write
content = path.read_text(encoding="utf-8")
path.write_bytes(image_data)

# Get parts
path.parent  # output/images
path.name    # file.png
path.suffix  # .png

# Create directories
path.parent.mkdir(parents=True, exist_ok=True)
```

### 4.4 Error Handling

```python
# Custom error messages
if not api_key:
    raise ValueError(
        f"API key not found.\n"
        f"Set: export {ENV_VAR}='your-key'"
    )

# Import error handling
try:
    from google import genai
except ImportError:
    raise ImportError(
        "Package required. Install: pip install google-genai"
    )

# API error handling with fallback
try:
    result = call_responses_api(...)
except Exception as e:
    print(f"Falling back: {e}")
    result = call_chat_completions(...)
```

### 4.5 Dictionary Merging

```python
# Merging multiple prompt dictionaries
all_prompts: dict[str, str] = {}
all_prompts.update(generate_base_prompts(spec))     # Stage 1
all_prompts.update(generate_gemini_prompts(spec))   # Stage 2a
all_prompts.update(generate_common_prompts(spec))   # Stage 3
```

---

## 5. API Integration Patterns

### 5.1 Environment Variable Pattern

```python
# Define the env var NAME (not the value!)
API_KEY_ENV = "GEMINI_API_KEY"

def get_api_key() -> str:
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Set {API_KEY_ENV} environment variable")
    return api_key
```

### 5.2 Lazy Import Pattern

```python
def generate_image(...) -> bytes:
    # Import inside function - allows code to load without package
    try:
        from google import genai
    except ImportError:
        raise ImportError("Install: pip install google-genai")
    
    # Now use genai...
```

### 5.3 Configuration Object Pattern

```python
# Group related config into objects
config = types.GenerateContentConfig(
    response_modalities=['IMAGE'],
    image_config=types.ImageConfig(
        aspect_ratio="1:1",
        image_size="2K",
    ),
)

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt],
    config=config,
)
```

### 5.4 Response Parsing Pattern

```python
# Handle multiple response parts
for part in response.parts:
    if part.text is not None:
        text_response = part.text
    elif part.inline_data is not None:
        image_data = part.inline_data.data

if image_data is None:
    raise Exception("No image in response")
```

---

## 6. Design Patterns Used

### 6.1 Single Responsibility Principle

Each module does ONE thing:
- `models.py` → Data structures
- `stage1_*.py` → Base prompts
- `stage2_*.py` → LLM integration
- `stage3_*.py` → Human documents
- `stage4_*.py` → Image generation
- `file_utils.py` → File I/O

### 6.2 DRY (Don't Repeat Yourself)

Helper functions are defined once and imported:
```python
# stage1_base_prompts.py
def format_color_palette(colors: list[str]) -> str: ...

# stage2_gemini_prompts.py
from .stage1_base_prompts import format_color_palette  # Reuse!
```

### 6.3 Factory Pattern

Functions that create and return objects:
```python
def generate_base_prompts(spec: CharacterSpec) -> dict[str, str]:
    return {
        "base_2d_full_body": generate_base_2d_full_body(spec),
        "base_2d_sheet": generate_base_2d_sheet(spec),
    }
```

### 6.4 Template Method Pattern

Each stage follows the same structure:
```python
# Every stage module has:
# 1. Helper functions for formatting
# 2. Individual prompt generators
# 3. Main export function that returns dict[str, str]
```

### 6.5 Strategy Pattern

Multiple API calling strategies with fallback:
```python
if USE_RESPONSES_API:
    try:
        return call_responses_api(...)
    except:
        return call_chat_completions(...)  # Fallback
else:
    return call_chat_completions(...)
```

---

## 7. Code Walkthrough

### 7.1 Complete Flow: Text Spec → Image

```python
# 1. Load character specification
spec = load_character_spec(Path("configs/aethel.yaml"))
# → CharacterSpec(name="Aethel", role="Android archaeologist", ...)

# 2. Generate base prompts (Stage 1)
base = generate_base_prompts(spec)
# → {"base_2d_full_body": "full-body concept art of a...", ...}

# 3. Refine with LLM (Stage 2)
refined = refine_prompts_to_dict(spec, api_key, model="gpt-5")
# → {"refined_concept": "...", "refined_tpose_front": "...", ...}

# 4. Generate images (Stage 4)
images = generate_tpose_images(spec, version="v1")
# → [GeneratedImage(view="front", image_data=b"...", ...), ...]

# 5. Save to disk
saved_paths = save_generated_images(images, spec, output_dir, "v1")
# → [Path("output/images/aethel_tpose_front_v1.jpg"), ...]
```

### 7.2 CLI Command Flow

```bash
uv run generate_prompts.py all -i configs/aethel.yaml
```

```python
# Inside generate_all_command():

# 1. Load spec
spec = load_character_spec(input_file)

# 2. Create timestamped folder
run_output_dir = create_timestamped_output_dir(output_dir)
# → output/2024-12-09_15-30-45/

# 3. Generate static prompts
prompts = generate_all_prompts(spec)
write_prompts(prompts, spec, run_output_dir, version)

# 4. LLM refinement (if not skipped)
if not skip_refine:
    refined = refine_prompts_to_dict(spec, openai_key)
    write_prompts(refined, spec, run_output_dir, version)

# 5. Image generation (if not skipped)
if not skip_images:
    images = generate_tpose_images(spec, version, gemini_key)
    save_generated_images(images, spec, run_output_dir / "images", version)
```

---

## 8. Extension Points

### 8.1 Adding a New Stage

1. Create `src/stage5_new_stage.py`
2. Add generator function returning `dict[str, str]`
3. Import in `src/__init__.py`
4. Add to CLI in `generate_prompts.py`
5. Add file mapping in `file_utils.py`

### 8.2 Adding New Output Formats

Update `PROMPT_FILE_MAP` in `file_utils.py`:
```python
PROMPT_FILE_MAP = {
    ...
    "my_new_output": ("new_folder", "{name}_new_{version}.txt"),
}
```

### 8.3 Adding New Image Models

Update `stage4_image_generation.py`:
```python
IMAGE_MODEL = "new-model-name"
# Update config options as needed
```

### 8.4 Adding New CLI Commands

```python
@app.command("my_command")
def my_command(
    input_file: Annotated[Path, typer.Option("--input", "-i")],
) -> None:
    """My new command description."""
    spec = load_character_spec(input_file)
    # Do something with spec
```

---

## 📖 Key Takeaways

1. **Modular Design**: Each file has a single responsibility
2. **Type Safety**: Full type hints throughout the codebase
3. **Reusable Helpers**: DRY principle with shared utility functions
4. **Clean APIs**: Functions return dictionaries for flexible output
5. **Error Handling**: Clear error messages with recovery suggestions
6. **Documentation**: Extensive comments explain the "why"
7. **CLI Best Practices**: Typer for clean command-line interfaces
8. **API Patterns**: Lazy imports, env vars, config objects

---

## 🎓 Learning Path

### For Developers (This Document)

1. **Start with `models.py`** - Understand the data structure
2. **Read `stage1_base_prompts.py`** - See simple template generation
3. **Study `file_utils.py`** - Learn Path operations
4. **Explore `stage2_llm_refiner.py`** - See API integration
5. **Examine `stage4_image_generation.py`** - See binary data handling
6. **Review `generate_prompts.py`** - See how it all connects

### For Instructors & Students

For comprehensive teaching materials including:
- **Slide deck templates** (100+ slides across 7 modules)
- **Tutorial documentation** (step-by-step guides)
- **Assessment materials** (quizzes, exercises, debugging scenarios)
- **Video script** (15-minute show-and-tell)
- **Quick reference cards** (prompt engineering, rig quality, Eval3D scores)

👉 See [COURSE_MATERIALS_GUIDE.md](./COURSE_MATERIALS_GUIDE.md)

---

## 📚 Related Documentation

| Document | Purpose |
|----------|---------|
| [README.md](./README.md) | Project overview, quick start |
| [COURSE_MATERIALS_GUIDE.md](./COURSE_MATERIALS_GUIDE.md) | **Full teaching curriculum** |
| [prompt_generation/README.md](./prompt_generation/README.md) | CLI usage documentation |

---

*This guide was generated from codebase analysis on December 2025.*

