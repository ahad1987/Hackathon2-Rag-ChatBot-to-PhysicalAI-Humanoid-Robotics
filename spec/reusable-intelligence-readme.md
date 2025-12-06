# Reusable Intelligence System

**Master guide to the Physical AI & Humanoid Robotics book's AI-powered content creation framework**

Version 1.0 | Last Updated: 2025-12-07

---

## Quick Start

The reusable-intelligence system provides three layers of AI workers:

1. **Subagents** — Specialized AI workers (BookWriter, CodeAgent, QualityGuard, etc.)
2. **Skills** — Reusable competencies (VisionaryTone, CleanMarkdown, ROS2Example, etc.)
3. **Presets** — Pre-configured workflows combining subagents + skills

### Most Common Workflows

| Task | Preset | Time |
|------|--------|------|
| Write a complete chapter (5-7 sections) | `WriteChapter` | 2-3 hours |
| Write a single lesson section (~400 words) | `WriteLesson` | 30 minutes |
| Audit module for Markdown/tone issues | `CleanStyle` | 45 minutes |
| Validate all links and glossary | `ValidateCrossModule` | 30 minutes |
| Test all code examples in chapter | `CodeValidation` | 30 minutes |
| Create reading guide for learners | `GenerateReadingGuide` | 20 minutes |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESETS (Workflows)                    │
│  WriteChapter  WriteLesson  CleanStyle  CodeValidation etc. │
└────────────────────────┬────────────────────────────────────┘
                         │
           ┌─────────────┴──────────────┐
           │                            │
