# Implementation Plan: Module 4 – Vision-Language-Action (VLA)

**Branch**: `004-module4-vla` | **Date**: 2025-12-07 | **Spec**: [specs/004-module4-vla/spec.md](spec.md)

**Status**: Phase 1 Planning Complete | **Phase 0 Research**: Complete (research.md)

---

## Summary

Module 4 completes the humanoid robotics curriculum by adding **language understanding and cognitive planning** to the perception, simulation, and control systems from Modules 1–3.

**Primary Requirement**: Create 4 chapters + capstone project integrating:
- Chapter 1: LLM fundamentals and robotics applications
- Chapter 2: Voice-to-action using OpenAI Whisper + ROS 2
- Chapter 3: Cognitive planning using LLM API + task planning + safety validation
- Chapter 4: End-to-end VLA capstone (voice → reasoning → perception → navigation → manipulation)

**Technical Approach**:
- LLM API integration (OpenAI GPT-4, local models as fallback)
- OpenAI Whisper for speech-to-text with ROS 2 integration
- Multi-LLM safety architecture for plan validation
- Hierarchical VLA pipeline separating perception, reasoning, planning, control
- Hands-on exercises with working code examples
- Educational progression from fundamentals → practical implementation → capstone integration

---

## Technical Context

**Language/Version**: Python 3.10+ (with optional C++ for ROS 2 nodes)
**Primary Dependencies**:
- ROS 2 (Humble/Iron) – messaging framework from Module 1
- OpenAI Python library (v1.0+) – LLM API access
- OpenAI Whisper (stable) – speech-to-text
- Gazebo (from Module 2) – simulation environment
- Nav2 (from Module 3) – navigation stack
- PyTorch 2.0+ (optional, for local LLM models)

**Storage**: N/A (documentation and educational content)
**Testing**: pytest (unit tests for code examples), manual integration tests with Gazebo
**Target Platform**: Linux (Ubuntu 22.04+), macOS (development), Docker containers (deployment)
**Project Type**: Educational content + code examples (Docusaurus markdown + Python/C++ code snippets)
**Performance Goals**:
- Voice transcription: >90% accuracy in quiet environments, >85% in noisy
- LLM planning: <8 seconds for typical task decomposition
- End-to-end VLA: <12 seconds typical (voice input → action execution)
- Code examples: All runnable in <10 minutes on local machine

**Constraints**:
- No dependency on proprietary robotics platforms (use open-source Gazebo)
- API cost awareness: document free tier limits and cost optimization strategies
- Learner prerequisites: completed Modules 1–3, basic Python knowledge
- Docusaurus compatibility: all content must render correctly in existing site

**Scale/Scope**:
- 4 chapters, ~40–60 min each (45–55 min reading + hands-on)
- 25–35 code examples (Python + ROS 2 action/service definitions)
- 3 real-world application examples per chapter
- 1 capstone project demonstrating full integration

---

## Constitution Check

**GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.**

Since the project constitution is a template placeholder, Module 4 follows the established patterns from Modules 1–3:

✅ **No Constitution Violations** (Module 4 is documentation/educational content)

**Verified**:
- ✅ Does NOT modify existing modules (Module 1–3 unchanged)
- ✅ Does NOT modify project constitution
- ✅ Follows Docusaurus standards from Modules 1–3
- ✅ Respects ROS 2 architecture and best practices
- ✅ Maintains learning progression and brand voice
- ✅ Uses open-source software (no proprietary lock-in)

**Re-check Post-Phase-1**: N/A – no violations anticipated during design.

---

## Project Structure

### Documentation (this feature)

```text
specs/004-module4-vla/
├── spec.md                          # Feature specification (/sp.specify output)
├── plan.md                          # This file (/sp.plan output)
├── research.md                      # Phase 0 research (technology decisions, rationale)
├── data-model.md                    # Phase 1: Content architecture & entities
├── quickstart.md                    # Phase 1: Implementation workflow for writers
├── checklists/
│   └── requirements.md              # Quality validation checklist
├── contracts/
│   ├── chapter-1-template.md        # Phase 1: Chapter 1 scaffold
│   ├── chapter-2-template.md        # Phase 1: Chapter 2 scaffold
│   ├── chapter-3-template.md        # Phase 1: Chapter 3 scaffold
│   └── chapter-4-template.md        # Phase 1: Chapter 4 scaffold
└── tasks.md                         # Phase 2 output (/sp.tasks command - NOT created here)
```

