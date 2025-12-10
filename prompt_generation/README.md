# AI Character Prompt Generator

A clean, teachable Python CLI tool that generates structured text prompts for the **2D → 3D character pipeline**.

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AI CHARACTER PROMPT PIPELINE                            │
│                                                                              │
│   TEXT SPEC  →  BASE PROMPTS  →  LLM REFINE  →  CHECKLIST  →  IMAGE GEN    │
│   (YAML/JSON)    (Stage 1)       (Stage 2)      (Stage 3)     (Stage 4)    │
│                                                                              │
│   Stage 2: Uses OpenAI GPT-5 (with web search tool) to refine prompts       │
│   Stage 4: Generates T-pose images (front/side/back) via Gemini API         │
│   Then manually: Upload to Hunyuan.3D → Download .fbx/.obj                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Install dependencies with uv
uv sync

# Set up API keys (copy template and edit)
cp .env.example .env
# Edit .env and add your API keys

# Generate static prompts (Stages 1, 2a, 3) - no API key needed
uv run generate_prompts.py prompts -i configs/aethel.yaml

# Refine prompts with OpenAI GPT (Stage 2b)
uv run generate_prompts.py refine -i configs/aethel.yaml

# Refine with web search (for current AI art trends)
uv run generate_prompts.py refine -i configs/aethel.yaml --web-search

# Generate T-pose images (Stage 4)
uv run generate_prompts.py images -i configs/aethel.yaml

# Run FULL pipeline (all stages)
uv run generate_prompts.py all -i configs/aethel.yaml

# Preview mode (no API calls)
uv run generate_prompts.py refine -i configs/aethel.yaml --preview
uv run generate_prompts.py images -i configs/aethel.yaml --prompts-only
```

## API Keys Setup

### Option 1: `.env` File (Recommended)

Copy the template and add your keys:
```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
```

> ⚠️ Never commit `.env` to version control! It's already in `.gitignore`.

### Option 2: Environment Variables

```bash
export OPENAI_API_KEY='sk-...'
export GEMINI_API_KEY='AI...'
```

### Required Keys

| Stage | API Key | Description | Get Key |
|-------|---------|-------------|---------|
| Stage 2 (refine) | `OPENAI_API_KEY` | OpenAI GPT-5 with web search | [platform.openai.com](https://platform.openai.com/api-keys) |
| Stage 4 (images) | `GEMINI_API_KEY` | Google Gemini image gen | [aistudio.google.com](https://aistudio.google.com/apikey) |

### OpenAI Models Supported

The refiner uses the **Responses API** with GPT-5:

| Model | Description |
|-------|-------------|
| `gpt-5` | Flagship reasoning model (default) |
| `gpt-5-mini` | Faster, cost-efficient |
| `gpt-5-nano` | Fastest, lowest cost |
| `gpt-4.1` | Smart non-reasoning model (1M context) |

With `--web-search` enabled, the model uses the `web_search` tool to find current AI art trends and best practices.

## Project Structure (Teachable Code)

```
prompt_generation/
├── generate_prompts.py          # Main CLI entry point (thin layer)
├── src/
│   ├── __init__.py                # Package exports
│   ├── models.py                  # CharacterSpec dataclass + file loading
│   ├── stage1_base_prompts.py     # Stage 1: Base 2D prompts (static)
│   ├── stage2_gemini_prompts.py   # Stage 2a: Gemini meta-prompts (static)
│   ├── stage2_llm_refiner.py      # Stage 2b: LLM-refined prompts (OpenAI)
│   ├── stage3_common_prompts.py   # Stage 3: Checklist and design notes
│   ├── stage4_image_generation.py # Stage 4: Gemini image generation
│   └── file_utils.py              # File output utilities
├── configs/
│   ├── _template.yaml           # Character spec template with docs
│   └── aethel.yaml              # Example character spec
├── pyproject.toml               # Project config for uv
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

### Module Responsibilities

| Module | Pipeline Stage | Description |
|--------|----------------|-------------|
| `models.py` | Input | `CharacterSpec` dataclass + YAML/JSON loading |
| `stage1_base_prompts.py` | Stage 1 | Base 2D prompts (static templates) |
| `stage2_gemini_prompts.py` | Stage 2a | Meta-prompts for manual Gemini use |
| `stage2_llm_refiner.py` | **Stage 2b** | **LLM-refined prompts via OpenAI API** |
| `stage3_common_prompts.py` | Stage 3 | Checklist and design notes for humans |
| `stage4_image_generation.py` | Stage 4 | Gemini API image generation (3 views) |
| `file_utils.py` | Output | File writing and path resolution |

## Output Structure

Each run creates a **timestamped folder** inside `output/`:

```
output/
├── 2024-12-09_15-30-45/              # Run 1
│   ├── base/                         # Stage 1: Base 2D prompts (static)
│   │   ├── aethel_2d_base_v1.txt
│   │   └── aethel_2d_sheet_v1.txt
│   ├── gemini/                       # Stage 2a: Gemini meta-prompts (static)
│   │   ├── aethel_2d_refiner_v1.txt
│   │   └── aethel_tpose_prompt_v1.txt
│   ├── refined/                      # Stage 2b: LLM-refined prompts (OpenAI)
│   │   ├── aethel_refined_concept_v1.txt
│   │   ├── aethel_refined_tpose_front_v1.txt
│   │   ├── aethel_refined_tpose_side_v1.txt
│   │   └── aethel_refined_tpose_back_v1.txt
│   ├── common/                       # Stage 3: Checklist & notes
│   │   ├── aethel_2d_refinement_criteria_v1.txt
│   │   └── aethel_design_notes_v1.txt
│   └── images/                       # Stage 4: Generated T-pose images
│       ├── aethel_tpose_front_v1.png
│       ├── aethel_tpose_side_v1.png
│       └── aethel_tpose_back_v1.png
└── 2024-12-09_16-00-12/              # Run 2 (different timestamp)
    └── ...
```

