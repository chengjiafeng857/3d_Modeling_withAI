# 🎮 3D Modeling with AI

> **AI-Assisted Character Asset Pipeline: From Prompt to Playable Character**
> 
> An AI-powered pipeline for generating game-ready 3D character models from simple text descriptions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 Vision

Transform the traditional 3D character creation workflow:

```
TRADITIONAL CHARACTER PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Concept Artist  →  2D Artist  →  3D Modeler  →  Rigger  →  Animator
     │                │              │            │           │
     ▼                ▼              ▼            ▼           ▼
  (1-2 weeks)    (1-2 weeks)   (2-4 weeks)  (1-2 weeks) (2-4 weeks)

                    TOTAL: 8-14 weeks per character
```

```
AI-ASSISTED CHARACTER PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Text Spec  →  AI Prompts  →  AI Images  →  AI 3D  →  3D Eval  →  AI Rig  →  Game
    │             │             │            │          │          │         │
    ▼             ▼             ▼            ▼          ▼          ▼         ▼
 (5 min)      (5 min)       (5 min)     (30 min)  (5 min)    (30 min)   (import)
                                            │          │
                                            └────◄─────┘
                                          (iterate if neccessary)

                    TOTAL: 1-2 hours per character

⚠️ Human judgment still required at each stage!
```

This project automates the character creation pipeline using multiple AI models working together.

---

## 🏗️ Architecture Overview

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
│        │                │                │                                  │
│        ▼                ▼                ▼                                  │
│   Idle/Walk/        Quality          Playable                              │
│   Attack Clips      Scores           Character                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Project Components

