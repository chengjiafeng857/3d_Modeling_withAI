# 📚 AI-Driven Asset Pipeline Course Materials Guide

> **Master Document for Teaching Material Generation**
> 
> **Course:** AI-Assisted Character Asset Pipeline: From Prompt to Playable Character  
> **Target:** Intermediate Game Development Students  
> **Duration:** 4-6 hours of content

---

## 📑 Table of Contents

1. [Course Overview](#1-course-overview)
2. [Slide Deck Templates](#2-slide-deck-templates)
3. [Tutorial Documentation](#3-tutorial-documentation)
4. [Assessment Materials](#4-assessment-materials)
5. [Video Script](#5-video-script)
6. [Implementation Reference](#6-implementation-reference)
7. [Asset Licensing Guide](#7-asset-licensing-guide)

---

## 1. Course Overview

### 1.1 One-Sentence Pitch

> **"We will build an AI-assisted pipeline that turns a text character spec into 2D concept art, a rigged 3D model, and a playable animated character in Unreal, while teaching students prompt engineering and model evaluation."**

### 1.2 Learning Objectives

By the end of this course, students will be able to:

| # | Objective | Assessment Method |
|---|-----------|------------------|
| 1 | Explain how generative models (Hunyuan, Gemini, Meshy/MexMiao) fit into a game art pipeline | Quiz + Diagram |
| 2 | Design **prompt templates** to generate consistent character concepts | Exercise 1 |
| 3 | Use AI tools to generate **2D concept art → 3D character → auto-rig + animation** | Exercise 2 |
| 4 | Evaluate AI outputs with **quality criteria** (pose readability, topology, rig behavior) | Eval3D Pipeline |
| 5 | Import and hook the character into Unreal with a starter Animation Blueprint | Exercise 3 |
| 6 | Understand licensing, TOS, and reproducibility issues in AI content pipelines | Quiz |

### 1.3 Pipeline Architecture

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

### 1.4 Tools & Technologies

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

## 2. Slide Deck Templates

### 2.1 Module 1: Introduction to AI Asset Pipelines (15 slides)

#### Slide 1: Title
```
AI-ASSISTED CHARACTER ASSET PIPELINE
From Prompt to Playable Character

[Course Name] | [Instructor Name]
[Date]
```

#### Slide 2: The Traditional Pipeline Problem
```
TRADITIONAL CHARACTER PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Concept Artist     →  2D Artist    →  3D Modeler  →  Rigger  →  Animator
     │                    │               │            │           │
     ▼                    ▼               ▼            ▼           ▼
  (1-2 weeks)        (1-2 weeks)    (2-4 weeks)  (1-2 weeks) (2-4 weeks)

                    TOTAL: 8-14 weeks per character

[Image: Pipeline timeline diagram]
```

#### Slide 3: The AI-Assisted Solution
```
AI-ASSISTED CHARACTER PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Text Spec  →  AI Prompts  →  AI Images  →  AI 3D  →  AI Rig
    │             │             │            │          │
    ▼             ▼             ▼            ▼          ▼
 (5 min)      (5 min)       (5 min)     (30 min)   (30 min)

                    TOTAL: 1-2 hours per character

⚠️ Human judgment still required at each stage!

[Image: Compressed pipeline diagram]
```

#### Slide 4: Real Studios Using This Approach
```
INDUSTRY ADOPTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Ubisoft - AI concept art variations
• EA - NPC generation at scale
• Indie Studios - Full pipeline automation
• Roblox - User-generated character tools

"AI won't replace artists; it will make artists 10x more productive."
                                        — Industry Analyst, 2024

[Image: Screenshots from industry examples]
```

#### Slide 5: Course Learning Path
```
YOUR LEARNING JOURNEY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Module 1: Introduction & Setup           ← You are here
Module 2: Character Specs & Prompt Engineering
Module 3: 2D Concept Generation
Module 4: 2D → 3D Conversion
Module 5: Rigging & Animation
Module 6: Quality Assessment (Eval3D)
Module 7: Unreal Integration

[Progress bar visualization]
```

#### Slides 6-15: Additional Introduction Slides
```
6. What is Prompt Engineering?
7. Generative AI Models Overview (Diffusion, Transformers)
8. The Character Spec Schema
9. Quality Control Checkpoints
10. Licensing & Legal Considerations
11. Tools We'll Use (Overview)
12. Setup Instructions
13. API Keys & Environment
14. Course Deliverables
15. Q&A / Discussion Points
```

---

### 2.2 Module 2: Character Specs & Prompt Engineering (20 slides)

#### Slide 1: Module Title
```
MODULE 2: CHARACTER SPECS & PROMPT ENGINEERING

"The quality of your output depends entirely on the quality of your input."

[Image: Prompt → Output comparison]
```

#### Slide 2: The Character Spec Schema
```yaml
# YAML CHARACTER SPECIFICATION SCHEMA
# ─────────────────────────────────────────────────────

name: "Aethel"                    # Required: Character name
role: "Android archaeologist"     # What they do
game_style: "stylized sci-fi"     # Visual style
silhouette: "tall, long coat"     # Shape/outline
color_palette:                    # 2-4 colors
  - "teal"
  - "black"
  - "orange accents"
key_props:                        # Important items
  - "data tablet"
  - "arm-mounted scanner"
animation_focus:                  # Planned animations
  - "walk"
  - "idle scanning"
extra_notes: "Neon-lit environment"  # Additional context
```

#### Slide 3: Why YAML Over Natural Language?
```
STRUCTURED VS. UNSTRUCTURED INPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Unstructured:
"Make me a cool sci-fi character with a robot arm"

✅ Structured (YAML):
name: "Aethel"
role: "Android archaeologist"
silhouette: "tall, long coat, mechanical arm"
...

WHY STRUCTURED IS BETTER:
• Reproducible - Same spec → Same output
• Version controlled - Track changes in git
• Automated - Scripts can process it
• Consistent - No ambiguity
```

#### Slide 4: The Prompt Template System
```
PROMPT TEMPLATE ARCHITECTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Character   │ →   │  Template   │ →   │  Final      │
│ Spec (YAML) │     │  Engine     │     │  Prompt     │
└─────────────┘     └─────────────┘     └─────────────┘

TEMPLATE EXAMPLE:
"Full-body concept art of a {role}, {game_style} style,
{silhouette}, color palette {color_palette}, holding {key_props},
front view, neutral pose, plain background, high detail"

OUTPUT:
"Full-body concept art of a Android archaeologist,
stylized sci-fi style, tall long coat mechanical arm,
color palette teal black orange accents, holding data tablet,
front view, neutral pose, plain background, high detail"
```

#### Slide 5: Prompt Engineering Best Practices
```
PROMPT ENGINEERING GOLDEN RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. BE SPECIFIC
   ❌ "robot character"
   ✅ "Android archaeologist with mechanical arm"

2. CONSTRAIN THE VIEW
   ❌ "character image"
   ✅ "front view, T-pose, white background"

3. SPECIFY STYLE
   ❌ "cool looking"
   ✅ "stylized sci-fi, slightly realistic, game concept art"

4. USE NEGATIVE PROMPTS
   "No text, no watermarks, no signature, no frame"

5. REQUEST MULTIPLE VIEWS
   "Front and side view, character turnaround sheet"
```

#### Slides 6-20: Additional Prompt Engineering Slides
```
6. Live Demo: generate_prompts.py
7. Stage 1: Base Prompt Generation
8. Stage 2: LLM Refinement with GPT-5
9. Web Search for Current AI Art Trends
10. Comparing Prompt Versions (v1, v2, v3)
11. T-Pose Requirements for 3D Modeling
12. Common Prompt Mistakes
13. Debugging Bad Outputs
14. Exercise 1 Introduction
15. Color Palette Psychology
16. Silhouette Design Principles
17. Props and Character Identity
18. Style Tokens Reference
19. Model-Specific Prompt Adjustments
20. Module Summary & Quiz Preview
```

---

### 2.3 Module 3: 2D Concept Generation (15 slides)

#### Key Slides:
```
1. Module Title: 2D Concept Generation with Gemini
2. Gemini 3 Pro Image Preview Overview
3. API Setup & Authentication
4. T-Pose Requirements for 3D
5. Front/Side/Back View Generation
6. Image Quality Assessment Checklist
7. Common Problems: Weird Poses
8. Common Problems: Bad Lighting
9. Common Problems: Inconsistent Style
10. Iteration Strategy: Prompt Refinement Loop
11. Batch Generation for Variations
12. Selecting the Best Candidate
13. Preparing Images for 3D Conversion
14. Exercise 2 Introduction
15. Module Summary
```

---

### 2.4 Module 4: 2D → 3D Conversion (15 slides)

#### Key Slides:
```
1. Module Title: From 2D Concepts to 3D Models
2. Tencent Hunyuan.3D Overview
3. Alternative: Meshy AI
4. Input Requirements: Image Preparation
5. Upload & Generation Process
6. Understanding Mesh Output
7. Topology Quality Assessment
8. Common Problems: Holes & Artifacts
9. Common Problems: Bad Proportions
10. Export Formats: FBX vs OBJ vs GLB
11. Naming Conventions for Pipeline
12. Quick Cleanup in Blender (Optional)
13. Eval3D Integration Preview
14. Exercise 3 Introduction
15. Module Summary
```

---

### 2.5 Module 5: Rigging & Animation (15 slides)

#### Key Slides:
```
1. Module Title: Auto-Rigging with AI
2. What is Rigging? (For Non-Artists)
3. Meshy AI Auto-Rig Overview
4. MexMiao Alternative
5. Humanoid Skeleton Standard
6. Upload & Auto-Rig Process
7. Animation Generation: Idle
8. Animation Generation: Walk Cycle
9. Animation Generation: Attack
10. Rig Quality Checklist
11. Common Problems: Shoulder Deformation
12. Common Problems: Hand Explosion
13. Export Settings for Unreal
14. File Organization
15. Module Summary
```

---

### 2.6 Module 6: Quality Assessment with Eval3D (20 slides)

#### Slide 1: Module Title
```
MODULE 6: QUALITY ASSESSMENT WITH EVAL3D

"You can't improve what you can't measure."

[Image: Eval3D metric visualization]
```

#### Slide 2: Why Quality Assessment Matters
```
THE AI QUALITY PROBLEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI generates many outputs. How do you pick the best one?

COMMON ISSUES:
• Janus Problem (different faces from different views)
• Topology holes and artifacts
• Texture-geometry mismatch
• Poor rigging deformation

SOLUTION: Automated quality metrics

[Image: Good vs Bad AI 3D model comparison]
```

#### Slide 3: Eval3D Metrics Overview
```
EVAL3D: 5 QUALITY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────┬───────────┬────────────────────────┐
│ Metric              │ Range     │ What It Measures       │
├─────────────────────┼───────────┼────────────────────────┤
│ Geometric Consist.  │ 0-100     │ Surface normal quality │
│ Semantic Consist.   │ 0-100     │ View consistency       │
│ Structural Consist. │ 0-100     │ 3D predictability      │
│ Aesthetics          │ 0-1       │ Visual appeal          │
│ Text-3D Alignment   │ 0-1       │ Prompt adherence       │
└─────────────────────┴───────────┴────────────────────────┘

GOOD SCORES:
• Geometric: 85+
• Semantic: 80+
• Aesthetics: 0.7+
• Text-3D: 0.8+
```

#### Slide 4: Running Eval3D
```bash
# EVAL3D PIPELINE USAGE
# ─────────────────────────────────────────────────────

# Evaluate a single mesh
uv run eval3d-pipeline eval-mesh ./aethel.obj \
    --algo my_pipeline \
    --prompt "Android archaeologist, stylized sci-fi"

# Quick evaluation (aesthetics + text-3D only)
uv run eval3d-pipeline eval-mesh ./aethel.obj --quick

# Specific metrics
uv run eval3d-pipeline eval-mesh ./aethel.obj \
    -m geometric -m semantic -m aesthetics
```

#### Slides 5-20: Additional Eval3D Slides
```
5. Geometric Consistency Deep Dive
6. Semantic Consistency & Janus Problem
7. Structural Consistency with Zero123
8. Aesthetics Scoring with ImageReward
9. Text-3D Alignment with GPT-4o
10. Interpreting Your Results
11. Threshold Guidelines
12. Batch Evaluation for Multiple Models
13. Comparing Different Generation Methods
14. Using Metrics to Guide Iteration
15. Integration with Production Pipeline
16. Exercise 4: Evaluate Your Character
17. Case Study: Good vs Bad Model
18. Limitations of Automated Metrics
19. Human-in-the-Loop Evaluation
20. Module Summary
```

---

### 2.7 Module 7: Unreal Integration (15 slides)

#### Key Slides:
```
1. Module Title: Bringing Your Character to Life in Unreal
2. Project Setup & Folder Structure
3. Importing Rigged FBX
4. Skeleton & Skeletal Mesh Setup
5. Material & Texture Assignment
6. Animation Blueprint Basics
7. State Machine: Idle ↔ Walk
8. Speed-Based Blending
9. Adding Attack Animation
10. Character Blueprint Setup
11. Replacing the Default Mannequin
12. Testing in PIE (Play in Editor)
13. Common Import Problems
14. Exercise 5: Complete Integration
15. Module Summary & Course Wrap-Up
```

---

## 3. Tutorial Documentation

### 3.1 Document Structure

```
docs/
├── 00_prerequisites.md
├── 01_setup_guide.md
├── 02_character_spec_tutorial.md
├── 03_prompt_engineering_tutorial.md
├── 04_2d_generation_tutorial.md
├── 05_3d_conversion_tutorial.md
├── 06_rigging_tutorial.md
├── 07_eval3d_tutorial.md
├── 08_unreal_integration_tutorial.md
├── 09_troubleshooting_guide.md
└── 10_reference_sheets/
    ├── prompt_cheatsheet.md
    ├── rig_quality_checklist.md
    ├── import_settings_reference.md
    └── api_quick_reference.md
```

---

### 3.2 Tutorial Template: Character Spec (02_character_spec_tutorial.md)

```markdown
# Tutorial 2: Creating a Character Specification

## Overview

In this tutorial, you will:
- Understand the character specification schema
- Create your first character YAML file
- Run the prompt generator to verify your spec

**Time:** 15-20 minutes  
**Prerequisites:** Tutorial 1 complete, Python environment ready

---

## Step 1: Understand the Schema

The character specification uses YAML format with these fields:

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `name` | ✅ Yes | Character name | "Aethel" |
| `role` | No | Character role | "Android archaeologist" |
| `game_style` | No | Visual style | "stylized sci-fi" |
| `silhouette` | No | Body shape | "tall, long coat" |
| `color_palette` | No | Main colors | ["teal", "black"] |
| `key_props` | No | Items carried | ["data tablet"] |
| `animation_focus` | No | Planned animations | ["walk", "idle"] |
| `extra_notes` | No | Additional context | "Neon environment" |

---

## Step 2: Create Your Character File

1. Copy the template:
```bash
cp configs/_template.yaml configs/my_character.yaml
```

2. Open `configs/my_character.yaml` in your editor

3. Fill in your character details:

```yaml
name: "Nova"
role: "Space bounty hunter"
game_style: "cyberpunk, neon noir"
silhouette: "athletic build, armored vest, dual pistols"
color_palette:
  - "deep purple"
  - "neon pink accents"
  - "chrome silver"
key_props:
  - "twin plasma pistols"
  - "holographic visor"
animation_focus:
  - "run"
  - "aim"
  - "combat roll"
extra_notes: "Confident stance, battle-worn gear, slight smirk."
```

---

## Step 3: Validate Your Spec

Run the prompt generator in dry-run mode:

```bash
cd prompt_generation
uv run generate_prompts.py prompts -i configs/my_character.yaml --dry-run
```

**Expected Output:**
```
Loading character spec from: configs/my_character.yaml
Character: Nova (Space bounty hunter)
Generating prompts (version: v1)...

[DRY RUN] Printing prompts to stdout:

=== base_2d_full_body ===
Full-body concept art of a Space bounty hunter...
```

---

## Step 4: Common Mistakes to Avoid

### ❌ Too Vague
```yaml
role: "fighter"  # Too generic
```
### ✅ Specific
```yaml
role: "Space bounty hunter specializing in high-value targets"
```

### ❌ Too Many Colors
```yaml
color_palette: ["red", "blue", "green", "yellow", "purple", "orange"]
```
### ✅ Focused Palette
```yaml
color_palette: ["deep purple", "neon pink accents", "chrome silver"]
```

### ❌ Unclear Silhouette
```yaml
silhouette: "normal person"
```
### ✅ Distinctive Silhouette
```yaml
silhouette: "athletic build, armored vest, dual pistols on hips"
```

---

## Step 5: Exercise

Create a character spec for ONE of these archetypes:
- Medieval knight with enchanted shield
- Steampunk inventor with mechanical companion
- Underwater explorer with bio-luminescent suit

Save as `configs/exercise_character.yaml` and validate with dry-run.

---

## Summary

✅ You learned the YAML character spec schema  
✅ You created and validated a character file  
✅ You understand common mistakes to avoid

**Next:** Tutorial 3 - Prompt Engineering Deep Dive
```

---

### 3.3 Tutorial Template: Eval3D Integration (07_eval3d_tutorial.md)

```markdown
# Tutorial 7: Quality Assessment with Eval3D

## Overview

In this tutorial, you will:
- Set up the Eval3D pipeline
- Evaluate your AI-generated 3D model
- Interpret quality scores
- Use metrics to guide iteration

**Time:** 30-45 minutes  
**Prerequisites:** 3D model exported from Hunyuan/Meshy

---

## Step 1: Set Up Eval3D Pipeline

```bash
# Navigate to Eval3D pipeline
cd /path/to/Eval3d_pipline/eval3d-pipeline

# Install dependencies
uv sync

# Install rendering requirements
uv pip install trimesh pyrender opencv-python PyOpenGL numpy Pillow torch

# Set API key for Text-3D metric
export OPENAI_API_KEY=your-key-here
```

---

## Step 2: Prepare Your Mesh

Ensure your mesh is in the correct format:

```
my_character/
├── aethel.obj          # Main mesh file
├── aethel.mtl          # Material file (if OBJ)
└── textures/           # Texture images
    └── diffuse.png
```

**Supported formats:** `.obj`, `.glb`, `.ply`, `.stl`, `.fbx`

---

## Step 3: Run Quick Evaluation

Start with quick mode to get fast feedback:

```bash
uv run eval3d-pipeline eval-mesh ./my_character/aethel.obj \
    --algo ai_pipeline \
    --prompt "Android archaeologist, stylized sci-fi, tall with long coat" \
    --quick
```

**Quick mode runs:**
- Aesthetics (visual quality)
- Text-3D Alignment (prompt adherence)

---

## Step 4: Run Full Evaluation

For comprehensive assessment:

```bash
uv run eval3d-pipeline eval-mesh ./my_character/aethel.obj \
    --algo ai_pipeline \
    --prompt "Android archaeologist, stylized sci-fi, tall with long coat"
```

**Full mode adds:**
- Geometric Consistency (surface normals)
- Semantic Consistency (view identity)
- Structural Consistency (if Zero123 is set up)

---

## Step 5: Interpret Your Results

### Example Output:
```
🎨 Eval3D Pipeline Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Asset: aethel
Algorithm: ai_pipeline

┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                ┃ Score     ┃ Interpretation         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Geometric Consistency │ 78.5      │ ⚠️  Needs Improvement   │
│ Semantic Consistency  │ 85.2      │ ✅ Good                │
│ Aesthetics            │ 0.72      │ ✅ High Quality        │
│ Text-3D Alignment     │ 0.80      │ ✅ Strong Match        │
└───────────────────────┴───────────┴────────────────────────┘
```

### Score Interpretation Guide:

| Metric | Poor | Fair | Good | Excellent |
|--------|------|------|------|-----------|
| Geometric | <60 | 60-75 | 75-85 | 85+ |
| Semantic | <65 | 65-75 | 75-85 | 85+ |
| Aesthetics | <0.4 | 0.4-0.6 | 0.6-0.75 | 0.75+ |
| Text-3D | <0.5 | 0.5-0.7 | 0.7-0.85 | 0.85+ |

---

## Step 6: Diagnose Problems

### Low Geometric Score (< 75)

**Symptom:** Texture looks painted-on, doesn't match geometry  
**Cause:** AI created 2D details that aren't reflected in 3D

**Fix:**
- Regenerate with cleaner input images
- Use more explicit 3D-friendly prompts
- Consider manual mesh cleanup in Blender

### Low Semantic Score (< 75)

**Symptom:** Janus problem - different faces from different views  
**Cause:** AI didn't maintain consistent identity around the model

**Fix:**
- Use stricter T-pose prompts
- Generate more views before 3D conversion
- Select candidates with consistent front/back in 2D stage

### Low Aesthetics Score (< 0.6)

**Symptom:** Visual artifacts, poor materials, unpleasant appearance  
**Cause:** Generation quality issues

**Fix:**
- Higher resolution input images
- Better lighting in prompts
- Post-process textures in image editor

### Low Text-3D Score (< 0.7)

**Symptom:** Model doesn't match the prompt description  
**Cause:** Lost details during 2D→3D conversion

**Fix:**
- More explicit prompt details
- Select 2D candidates that clearly show all features
- Consider including props separately

---

## Step 7: Iteration Loop

Use metrics to guide your improvements:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Generate  →  Evaluate  →  Identify Problem  →  Fix   │
│      ↑                                            │     │
│      └────────────────────────────────────────────┘     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Track your iterations:**

| Version | Geometric | Semantic | Aesthetics | Text-3D | Notes |
|---------|-----------|----------|------------|---------|-------|
| v1 | 72.3 | 81.2 | 0.65 | 0.75 | Initial |
| v2 | 78.5 | 83.4 | 0.70 | 0.78 | Better pose |
| v3 | 84.1 | 86.7 | 0.75 | 0.82 | Fixed lighting |

---

## Step 8: Exercise

1. Evaluate your character from Tutorial 5
2. Record scores in the iteration table above
3. Identify the lowest-scoring metric
4. Propose a fix based on the diagnosis guide
5. (Optional) Implement fix and re-evaluate

---

## Summary

✅ You set up and ran the Eval3D pipeline  
✅ You interpreted quality scores  
✅ You learned to diagnose common problems  
✅ You understand the iteration loop

**Next:** Tutorial 8 - Unreal Integration
```

---

## 4. Assessment Materials

### 4.1 Quiz Questions

#### Module 1 Quiz: Introduction
```markdown
## Quiz 1: AI Asset Pipeline Fundamentals

**Instructions:** Answer all questions. Each correct answer = 1 point.

---

### Q1. What is the main advantage of AI-assisted character pipelines?
a) Characters look better than human-made ones
b) Dramatically reduced production time ✅
c) No human judgment required
d) Free to use commercially

### Q2. Which of these is NOT a stage in our pipeline?
a) Character specification
b) Prompt refinement
c) Neural network training ✅
d) Quality assessment

### Q3. Why do we use YAML for character specs instead of natural language?
a) YAML is faster to write
b) YAML enables reproducibility and automation ✅
c) AI models only understand YAML
d) YAML is more creative

### Q4. What is the "Janus problem" in AI 3D generation?
a) The model is too small
b) Different faces appear from different viewing angles ✅
c) The texture doesn't load
d) Animation doesn't work

### Q5. Which metric measures how well a 3D model matches its text prompt?
a) Geometric Consistency
b) Semantic Consistency
c) Aesthetics
d) Text-3D Alignment ✅
```

#### Module 2 Quiz: Prompt Engineering
```markdown
## Quiz 2: Prompt Engineering

---

### Q1. What is a "negative prompt"?
a) A prompt that generates sad characters
b) Instructions for what NOT to include in the image ✅
c) A prompt with mathematical expressions
d) A prompt written in reverse

### Q2. Which prompt is better for 3D modeling preparation?
a) "Cool robot character"
b) "Robot character, front view, T-pose, white background" ✅
c) "Robot doing a cool pose"
d) "Any robot picture"

### Q3. What is the recommended number of colors in a character palette?
a) 1
b) 2-4 ✅
c) 7-10
d) As many as possible

### Q4. Why is "silhouette" important in character spec?
a) It makes the character easier to recognize ✅
b) It determines the file size
c) It affects render time
d) It changes the animation speed

### Q5. What does "web search" do in our LLM refinement step?
a) Finds similar characters online
b) Looks up current AI art trends and techniques ✅
c) Downloads reference images
d) Checks for copyright issues
```

---

### 4.2 Practical Exercises

#### Exercise 1: Character Spec Design
```markdown
# Exercise 1: Design Your Character Specification

## Objective
Create a complete, well-designed character specification for an original character.

## Requirements
- [ ] Use the YAML template format
- [ ] Include ALL fields (name, role, game_style, silhouette, color_palette, key_props, animation_focus, extra_notes)
- [ ] Color palette has 2-4 colors with clear roles (primary, secondary, accent)
- [ ] Silhouette is distinctive and recognizable
- [ ] Props define character identity
- [ ] Animation focus is realistic for the character type

## Deliverable
- `configs/my_original_character.yaml`
- Brief explanation (2-3 sentences) of design choices

## Grading Rubric
| Criterion | Points |
|-----------|--------|
| All fields complete | 2 |
| Coherent design | 2 |
| Distinctive silhouette | 2 |
| Appropriate props | 2 |
| Explanation quality | 2 |
| **Total** | **10** |

## Due Date
[Insert date]
```

#### Exercise 2: Prompt Iteration
```markdown
# Exercise 2: Prompt Engineering Iteration

## Objective
Demonstrate the iterative prompt refinement process by generating three versions of prompts.

## Requirements
1. Use your character from Exercise 1
2. Generate base prompts (v1): `uv run generate_prompts.py prompts`
3. Refine with LLM (v2): `uv run generate_prompts.py refine`
4. Manually edit prompts (v3) based on what you learned
5. Generate images for each version

## Deliverable
- Three sets of prompts (v1, v2, v3)
- Generated images for each version (at least front view)
- Comparison document explaining:
  - What changed between versions
  - Which version produced the best results
  - Why you think certain changes helped or hurt

## Grading Rubric
| Criterion | Points |
|-----------|--------|
| Three prompt versions | 3 |
| Images generated | 3 |
| Meaningful changes between versions | 4 |
| Quality comparison analysis | 5 |
| **Total** | **15** |
```

#### Exercise 3: Full Pipeline
```markdown
# Exercise 3: Full Pipeline Execution

## Objective
Complete the entire pipeline from character spec to Unreal-ready asset.

## Requirements
1. Start with your character spec
2. Generate refined prompts
3. Generate T-pose images (front, side, back)
4. Convert to 3D using Hunyuan or Meshy
5. Auto-rig with MexMiao or Meshy
6. Generate at least 2 animations (idle + walk)
7. Run Eval3D assessment
8. Import into Unreal and test

## Deliverable
- Character YAML spec
- Generated prompts (final version)
- T-pose images (3 views)
- 3D model files (.fbx or .obj)
- Animation files
- Eval3D report (screenshot or JSON)
- Unreal project with:
  - Imported skeletal mesh
  - Animation Blueprint with idle ↔ walk
  - Video recording of character moving in game

## Grading Rubric
| Criterion | Points |
|-----------|--------|
| Complete spec | 2 |
| Quality prompts | 3 |
| Quality T-pose images | 5 |
| 3D model without major artifacts | 5 |
| Working rig with 2+ animations | 5 |
| Eval3D scores (bonus for >80% avg) | 5 |
| Unreal integration complete | 10 |
| Video demonstration | 5 |
| **Total** | **40** |
```

---

### 4.3 Debugging Scenarios

```markdown
# Debugging Practice Scenarios

## Scenario 1: T-Posing Character

**Symptom:** 
Your character appears in T-pose in the game instead of playing animations.

**Screenshot:**
[Character standing with arms out, no animation]

**Diagnostic Questions:**
1. Is the Animation Blueprint assigned to the Skeletal Mesh?
2. Does the Animation Blueprint have a valid State Machine?
3. Is the Anim Class set on the Character Blueprint?

**Solution:**
1. Open your Character Blueprint (BP_MyCharacter)
2. Select the Mesh component
3. In Details panel, find "Animation" section
4. Set "Anim Class" to your Animation Blueprint (ABP_MyCharacter)
5. Compile and Save
6. Play in Editor to test

---

## Scenario 2: Weird Hand Deformation

**Symptom:**
Character's hands deform strangely or "explode" during walk animation.

**Screenshot:**
[Hands stretching unnaturally]

**Diagnostic Questions:**
1. Were the hands properly weighted during auto-rigging?
2. Is the skeleton hierarchy correct?
3. Is the mesh scaled correctly?

**Solution:**
1. Re-run auto-rigging with "finger bones" option enabled
2. If using Meshy, try the "detailed hands" preset
3. As last resort, manually adjust hand bone weights in Blender

---

## Scenario 3: Concept Art Not Suitable for 3D

**Symptom:**
The 2D concept looks great, but the 3D conversion produces garbage.

**Screenshot:**
[Nice 2D art, terrible 3D mesh]

**Diagnostic Questions:**
1. Is the pose clear and T-pose-like?
2. Is the background clean/white?
3. Are front and side views provided?
4. Is lighting neutral (no dramatic shadows)?

**Solution:**
Regenerate 2D with better prompts:
```
BEFORE: "Cool android character with dramatic lighting"
AFTER:  "Full body T-pose of android character, front view, 
         white background, even lighting, no shadows, 
         neutral pose, clear silhouette"
```

---

## Scenario 4: Low Semantic Consistency Score

**Symptom:**
Eval3D gives semantic consistency score below 70.

**Eval3D Output:**
```
Semantic Consistency: 64.3  ⚠️ Needs Improvement
```

**Diagnostic Questions:**
1. Does the character look the same from all angles?
2. Are there multiple faces/identities on the model?
3. Did the 2D images have consistent style?

**Solution:**
1. Generate more 2D views before 3D conversion
2. Ensure all 2D images are from the same generation run
3. Use explicit "single character, one face" in prompts
4. Regenerate 3D with more consistent input images
```

---

## 5. Video Script

### 5.1 Show-and-Tell Video (15 minutes)

```markdown
# VIDEO SCRIPT: AI-Assisted Character Asset Pipeline
# Duration: 15 minutes
# Structure: Explain → Show → Try

═══════════════════════════════════════════════════════════════════════════════
SEGMENT 1: EXPLAIN (3 minutes)
═══════════════════════════════════════════════════════════════════════════════

## [0:00-0:30] Opening Hook

VISUALS: Time-lapse of traditional character creation (stock footage)

NARRATION:
"Creating a game character traditionally takes weeks. A concept artist sketches 
ideas. A 2D artist refines them. A 3D modeler builds the mesh. A rigger adds 
bones. An animator brings it to life. What if we could compress this into hours?"

TRANSITION: Pipeline diagram appears

---

## [0:30-1:30] The AI Pipeline Concept

VISUALS: Animated pipeline diagram (YAML → prompts → images → 3D → rig → game)

NARRATION:
"In this course, you'll build an AI-assisted pipeline that does exactly that.
We start with a simple YAML file describing our character. A Python script 
generates optimized prompts. These prompts feed into Gemini to create T-pose 
images. Those images go into Hunyuan 3D for mesh generation. Then MexMiao 
auto-rigs and animates. Finally, we import into Unreal.

The key insight: AI doesn't replace human creativity—it amplifies it. You still 
make all the creative decisions through your character spec and prompt engineering.
The AI just handles the labor-intensive execution."

---

## [1:30-2:30] Real-World Relevance

VISUALS: Screenshots from Ubisoft, EA presentations about AI tools

NARRATION:
"This isn't just an academic exercise. Major studios are already using similar 
pipelines. Ubisoft generates concept variations with AI. EA creates NPC assets 
at scale. Indie studios can now produce content that previously required large 
teams.

Understanding these tools isn't optional—it's becoming essential for modern 
game development."

---

## [2:30-3:00] What You'll Learn

VISUALS: Learning objectives bullet points

NARRATION:
"By the end of this course, you'll be able to:
- Design character specifications that work with AI tools
- Engineer prompts that produce consistent, high-quality results
- Evaluate AI outputs using metrics like Eval3D
- And integrate AI-generated characters into Unreal Engine

Let me show you how it works."

═══════════════════════════════════════════════════════════════════════════════
SEGMENT 2: SHOW (8 minutes)
═══════════════════════════════════════════════════════════════════════════════

## [3:00-4:00] The Character Spec

VISUALS: Screen recording of VS Code with aethel.yaml

NARRATION:
"Everything starts with a character spec. This YAML file defines who our 
character is. Let me walk you through each field.

[Scroll through file]

Name: Aethel. Role: Android archaeologist—this tells the AI what kind of 
character we're making. Game style: stylized sci-fi—this guides the visual 
aesthetic.

Silhouette is crucial: 'tall, long coat, mechanical arm.' This defines the 
recognizable shape. Color palette: teal, black, orange accents—just three 
colors keeps the design cohesive.

Key props: data tablet, arm-mounted scanner. These items define the character's 
identity and purpose.

Animation focus tells us what movements we'll need: walk, idle scanning, 
simple attack."

---

## [4:00-5:30] Running the Prompt Generator

VISUALS: Screen recording of terminal running generate_prompts.py

NARRATION:
"Now let's generate prompts. In the terminal, we run:

[Type command]
uv run generate_prompts.py prompts -i configs/aethel.yaml --dry-run

The dry-run flag shows us what would be generated without writing files.

[Show output]

Look at this base prompt. It combines all our spec fields into a coherent 
image generation prompt. Notice how it specifies 'front view, neutral pose, 
plain background'—these are critical for 3D conversion later.

But we can do better. Let's refine with GPT-5:

[Type command]
uv run generate_prompts.py refine -i configs/aethel.yaml --preview

[Show refined prompt]

The LLM has enhanced our prompt with more specific details, better style 
tokens, and negative prompts to avoid common problems."

---

## [5:30-7:00] Generated Images

VISUALS: Screen showing generated T-pose images

NARRATION:
"Here are the T-pose images generated by Gemini 3 Pro.

[Show front view]
The front view clearly shows the character's design: the mechanical arm, 
the long coat, the color scheme. Notice the clean background and neutral 
pose—perfect for 3D conversion.

[Show side view]
The side view gives us depth information. You can see how the coat flows, 
the thickness of the arm, the profile of the face.

[Show back view]
And the back view completes the turnaround. These three images together 
give the 3D generator everything it needs."

---

## [7:00-8:30] 3D Model & Rig

VISUALS: Screen recording of Hunyuan/Meshy output, then MexMiao rigging

NARRATION:
"I uploaded these images to Hunyuan 3D, and after about 30 seconds of 
processing, we got this mesh.

[Rotate 3D model]

It's not perfect—you can see some artifacts here—but it captures the overall 
design. The silhouette is correct. The proportions match. The key features 
are there.

Next, I ran this through MexMiao for auto-rigging:

[Show rigging interface]

It detected the humanoid structure and added a standard skeleton. Then I 
generated these animation clips:

[Play idle animation]
Idle: a subtle breathing motion.

[Play walk animation]
Walk: a full locomotion cycle.

These exported as FBX files ready for Unreal."

---

## [8:30-9:30] Eval3D Quality Check

VISUALS: Terminal showing Eval3D output

NARRATION:
"Before we import to Unreal, let's check quality with Eval3D:

[Run command]
uv run eval3d-pipeline eval-mesh ./aethel.obj --quick

[Show results]

Geometric consistency: 82. This means the surface normals match well.
Semantic consistency: 85. The character looks the same from all angles.
Aesthetics: 0.74. Good visual quality.
Text-3D alignment: 0.81. Strong match to our original prompt.

These scores tell us this model is ready for production. If any score was 
below 70, we'd want to regenerate."

---

## [9:30-11:00] Unreal Integration

VISUALS: Screen recording of Unreal Editor

NARRATION:
"Finally, let's bring Aethel into Unreal.

[Import FBX]
I import the rigged FBX. Unreal automatically creates the skeleton and 
skeletal mesh.

[Open Animation Blueprint]
In the Animation Blueprint, I've set up a simple state machine. Idle 
transitions to Walk based on speed. Walk transitions back to Idle when 
speed drops to zero.

[Open Character Blueprint]
The Character Blueprint uses our mesh and Animation Blueprint. I've assigned 
the mesh component and set the anim class.

[Play in Editor]
And here we go—Aethel walking around in our game world.

[WASD movement demonstration]

From a YAML file to a playable character. That's the AI asset pipeline."

═══════════════════════════════════════════════════════════════════════════════
SEGMENT 3: TRY (4 minutes)
═══════════════════════════════════════════════════════════════════════════════

## [11:00-13:00] Live Exercise

VISUALS: Screen recording of editing YAML file

NARRATION:
"Let's try creating a variation together. I'll modify Aethel's spec to 
create a different character.

[Open YAML file]

I'll change:
- name: 'Aethel' to 'Nova'
- role: 'Android archaeologist' to 'Space bounty hunter'
- color_palette: from teal/black to purple/pink
- key_props: from tablet to 'twin plasma pistols'

[Save file]

Now let's generate new prompts:

[Run generate command]

And generate just the front view to see the difference:

[Run image command]

[Show result]

Look at that—a completely different character from the same pipeline. The 
purple color scheme, the pistols, the confident stance. Same process, 
different creative direction."

---

## [13:00-14:30] Your Challenge

VISUALS: Challenge text on screen

NARRATION:
"Now it's your turn. Here's your challenge:

Create a character spec for one of these archetypes:
- A medieval knight with an enchanted shield
- A steampunk inventor with a mechanical companion
- An underwater explorer with a bio-luminescent suit

Then run the full pipeline:
1. Write the YAML spec
2. Generate and refine prompts
3. Create T-pose images
4. Convert to 3D and rig
5. Evaluate with Eval3D
6. Import to Unreal

Use the debugging guide when you get stuck. The troubleshooting scenarios 
cover the most common problems.

Post your results in the discussion forum. I'd love to see what you create!"

---

## [14:30-15:00] Closing

VISUALS: Course overview with links

NARRATION:
"In this video, we covered the complete AI asset pipeline from text spec 
to playable character. The documentation in the course repository has 
detailed tutorials for each step.

Remember: AI is a tool that amplifies your creativity. You're still the 
designer making the important decisions. You just have a much faster 
way to execute your vision.

Thanks for watching. See you in the exercises!"

[END CARD with links to:
- Course repository
- Discussion forum  
- Tutorial documentation]
```

---

### 5.2 Module-Specific Video Outlines

```markdown
# Video Outline: Module 2 - Prompt Engineering Deep Dive (8 minutes)

## Structure
- [0:00] Introduction to prompt engineering
- [1:00] Template system walkthrough
- [2:00] Style tokens reference
- [3:30] Negative prompts and why they matter
- [5:00] T-pose specific requirements
- [6:30] Live prompt iteration demo
- [7:30] Exercise introduction

---

# Video Outline: Module 6 - Eval3D Tutorial (10 minutes)

## Structure
- [0:00] Why quality metrics matter
- [1:00] Installing Eval3D pipeline
- [2:00] Understanding the 5 metrics
- [4:00] Running your first evaluation
- [5:30] Interpreting scores
- [7:00] Diagnosing common problems
- [8:30] Iteration strategy
- [9:30] Exercise introduction
```

---

## 6. Implementation Reference

### 6.1 Complete Pipeline Commands

```bash
# ═══════════════════════════════════════════════════════════════════════════
# COMPLETE PIPELINE COMMAND REFERENCE
# ═══════════════════════════════════════════════════════════════════════════

# --- SETUP ---
cd /path/to/3d_Modeling_withAI/prompt_generation
uv sync

# Set API keys
export OPENAI_API_KEY='sk-...'
export GEMINI_API_KEY='AI...'

# --- STAGE 1: Create Character Spec ---
cp configs/_template.yaml configs/my_character.yaml
# Edit the file with your character details

# --- STAGE 2: Generate & Refine Prompts ---
# Preview only (no API calls)
uv run generate_prompts.py prompts -i configs/my_character.yaml --dry-run

# Generate static prompts
uv run generate_prompts.py prompts -i configs/my_character.yaml -v v1

# Refine with LLM
uv run generate_prompts.py refine -i configs/my_character.yaml -v v1

# Refine with web search for current trends
uv run generate_prompts.py refine -i configs/my_character.yaml -v v1 --web-search

# --- STAGE 3: Generate T-Pose Images ---
# Preview prompts only
uv run generate_prompts.py images -i configs/my_character.yaml --prompts-only

# Generate all views
uv run generate_prompts.py images -i configs/my_character.yaml -v v1

# Generate specific views
uv run generate_prompts.py images -i configs/my_character.yaml --views front,side

# --- FULL PIPELINE (ALL STAGES) ---
uv run generate_prompts.py all -i configs/my_character.yaml -v v1

# --- STAGE 4-5: Manual Steps ---
# 1. Upload T-pose images to Hunyuan.3D or Meshy
# 2. Download generated mesh (.obj or .fbx)
# 3. Upload mesh to MexMiao or Meshy for rigging
# 4. Generate animations and download

# --- STAGE 6: Quality Assessment ---
cd /path/to/Eval3d_pipline/eval3d-pipeline

# Quick evaluation
uv run eval3d-pipeline eval-mesh /path/to/mesh.obj \
    --algo my_pipeline \
    --prompt "Character description" \
    --quick

# Full evaluation
uv run eval3d-pipeline eval-mesh /path/to/mesh.obj \
    --algo my_pipeline \
    --prompt "Character description"

# --- STAGE 7: Unreal Import ---
# 1. Import FBX to Unreal Content Browser
# 2. Create Animation Blueprint
# 3. Set up state machine
# 4. Create Character Blueprint
# 5. Test in Play-in-Editor
```

---

### 6.2 File Structure Reference

```
AI_Character_Pipeline_Project/
│
├── prompt_generation/                    # Stage 1-3: Prompts & Images
│   ├── configs/
│   │   ├── _template.yaml               # Character template
│   │   ├── aethel.yaml                  # Example character
│   │   └── my_character.yaml            # Your character
│   │
│   ├── output/
│   │   └── [timestamp]/
│   │       ├── base/                    # Stage 1 outputs
│   │       ├── refined/                 # Stage 2 outputs
│   │       ├── common/                  # Stage 3 outputs
│   │       └── images/                  # Stage 4 outputs
│   │           ├── character_tpose_front_v1.jpg
│   │           ├── character_tpose_side_v1.jpg
│   │           └── character_tpose_back_v1.jpg
│   │
│   └── src/                             # Pipeline source code
│
├── 3d_assets/                           # Stage 4-5: 3D Models
│   └── [character_name]/
│       ├── mesh/
│       │   ├── character.obj
│       │   ├── character.mtl
│       │   └── textures/
│       │
│       ├── rigged/
│       │   └── character_rigged.fbx
│       │
│       └── animations/
│           ├── character_idle.fbx
│           ├── character_walk.fbx
│           └── character_attack.fbx
│
├── eval3d_results/                      # Stage 6: Quality Assessment
│   └── [character_name]/
│       ├── renders/                     # Multi-view renders
│       └── eval3d_scores.json          # Metric scores
│
└── UnrealProject/                       # Stage 7: Game Integration
    └── Content/
        └── Characters/
            └── [character_name]/
                ├── Mesh/
                │   └── SK_Character.uasset
                ├── Animations/
                │   ├── A_Character_Idle.uasset
                │   ├── A_Character_Walk.uasset
                │   └── ABP_Character.uasset
                └── Blueprints/
                    └── BP_Character.uasset
```

---

## 7. Asset Licensing Guide

### 7.1 License Template

```markdown
# Asset License Notice

## AI-Generated Content

The following assets in this project were generated using AI tools:

### 2D Concept Art
- **Tool:** Google Gemini 3 Pro Image Preview
- **TOS:** https://ai.google.dev/terms
- **Usage Rights:** Educational, non-commercial use only

### 3D Models
- **Tool:** Tencent Hunyuan.3D / Meshy AI
- **TOS:** [Link to respective TOS]
- **Usage Rights:** Check tool-specific licensing

### Rigged Animations
- **Tool:** MexMiao / Meshy AI Auto-Rig
- **TOS:** [Link to respective TOS]
- **Usage Rights:** Check tool-specific licensing

## Commercial Use Warning

These assets are provided for **educational purposes only**. 

For commercial use:
1. Generate your own assets using the pipeline
2. Review the Terms of Service of each AI tool
3. Ensure compliance with commercial licensing requirements
4. Consider using commercially-licensed alternatives

## Attribution

When sharing or extending this project, please attribute:
- Original prompt engineering by [Your Name]
- AI tools used: Gemini, Hunyuan, Meshy, MexMiao
- Eval3D metrics by Duggal et al. (CVPR 2025)
```

---

### 7.2 TOS Quick Reference

| Tool | Commercial Use | Attribution Required | Data Usage |
|------|---------------|---------------------|------------|
| **Gemini** | Check plan | Varies | May train on outputs |
| **Hunyuan** | Check TOS | Varies | Review data policy |
| **Meshy** | Paid plans | Check TOS | May retain data |
| **MexMiao** | Check TOS | Check TOS | Review policy |
| **OpenAI** | Business API | No | API data not used |

**Always check current TOS before commercial deployment.**

---

## 8. Quick Reference Cards

### 8.1 Prompt Engineering Cheatsheet

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PROMPT ENGINEERING CHEATSHEET                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STRUCTURE:                                                                  │
│  [Subject] + [Style] + [View] + [Background] + [Quality] + [Negative]       │
│                                                                              │
│  EXAMPLE:                                                                    │
│  "Full-body concept art of an android archaeologist, stylized sci-fi,       │
│   front view T-pose, white background, high detail, 4K resolution.          │
│   No text, no watermarks, no shadows."                                      │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  STYLE TOKENS:                                                               │
│  • "game concept art"     • "character turnaround"                          │
│  • "stylized AAA game"    • "hand-painted textures"                         │
│  • "semi-realistic"       • "anime style"                                   │
│  • "cel-shaded"           • "low poly"                                      │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  T-POSE REQUIREMENTS:                                                        │
│  ✅ "arms extended horizontally at shoulder height"                          │
│  ✅ "palms facing down, fingers spread"                                      │
│  ✅ "feet shoulder-width apart"                                              │
│  ✅ "facing camera directly (front) / profile (side)"                        │
│  ✅ "neutral expression, relaxed pose"                                       │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  NEGATIVE PROMPTS (Always include):                                          │
│  "No text, no watermarks, no signature, no frame, no border,                │
│   no multiple characters, no extreme angles, no dramatic lighting"          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Rig Quality Checklist

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RIG QUALITY CHECKLIST                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  JOINT DEFORMATION (Test in idle/walk)                                       │
│  [ ] Shoulders rotate without mesh tearing                                   │
│  [ ] Elbows bend naturally (no candy-wrapper effect)                         │
│  [ ] Wrists rotate without hand explosion                                    │
│  [ ] Hips deform smoothly in walk cycle                                      │
│  [ ] Knees bend without mesh intersection                                    │
│  [ ] Spine bends without breaking mesh                                       │
│                                                                              │
│  SKELETON STRUCTURE                                                          │
│  [ ] Root bone at origin (0, 0, 0)                                           │
│  [ ] Hips as first child of root                                             │
│  [ ] Symmetric left/right bone naming                                        │
│  [ ] Finger bones present (if needed)                                        │
│                                                                              │
│  ANIMATION COMPATIBILITY                                                     │
│  [ ] Idle animation loops smoothly                                           │
│  [ ] Walk cycle has no foot sliding                                          │
│  [ ] Attack animation returns to idle                                        │
│  [ ] No jitter or pops between animations                                    │
│                                                                              │
│  SCORING:                                                                     │
│  Excellent: All checkboxes ✓                                                 │
│  Good: 10-12 checkboxes ✓                                                    │
│  Fair: 7-9 checkboxes ✓                                                      │
│  Poor: <7 checkboxes ✓ (consider regenerating)                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.3 Eval3D Score Interpretation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      EVAL3D SCORE INTERPRETATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  GEOMETRIC CONSISTENCY (0-100)                                               │
│  85+ : Excellent - Texture matches geometry perfectly                        │
│  75-84: Good - Minor texture-geometry mismatch                               │
│  60-74: Fair - Noticeable painted-on details                                 │
│  <60 : Poor - Significant texture-geometry conflict                          │
│                                                                              │
│  SEMANTIC CONSISTENCY (0-100)                                                │
│  85+ : Excellent - Same identity from all views                              │
│  75-84: Good - Minor view inconsistencies                                    │
│  65-74: Fair - Noticeable Janus problem                                      │
│  <65 : Poor - Multiple identities detected                                   │
│                                                                              │
│  AESTHETICS (0-1)                                                            │
│  0.75+: Excellent - High visual quality                                      │
│  0.6-0.74: Good - Acceptable quality                                         │
│  0.4-0.59: Fair - Visible artifacts                                          │
│  <0.4 : Poor - Major visual issues                                           │
│                                                                              │
│  TEXT-3D ALIGNMENT (0-1)                                                     │
│  0.85+: Excellent - Strong prompt adherence                                  │
│  0.7-0.84: Good - Most prompt elements present                               │
│  0.5-0.69: Fair - Missing some prompt elements                               │
│  <0.5 : Poor - Significant prompt mismatch                                   │
│                                                                              │
│  OVERALL RECOMMENDATION:                                                      │
│  Average ≥ 75%: Ship it ✅                                                   │
│  Average 65-74%: Consider improvements                                       │
│  Average < 65%: Regenerate                                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Appendix: Slide Deck Image Suggestions

### 9.1 Required Visuals

| Slide | Visual | Source Suggestion |
|-------|--------|-------------------|
| Pipeline Overview | Animated flow diagram | Create in Figma/Miro |
| Traditional Pipeline | Timeline infographic | Stock + annotation |
| YAML Example | Syntax-highlighted code | Screenshot from VS Code |
| Prompt Comparison | Before/After images | Generated samples |
| T-Pose Examples | 3-view character | Pipeline output |
| Eval3D Results | Terminal screenshot | Actual eval output |
| Unreal Integration | Editor screenshot | Your UE project |

### 9.2 Video B-Roll Needs

| Segment | B-Roll | Duration |
|---------|--------|----------|
| Opening | Game character montage | 10s |
| Industry | Studio logos/screenshots | 15s |
| Demo | Screen recordings | 5min |
| Exercise | Text overlay animations | 30s |

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Created** | December 2025 |
| **Author** | AI Asset Pipeline Course Team |
| **Last Updated** | [Auto-update on commit] |
| **License** | MIT (Code), CC-BY (Documentation) |

---

<p align="center">
<i>Building the future of game character creation, one prompt at a time.</i>
</p>

