# Preset: GenerateReadingGuide

## Purpose
Create learner-facing reading guides for modules or chapters with time estimates, prerequisite summaries, learning outcomes, and navigation hints. Helps learners plan their study time and understand expectations.

## Subagents Called
1. **BookWriter** — Generates guide content, learning summaries, navigation suggestions
2. **StructureAgent** — Analyzes module structure to extract outline and flow
3. **ContentValidator** — Verifies prerequisites and cross-module references are accurate
4. **QualityGuard** — Reviews guide for clarity and accessibility

## Skills Used
1. **VisionaryTone** — Makes reading guides inspiring and motivational
2. **ExplainSimple** — Breaks down learning outcomes into simple language
3. **GenerateLessonFormat** — Structures guide with clear sections
4. **ConsistencyCheck** — Ensures recommendations match established patterns

## Input Signature
```yaml
scope: string               # "module" | "chapter" (e.g., "module4" or "module4/chapter-2")
include_sections: list     # Sections to include: ["overview", "prerequisites", "learning_outcomes", "time_estimate", "topics", "practice", "glossary_preview", "next_steps"]
format: string             # "markdown" | "html" | "json"
estimate_type: string      # "reading_time" | "total_time" | "detailed_breakdown" (default: "total_time")
target_audience: string    # "beginner" | "intermediate" | "advanced" (for context/tone)
```

## Output Format
```yaml
guide_content: string           # Full reading guide text (Markdown/HTML/JSON)
scope_covered: string           # What module/chapter was analyzed
sections_included: list         # Sections generated
total_time_estimate: string     # "2.5 hours" or "2 hours 30 minutes"
time_breakdown: object          # Breakdown by section (reading, exercises, review)
prerequisites_listed: integer   # Count of prerequisite modules/chapters
learning_outcomes_count: integer # Count of learning objectives
glossary_terms_preview: integer  # Count of new terms introduced
internal_links: integer         # Cross-module references included
file_created: string            # Path to generated guide file
```

## Safety Rules

1. **Time estimates must be realistic** — Based on actual chapter length and complexity
2. **Prerequisite accuracy critical** — Verify each listed prerequisite is actually required
3. **Don't over-promise** — Avoid claiming learners will master advanced topics in short time
4. **Link validation** — Every cross-module reference must be verified to exist
5. **Tone must inspire** — Reading guide should motivate learner to start, not overwhelm

## Workflow Steps

### Step 1: Content Analysis
- StructureAgent reads target module/chapter files
- Count total words, sections, code examples, exercises
- Identify all prerequisite modules/chapters referenced
- Extract all learning objectives already written

### Step 2: Time Estimation
- BookWriter calculates reading time (assume 200 words/minute for comprehension)
- Add exercise time (based on hands-on exercise complexity)
- Add review/practice time (assume 10-15 minutes per chapter)
- Total time = reading + exercises + review

### Step 3: Content Generation
- **Overview:** 2-3 sentence summary answering "What will I learn?"
- **Prerequisites:** List of modules/chapters that should be completed first
- **Learning Outcomes:** Testable objectives learner will achieve
- **Time Breakdown:** Estimate for reading, exercises, review (can be per-section)
- **Topics Overview:** List of sections/lessons in order
- **Practice Opportunities:** Count and type of hands-on exercises
- **Glossary Preview:** Key terms learner will encounter (sample 5-10 terms)
- **What's Next:** Teaser for following module/chapter

### Step 4: Formatting & Enhancement
- VisionaryTone ensures motivational, inspiring language
- ExplainSimple makes expectations clear and achievable
- GenerateLessonFormat structures guide with clear sections
- Add visual elements (emojis, checkmarks) to break up text

### Step 5: Integration & Output
- Save guide to appropriate location (e.g., docs/module4/READING_GUIDE.md)
- Generate version for display in Docusaurus if applicable
- Output guide in requested format (Markdown, HTML, JSON)

## Example Invocation

### Command
```
GenerateReadingGuide --scope module4 --include_sections ["overview", "prerequisites", "learning_outcomes", "time_estimate", "topics", "practice", "glossary_preview", "next_steps"] --format markdown --estimate_type detailed_breakdown --target_audience beginner
```

