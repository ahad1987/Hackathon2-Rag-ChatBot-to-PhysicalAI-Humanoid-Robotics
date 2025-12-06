# Preset: BuildModuleFolderTree

## Purpose
Create a new module directory structure with placeholder files, category configuration, and sidebar entries. Establishes scaffolding for a complete module ready to populate with content.

## Subagents Called
1. **StructureAgent** — Creates directory structure, generates placeholder files, updates sidebar configuration
2. **MarkdownCleaner** — Ensures all placeholder files have valid Markdown frontmatter
3. **ContentValidator** — Validates new module integrates correctly with existing module hierarchy

## Skills Used
1. **ConsistencyCheck** — Ensures new module structure matches Modules 1-4 patterns
2. **CleanMarkdown** — Applies correct Markdown formatting to all placeholders

## Input Signature
```yaml
module_number: integer      # Module to create (e.g., 5 for Module 5)
module_title: string        # Full module title (e.g., "Module 5: Reinforcement Learning for Robotics")
chapter_count: integer      # Number of chapters (typically 4)
chapter_titles: list        # Chapter titles in order (must match count)
include_glossary: boolean   # Create glossary.md file? (default: true)
update_sidebar: boolean     # Update sidebars.ts? (default: true)
```

## Output Format
```yaml
module_path: string                 # Created directory path
files_created: list                 # All generated files with paths
sidebar_entry_created: boolean      # Successfully added to sidebars.ts?
structure_tree: string              # ASCII tree of created structure
validation_passed: boolean          # Module structure valid?
next_steps: list                    # Recommended actions (populate chapters, add glossary)
placeholder_count: integer          # Number of placeholder files generated
glossary_entries_template: integer  # Count of example glossary terms included (if applicable)
```

## Safety Rules

1. **Never overwrite existing modules** — Check if module already exists; refuse if conflict detected
2. **Preserve existing sidebar entries** — Only add new module; don't modify other modules
3. **Create placeholders only** — Generated files should have clear "TODO" markers for content writers
4. **Validate TypeScript syntax** — Any sidebars.ts modifications must be syntactically valid
5. **Document scaffold clearly** — Each placeholder file should explain what content goes there

## Workflow Steps

### Step 1: Validation
- StructureAgent checks if module directory already exists (refuse if found)
- ConsistencyCheck verifies new module number doesn't conflict with existing modules
- Validate chapter_count matches chapter_titles list

### Step 2: Directory Creation
- Create `/docs/moduleX/` directory
- Create `/docs/moduleX/_category_.json` with module title and ordering
- StructureAgent generates placeholder files:
  - `introduction.md` (placeholder with TODO markers)
  - `chapter-1-title.md` (placeholder for first chapter)
  - `chapter-2-title.md` (placeholder for second chapter)
  - `chapter-3-title.md` (placeholder for third chapter)
  - `chapter-4-title.md` (placeholder for fourth chapter)
  - `glossary.md` (template with example entries)

### Step 3: Frontmatter & Metadata
- MarkdownCleaner ensures all files have YAML frontmatter (title, id, sidebar_position)
- Add clear "TODO" comments explaining what content should be written
- Include learning objectives placeholder sections

### Step 4: Sidebar Configuration
- If update_sidebar=true, add new module entry to sidebars.ts
- Maintain consistent formatting with existing modules
- Validate TypeScript syntax

### Step 5: Validation & Output
- ContentValidator checks new module structure against Modules 1-4 patterns
- Confirm all files created successfully
- Output tree view and recommended next steps

## Example Invocation

### Command
```
BuildModuleFolderTree --module_number 5 --module_title "Module 5: Reinforcement Learning for Robotics" --chapter_count 4 --chapter_titles ["Introduction to RL Theory","Policy Gradient Methods","Q-Learning and Deep RL","Humanoid Robot Training Capstone"] --update_sidebar true
```