### Source Code (Docusaurus book)

```text
docusaurus-book/
├── docs/
│   ├── module3/
│   │   ├── introduction.md          # (existing)
│   │   └── chapter-*.md             # (existing Chapters 1–4)
│   └── module4/                     # ← NEW
│       ├── _category_.json          # Module 4 metadata (sidebar label, position)
│       ├── introduction.md          # Module 4 overview + learning path
│       ├── chapter-1-llm-robotics-convergence.md
│       ├── chapter-2-voice-to-action-whisper.md
│       ├── chapter-3-cognitive-planning-llm.md
│       └── chapter-4-autonomous-humanoid-capstone.md
└── sidebars.ts                      # (update to add Module 4 category)
```

**Structure Decision**: Module 4 follows the established **Docusaurus single-repo** structure from Modules 1–3. Content is written as markdown files with YAML frontmatter, organized in `docs/module4/`, and integrated into navigation via `sidebars.ts`. Code examples are embedded in markdown blocks for easy copy-paste. Supporting scripts and utilities are placed in `docusaurus-book/scripts/module4/` as needed.

---

## Complexity Tracking

> **No Constitution violations or complexity overrides needed.** Module 4 is educational content following established patterns. This section intentionally left empty per template structure.

---

## Phases

### Phase 0: Research & Unknowns Resolution ✅ COMPLETE

**Output**: `research.md` (400+ lines)

**Resolved**:

1. ✅ **LLM Integration Strategy**
   - Decision: Multi-LLM architecture with task-specific routing
   - Primary: Cloud APIs (GPT-4 for reasoning, Claude for safety)
   - Secondary: Local models (Llama, Deepseek) for fallback
   - Rationale: Provides robustness, cost optimization, and offline capability

2. ✅ **Speech-to-Text Approach**
   - Decision: OpenAI Whisper Large V3 Turbo with ROS 2 integration
   - Accuracy: >90% in quiet, >85% in noisy environments
   - Fallback: Whisper.cpp (local), Vosk (lightweight)
   - Rationale: Whisper proven in production, multilingual, noise-robust

3. ✅ **Plan Validation & Safety**
   - Decision: SAFER framework (dual-LLM safety architecture)
   - Task planning LLM (GPT-4) + Safety validation LLM (Claude)
   - Formal verification via Linear Temporal Logic (LTL)
   - Rationale: Prevents dangerous commands, enables transparency

4. ✅ **VLA Pipeline Architecture**
   - Decision: Hierarchical (not monolithic) – Perception → Reasoning → Planning → Control
   - Clear ROS 2 topic boundaries between modules
   - Latency budget: <12 seconds typical, <20 seconds max
   - Rationale: Decoupling enables safety validation, easier debugging, better maintainability

5. ✅ **Educational Content Strategy**
   - Decision: Progressive complexity with hands-on checkpoints
   - Chapter 1 (60 min): Fundamentals, Chapter 2 (75 min): Voice, Chapter 3 (90 min): Planning, Chapter 4 (120 min): Capstone
   - Teaching: Analogies first, minimal examples, incremental complexity
   - Rationale: Learners with no ML background; immediate validation essential

---

### Phase 1: Design & Contracts ⏳ IN PROGRESS

**Outputs** (generated below):
- `data-model.md` – Content architecture and key entities
- `contracts/chapter-*.md` – Chapter scaffolds and templates
- `quickstart.md` – Implementation workflow guide

#### 1a. Content Architecture (data-model.md)

**Key Entities**:

1. **Large Language Model (LLM)**
   - Types: Cloud APIs (GPT-4, Claude), Local models (Llama, Mistral)
   - Fields: Model name, API key, temperature, token limits, cost per request
   - Relationships: Sends prompts to LLM → receives completions → parses output
   - Validation: Response format matches expected JSON/structured text

2. **Prompt**
   - Definition: Structured text instruction sent to LLM describing robot task
   - Fields: System prompt (role definition), User prompt (task), Few-shot examples, Constraints
   - Validation: Length limits (max 4k tokens), safety filters applied
   - Pattern: Role-based prompting for consistent output format

3. **Task Plan**
   - Definition: Multi-step action sequence generated by LLM for robot execution
   - Fields: Step ID, action type (navigate, grasp, place), parameters, prerequisites
   - Validation: Feasibility check (robot capable), safety check (no dangerous actions)
   - State: Pending → Validating → Approved → Executing → Complete