┌──────────▼────────────────┐  ┌───────▼──────────────────┐
│   SUBAGENTS (Workers)     │  │   SKILLS (Competencies) │
│                           │  │                          │
│ • BookWriter              │  │ • VisionaryTone          │
│ • CodeAgent               │  │ • CleanMarkdown          │
│ • StructureAgent          │  │ • ROS2Example            │
│ • MarkdownCleaner         │  │ • ExplainSimple          │
│ • QualityGuard            │  │ • GenerateLessonFormat   │
│ • ContentValidator        │  │ • ConsistencyCheck       │
│                           │  │ • GlossaryIntegration    │
│                           │  │ • CrossModuleReference   │
└───────────────────────────┘  └──────────────────────────┘
```

---

## Subagents: Detailed Reference

Subagents are specialized AI workers. Each handles a specific domain. They receive **input specifications** and return **validated output**.

### 1. BookWriter

**Purpose:** Generate chapter and lesson content

**When to use:** Writing new course material (intros, learning objectives, theory, exercises)

**Key Constraints:**
- Max 2000 words per chapter
- Max 400 words per lesson
- Always include learning objectives, theory, code examples, real-world applications, hands-on exercise
- Follow Module 3 patterns

**Example Call:**
```
BookWriter --section "learning_objectives" --module 4 --chapter 1 --num_objectives 5 --action_verbs ["Understand","Implement","Explain","Apply"]
```

**Input Signature:**
```yaml
section: string          # "intro" | "learning_objectives" | "theory" | "exercise" | "summary"
module: integer          # Module number
chapter: integer         # Chapter number
content_type: string     # "concept" | "skill" | "project"
target_words: integer    # Word count target
tone: string            # Brand voice level: "visionary" | "technical" | "beginner_friendly"
```

**Output:**
- Markdown text with proper heading hierarchy
- Glossary terms bolded on first mention
- Cross-module links in Docusaurus format
- Learning objectives with testable action verbs

---

### 2. CodeAgent

**Purpose:** Write, validate, test Python+rclpy code examples

**When to use:** Creating or validating code examples for lessons

**Key Constraints:**
- Python 3.10+ only
- rclpy only (no external dependencies)
- Max 30 lines per example
- Always include expected output
- Always include common error + fix

**Example Call:**
```
CodeAgent --code_type "subscriber" --module 4 --chapter 2 --topic "/audio_input" --callback_description "Process Whisper transcription"
```

**Input Signature:**
```yaml
code_type: string               # "node" | "subscriber" | "publisher" | "service" | "action"
module: integer                 # Module number
chapter: integer                # Chapter number
description: string             # What code should demonstrate
include_error_handling: boolean  # Add try-catch? (default: true)
```

**Output:**
- Python code block (< 30 lines)
- Expected output showing realistic results
- Common error with fix
- Runnable as-is (copy-paste and go)

---

### 3. StructureAgent

**Purpose:** Plan module hierarchies, create scaffolds, maintain naming consistency

**When to use:** Creating new modules, refactoring directory structure, updating sidebars

**Key Constraints:**
- File naming: `chapter-N-descriptive-title.md` (lowercase, hyphens)
- All modules follow: intro + 4 chapters + glossary
- sidebars.ts must be valid TypeScript
- Never delete; only move/create

**Example Call:**
```
StructureAgent --action "scaffold_module" --module_number 5 --chapter_count 4 --chapter_titles ["Intro to RL","Policy Methods","Q-Learning","Capstone"]
```

**Input Signature:**
```yaml
action: string                  # "scaffold_module" | "scaffold_chapter" | "validate_structure"
scope: string                   # Module/chapter identifier
show_plan_first: boolean        # If true, output plan without executing
```

**Output:**
- ASCII directory tree
- File creation checklist
- Updated sidebars.ts configuration
- Validation report

---

### 4. MarkdownCleaner

**Purpose:** Validate and fix Markdown syntax, frontmatter, links, code blocks

**When to use:** Pre-publishing audits, fixing formatting issues, validating syntax

**Key Constraints:**
- Never delete content
- Code blocks must have language tags
- Heading hierarchy: no skipped levels
- Links must be Docusaurus format: `[text](/docs/moduleX/...)`
- HTML entities: escape `<` and `>` as `&lt;` and `&gt;`

**Example Call:**
```
MarkdownCleaner --target_path "docs/module4" --check_type "all" --action "fix_automatically"
```

**Input Signature:**
```yaml
target_path: string             # File or directory to check
check_type: string              # "syntax" | "frontmatter" | "links" | "code_blocks" | "all"
action: string                  # "report_only" | "fix_automatically"
```

**Output:**
- List of issues with location and severity
- Summary of fixes applied
- Validation report

---

### 5. QualityGuard

**Purpose:** Review content for brand voice, learning outcomes, pedagogical soundness

**When to use:** Final review before publishing, tone/quality assessment

**Key Constraints:**
- Must align with "visionary yet accessible" brand voice
- Learning objectives must be testable
- Content must be appropriate for learner level (Modules 1-3 knowledge assumed)
- No contradictions with established patterns

**Example Call:**
```
QualityGuard --content_path "docs/module4/chapter-2.md" --criteria "all" --action "review"
```

**Input Signature:**
```yaml
content_path: string            # File to review
criteria: string                # "brand_voice" | "learning_outcomes" | "pedagogy" | "all"
action: string                  # "review" | "suggest_revisions"
```

**Output:**
- Issues found with severity levels
- Specific suggestions with before/after examples
- Pass/fail verdict

---

### 6. ContentValidator

**Purpose:** Check cross-module consistency, glossary accuracy, link integrity

**When to use:** Before publishing chapters, after major edits, validation gates

**Key Constraints:**
- Every cross-module link must point to actual file
- Glossary terms must be consistent (same definition across modules)
- Prerequisites must be accurate
- No forward references (don't link to content not yet written)

**Example Call:**
```
ContentValidator --scope "module4" --check_type "all" --strict_mode true
```

**Input Signature:**
```yaml
scope: string                   # "all" | "module" | "chapter" | "file"
check_type: string              # "glossary" | "cross_links" | "prerequisites" | "all"
strict_mode: boolean            # Fail on warnings?
```

**Output:**
- Detailed issue list with file locations
- Glossary conflict analysis
- Link validation report
- Recommendations for fixes

---

## Skills: Detailed Reference

Skills are reusable competencies applied across subagents. Each skill encapsulates a specific expertise.

### 1. VisionaryTone

**Purpose:** Maintain visionary yet accessible brand voice

**How it's used:** Applied to intros, summaries, and marketing materials

**Key Principles:**
- Inspire learners ("Imagine a robot that...")
- Make complex topics accessible (use analogies, concrete examples)
- Active voice preferred
- Second person when teaching ("You will...")
- Avoid jargon without explanation

**Example:**
```
BEFORE (Technical):
"LLMs are neural networks trained on text using transformer architecture."

