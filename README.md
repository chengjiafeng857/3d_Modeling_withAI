# 🎮 3D Modeling with AI

> An AI-powered pipeline for generating game-ready 3D character models from simple text descriptions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 Vision

Transform the traditional 3D character creation workflow:

```
Traditional:  Concept Artist → 2D Art → 3D Modeler → Rigger → Animator
                   ↓              ↓          ↓          ↓
              (weeks)        (weeks)    (weeks)    (weeks)

With AI:      Text Description → AI Pipeline → Game-Ready 3D Model
                    ↓                               ↓
               (minutes)                        (minutes)
```

This project automates the character creation pipeline using multiple AI models working together.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        3D MODELING WITH AI PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐│
│  │  Text    │ → │  Prompt  │ → │  2D      │ → │  3D      │ → │ Game   ││
│  │  Spec    │    │Generator │    │ T-pose  │    │ Model   │    │ Ready  ││
│  │  (YAML)  │    │(GPT+Gemini)   │ Images  │    │(Hunyuan)│    │ Asset  ││
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └────────┘│
│       │               │               │               │              │      │
│       ▼               ▼               ▼               ▼              ▼      │
│   Character      Optimized       Front/Side/      .fbx/.obj       Rigged   │
│   Definition     Prompts         Back Views       Mesh            Model    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Project Components

| Component | Status | Description |
|-----------|--------|-------------|
| **[Prompt Generation](./prompt_generation/)** | ✅ Complete | AI prompt engineering pipeline |
| **3D Generation** | 🔜 Planned | Hunyuan.3D integration |
| **Model Assessment** | 🔜 Planned | Quality validation pipeline |
| **Rigging Automation** | 🔜 Planned | Auto-rigging with Mixamo/AI |

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
├── README.md                    # This file
├── LICENSE                      # MIT License
│
└── prompt_generation/           # 🎨 AI Prompt Engineering Tool
    ├── README.md                #    Detailed documentation
    ├── TEACHING_GUIDE.md        #    Educational walkthrough
    ├── generate_prompts.py      #    CLI entry point
    ├── src/                     #    Core modules
    │   ├── models.py            #    Data models
    │   ├── stage1_base_prompts.py    # Base prompts
    │   ├── stage2_gemini_prompts.py  # Meta-prompts
    │   ├── stage2_llm_refiner.py     # OpenAI integration
    │   ├── stage3_common_prompts.py  # Checklists
    │   ├── stage4_image_generation.py # Gemini images
    │   └── file_utils.py        #    File I/O
    ├── configs/                 #    Character specs
    │   ├── _template.yaml       #    Template
    │   └── aethel.yaml          #    Example character
    └── output/                  #    Generated outputs
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

### Planned: Hunyuan.3D

- **Purpose:** Convert 2D T-pose images to 3D models
- **Output:** .fbx/.obj files ready for game engines

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

This codebase is designed to be **educational**. Key resources:

| Resource | Description |
|----------|-------------|
| [TEACHING_GUIDE.md](./prompt_generation/TEACHING_GUIDE.md) | 770+ line comprehensive code walkthrough |
| [prompt_generation/README.md](./prompt_generation/README.md) | Detailed usage documentation |
| Source code comments | Every function has line-by-line explanations |

### Python Concepts Demonstrated

- `@dataclass` decorators
- Type hints (`def func(x: str) -> dict[str, str]`)
- `pathlib.Path` for file operations
- API client patterns (OpenAI, Google)
- CLI frameworks (Typer)
- Environment variable handling
- Error handling with helpful messages

---

## 🛣️ Roadmap

- [x] **Phase 1:** Prompt Generation Pipeline
  - [x] Base prompt templates
  - [x] LLM refinement with GPT-5
  - [x] Gemini image generation
  - [x] T-pose multi-view support (front/side/back)
  
- [ ] **Phase 2:** 3D Model Generation
  - [ ] Hunyuan.3D integration
  - [ ] Automatic image-to-3D conversion
  - [ ] Mesh quality validation
  
- [ ] **Phase 3:** Model Assessment
  - [ ] Topology checker
  - [ ] UV mapping validation
  - [ ] Animation-readiness score
  
- [ ] **Phase 4:** Rigging & Animation
  - [ ] Auto-rigging integration
  - [ ] Animation clip generation
  - [ ] Export to game engines (Unity/Unreal)

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
- **Community** - AI art prompt engineering best practices

---

## 📬 Contact

- **Author:** chengjiafeng857
- **GitHub:** [github.com/chengjiafeng857/3d_Modeling_withAI](https://github.com/chengjiafeng857/3d_Modeling_withAI)

---

<p align="center">
  <i>Making game character creation accessible to everyone through AI.</i>
</p>