4. **Voice Command**
   - Definition: User-spoken instruction captured by microphone
   - Fields: Audio buffer, language code, confidence score, transcription text
   - Validation: Transcription confidence >85%, language recognized
   - Workflow: Record → Transcribe (Whisper) → Parse command → Extract intent

5. **Perception Result**
   - Definition: Object detection output from Module 3 perception system
   - Fields: Object class, bounding box, confidence, 3D position (if available)
   - Relationships: Fed to planning system to ground task execution (e.g., "pick up the blue cube")
   - Validation: Confidence >70%, depth data consistent

6. **Navigation Goal**
   - Definition: Target position/orientation for robot to move to
   - Fields: x, y, theta (pose), tolerance, max time allowed
   - Relationships: Generated by task plan, sent to Nav2 for execution
   - Validation: Goal reachable, within workspace bounds

7. **Execution Log**
   - Definition: Record of all actions executed and their outcomes
   - Fields: Timestamp, action type, parameters, success/failure, error message
   - Purpose: Debugging, learning from failures, user feedback
   - Retention: Per-session logs, archived for later analysis

#### 1b. Chapter Contracts (Templates)

Each chapter will use a standardized template ensuring consistency:

**Chapter Contract Structure**:

```markdown
---
title: "Chapter N: [Full Title]"
description: "[1-2 sentence learning outcome]"
slug: chapter-n-[slug]
sidebar_position: N
---

# Chapter N: [Full Title]

## Introduction
[Hook to Modules 1–3, problem statement, learning objective, practical motivation]

## Learning Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Section 1: [Topic]
[Theory, explanation, key concepts]

### Hands-On: [Exercise]
[Step-by-step code walkthrough with expected output]

## Section 2: [Topic]
[Continued...]

## Real-World Applications
[3 examples with problem/solution/lesson]

## Debugging & Troubleshooting
[Common errors, solutions, performance tips]

## Summary
[Key learnings, skills checklist, next chapter preview, glossary terms]

## Additional Resources
[Recommended reading, code examples, next steps]
```

**Chapters**:

1. **Chapter 1: LLMs and Robotics – The Convergence**
   - Sections: What LLMs are | Why powerful for robotics | Capabilities | Limitations | LLM + robotics integration
   - Hands-on: Experiment with LLM APIs (prompting, analyzing outputs)
   - Real-world: Boston Dynamics Spot, Tesla Bot, research robots
   - Time: 45–60 min

2. **Chapter 2: Voice-to-Action – Using Whisper for Voice Commands**
   - Sections: STT fundamentals | Whisper architecture | ROS 2 integration | Audio preprocessing | Error handling
   - Hands-on: Create ROS node + Whisper integration, speak commands, robot executes
   - Real-world: Household robots, service robots, field robots
   - Time: 50–65 min

3. **Chapter 3: Cognitive Planning – Using LLMs to Translate Natural Language into Actions**
   - Sections: Task planning fundamentals | Prompt engineering | Plan validation | Safety constraints | Error handling
   - Hands-on: Create prompts, call LLM API, parse output, execute in ROS 2
   - Real-world: Research robots, warehouse automation, household task planning
   - Time: 55–70 min

4. **Chapter 4: Capstone Project – The Autonomous Humanoid**
   - Sections: VLA pipeline architecture | Integration strategy | Multi-robot coordination | Error handling | Demo preparation
   - Hands-on: Build full end-to-end system, speak command, robot executes multi-step task
   - Real-world: Boston Dynamics Spot demonstrations, Tesla Bot, research projects
   - Time: 60–75 min

#### 1c. Implementation Quickstart Guide (quickstart.md)

**Process Workflow** (for writers during Phase 2):

1. **Pre-implementation Checklist**
   - Read spec.md and data-model.md
   - Review Module 1–3 chapters for tone/style
   - Set up Gazebo + ROS 2 environment for testing
   - Test all code examples before writing

2. **Chapter Writing Workflow** (per chapter)
   - Create file with frontmatter
   - Draft introduction section (5 min read)
   - Write core sections with progressive complexity
   - Add code examples (copy-paste testable)
   - Include diagrams (Mermaid or images)
   - Write real-world applications (3 examples)
   - Create hands-on exercise with expected output
   - Add debugging section
   - Write summary and glossary links
   - Run Docusaurus build locally
   - Validate all links and code