AFTER (Visionary):
"Imagine a robot that understands intent, not just words.
That's what happens when we combine Large Language Models with robotics."
```

---

### 2. CleanMarkdown

**Purpose:** Apply strict Markdown/Docusaurus formatting standards

**How it's used:** Applied to all generated content before publishing

**Key Standards:**
- Heading hierarchy: `#` for title, `##` sections, `###` subsections (no skipping levels)
- Code blocks always tagged: ` ```python` (not just ` ``` `)
- Links in Docusaurus format: `[text](/docs/moduleX/chapter-name)` (not relative paths)
- HTML entities escaped: `<` → `&lt;`, `>` → `&gt;` (for tables and code)
- Inline code with backticks: `` `variable` ``
- 2-space indentation for lists

**Example:**
```
BEFORE (Broken):
```
import rclpy  # Missing language tag

Check if x < 12  # Not escaped in table

[Link](../module1/chapter-1.md)  # Relative path

## Topic
#### Detail  # Skipped level
```

AFTER (Fixed):
```python
import rclpy  # Added language tag
```

Check if x &lt; 12  # Escaped entity

[Link](/docs/module1/chapter-1-ros2-fundamentals)  # Docusaurus format

## Topic
### Detail  # Correct hierarchy
```

---

### 3. ROS2Example

**Purpose:** Generate correct, tested Python+rclpy code snippets

**How it's used:** All code examples in chapters

**Key Standards:**
- Python 3.10+ syntax
- rclpy only (no rospy, no external libraries)
- Max 30 lines
- Runnable in isolation (copy-paste works)
- Include expected output showing realistic results
- Document 1 common error with fix
- Follow Module 1 patterns (node.create_node(), create_subscription(), etc.)

**Example Code:**
```python
import rclpy
from std_msgs.msg import String

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('listener')

    def callback(msg):
        print(f"Received: {msg.data}")

    sub = node.create_subscription(String, '/topic', callback, 10)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```

**Expected Output:**
```
Received: hello world
Received: test message
```

---

### 4. ExplainSimple

**Purpose:** Break complex concepts into beginner-friendly language

**How it's used:** Theory sections and learning objective descriptions

**Key Techniques:**
- Use analogies ("Think of tokens like words in a sentence...")
- Short sentences (12-15 words average)
- Active examples over abstract explanations
- Acknowledge learner's prior knowledge (Modules 1-3)
- Show why it matters ("This matters for robots because...")

**Example:**
```
BEFORE (Jargon-heavy):
"Transformers employ multi-head attention mechanisms to compute
contextual representations via scaled dot-product attention."

AFTER (Simple):
"Transformers use attention to focus on relevant parts of input.
Think of attention as a learner highlighting the important parts of a textbook.
When the model reads 'pick up the cup,' it focuses on 'cup' (the object)
and 'pick up' (the action), ignoring less important words."
```

---

### 5. GenerateLessonFormat

**Purpose:** Structure lessons consistently for maximum learning

**How it's used:** All lesson sections follow standard structure

**Key Structure:**
- **Introduction (5-10%)**: Hook ("Why does this matter?"), context
- **Learning Objectives (5%)**: 2-3 testable outcomes with action verbs
- **Theory (20-30%)**: Conceptual explanation, progressive
- **Code Examples (15-20%)**: 1-2 runnable examples with output
- **Real-World Applications (15%)**: 2-3 industry examples
- **Hands-On Exercise (20-30%)**: Guided step-by-step with success criteria
- **Debugging (10%)**: 3-5 common errors with fixes
- **Summary (5-10%)**: Recap, glossary, preview next

**Time Allocation for 1-Hour Lesson:**
- Reading: 40 minutes
- Hands-On: 15 minutes
- Review: 5 minutes

---

### 6. ConsistencyCheck

**Purpose:** Validate alignment with constitution and established patterns

**How it's used:** Applied when creating new content or refactoring

**Key Validations:**
- File naming: `chapter-N-descriptive-title.md` (lowercase, hyphens, no underscores)
- Module structure: All modules follow 4-chapter + intro + glossary pattern
- Cross-links: `/docs/moduleX/` format (not relative paths)
- Code examples: 2 per lesson with expected output
- Real-world applications: 3+ per chapter
- Glossary: Terms bolded on first mention, defined in context

---

### 7. GlossaryIntegration

**Purpose:** Identify technical terms, bold them, maintain master glossary

**How it's used:** Applied when writing new content

**Key Requirements:**
- **Bold first mention**: `` **Term** is defined as... ``
- **Define immediately**: Within 2 sentences of first use
- **Consistent language**: If Module 1 defined "Node", use same definition everywhere
- **Update master glossary**: Every new term added to /docs/glossary.md
- **Format**: Keep definitions 1-2 sentences max