### Expected Output
```markdown
# Module 4 Reading Guide: LLM & Humanoid Robotics

## Overview

Welcome to **Module 4: LLM & Humanoid Robotics**! In this module, you'll discover how **Large Language Models** (the technology behind ChatGPT) can power robots to understand human commands, plan complex behaviors, and interact naturally with people.

By the end of Module 4, you'll understand:
- How LLMs "think" and generate intelligent responses
- How to connect LLMs to ROS 2 robots via Python
- How to build voice-controlled robots using Whisper (speech recognition)
- How to implement task planning and autonomous decision-making
- How to train and deploy a humanoid robot capstone project

**Time Commitment:** 3 hours total (broken down below)

---

## Prerequisites

Before starting Module 4, make sure you've completed:

- ✅ **Module 1: ROS 2 Fundamentals** — You'll need to understand ROS 2 nodes, subscriptions, publishers, and services
- ✅ **Module 2: Gazebo & Digital Twins** — You'll work with simulated robots and physics
- ✅ **Module 3: Advanced Perception & Planning** — You'll build on concepts of computer vision and path planning

If you haven't completed these modules, we recommend reviewing:
- [Module 1 Recap: ROS 2 Nodes](/docs/module1/chapter-1-ros2-fundamentals)
- [Module 3 Recap: Navigation Planning](/docs/module3/chapter-4-nav2-path-planning)

---

## Learning Outcomes

By completing Module 4, you will be able to:

- [ ] **Understand** how Large Language Models work (neural networks, tokens, inference)
- [ ] **Explain** the difference between supervised learning and LLMs' generative approach
- [ ] **Implement** a ROS 2 node that uses Whisper for voice recognition
- [ ] **Design** a task planner that uses LLM reasoning for robot decision-making
- [ ] **Build** a complete humanoid robot capstone project integrating all concepts
- [ ] **Debug** common LLM and speech recognition issues
- [ ] **Apply** LLM techniques to your own robotics projects

---

## Time Breakdown

### Total Time: ~3 hours

| Activity | Time | Details |
|----------|------|---------|
| **Chapter 1: LLM-Robotics Convergence** | 50 min | Reading + code examples + real-world applications |
| **Chapter 2: Voice-to-Action with Whisper** | 50 min | Reading + Whisper integration + hands-on exercise |
| **Chapter 3: Cognitive Planning with LLM** | 55 min | Advanced planning concepts + capstone introduction |
| **Chapter 4: Autonomous Humanoid Capstone** | 60 min | Full capstone project + debugging + summary |
| **Total Reading & Theory** | 100 min | Distributed across all chapters |
| **Total Hands-On Exercises** | 80 min | Coding, testing, running examples |
| **Total Review & Debugging** | 20 min | Troubleshooting + summary |

**Study Tips:**
- Schedule 1-2 hour blocks for best retention (with 10-minute breaks)
- Complete each chapter before moving to the next (they build on each other)
- Don't skip code examples—run them and experiment
- Use the glossary to clarify terms you encounter

---

## Topics Overview

Module 4 consists of 4 chapters + introduction + glossary:

1. **Introduction: Why LLMs + Robotics?**
   - Hook: Humanoid robots that understand and respond to humans
   - Learning objectives overview
   - Estimated time: 10 minutes

2. **Chapter 1: LLM-Robotics Convergence** (50 min)
   - How neural networks work (LLM foundation)
   - Transformer architecture (why LLMs are powerful)
   - Token prediction (how LLMs generate text)
   - Integrating LLMs with ROS 2
   - 2 code examples (Python + rclpy)
   - Real-world applications (Tesla, OpenAI, Boston Dynamics)

3. **Chapter 2: Voice-to-Action with Whisper** (50 min)
   - What is automatic speech recognition (ASR)?
   - Whisper: How it works
   - Audio processing pipeline
   - Building a ROS 2 speech-to-action node
   - 2 code examples
   - Real-world applications (voice assistants, accessibility)

4. **Chapter 3: Cognitive Planning with LLM** (55 min)
   - Task decomposition (breaking big problems into steps)
   - LLM-based reasoning for robotics
   - Prompt engineering (how to ask robots the right questions)
   - Advanced error handling
   - 2 code examples
   - Introduction to capstone project

5. **Chapter 4: Autonomous Humanoid Capstone** (60 min)
   - Building complete end-to-end system
   - Integration of LLM + voice + planning
   - Hands-on capstone exercise
   - Debugging common issues
   - Where to go next (Module 5 preview)

6. **Glossary: Key Terms** (as reference)
   - All new technical terms bolded and defined
   - Quick lookup while reading

---

## Practice Opportunities

Module 4 includes **hands-on exercises** to solidify learning:

| Chapter | Exercise Type | Estimated Time | Difficulty |
|---------|---------------|-----------------|-----------|
| Chapter 1 | 2 code examples | 15 min | Beginner |
| Chapter 2 | Voice command node | 20 min | Beginner-Intermediate |
| Chapter 3 | Task planner implementation | 25 min | Intermediate |
| Chapter 4 | Full capstone project | 30 min | Intermediate-Advanced |
| **Total** | **4 exercises** | **~90 min** | **Beginner → Advanced** |

All exercises are:
- ✓ Runnable in isolation (copy-paste and go)
- ✓ Include expected output (so you know if you're on track)
- ✓ Include common errors & fixes (debugging guidance)
- ✓ Build toward the capstone project

---

## Glossary Preview

You'll encounter these technical terms in Module 4. They're defined in context as you read, and collected in the glossary:

- **LLM (Large Language Model)** — A neural network trained on vast text to generate language
- **Token** — A unit of text (word or subword) processed by language models
- **Transformer** — Neural network architecture that powers modern LLMs
- **Attention Mechanism** — How transformers focus on relevant parts of input
- **Whisper** — OpenAI's automatic speech recognition model
- **ASR (Automatic Speech Recognition)** — Converting speech audio to text
- **Task Decomposition** — Breaking complex problems into simpler steps
- **Prompt Engineering** — Writing instructions to guide LLM behavior
- **Inference** — Running a trained model to generate predictions/outputs

[See full glossary at end of module]

---

## What's Next?

After completing Module 4, you'll be ready for:

- **Module 5: Reinforcement Learning for Robotics** — Train robots to learn from experience
- **Advanced Capstone Projects** — Combine everything you've learned into real-world applications
- **Research & Development** — Explore cutting-edge robotics and AI

---

## How to Use This Guide

1. **First Time?** Read this guide top-to-bottom to understand scope and time commitment
2. **Planning Your Study?** Use the time breakdown to schedule your learning
3. **Already Reading?** Use the topics overview to navigate between sections
4. **Need Prerequisites?** Click links above to refresh concepts from earlier modules
5. **Stuck?** Check the glossary preview, then detailed glossary at end of module

---

## Tips for Success

✨ **Best Practices:**
- **Schedule concentrated study time** (1-2 hour blocks work best)
- **Type out code examples** rather than copy-pasting (builds muscle memory)
- **Experiment with code** — change values, try different inputs
- **Debug hands-on** — error messages are learning opportunities
- **Join the community** — discuss challenges in forums/Discord if available

---

## Questions or Feedback?

If something is unclear, broken, or could be better explained, please share feedback. This curriculum is continuously improved based on learner input.

---

**Ready to start?** Begin with [Module 4 Introduction](/docs/module4/introduction) or jump to [Chapter 1: LLM-Robotics Convergence](/docs/module4/chapter-1-llm-robotics-convergence).

Happy learning! 🚀

---

output_yaml:
  guide_content: "[Full markdown above]"
  scope_covered: "module4"
  sections_included: ["overview", "prerequisites", "learning_outcomes", "time_estimate", "topics", "practice", "glossary_preview", "next_steps"]
  total_time_estimate: "3 hours"
  time_breakdown:
    reading_and_theory: "100 minutes"
    hands_on_exercises: "80 minutes"
    review_and_debugging: "20 minutes"
  prerequisites_listed: 3
  learning_outcomes_count: 7
  glossary_terms_preview: 9
  internal_links: 6
  file_created: "docs/module4/READING_GUIDE.md"
```