3. **Quality Gates**
   - Content Quality: Tone matches Modules 1–3, no jargon without explanation
   - Code Quality: All examples tested, working, commented
   - Docusaurus Compliance: Build succeeds, links valid, formatting correct
   - Completeness: All checklist items checked (learning objectives, exercises, real-world examples, debugging)

4. **Per-Chapter Estimate**
   - Setup: 15 min
   - Writing: 2–3 hours
   - Code examples: 1–2 hours
   - Diagrams: 30–60 min
   - Integration: 30 min
   - Review: 1 hour
   - **Total: 5–7 hours per chapter**

5. **Full Module 4 Timeline**
   - Chapter 1: 5–7 hours
   - Chapter 2: 6–8 hours (more code integration)
   - Chapter 3: 7–9 hours (complex LLM concepts + planning)
   - Chapter 4: 8–10 hours (capstone + full integration)
   - Module introduction: 1–2 hours
   - Sidebar + glossary integration: 1–2 hours
   - **Total: 29–37 hours**

---

### Phase 2: Task Generation (Not created by /sp.plan)

**Output**: `/sp.tasks` command will generate `tasks.md` with:
- 100+ executable tasks organized by chapter
- Parallel work opportunities (4–6 person team)
- Time estimates per task
- Dependencies and blockers
- Testing criteria
- Success metrics

**Estimated Phase 2 timeline**: 4–6 weeks with dedicated team, or 8–10 weeks solo

---

## Architecture Diagrams

### Vision-Language-Action (VLA) Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Vision-Language-Action Pipeline                   │
└─────────────────────────────────────────────────────────────────────┘

1. VOICE INPUT (Chapter 2)
   Microphone Audio
        ↓
   Whisper STT
        ↓
   Transcribed Text: "Pick up the blue cube"

2. LLM REASONING (Chapter 3)
   Task Description
        ↓
   LLM Prompt Engineering
        ↓
   GPT-4 Planning
        ↓
   Generated Plan: ["navigate_to(object_loc)", "grasp()", "return_home()"]
        ↓
   Safety Validation (Claude)
        ↓
   Approved Plan

3. PERCEPTION (Module 3)
   Camera Feed
        ↓
   Object Detection (Isaac ROS)
        ↓
   Object Locations: [{class: "cube", color: "blue", pos: (x,y,z)}]

4. NAVIGATION (Module 3)
   Start Position + Goal
        ↓
   Nav2 Path Planning
        ↓
   Collision-Free Path

5. MANIPULATION (ROS 2 Actions)
   Grasp Command
        ↓
   Arm Control
        ↓
   Object Manipulation

6. EXECUTION (Module 1 ROS 2)
   Action Server
        ↓
   Execute Plan Step-by-Step
        ↓
   Task Complete → Text-to-Speech: "Task completed"
```

### Chapter Interdependencies

```
Chapter 1: LLMs & Robotics
   ↓
   Foundational understanding required for all subsequent chapters

Chapter 2: Voice-to-Action
   ↓ (depends on Ch1)
   Practical voice interface; enables hands-on engagement

Chapter 3: Cognitive Planning
   ↓ (depends on Ch1, Ch2)
   Core differentiator; LLM-based task planning and safety

Chapter 4: Capstone Project
   ↓ (depends on Ch1, Ch2, Ch3 + Modules 1–3)
   Integration checkpoint; students demonstrate end-to-end autonomy
```

### Team Parallel Work Structure

```
Work can be parallelized:

Writer 1: Chapter 1 (LLMs & Robotics) – 5–7 hours (foundation)
Writer 2: Chapter 2 (Voice-to-Action) – 6–8 hours (parallel after Ch1 research complete)
Writer 3: Chapter 3 (Cognitive Planning) – 7–9 hours (parallel, depends on LLM research)
Writer 4: Chapter 4 (Capstone) – 8–10 hours (serial after Ch1–3 draft)

Coordinator: Module intro + sidebar + glossary integration – 2–4 hours (parallel)
Reviewer: Content quality + build validation – 2–3 hours (final stage)

