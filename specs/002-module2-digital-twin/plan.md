# Implementation Plan: Module 2 – The Digital Twin (Gazebo & Unity)

**Branch**: `002-module2-digital-twin` | **Date**: 2025-12-06 | **Spec**: [specs/002-module2-digital-twin/spec.md](spec.md)

**Input**: Feature specification from `/specs/002-module2-digital-twin/spec.md`

---

## Summary

Module 2 extends the Physical AI & Humanoid Robotics book with 4 chapters on digital twins—virtual robot simulations using Gazebo (physics) and Unity (rendering). The implementation focuses on:

1. **Content development workflow**: Progressive chapter writing with hands-on exercises
2. **Docusaurus integration**: Proper frontmatter, sidebar navigation, code examples
3. **ROS 2 bridge**: All simulations connect to learners' Module 1 ROS 2 knowledge
4. **Quality gates**: All code examples tested; all terms glossary-linked; brand voice consistent

The plan prioritizes **learning progression** (Chapters 1→4 build confidence and skills) and **practical applicability** (every exercise produces working code learners can modify and deploy).

---

## Technical Context

**Content Type**: Educational Docusaurus book (Markdown + code examples)
**Language/Framework**: Markdown (content), Gazebo (physics), Unity (3D rendering), Python/C++ (code examples)
**Primary Dependencies**: ROS 2, Gazebo, Unity, rclpy, ROS# (Unity bridge)
**Storage**: Local file system (Markdown); Docker images for simulation environments
**Testing**: Code example validation (executable, no errors); brand voice consistency checks
**Target Platform**: Web (Docusaurus static site); learners run simulations locally (Linux/Docker)
**Project Type**: Hybrid (content + interactive simulation guides)
**Performance Goals**: Chapters load <2 seconds; code examples run without errors
**Constraints**: Simple English (20-word sentences); beginner-friendly (no assumed graphics experience); offline-capable
**Scale/Scope**: 4 chapters (~40-50 pages total); 12-16 code examples; 15 glossary terms; 4 real-world case studies

---

## Constitution Check

**Gate Status**: ✅ PASS (Module 2 is a documentation/content module, not a software library)

**Applicability Notes**:

- **Library-First Principle**: N/A (not a software library; content module extending the book)
- **CLI Interface**: N/A (content-focused; no CLI required)
- **Test-First**: ✅ Applies (all code examples must be executable and tested before publishing)
- **Brand Voice Consistency**: ✅ Applies (all writing must follow established constitution rules: simple English, visionary, human-centered)
- **Glossary & Terminology**: ✅ Applies (all new terms integrated into Module 1 glossary; no synonyms introduced)

**Compliance Rationale**: Module 2 is a pure content extension following the established book constitution. No new principles violated. All existing constraints (simple English, Docusaurus markdown, progressive learning) apply.

---

## Project Structure

### Documentation (this feature)

```text
specs/002-module2-digital-twin/
├── spec.md                          # Feature specification ✅ (created)
├── requirements-checklist.md        # Quality validation ✅ (created)
├── plan.md                          # This file (implementation plan)
├── research.md                      # Phase 0 output (TBD)
├── data-model.md                    # Phase 1 output (TBD)
├── writing-workflow.md              # Phase 1 output (TBD)
├── docusaurus-integration.md        # Phase 1 output (TBD)
└── tasks.md                         # Phase 2 output (/sp.tasks command - NOT created here)
```

### Content Structure (Docusaurus)

```text
docusaurus-book/docs/
├── module2/                         # NEW: Module 2 root
│   ├── _category_.json              # Sidebar configuration
│   ├── introduction.md              # Module 2 intro & learning path
│   ├── chapter-1-environment.md     # Ch 1: Physics simulation
│   ├── chapter-2-physics.md         # Ch 2: Gravity, collisions
│   ├── chapter-3-unity.md           # Ch 3: High-fidelity rendering
│   ├── chapter-4-sensors.md         # Ch 4: Sensor simulation
│   └── code-examples/               # NEW: Executable code examples
│       ├── ch1-gazebo-world.py
│       ├── ch2-physics-params.py
│       ├── ch3-unity-bridge/
│       └── ch4-sensor-sim.py
│
├── glossary.md                      # UPDATED: Extend with 15 new Module 2 terms
└── sidebar-config.md                # UPDATED: Register Module 2 chapters
```