**Example:**
```
BEFORE:
"LLMs are neural networks trained on text."

AFTER (with GlossaryIntegration):
"**Large Language Models (LLMs)** are neural networks trained on vast
text to predict and generate language. Each **token**—a word or
subword—is processed sequentially, building an answer one piece at a time."

Glossary entries:
- **LLM:** A neural network trained on text to predict and generate language
- **Token:** A unit of text (word or subword) processed by language models
```

---

### 8. CrossModuleReference

**Purpose:** Create accurate inter-module links and prerequisite callouts

**How it's used:** When referencing other modules or chapters

**Key Requirements:**
- **Link format**: `[text](/docs/moduleX/chapter-name)` (Docusaurus, not relative)
- **Always provide context**: Explain why learner needs this prior knowledge
- **Prerequisite callouts**: Use blockquote at chapter start if needed
- **Verify before publishing**: All links must resolve to actual files
- **No forward references**: Don't link to content not yet written
- **Consistent language**: "Module 3, Chapter 1" not "Ch3-1" or "Module III"

**Example:**
```
PREREQUISITE CALLOUT:
> ⚠️ **Prerequisite:** This chapter assumes you have completed Module 3, Chapter 4
> (Nav2 Path Planning). Review [Module 3: Navigation](/docs/module3/chapter-4-nav2-path-planning)
> if needed.

CROSS-MODULE LINK WITH CONTEXT:
Recall from [Module 1: ROS 2 Nodes](/docs/module1/chapter-1-ros2-fundamentals)—
a node is a ROS 2 process that communicates via topics. Our voice listener is a
node that subscribes to `/microphone_input`.
```

---

## Presets: Workflow Reference

Presets are pre-configured workflows combining multiple subagents and skills.

### 1. WriteChapter

**Purpose:** Complete 5-7 section chapter (∼2000 words)

**Workflow:**
1. BookWriter generates all sections
2. CodeAgent writes and validates 2 code examples
3. GlossaryIntegration bolds terms and updates glossary
4. CrossModuleReference adds prerequisite callouts and links
5. CleanMarkdown applies formatting standards
6. QualityGuard reviews brand voice and pedagogy
7. ContentValidator checks cross-module consistency

**Time:** 2-3 hours

**Example:**
```
WriteChapter --module 4 --chapter 2 --title "Chapter 2: Voice-to-Action" \
  --outline ["Intro","How ASR Works","Whisper","ROS 2 Integration","Applications","Exercise","Debugging","Summary"] \
  --code_topics ["whisper_subscriber","voice_command_handler"] \
  --prerequisites ["Module 3, Chapter 4"]
```

---

### 2. WriteLesson

**Purpose:** Single lesson section (∼400-600 words + 1 code example)

**Workflow:**
1. BookWriter generates focused lesson content
2. CodeAgent writes 1 runnable example
3. ExplainSimple makes concepts beginner-accessible
4. GlossaryIntegration handles new terms
5. CleanMarkdown applies standards
6. ContentValidator checks links

**Time:** 30 minutes

**Example:**
```
WriteLesson --chapter_path docs/module4/chapter-2.md \
  --lesson_title "Whisper: Automatic Speech Recognition" \
  --concept "How OpenAI's Whisper converts speech to text" \
  --code_example "ROS 2 subscriber for audio processing"
```

---

### 3. CleanStyle

**Purpose:** Audit module for Markdown/tone consistency

**Workflow:**
1. MarkdownCleaner identifies syntax issues
2. QualityGuard reviews brand voice
3. ContentValidator checks links
4. Auto-fix non-critical issues or report for review

**Time:** 45 minutes

**Example:**
```
CleanStyle --scope module4 --check_type ["markdown","brand_voice"] --action report_only
```

---

### 4. CodeValidation

**Purpose:** Test all code examples in chapter/module

**Workflow:**
1. MarkdownCleaner extracts code blocks
2. CodeAgent validates syntax and executes examples
3. Report results (passed/failed) with output

**Time:** 30 minutes per chapter

**Example:**
```
CodeValidation --scope module4/chapter-2 --test_mode full_validation --ros_environment docker
```

---

### 5. ValidateCrossModule

**Purpose:** Check links, glossary, prerequisites across modules

**Workflow:**
1. ContentValidator scans links (all must resolve)
2. GlossaryIntegration checks term consistency
3. CrossModuleReference validates prerequisite callouts
4. Report all issues with fixes