## CLI Commands

### `prompts` - Generate Static Prompts (Stages 1, 2a, 3)

```bash
uv run generate_prompts.py prompts -i configs/aethel.yaml
uv run generate_prompts.py prompts -i configs/aethel.yaml --dry-run  # Preview
```

### `refine` - LLM Prompt Refinement (Stage 2b)

```bash
# Basic refinement
uv run generate_prompts.py refine -i configs/aethel.yaml

# With web search for current AI art trends
uv run generate_prompts.py refine -i configs/aethel.yaml --web-search

# Choose model
uv run generate_prompts.py refine -i configs/aethel.yaml --model gpt-4o-mini

# Preview requests (no API calls)
uv run generate_prompts.py refine -i configs/aethel.yaml --preview
```

### `images` - Generate T-pose Images (Stage 4)

```bash
# Generate images
uv run generate_prompts.py images -i configs/aethel.yaml

# Specific views only
uv run generate_prompts.py images -i configs/aethel.yaml --views front,side

# Preview prompts (no API calls)
uv run generate_prompts.py images -i configs/aethel.yaml --prompts-only
```

### `all` - Full Pipeline (All Stages)

```bash
# Full pipeline
uv run generate_prompts.py all -i configs/aethel.yaml

# With web search for refinement
uv run generate_prompts.py all -i configs/aethel.yaml --web-search

# Skip LLM refinement (static prompts only)
uv run generate_prompts.py all -i configs/aethel.yaml --skip-refine

# Skip image generation (prompts only)
uv run generate_prompts.py all -i configs/aethel.yaml --skip-images
```

## Character Spec Format

**Start with the template:**

```bash
cp configs/_template.yaml configs/my_character.yaml
```

Example character spec:

```yaml
name: "Aethel"
role: "Android archaeologist"
game_style: "stylized sci-fi, slightly realistic"
silhouette: "tall, long coat, mechanical arm"
color_palette:
  - "teal"
  - "black"
  - "orange accents"
key_props:
  - "data tablet"
  - "arm-mounted scanner"
animation_focus:
  - "walk"
  - "idle scanning"
  - "simple attack"
extra_notes: "Set in a neon-lit cyber-ruin environment, neutral expression."
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ Yes | Character name (used in filenames) |
| `role` | No | Character's role/occupation |
| `game_style` | No | Visual art style |
| `silhouette` | No | Body shape and distinctive features |
| `color_palette` | No | List of main colors |
| `key_props` | No | Important items/accessories |
| `animation_focus` | No | Planned animation types |
| `extra_notes` | No | Additional context |

## Prompt Stages Explained

### Stage 1: Base 2D Prompts (Static)

Simple template-based prompts as a starting point.

### Stage 2a: Gemini Meta-Prompts (Static)

Meta-prompts you can manually paste into Gemini for refinement.

### Stage 2b: LLM-Refined Prompts (OpenAI GPT-5) ⭐

**The key feature!** Uses OpenAI GPT-5 via the Responses API to transform your character spec into optimized image generation prompts.

**Models:**
- **gpt-5**: Flagship reasoning model (default)
- **gpt-5-mini**: Faster, cost-efficient
- **gpt-4.1**: Smart non-reasoning model

**With `--web-search` enabled:**
- Uses the `web_search` tool to find current AI art prompt trends
- Searches for popular style keywords that work with image generators
- Finds reference images of similar character types

The LLM generates:
1. `refined_concept` - Optimized concept art prompt
2. `refined_tpose_front` - Front view T-pose prompt
3. `refined_tpose_side` - Side view T-pose prompt  
4. `refined_tpose_back` - Back view T-pose prompt

These refined prompts are ready to use directly in image generators!

### Stage 3: Checklist & Notes

Human-readable documents for validation:
- **2D Refinement Criteria**: Checklist to validate T-pose images
- **Design Notes**: Internal reference document

### Stage 4: Image Generation (Gemini API)

Generates actual T-pose images using Gemini 3 Pro Image Preview:
- Front view
- Side view  
- Back view

## Workflow

1. **Define Character** → Create YAML spec in `configs/`
2. **Refine Prompts** → Run `refine` command with OpenAI
3. **Generate Images** → Run `images` command with Gemini
4. **Validate** → Use `2d_refinement_criteria` checklist
5. **Convert to 3D** → Upload validated T-pose to Hunyuan.3D
6. **Download Assets** → Get .fbx/.obj for further pipeline

Or run `all` to do everything in one command!

## Code Design (For Learners)

This codebase is designed to be **teachable**:

- **Single Responsibility**: Each module does ONE thing
- **Extensive Comments**: Every function has line-by-line explanations
- **Type Hints**: All functions have full type annotations
- **Dataclasses**: Modern Python data modeling with `@dataclass`
- **Clean Separation**: CLI layer is thin, logic is in `src/`

### Key Python Concepts Demonstrated

| Concept | Where |
|---------|-------|
| `@dataclass` | `src/models.py` - CharacterSpec |
| `pathlib.Path` | `src/file_utils.py` - file operations |
| Type hints | Everywhere - `def func(x: str) -> dict[str, str]` |
| `logging` | `src/models.py` - warning messages |
| f-strings | All prompt templates |
| Dictionary merging | `generate_prompts.py` - `dict.update()` |
| CLI with Typer | `generate_prompts.py` - `@app.command()` |
| API clients | `stage2_llm_refiner.py`, `stage4_image_generation.py` |

## License

MIT