**Structure Decision**: Module 2 is a self-contained section within the existing Docusaurus structure. It mirrors Module 1's layout (chapters as individual files) for consistency. Code examples live in a dedicated `code-examples/` subdirectory for easy testing and maintenance.

---

## Phase 0: Research & Design Decisions

### Research Tasks (Deferred Clarifications)

The following design decisions are resolved for planning; implementation will follow established patterns:

#### 1. **Exercise Approach: Scaffolded Progressive Independence**

**Decision**: Mix of approaches (tutorials → scaffolds → from-scratch)

**Rationale**:
- Chapter 1: Step-by-step tutorial (build confidence with Gazebo basics)
- Chapter 2: Scaffolded code (learners fill in physics parameters, observe changes)
- Chapter 3: Step-by-step tutorial with guided extension (Unity is new; scaffolding reduces frustration)
- Chapter 4: From-scratch (learners have skills; building sensor sim from scratch reinforces autonomy)

**Alternatives Considered**:
- Full from-scratch (risky; learners may struggle early, reducing confidence)
- Full tutorials (safe but boring; learners don't own the code)
- Consistent approach (violates progressive complexity principle)

#### 2. **Chapter 3 (Unity) Requirement Status: REQUIRED**

**Decision**: Chapter 3 is required; all learners must complete it.

**Rationale**:
- Spec emphasizes digital twins = physics + rendering (Gazebo + Unity)
- Skipping rendering means missing 25% of module value
- "High-fidelity rendering enables human-robot interaction" is core to the Digital Human vision
- Progression without Chapter 3 breaks the complete digital twin narrative

**Alternatives Considered**:
- Optional chapter (learners might skip; incomplete understanding of digital twins)
- Recommended but skippable (confusing; inconsistent with Module 1 mandatory structure)

#### 3. **Code Example Language: Python Primary + C++ Secondary**

**Decision**: Python primary; C++ optional supplementary examples

**Rationale**:
- Module 1 uses rclpy (Python); continuity important for learners
- Gazebo sensor simulation: Python examples (via rospy/rclpy) are most beginner-friendly
- Unity integration: C# for game engine scripts; Python for ROS 2 bridges
- C++ examples provided for performance-critical learners (advanced)

**Alternatives Considered**:
- C++ only (too complex for beginners; violates accessibility principle)
- Mixed equally (confusing; learners don't know which to follow)

#### 4. **Simulation Environment Delivery: Docker Container**

**Decision**: Provide pre-built Docker image with Gazebo + ROS 2 + development tools

**Rationale**:
- Removes environment setup friction (learners get hands-on immediately)
- Consistent across Windows/Mac/Linux (learners can follow tutorials exactly)
- Offline-capable (Docker image is self-contained)
- Low barrier to start (one command: `docker run`)

**Alternatives Considered**:
- Local installation guides (setup guides get outdated; OS-specific issues)
- Cloud-based simulation (requires internet; violates offline-capable constraint)

#### 5. **Real-World Examples: Case Studies + Links**

**Decision**: Each chapter includes 1 concrete case study + links to open-source projects

**Rationale**:
- Case studies make concepts tangible ("How Tesla Bot uses simulation")
- Links enable deeper learning for motivated readers
- Builds credibility and relevance (learners see real robots use these techniques)

**Alternatives Considered**:
- Hypothetical examples only (less motivating; less credible)
- Many examples per chapter (overwhelms learners; dilutes focus)

---

## Writing Workflow

### Content Development Phases

#### **Phase 1A: Chapter Outlines & Learning Objectives**

**Output**: Detailed outlines for each chapter with:
- Learning objectives (3-5 per chapter)
- Section breakdown with subsection topics
- Exercise specification (inputs, expected outputs, evaluation criteria)
- Real-world example outline (company, technology, lesson)

**Success Criteria**:
- Outlines approved by book architect (consistency with Module 1 style)
- Learning objectives map 1:1 to acceptance scenarios in spec
- Exercises are independent, testable, and producible within 15-20 minutes

#### **Phase 1B: Chapter Drafts**

**Output**: Full chapter drafts in Docusaurus markdown

**Writing Process Per Chapter**:
1. Write section content (progressive complexity; explain jargon on first use)
2. Embed code examples inline (with syntax highlighting)
3. Include real-world example (3-5 paragraphs with image/diagram if available)
4. Add exercise section with step-by-step guidance
5. Summarize learning objectives achieved

**Brand Voice Checkpoints**:
- Sentence length: ≤20 words (auto-check via word count)
- Paragraph length: 2-4 sentences (visual scan)
- Active voice: Prefer "learners will" over "it is expected that"
- No undefined jargon: Every new term introduced and glossary-linked

**Code Quality Checkpoints**:
- All examples executable (tested in Docker environment)
- All examples include comments (explain intent, not syntax)
- All examples integrate with ROS 2 (demonstrate Module 1 continuity)

#### **Phase 1C: Peer Review & Refinement**

**Output**: Final chapter drafts with feedback incorporated

**Review Process**:
- Content review (clarity, accuracy, pace appropriate for beginners)
- Brand voice review (consistency with Module 1; simple English)
- Code review (executability, clarity, best practices)
- Integration review (links to glossary, cross-references, sidebar structure)

#### **Phase 1D: Glossary & Sidebar Integration**

**Output**: Updated glossary.md + _category_.json sidebar configuration

**Glossary Updates**:
- Add 15 new Module 2 terms with definitions
- Review Module 1 terms; update if needed for consistency
- Ensure all chapter content links to glossary entries

**Sidebar Configuration**:
- Register Module 2 as a top-level section
- Order chapters 1→4 with clear titles
- Add metadata: description, icon, position

---

## Docusaurus Integration

### Frontmatter Requirements (Per Chapter)

Every chapter file **must** include:

```markdown
---
title: "Chapter 1: Physics Simulation and Environment Building"
description: "Learn Gazebo basics: creating worlds, adding gravity, and simulating robot environments."
slug: /module2/chapter-1-environment
sidebar_position: 1
sidebar_label: "Ch 1: Environment Building"
---
```

**Fields**:
- `title`: Full chapter title (matches spec)
- `description`: 1-2 sentence summary (appears in search, sidebar hover)
- `slug`: URL path (must start with `/module2/` for proper routing)
- `sidebar_position`: Order (1-4 for chapters; 0 for introduction)
- `sidebar_label`: Short label for sidebar (max 30 chars)

### Heading Hierarchy

**Required Structure**:
- H1: Chapter title (one per file)
- H2: Major sections (Learning Objectives, Topics, Exercise, Real-World Example, Summary)
- H3: Subsections within topics (e.g., "Creating a Gazebo World", "Understanding Friction")

**Example**:
```markdown
# Chapter 1: Physics Simulation and Environment Building

## Learning Objectives

### By the end of this chapter, you will be able to:

## Topics

### What is a Digital Twin?

### Gazebo Overview

## Exercise

### Step 1: Install Gazebo

## Summary
```

### Code Block Formatting

**Requirements**:
- Use triple backticks with language identifier: ` ```python`, ` ```bash`, etc.
- Include comments explaining intent
- Keep examples <40 lines (readability)
- Test all examples before publishing

**Example**:
```python
# Ch 2: Adjust physics parameters to simulate heavier objects
import rospy
from gazebo_msgs.srv import SetModelProperties

def increase_mass(model_name, new_mass):
    """Set a model's mass in Gazebo simulation."""
    rospy.wait_for_service('/gazebo/set_model_properties')
    set_props = rospy.ServiceProxy('/gazebo/set_model_properties', SetModelProperties)
    set_props(model_name, mass=new_mass)
    print(f"Updated {model_name} mass to {new_mass} kg")
```

### Internal Links

**Format**: Use relative paths from `docusaurus-book/docs/`

**Examples**:
- Link to glossary term: `[Digital Twin](../glossary.md#digital-twin)`
- Link to Module 1 chapter: `[Module 1 ROS 2 basics](../module1/chapter-1-middleware.md)`
- Link to code example: `[Full code example](../module2/code-examples/ch1-gazebo-world.py)`

### Images & Assets

**Storage**: `docusaurus-book/static/images/module2/`

**Requirements**:
- Optimize to <200 KB per image (web performance)
- Include alt-text for accessibility
- Use descriptive filenames: `ch1-gazebo-world-example.png` (not `image1.png`)

**Markdown Format**:
```markdown
![Gazebo world with robot and obstacles](../../../static/images/module2/ch1-gazebo-world.png)
```

---

## Testing & Validation

### Code Example Validation

**Process**:
1. Run each code example in Docker environment
2. Verify no errors, warnings, or exceptions
3. Verify output matches expected behavior described in chapter
4. Document any setup steps (install packages, source environment, etc.)

**Checklist per Example**:
- ✅ Executable without modification
- ✅ Imports resolved (no missing dependencies)
- ✅ Output matches chapter description
- ✅ Comments explain intent and key steps

### Brand Voice Validation

**Automated Checks**:
- Sentence length tool: flag sentences >20 words
- Readability: ensure 8th-grade reading level (Flesch-Kincaid)
- Jargon check: ensure all technical terms are in glossary

**Manual Checks**:
- Visionary tone: every chapter connects to "Digital Human" vision
- Human-centered: focus on learner benefit, not technology for its own sake
- Engaging: real-world examples motivate; exercises give wins

### Integration Tests

**Docusaurus Build**:
```bash
cd docusaurus-book
npm run build  # Must succeed with zero errors
```

**Link Validation**:
- All internal links resolve (no 404s in sidebar, code, glossary)
- All external links tested (case studies, open-source projects)

**Sidebar Navigation**:
- Module 2 appears in sidebar
- Chapters 1-4 nest under Module 2
- Clickable links work; landing pages render correctly

---

## Deliverables & Success Criteria

### Phase 0 Deliverables (Research)
- ✅ Design decisions documented (this section)
- ✅ Exercise approach finalized
- ✅ Chapter 3 status confirmed (required)
- ✅ Code language choices justified

### Phase 1 Deliverables (Design)
- ✅ Chapter outlines with learning objectives
- ✅ Writing workflow documented
- ✅ Docusaurus integration guide finalized
- ✅ Code testing requirements specified

### Phase 2 Deliverables (Tasks - via /sp.tasks)
- Detailed task breakdown for each chapter
- Acceptance criteria for each section
- Code example specifications with test cases

### Success Metrics

**Content Quality**:
- 4 chapters, 40-50 pages total
- 12-16 executable code examples (100% pass tests)
- 15 glossary terms (all linked)
- 4 real-world case studies

**Learning Outcomes**:
- Learners complete Chapter 1 → understand Gazebo basics (90% completion)
- Learners complete Chapter 2 → predict robot behavior from physics (80% accuracy)
- Learners complete Chapter 3 → create realistic Unity robots (85% completion)
- Learners complete Chapter 4 → simulate sensors realistically (85% completion)

**Brand Voice Consistency**:
- 0 undefined jargon terms
- 100% sentences ≤20 words (or justified exceptions)
- 80%+ readers rate as "engaging and practical"

**Technical Integration**:
- Docusaurus build succeeds (0 errors)
- All internal links valid (0 broken links)
- All code examples executable in Docker environment (0 failures)
- Sidebar navigation shows Module 2 chapters correctly

---

## Next Steps

1. **Phase 0 Complete**: Design decisions finalized ✅
2. **Phase 1: Design** (Next):
   - Run `/sp.tasks` to generate detailed task breakdown for each chapter
   - Create research.md with full design patterns
   - Create writing-workflow.md with chapter-specific guidance
3. **Phase 2: Implementation** (After tasks approved):
   - Write chapter outlines and learning objectives
   - Draft chapter content (4 chapters)
   - Develop and test code examples
   - Review and refine
4. **Phase 3: Integration** (Final):
   - Build Docusaurus locally
   - Validate all links and code examples
   - Submit for peer review

---

**Status**: Plan complete. Ready for `/sp.tasks` to generate detailed implementation task breakdown.