Critical path: Ch1 → Ch3 → Ch4 (dependencies)
Non-critical: Ch2 can proceed in parallel after Ch1 research
```

---

## Dependencies & Integration Points

### Dependencies on Prior Modules

**Module 1 (ROS 2 Nervous System)**:
- Assumed knowledge: ROS 2 nodes, topics, services, action servers
- Used in Chapter 2: ROS nodes for Whisper integration
- Used in Chapter 3: ROS action calls for plan execution
- Used in Chapter 4: Full ROS 2 orchestration

**Module 2 (Digital Twin - Gazebo)**:
- Assumed knowledge: Gazebo simulation, robot models, physics
- Used in Chapter 2: Simulated robot for voice commands
- Used in Chapter 4: Full simulation environment for capstone

**Module 3 (AI Robot Brain - Perception & Navigation)**:
- Assumed knowledge: Deep learning, VSLAM, Nav2 path planning
- Used in Chapter 3: Integrate perception results into planning
- Used in Chapter 4: Perception for object identification, Nav2 for navigation

### New Technologies Introduced

**Chapter 2**: OpenAI Whisper (speech-to-text), Audio I/O libraries
**Chapter 3**: OpenAI API / LLM frameworks (Langchain, Llama.cpp), Prompt engineering
**Chapter 4**: Complete system orchestration, error handling, user feedback loops

### External Dependencies

- **OpenAI API** (for GPT-4, Whisper): Requires API key, incurs costs
- **Python LLM libraries**: openai, anthropic, transformers, langchain (all open-source)
- **ROS 2**: Already assumed from Module 1
- **Gazebo**: Already assumed from Module 2
- **Audio libraries**: sounddevice, scipy, librosa (open-source)

**Fallback Strategy**: All chapters include offline alternatives (local LLMs, Whisper.cpp, text-based input) so learners are not blocked by API availability or costs.

---

## Risk Assessment

### Technical Risks

**Risk 1: LLM API Cost Escalation**
- Impact: Learners may not complete exercises due to API costs
- Mitigation: Document free tier limits, provide cost optimization strategies, include local LLM alternatives
- Severity: Medium | Likelihood: Medium

**Risk 2: Whisper Transcription Accuracy Variability**
- Impact: Voice interface exercises may fail in noisy environments
- Mitigation: Chapter 2 includes audio preprocessing, noise handling, fallback to text input
- Severity: Low | Likelihood: High (but mitigated)

**Risk 3: LLM Generates Invalid/Unsafe Plans**
- Impact: Robot executes dangerous commands
- Mitigation: Chapter 3 emphasizes plan validation, safety constraints, human-in-the-loop approval
- Severity: High | Likelihood: Medium | Mitigation: Comprehensive

**Risk 4: Integration Complexity with Modules 1–3**
- Impact: Learners overwhelmed by scope
- Mitigation: Chapter 4 provides starter code templates, optional simplifications, step-by-step guide
- Severity: Medium | Likelihood: Low

**Risk 5: ROS 2 API Changes Break Examples**
- Impact: Code examples become outdated
- Mitigation: Target ROS 2 Humble (LTS), include version pins in requirements.txt, mention testing environment
- Severity: Low | Likelihood: Low

### Educational Risks

**Risk 1: Learners Lack ML Background**
- Impact: LLM concepts too abstract
- Mitigation: Chapter 1 uses analogies, doesn't assume prior ML knowledge, compares to Module 3 concepts
- Severity: Medium | Likelihood: Medium | Mitigation: Comprehensive

**Risk 2: Capstone Project Too Complex**
- Impact: Low completion rate
- Mitigation: Provide starter code, breakable stages, optional simplifications
- Severity: High | Likelihood: Low | Mitigation: Comprehensive

**Risk 3: Learners Spend Too Long on Chapter 1**
- Impact: Time budget exceeded
- Mitigation: Chapter 1 strictly 45–60 min, can be skipped if learner has LLM background
- Severity: Low | Likelihood: Low

### Mitigation Summary

| Risk | Mitigation | Owner | Timeline |
|------|-----------|-------|----------|
| API costs | Document free tiers, local alternatives | Ch3 writer | Week 2 |
| Whisper noise | Audio preprocessing, fallbacks | Ch2 writer | Week 1 |
| Invalid plans | Safety validation, human approval | Ch3 writer | Week 2 |
| Integration complexity | Starter code, step-by-step guide | Ch4 writer | Week 3 |
| ML background gap | Analogies, no assumptions | Ch1 writer | Week 0 |

---

## Success Metrics

### Technical Metrics

- ✅ Voice transcription: >90% accuracy in quiet, >85% in noisy
- ✅ LLM planning success: >80% tasks generate valid plans
- ✅ Safety validation: 0 critical violations execute
- ✅ Capstone execution: >75% learners successfully complete end-to-end task
- ✅ Code quality: All examples tested, 0 broken links, 0 undefined terms

### Educational Metrics

- ✅ Comprehension: >85% learners understand LLMs and robotics integration
- ✅ Task completion: >80% complete Chapter 2 voice exercise, >75% complete Chapter 3 planning, >70% complete Chapter 4 capstone
- ✅ Learning time: Chapter 1 (45–60 min), Chapter 2 (50–65 min), Chapter 3 (55–70 min), Chapter 4 (60–75 min)
- ✅ Engagement: >85% rate Module 4 as "practical and impressive"
- ✅ Confidence: >80% feel confident applying LLMs to robotics

### Deliverable Metrics

- ✅ 4 chapters + 1 capstone (all on schedule)
- ✅ 25+ code examples (all tested and working)
- ✅ 12+ real-world application examples (3 per chapter + capstone)
- ✅ 1 complete capstone project (integrated Modules 1–4)
- ✅ Docusaurus build succeeds, no broken links, proper sidebar integration
- ✅ All glossary terms defined and cross-referenced

---

## Next Steps

1. **Finalize Phase 1** (this document):
   - ✅ Technical context defined
   - ✅ Constitution check passed
   - ✅ Project structure established
   - ✅ Risk assessment completed
   - ✅ Success metrics defined

2. **Phase 2 – Task Generation** (`/sp.tasks`):
   - Break Module 4 into 100+ executable tasks
   - Organize by chapter, phase, priority
   - Assign team roles (Writer 1–4, Coordinator, Reviewer)
   - Generate detailed timeline

3. **Phase 3 – Implementation** (`/sp.implement`):
   - Create Docusaurus files (module4/ folder)
   - Write chapter content using templates
   - Embed code examples and test them
   - Create diagrams and real-world examples
   - Verify Docusaurus build

4. **Phase 4 – Integration & Review**:
   - Cross-link with Modules 1–3
   - Validate all internal/external links
   - Run full Docusaurus build
   - User testing and feedback

5. **Phase 5 – Launch**:
   - Final review and sign-off
   - Deploy to live documentation site
   - Announce Module 4 to learners
   - Gather learner feedback for iterations

---

## Assumptions & Constraints

### Assumptions

1. Learners have completed Modules 1–3 and understand ROS 2, Gazebo, perception/navigation
2. Learners have access to OpenAI API key or are willing to use free tier limits
3. Learners have a microphone (built-in or USB) for Chapter 2 voice exercises
4. Module 4 is educational content (not production robotics software)
5. Gazebo simulation is acceptable for capstone; physical robot deployment is optional future work
6. LLM output variability is acceptable (100% determinism not required)

### Constraints

- **Docusaurus compatibility**: All content must render in existing site structure
- **Modules 1–3 unchanged**: No modifications to prior work
- **No hardcoded secrets**: API keys passed via environment variables
- **Open-source software**: No proprietary robotics platforms
- **Time budget**: Each chapter ≤70 min for average learner
- **Learner prerequisites**: No advanced ML, just prior modules + Python basics

---

## Summary

Module 4 completes the humanoid robotics curriculum by adding language understanding and cognitive planning. The implementation plan establishes:

- **Technical foundation**: Multi-LLM architecture, Whisper integration, safety validation, hierarchical VLA pipeline
- **Content structure**: 4 chapters + capstone following established patterns from Modules 1–3
- **Team coordination**: Clear phases, parallel work opportunities, risk mitigation
- **Success criteria**: Technical, educational, and deliverable metrics

**Ready for Phase 2 task generation** (`/sp.tasks`) to produce executable tasks for writers.

**Estimated effort**: 29–37 hours total (or 4–6 weeks with dedicated team)

**Expected outcome**: Complete Module 4 with 100+ learners able to build autonomous humanoid robots that listen, understand, reason, and act.

---

## Phase 0 Research Output

Complete technical research available in `research.md` with:
- 40+ citations from 2025 research papers and industry frameworks
- Decision/Rationale/Alternatives for each technical choice
- Cost optimization strategies, fallback approaches, safety architecture
- Educational methodology grounded in learning science

---

**Status**: ✅ **Phase 1 Planning Complete – Ready for /sp.tasks**