| Stage | Component | Automation | Tools |
|-------|-----------|------------|-------|
| 1-2 | **[Prompt Generation](./prompt_generation/)** | 🤖 Automated | Python + Typer CLI |
| 2 | **LLM Refinement** | 🤖 Automated | OpenAI GPT-5 |
| 3 | **2D T-Pose Generation** | 🤖 Automated | Gemini 3 Pro Image Preview |
| 4 | **3D Model Generation** | 👤 Manual | Tencent Hunyuan.3D (Web UI) |
| 6 | **Quality Assessment** | 🤖 Automated | [Eval3D Pipeline](https://github.com/chengjiafeng857/Eval3d_pipline) |
| 5 | **Auto-Rigging + Animation** | 👤 Manual | Meshy / MexMiao (Web UI) |
| 7 | **Game Integration** | 👤 Manual | Unreal Engine 5 (Editor) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- API Keys:
  - [OpenAI API Key](https://platform.openai.com/api-keys) (for prompt refinement)
  - [Google Gemini API Key](https://aistudio.google.com/apikey) (for image generation)

### Installation

```bash
# Clone the repository
git clone https://github.com/chengjiafeng857/3d_Modeling_withAI.git
cd 3d_Modeling_withAI

# Navigate to prompt generation tool
cd prompt_generation

# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -r requirements.txt
```

### Setup API Keys

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your keys:
# OPENAI_API_KEY=sk-...
# GEMINI_API_KEY=AI...
```

### Generate Your First Character

```bash
# 1. Create a character specification (or use the example)
cat configs/aethel.yaml

# 2. Generate prompts (no API needed for static prompts)
uv run generate_prompts.py prompts -i configs/aethel.yaml

# 3. Refine prompts with OpenAI GPT-5
uv run generate_prompts.py refine -i configs/aethel.yaml

# 4. Generate T-pose images with Gemini
uv run generate_prompts.py images -i configs/aethel.yaml

# Or run the FULL pipeline
uv run generate_prompts.py all -i configs/aethel.yaml
```

---

## 📁 Repository Structure

```
3d_Modeling_withAI/
├── README.md                    # This file - Project overview
├── LICENSE                      # MIT License
├── COURSE_MATERIALS_GUIDE.md    # 📚 Master teaching document (1850+ lines)
├── TEACHING_GUIDE.md            # 📖 Code architecture walkthrough
│
└── prompt_generation/           # 🎨 Stages 1-3: Prompt & Image Generation
    ├── README.md                #    CLI usage documentation
    ├── generate_prompts.py      #    CLI entry point
    ├── src/                     #    Core modules
    │   ├── models.py            #    CharacterSpec dataclass
    │   ├── stage1_base_prompts.py    # Base prompt templates
    │   ├── stage2_gemini_prompts.py  # Meta-prompts for Gemini
    │   ├── stage2_llm_refiner.py     # OpenAI GPT-5 integration
    │   ├── stage3_common_prompts.py  # Checklists & design notes
    │   ├── stage4_image_generation.py # Gemini 3 Pro images
    │   └── file_utils.py        #    File I/O utilities
    ├── configs/                 #    Character specifications
    │   ├── _template.yaml       #    Template with documentation
    │   └── aethel.yaml          #    Example: Android archaeologist
    └── output/                  #    Generated outputs (timestamped)
        ├── base/                #    Stage 1 outputs
        ├── refined/             #    Stage 2 outputs
        ├── common/              #    Stage 3 outputs
        └── images/              #    T-pose images (.jpg)
```

---

## 🎨 Prompt Generation Pipeline

The first (and currently most developed) component generates optimized prompts and T-pose images.

### Pipeline Stages

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PROMPT GENERATION PIPELINE                              │
│                                                                              │
│   TEXT SPEC  →  BASE PROMPTS  →  LLM REFINE  →  CHECKLIST  →  IMAGE GEN    │
│   (YAML/JSON)    (Stage 1)       (Stage 2)      (Stage 3)     (Stage 4)    │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Stage | Input | Output | AI Model |
|-------|-------|--------|----------|
| **Stage 1** | Character YAML | Base prompts | None (templates) |
| **Stage 2** | Base prompts | Refined prompts | OpenAI GPT-5 |
| **Stage 3** | Character spec | Checklists | None (templates) |
| **Stage 4** | Refined prompts | T-pose images | Gemini 3 Pro |

### CLI Commands

```bash
# Generate static prompts only
uv run generate_prompts.py prompts -i configs/character.yaml

# Refine with LLM (GPT-5)
uv run generate_prompts.py refine -i configs/character.yaml

# Refine with web search for current AI art trends
uv run generate_prompts.py refine -i configs/character.yaml --web-search

# Generate T-pose images
uv run generate_prompts.py images -i configs/character.yaml

# Run full pipeline
uv run generate_prompts.py all -i configs/character.yaml
```

### Character Specification Format

```yaml
# configs/my_character.yaml
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
extra_notes: "Set in a neon-lit cyber-ruin environment."
```

### Generated Outputs

Each run creates a timestamped folder with:

```
output/2024-12-09_15-30-45/
├── base/                    # Static base prompts
├── gemini/                  # Meta-prompts for Gemini
├── refined/                 # LLM-refined prompts ⭐
├── common/                  # Checklists & notes
└── images/                  # Generated T-pose images ⭐
    ├── character_tpose_front_v1.jpg
    ├── character_tpose_side_v1.jpg
    └── character_tpose_back_v1.jpg
```

---

## 🔧 AI Models Used

### OpenAI GPT-5 (Prompt Refinement)

- **Purpose:** Transform character specs into optimized image prompts
- **Feature:** Web search tool for current AI art trends
- **Models:** `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-4.1`

### Google Gemini 3 Pro Image Preview

- **Purpose:** Generate high-quality T-pose character images
- **Model:** `gemini-3-pro-image-preview` (Nano Banana Pro)
- **Features:**
  - 1K, 2K, 4K resolution support
  - Multiple aspect ratios
  - Up to 14 reference images
  - Built-in "thinking" mode

### Tencent Hunyuan.3D

- **Purpose:** Convert 2D T-pose images to 3D models
- **Output:** .fbx/.obj files ready for game engines

### Eval3D Pipeline (Quality Assessment)

- **Repository:** [github.com/chengjiafeng857/Eval3d_pipline](https://github.com/chengjiafeng857/Eval3d_pipline.git)
- **Based on:** [Eval3D: Interpretable and Fine-grained Evaluation for 3D Generation](https://github.com/eval3d/eval3d-codebase) (CVPR 2025)
- **Purpose:** Automated quality assessment for AI-generated 3D models

**5 Comprehensive Metrics:**

| Metric | Range | What It Measures |
|--------|-------|------------------|
| **Geometric Consistency** | 0-100 | Surface normal quality (texture-geometry alignment) |
| **Semantic Consistency** | 0-100 | View consistency (detects Janus problem) |
| **Structural Consistency** | 0-100 | 3D predictability via Zero123 |
| **Aesthetics** | 0-1 | Visual appeal (ImageReward) |
| **Text-3D Alignment** | 0-1 | Prompt adherence (GPT-4o VQA) |

**Quick Usage:**
```bash
# Evaluate any 3D mesh
uv run eval3d-pipeline eval-mesh ./character.obj \
    --algo my_pipeline \
    --prompt "Android archaeologist, stylized sci-fi"

# Quick evaluation (aesthetics + text-3D only)
uv run eval3d-pipeline eval-mesh ./character.obj --quick
```

**Key Features:**
- ✅ Universal mesh support (`.obj`, `.glb`, `.ply`, `.stl`, `.fbx`)
- ✅ Single command: mesh in → quality scores out
- ✅ No threestudio required
- ✅ Batch processing for multiple assets

---

## 📊 Example Results

### Input: Character Specification

```yaml
name: "Aethel"
role: "Android archaeologist"
game_style: "stylized sci-fi"
```

### Output: T-pose Images (2K Resolution)

| Front View | Side View | Back View |
|------------|-----------|-----------|
| ![Front](./prompt_generation/output/images/2025-12-09_18-15-47/aethel_tpose_front_full_test.jpg) | ![Side](./prompt_generation/output/images/2025-12-09_18-15-47/aethel_tpose_side_full_test.jpg) | ![Back](./prompt_generation/output/images/2025-12-09_18-15-47/aethel_tpose_back_full_test.jpg) |

---

## 🎓 Learning Resources

This codebase is designed to be **educational** and supports a full course curriculum.

| Resource | Lines | Description |
|----------|-------|-------------|
| [COURSE_MATERIALS_GUIDE.md](./COURSE_MATERIALS_GUIDE.md) | 1850+ | **Master teaching document** - slides, tutorials, assessments, video scripts |
| [TEACHING_GUIDE.md](./TEACHING_GUIDE.md) | 770+ | Code architecture walkthrough for developers |
| [prompt_generation/README.md](./prompt_generation/README.md) | 335 | CLI usage documentation |
| Source code comments | - | Every function has line-by-line explanations |

### Course Structure (7 Modules)

| Module | Topic | Duration |
|--------|-------|----------|
| 1 | Introduction to AI Asset Pipelines | 30 min |
| 2 | Character Specs & Prompt Engineering | 45 min |
| 3 | 2D Concept Generation (Gemini) | 30 min |
| 4 | 2D → 3D Conversion (Hunyuan) | 30 min |
| 5 | Rigging & Animation (MexMiao) | 30 min |
| 6 | Quality Assessment (Eval3D) | 45 min |
| 7 | Unreal Integration | 45 min |

### Python Concepts Demonstrated

- `@dataclass` decorators with `field(default_factory=list)`
- Type hints (`def func(x: str) -> dict[str, str]`)
- `pathlib.Path` for file operations
- API client patterns (OpenAI, Google Genai)
- CLI frameworks (Typer with `Annotated`)
- Environment variable handling with `dotenv`
- Error handling with helpful messages
- Lazy imports for optional dependencies

---

## 🛣️ Pipeline Stages

### Stage 1: Character Specification
- YAML/JSON config schema
- Template with documentation
- Validation and loading

### Stage 2: Prompt Engineering
- Base prompt templates
- LLM refinement with GPT-5
- Web search for current AI art trends
- T-pose specific prompts

### Stage 3: 2D T-Pose Generation
- Gemini 3 Pro Image Preview
- Multi-view support (front/side/back)
- 2K resolution output

### Stage 4: 3D Model Generation
- Tencent Hunyuan.3D
- Meshy AI alternative
- Mesh export (.fbx/.obj/.glb)

### Stage 5: Auto-Rigging & Animation
- MexMiao auto-rigging
- Idle/Walk/Attack animation generation
- FBX export for game engines

### Stage 6: Quality Assessment
- Eval3D pipeline integration
- Geometric/Semantic consistency metrics
- Aesthetics and Text-3D alignment scores

### Stage 7: Game Engine Integration
- Unreal Engine 5 import
- Animation Blueprint setup
- Character Blueprint integration

---

## 🐛 Debug Tips (quick checklist)

- **Gemini image is empty**: ensure `GEMINI_API_KEY` is set; include view and background constraints (front/side/back, white background, neutral lighting).
- **LLM refine fails**: set `OPENAI_API_KEY`; use `--preview` to inspect the payload before calling the API.
- **2D not 3D-friendly**: regenerate with stricter T-pose prompts (no dramatic lighting, no cluttered backgrounds, clear silhouette and props).
- **Eval3D score low (<75%)**: fix the lowest metric first (Janus → add consistent multi-view images; geometric → cleaner normals/textures); re-run [Eval3D](https://github.com/chengjiafeng857/Eval3d_pipline).
- **Unreal shows T-pose**: set Anim Blueprint on the Skeletal Mesh (Details → Animation → Anim Class) and ensure Idle/Walk transitions exist.
- **Rig hands/shoulders explode**: re-run auto-rig with finger bones enabled (Meshy/MexMiao) and verify scale on export/import.

---

## 🤝 Contributing

Contributions are welcome! Areas that need help:

1. **3D Pipeline Integration** - Hunyuan.3D, other 3D generators
2. **Model Assessment** - Quality metrics, validation tools
3. **Documentation** - More examples, tutorials
4. **Testing** - Unit tests, integration tests

### Development Setup

```bash
# Clone and setup
git clone https://github.com/chengjiafeng857/3d_Modeling_withAI.git
cd 3d_Modeling_withAI/prompt_generation

# Install dev dependencies
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-5 API for prompt refinement
- **Google** - Gemini 3 Pro for image generation
- **Tencent** - Hunyuan.3D (planned integration)
- **Eval3D Team** - [Duggal et al. (CVPR 2025)](https://github.com/eval3d/eval3d-codebase) for interpretable 3D evaluation metrics
- **Community** - AI art prompt engineering best practices

---

## 📬 Contact

- **Author:** chengjiafeng857
- **GitHub:** [github.com/chengjiafeng857/3d_Modeling_withAI](https://github.com/chengjiafeng857/3d_Modeling_withAI)

---

<p align="center">
  <i>Making game character creation accessible to everyone through AI.</i>
</p>