**Time:** 30 minutes for full curriculum

**Example:**
```
ValidateCrossModule --scope all --check_type ["links","glossary","prerequisites"] --report_format detailed
```

---

### 6. FixStructure

**Purpose:** Reorganize module content, update sidebars

**Workflow:**
1. StructureAgent plans reorganization
2. Show plan for approval
3. Execute moves/renames
4. ContentValidator updates all cross-references
5. Validate sidebars.ts syntax

**Time:** 1 hour for major reorganization

**Example:**
```
FixStructure --action reorganize_module --scope module4 --plan_only true
```

---

### 7. BuildModuleFolderTree

**Purpose:** Create new module scaffold with placeholders

**Workflow:**
1. StructureAgent creates directory and files
2. MarkdownCleaner ensures frontmatter validity
3. Generate placeholder content with TODO markers
4. Update sidebars.ts with new module entry

**Time:** 20 minutes

**Example:**
```
BuildModuleFolderTree --module_number 5 --module_title "Module 5: Reinforcement Learning" \
  --chapter_titles ["Intro to RL","Policy Methods","Q-Learning","Capstone"]
```

---

### 8. GenerateReadingGuide

**Purpose:** Create learner-facing reading guides with time estimates

**Workflow:**
1. StructureAgent analyzes module structure
2. BookWriter generates guide content
3. Compute realistic time estimates
4. Add prerequisites, learning outcomes, glossary preview

**Time:** 20 minutes

**Example:**
```
GenerateReadingGuide --scope module4 --include_sections ["overview","prerequisites","time_estimate","topics"] --estimate_type detailed_breakdown
```

---

## Safety Rules (Enforced Across All Tools)

### 1. Content Protection
- ✋ **Never modify existing chapters** without explicit user request
- ✋ **Never delete files** — only create/move
- ✋ **Never overwrite published content** — create new versions instead
- ✋ **Preserve all Modules 1-4 content** exactly as-is

### 2. Link Integrity
- ✋ **Every link must resolve** to actual file before publishing
- ✋ **No forward references** to content not yet written
- ✋ **Always use Docusaurus format** `[text](/docs/moduleX/...)`
- ✋ **Test all links** before marking as complete

### 3. Code Quality
- ✋ **All Python code must be runnable** (copy-paste works)
- ✋ **No external dependencies** (rclpy only)
- ✋ **Max 30 lines per example**
- ✋ **Always include expected output**

### 4. Glossary Consistency
- ✋ **No conflicting definitions** (same term = same definition across modules)
- ✋ **Every bolded term must have glossary entry**
- ✋ **Terms consistent with Module 1-3** definitions

### 5. Brand Voice
- ✋ **Maintain "visionary yet accessible" tone**
- ✋ **No unnecessary jargon** without explanation
- ✋ **Active voice preferred** (robots do X, not X is done)
- ✋ **Second person when teaching** ("You will..." not "The learner will...")

### 6. File Naming
- ✋ **Format:** `chapter-N-descriptive-title.md` (lowercase, hyphens only)
- ✋ **No underscores** in file names
- ✋ **Descriptive titles** (4-6 words typical)

---

## Quick Reference Table

| Task | Preset | Time | Subagents | Skills |
|------|--------|------|-----------|--------|
| Write full chapter | WriteChapter | 2-3h | BookWriter, CodeAgent, QualityGuard | VisionaryTone, GenerateLessonFormat, ROS2Example, GlossaryIntegration, CrossModuleReference |
| Write single lesson | WriteLesson | 30m | BookWriter, CodeAgent | ExplainSimple, ROS2Example, GlossaryIntegration |
| Audit style/tone | CleanStyle | 45m | MarkdownCleaner, QualityGuard | VisionaryTone, CleanMarkdown, ConsistencyCheck |
| Test code | CodeValidation | 30m | CodeAgent, MarkdownCleaner | ROS2Example, ConsistencyCheck |
| Validate links/glossary | ValidateCrossModule | 30m | ContentValidator, MarkdownCleaner | CrossModuleReference, GlossaryIntegration |
| Reorganize structure | FixStructure | 1h | StructureAgent, ContentValidator | ConsistencyCheck, CleanMarkdown, CrossModuleReference |
| Create module scaffold | BuildModuleFolderTree | 20m | StructureAgent, MarkdownCleaner | ConsistencyCheck |
| Generate reading guide | GenerateReadingGuide | 20m | BookWriter, StructureAgent | VisionaryTone, ExplainSimple |

