# Preset: WriteChapter

## Purpose
End-to-end workflow for generating a complete chapter (5-7 sections, ~2000 words) with integrated quality checks and brand consistency.

## Subagents Called
1. **BookWriter** — Generates all chapter sections (intro, learning objectives, theory, code examples, real-world applications, hands-on exercise, debugging, summary)
2. **StructureAgent** — Validates chapter hierarchies, heading levels, and sidebar integration
3. **CodeAgent** — Writes and validates Python+rclpy code examples (max 2 per chapter)
4. **QualityGuard** — Reviews content for brand voice, learning outcomes, pedagogical soundness
5. **ContentValidator** — Checks cross-module consistency, glossary, links, prerequisites

## Skills Used
1. **VisionaryTone** — Ensures visionary yet accessible brand voice throughout
2. **GenerateLessonFormat** — Applies consistent lesson structure across all sections
3. **ROS2Example** — Generates production-quality code snippets with expected output
4. **ConsistencyCheck** — Validates alignment with Module 3 patterns and naming conventions
5. **GlossaryIntegration** — Identifies new terms, bolding, and updates master glossary
6. **CrossModuleReference** — Creates accurate inter-module links and prerequisite callouts
7. **CleanMarkdown** — Applies Markdown/Docusaurus formatting standards

## Input Signature
```yaml
module: string          # Module number (1-4)
chapter: integer        # Chapter number (1-4)
title: string          # Full chapter title (e.g., "Chapter 1: LLM-Robotics Convergence")
outline: list          # 5-7 section titles in order
target_words: integer  # Target word count (~2000)
code_topics: list      # Topics for code examples (1-2 items)
prerequisites: list    # Prior modules/chapters that should be callout (optional)
glossary_terms: list   # New technical terms to introduce (optional)
```

## Output Format
```yaml
chapter_file: string          # Path: docs/moduleX/chapter-N-title.md
status: string                # "complete" | "review_needed" | "failed"
sections_created: integer     # Count of sections generated
code_examples: integer        # Count of tested code examples
glossary_entries_added: integer # Count of new glossary terms
validation_passed: boolean    # All quality checks passed?
warnings: list                # Style warnings or suggestions
issues: list                  # Critical issues requiring fixes
estimated_read_time: string   # "45-60 minutes"
```

## Safety Rules

1. **Never skip quality review** — All content must pass QualityGuard and ContentValidator before output
2. **Preserve existing structure** — Do not overwrite existing chapter files; report conflicts
3. **Cross-module consistency first** — Before writing new content, verify no glossary conflicts or broken references
4. **Code examples must be tested** — All Python+rclpy code must include expected output and common error fixes
5. **Brand voice non-negotiable** — Visionary tone applies to intro and summary; technical accuracy in theory sections

## Workflow Steps

### Step 1: Validation & Planning
- StructureAgent checks module/chapter naming and directory structure
- ContentValidator scans for prior glossary conflicts, cross-module prerequisites
- BookWriter reads existing modules (1-3) to understand patterns and context

### Step 2: Content Generation
- BookWriter generates introduction (hook, why it matters, learning goals)
- BookWriter generates learning objectives with testable action verbs
- BookWriter generates theory sections (20-30% of content) with diagrams/explanations
- CodeAgent writes 1-2 Python+rclpy examples with expected output and error handling
- BookWriter generates real-world applications (3+ examples from industry)
- BookWriter generates hands-on exercise (guided, with success criteria)
- BookWriter generates debugging & troubleshooting section (3-5 common errors)
- BookWriter generates summary & glossary preview

### Step 3: Formatting & Consistency
- CleanMarkdown applies Markdown standards (heading hierarchy, code block tags, link format)
- GlossaryIntegration bolds all new technical terms and creates master glossary entries
- CrossModuleReference adds prerequisite callouts (blockquotes) and inter-module links
- VisionaryTone reviews intro/summary for inspiring, accessible language

### Step 4: Quality Review
- QualityGuard checks brand voice, learning outcomes, pedagogical soundness
- ContentValidator verifies cross-module links (no broken references), glossary completeness
- CodeAgent validates all Python examples (runnable, tested, follows rclpy patterns)

### Step 5: Final Output
- Generate chapter file at `docs/moduleX/chapter-N-title.md`
- Output validation report with warnings/issues
- Provide estimated reading time (usually 45-60 minutes for full chapter)
- Return status (complete | review_needed | failed)

## Example Invocation

### Command
```
WriteChapter --module 4 --chapter 2 --title "Chapter 2: Voice-to-Action with Whisper" --outline ["Introduction","How Speech Recognition Works","Whisper: Automatic Speech Recognition","Integrating Whisper with ROS 2","Real-World Applications","Hands-On Exercise: Build a Voice Command Node","Debugging Common Issues","Summary"] --code_topics ["whisper_subscriber","voice_command_handler"] --prerequisites ["Module 3, Chapter 4: Navigation Path Planning"] --glossary_terms ["ASR","phonemes","language model inference"]
```

### Expected Output
```yaml
chapter_file: docs/module4/chapter-2-voice-to-action-whisper.md
status: complete
sections_created: 8
code_examples: 2
glossary_entries_added: 3
validation_passed: true
warnings:
  - "Code example 1 exceeds 30 lines; consider splitting into 2 examples"
issues: []
estimated_read_time: "50 minutes"

Sample section generated:
---
## Introduction: Why Voice Matters in Robotics

Imagine commanding a humanoid robot to "pick up the coffee cup" and having it understand not just the words, but the intent. **Automatic Speech Recognition (ASR)** is the AI technology that powers this magic...

[Full chapter follows with all 8 sections, 2 code examples with expected output, real-world applications, hands-on exercise, debugging section]
---
```

## Quality Checks
- ✅ Does content match learned Module 3 patterns (structure, tone, format)?
- ✅ Are all learning objectives testable with action verbs?
- ✅ Are code examples runnable in isolation with expected output?
- ✅ Is the chapter readable in 45-60 minutes?
- ✅ Do new glossary terms appear bolded and defined in context?
- ✅ Are cross-module prerequisites called out at chapter start?
- ✅ Does intro hook learner interest? Does summary tie everything together?

---

**Implementation Note:** WriteChapter is the most comprehensive preset and should be used for creating new main chapters. For single lesson sections (~400-600 words), use WriteLesson instead. After WriteChapter completes, run ValidateCrossModule to verify no broken links were introduced.