### Expected Output
```yaml
module_path: docs/module5
files_created:
  - docs/module5/_category_.json
  - docs/module5/introduction.md
  - docs/module5/chapter-1-introduction-to-rl-theory.md
  - docs/module5/chapter-2-policy-gradient-methods.md
  - docs/module5/chapter-3-q-learning-and-deep-rl.md
  - docs/module5/chapter-4-humanoid-robot-training-capstone.md
  - docs/module5/glossary.md

structure_tree: |
  docs/module5/
  ├── _category_.json (Module 5: Reinforcement Learning for Robotics)
  ├── introduction.md (TODO: Write module overview + learning objectives)
  ├── chapter-1-introduction-to-rl-theory.md (TODO: Write 5-7 sections)
  ├── chapter-2-policy-gradient-methods.md (TODO: Write 5-7 sections)
  ├── chapter-3-q-learning-and-deep-rl.md (TODO: Write 5-7 sections)
  ├── chapter-4-humanoid-robot-training-capstone.md (TODO: Capstone project)
  └── glossary.md (Template with examples: RL, policy, value function, etc.)

sidebar_entry_created: true

sidebar.ts addition:
  ```
  {
    type: 'category',
    label: 'Module 5: Reinforcement Learning for Robotics',
    items: [
      { type: 'doc', id: 'module5/introduction' },
      { type: 'doc', id: 'module5/chapter-1-introduction-to-rl-theory' },
      { type: 'doc', id: 'module5/chapter-2-policy-gradient-methods' },
      { type: 'doc', id: 'module5/chapter-3-q-learning-and-deep-rl' },
      { type: 'doc', id: 'module5/chapter-4-humanoid-robot-training-capstone' },
      { type: 'doc', id: 'module5/glossary' },
    ],
  }
  ```

validation_passed: true
placeholder_count: 7 (1 intro + 4 chapters + 1 glossary + 1 category.json)
glossary_entries_template: 8 (RL, Policy, Value Function, Reward, Episode, Discount Factor, Exploration-Exploitation, Deep Q-Network)

next_steps:
  1. Use WriteChapter preset to populate chapter-1-introduction-to-rl-theory.md
  2. Use WriteLesson preset to add focused lessons to each chapter
  3. Use CodeAgent to generate Python+rclpy examples for each chapter
  4. Populate glossary.md with all technical terms from chapters
  5. Run ValidateCrossModule to verify links work correctly
  6. Run CleanStyle to audit formatting and brand voice consistency

Scaffold Successfully Created!
All placeholder files are ready for content writers. Each file contains TODO markers and learning objectives templates to guide content creation.
```

## Sample Placeholder File

### chapter-1-introduction-to-rl-theory.md
```markdown
---
title: Chapter 1 - Introduction to RL Theory
id: chapter-1-introduction-to-rl-theory
sidebar_position: 1
---

# Chapter 1: Introduction to RL Theory

## TODO: Write Introduction Section
**Purpose:** Hook learner interest. Answer "Why is RL crucial for robotics?"
**Target:** 50-100 words
**Pattern:** See Module 4, Chapter 1 for style reference

---

## TODO: Learning Objectives
Create 3-5 testable outcomes using action verbs:
- [ ] Understand what reinforcement learning is
- [ ] Explain how RL differs from supervised learning
- [ ] Implement a basic policy gradient algorithm
- (Add more as needed)

---

## TODO: Theory Section 1 - What is Reinforcement Learning?
**Target:** 200-300 words
**Include:** Definition, diagram, concrete example from robotics

---

## TODO: Code Example 1 - Simple Policy Gradient Agent
**Target:** Python+rclpy, < 30 lines
**Pattern:** See Module 1, Chapter 1 code example style
**Include:** Expected output and common error with fix

---

## TODO: Real-World Application 1
**Example:** How Tesla/Boston Dynamics/Humanoid X uses RL
**Target:** 75-100 words

## TODO: Real-World Application 2
(Add second industry example)

## TODO: Real-World Application 3
(Add third industry example)

---

## TODO: Hands-On Exercise
**Objective:** Learner builds and trains simple RL agent
**Steps:** Step-by-step guide with expected outputs
**Success Criteria:** Clearly defined

---

## TODO: Debugging & Troubleshooting
**Common Error 1:** [Describe error]
- Symptom: What learner will see
- Cause: Why it happens
- Fix: How to resolve

(Add 3-5 common errors)

---

## TODO: Summary
Recap what learner accomplished, preview Chapter 2.

---

## TODO: Glossary
Add new technical terms introduced in this chapter:
- **RL (Reinforcement Learning):** Definition
- **Policy:** Definition
- **Reward:** Definition
(Use format: `**Term:** definition in 1-2 sentences`)
```

## Quality Checks
- ✅ Do all files follow naming convention (`chapter-N-descriptive-title.md`)?
- ✅ Does module structure match Modules 1-4 patterns?
- ✅ Is _category_.json valid JSON with correct ordering?
- ✅ Is sidebars.ts update syntactically valid TypeScript?
- ✅ Are all placeholder files clear with TODO markers?
- ✅ Does module number not conflict with existing modules?

---

**Implementation Note:** BuildModuleFolderTree creates the scaffolding for a new module. After creation, use WriteChapter and WriteLesson to populate chapters with actual content. The placeholder files provide clear guidance for content writers following established patterns from Modules 1-4.