---

## Example Workflow: Writing Module 5, Chapter 1

**Scenario:** User wants to create a new module with a first chapter on Reinforcement Learning.

### Step 1: Create Module Structure
```
BuildModuleFolderTree --module_number 5 \
  --module_title "Module 5: Reinforcement Learning for Robotics" \
  --chapter_titles ["Introduction to RL","Policy Gradient Methods","Q-Learning","RL Capstone"]
```
**Output:** /docs/module5/ directory with placeholder files

---

### Step 2: Write Chapter 1
```
WriteChapter --module 5 --chapter 1 --title "Chapter 1: Introduction to RL Theory" \
  --outline ["Intro","What is RL","Supervised vs RL","Agents and Environments","Reward Signals","Hands-On Exercise","Debugging","Summary"] \
  --code_topics ["simple_agent","reward_function"] \
  --prerequisites ["Module 4: LLM Fundamentals"]
```
**Output:** Complete chapter with all sections, code examples, glossary entries

---

### Step 3: Validate Code Examples
```
CodeValidation --scope module5/chapter-1 --test_mode full_validation --ros_environment docker
```
**Output:** Code test results; pass/fail for each example

---

### Step 4: Audit Style & Brand Voice
```
CleanStyle --scope module5/chapter-1 --check_type ["markdown","brand_voice"] --action fix_automatically
```
**Output:** Fixed any formatting issues; suggested tone improvements

---

### Step 5: Validate Cross-Module Consistency
```
ValidateCrossModule --scope module5 --check_type ["links","glossary","prerequisites"] --strict_mode true
```
**Output:** Confirm all links work, no glossary conflicts, prerequisites accurate

---

### Step 6: Generate Reading Guide
```
GenerateReadingGuide --scope module5/chapter-1 --include_sections ["overview","prerequisites","learning_outcomes","time_estimate","topics","practice"]
```
**Output:** READING_GUIDE.md for learners with time estimate and context

---

## Troubleshooting

### Issue: Broken Links Found
**Fix:** Run `ValidateCrossModule` with `--report_format detailed` to get exact locations, then:
1. Verify target file exists at correct path
2. Use Docusaurus format: `[text](/docs/moduleX/chapter-name)`
3. Re-run validation to confirm fix

### Issue: Glossary Conflicts
**Fix:**
1. Check `/docs/glossary.md` for conflicting definitions
2. Update to single consistent definition
3. Apply same definition across all modules

### Issue: Code Examples Fail
**Fix:** Run `CodeValidation` with `--test_mode full_validation`:
1. Check syntax errors (must be valid Python 3.10+)
2. Verify rclpy-only (no external dependencies)
3. Check line count (max 30)
4. Ensure expected output is realistic

### Issue: Brand Voice Inconsistent
**Fix:** Run `CleanStyle` to get specific suggestions, then:
1. Apply VisionaryTone skill suggestions
2. Use active voice ("you will..." not "the learner will...")
3. Include concrete examples over abstractions

---

## Best Practices

### For Writing New Content
1. **Start with WriteChapter** for complete chapters (saves time over manual writing)
2. **Use WriteLesson** for focused additions to existing chapters
3. **Always validate with ValidateCrossModule** before considering content done
4. **Test code with CodeValidation** to catch errors early

### For Quality Gates
1. **Run CleanStyle before publishing** to catch formatting/tone issues
2. **Run CodeValidation for any chapter with code** examples
3. **Run ValidateCrossModule for entire module** before release

### For Maintenance
1. **Keep glossary.md updated** — add terms as you create content
2. **Verify links regularly** (broken links destroy user experience)
3. **Use consistent naming conventions** (chapter-N-title.md format)
4. **Document prerequisite callouts** at chapter start if needed

---

## Contact & Feedback

This system is designed to accelerate content creation while maintaining quality. If you encounter issues, have suggestions, or want to extend the system:

1. **Report issues** in project GitHub or internal tracking
2. **Suggest new presets** for common workflows (e.g., "TranslateChapter")
3. **Request new skills** for specialized needs (e.g., "AccessibilityCheck")
4. **Share examples** of successful workflows for documentation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-07 | Initial release: 6 subagents, 8 skills, 8 presets |

---

**Ready to create content?** Start with `WriteChapter` or `WriteLesson` to generate your next piece, then validate with `ValidateCrossModule` before publishing.

🚀 **Happy creating!**