### Command (Chapter-Specific)
```
GenerateReadingGuide --scope module4/chapter-2 --include_sections ["overview", "prerequisites", "learning_outcomes", "time_estimate"] --format markdown --estimate_type reading_time --target_audience intermediate
```

### Expected Output (Excerpt)
```markdown
# Reading Guide: Chapter 2 - Voice-to-Action with Whisper

## Quick Facts
- **Time to Complete:** 50 minutes
  - Reading & Theory: 25 min
  - Code Examples: 12 min
  - Hands-On Exercise: 13 min
- **Prerequisite:** [Module 2, Chapter 2: Gazebo Physics](/docs/module2/chapter-2-gazebo-physics)
- **New Concepts:** 8 (ASR, phonemes, audio features, Whisper, callbacks, etc.)
- **Code Examples:** 2 (fully runnable)

## What You'll Learn
- [ ] How speech recognition converts audio to text
- [ ] Whisper model architecture and capabilities
- [ ] Building ROS 2 nodes that process voice input
- [ ] Debugging audio issues

## Glossary Preview
**ASR, Phoneme, Acoustic Features, Whisper, Token, Inference**

[Continue reading: Chapter 2](/docs/module4/chapter-2-voice-to-action-whisper)

---
```

## Quality Checks
- ✅ Are time estimates realistic based on word count and complexity?
- ✅ Are all prerequisites listed accurate and verified?
- ✅ Do learning outcomes use testable action verbs?
- ✅ Are all internal links verified to actual files?
- ✅ Is the guide motivating and accessible?
- ✅ Does glossary preview capture key new terms (5-10)?
- ✅ Is tone consistent with VisionaryTone standards?

---

**Implementation Note:** GenerateReadingGuide creates learner-facing documents that guide study planning and set expectations. Guides can be embedded in Docusaurus or provided separately. Generate guides after modules are complete to ensure time estimates and prerequisites are accurate.
