# Phase 1: Content Data Model & Structure

**Date**: 2025-12-06
**Feature**: Physical AI & Humanoid Robotics Book
**Status**: Complete

---

## Book Content Model

### Entity: Book

**What it represents**: The entire published work

**Attributes**:
- Title: "Physical AI & Humanoid Robotics: The Rise of the Digital Human"
- Author: Abdul Ahad Javaid
- Audience: Beginner–Intermediate Learners
- Publication Format: Docusaurus static site
- Total Chapters: 4 (in Module 1 only)
- Total Words: ~10,000–12,000
- Total Code Examples: 8 (max 2 per chapter)

**Relationships**:
- Book contains 1 Module
- Book contains Introduction section
- Book contains Foundations section
- Book contains Approach section
- Book contains Applications section
- Book contains Ethics section
- Book contains Glossary
- Book contains Writing Guidelines (internal)

---

### Entity: Section

**What it represents**: A major organizational unit within the book (introduction, foundations, etc.)

**Attributes**:
- Name: string (e.g., "Introduction", "Foundations")
- Position: integer (order in book)
- Description: string
- Pages: list of Pages

**Validation Rules**:
- Name must be unique
- Position must be sequential (no gaps)
- Each section contains 1–3 pages

**Relationships**:
- Section contains multiple Pages
- Section belongs to Book

**Sections Defined**:
1. Introduction (3 pages)
   - What is Physical AI?
   - Evolution of Systems
   - Why This Matters

2. Foundations (3 pages)
   - AI & Robotics Connection
   - Hardware Overview
   - Software Overview

3. Approach (3 pages)
   - Hands-On Philosophy
   - Prerequisites
   - How to Use This Book

4. Applications (1 page)
   - Real-World Use Cases

5. Module 1: ROS 2 (5 pages: index + 4 chapters)
   - Module Overview
   - Chapter 1: Middleware
   - Chapter 2: Nodes, Topics, Services
   - Chapter 3: Python Agents
   - Chapter 4: URDF

6. Ethics (2 pages)
   - Responsible AI
   - Future Directions

---

### Entity: Page (Chapter or Content Page)

**What it represents**: A single markdown file representing one piece of content

**Attributes**:
- Title: string
- Slug: string (URL path)
- Description: string (for SEO)
- Content: markdown text
- Section: string (parent section)
- Position: integer (order within section)
- Words: integer (content length)
- CodeExamples: integer (0–2 for chapters)
- Glossary: list of terms defined on this page

**Validation Rules**:
- Title must be unique within book
- Slug must be unique and URL-safe
- Description must be 50–100 characters
- Content must follow simple English rules
- CodeExamples must not exceed 2
- All technical terms must be in Glossary

**YAML Frontmatter Template** (every page):
```yaml
---
title: Page Title
description: 50-100 char description for SEO
slug: /path/to/page
sidebar_position: 1
---
```

**Relationships**:
- Page belongs to Section
- Page contains CodeExamples
- Page references GlossaryTerms

---

### Entity: CodeExample

**What it represents**: A runnable code snippet in Python

**Attributes**:
- Language: "python"
- Code: string (source code)
- Description: string (what the code does)
- IsRunnable: boolean (must be true)
- ExpectedOutput: string (what code should print)
- Comments: boolean (code must be well-commented)

**Validation Rules**:
- Code must be syntactically valid Python
- Code must run without errors
- Code must use rclpy or standard library (no external deps)
- Comments on every 3–4 lines
- Maximum 50 lines per example
- Must be tested before inclusion

**Relationships**:
- CodeExample belongs to Page
- Page contains 0–2 CodeExamples

---

### Entity: GlossaryTerm

**What it represents**: A technical or domain-specific term used in the book

**Attributes**:
- Term: string (unique)
- Definition: string (beginner-friendly, 1–3 sentences)
- Context: string (where term is introduced)
- Synonyms: list (alternative names)
- Chapter: string (which chapter introduces it)

**Validation Rules**:
- Term must be unique
- Definition must be in simple English
- Definition must not exceed 3 sentences
- Definition must not use undefined jargon

**Glossary Terms (14 Defined)**:
1. Artificial Intelligence (AI)
2. Physical AI
3. Robotics
4. Humanoid Robotics
5. ROS 2 (Robot Operating System 2)
6. Nodes
7. Topics
8. Services
9. rclpy
10. URDF (Unified Robot Description Format)
11. Sensors
12. Actuators
13. Autonomy
14. Machine Learning

**Relationships**:
- GlossaryTerm is referenced by Pages
- GlossaryTerm defined in Glossary page

---

## Content Structure Map

```
Book: "Physical AI & Humanoid Robotics: The Rise of the Digital Human"
│
├─ Title Page (special)
├─ Homepage (index.md)
│
├─ Section 1: Introduction (3 pages)
│  ├─ What is Physical AI?
│  ├─ Evolution of Systems
│  └─ Why This Matters
│
├─ Section 2: Foundations (3 pages)
│  ├─ AI & Robotics Connection
│  ├─ Hardware Overview
│  └─ Software Overview
│
├─ Section 3: Approach (3 pages)
│  ├─ Hands-On Philosophy
│  ├─ Prerequisites
│  └─ How to Use This Book
│
├─ Section 4: Applications (1 page)
│  └─ Real-World Use Cases
│
├─ Module 1: The Robotic Nervous System (ROS 2)
│  ├─ Module Overview/Index
│  ├─ Chapter 1: Middleware (1,500–2,000 words, 2 examples)
│  ├─ Chapter 2: Nodes, Topics, Services (2,000–2,500 words, 2 examples)
│  ├─ Chapter 3: Bridging Python Agents (2,000–2,500 words, 2 examples)
│  └─ Chapter 4: URDF for Humanoids (1,500–2,000 words, 2 examples)
│
├─ Section 5: Ethics (2 pages)
│  ├─ Responsible AI
│  └─ Future Directions
│
├─ Glossary (1 page, 14+ terms)
└─ Writing Guidelines (1 page, internal)

Total Pages: ~24
Total Words: ~10,000–12,000
Total Code Examples: 8
```

---

## Page Template Schema

Every content page follows this structure:

```markdown
---
title: [Page Title]
description: [50-100 character description]
slug: /section/page-name
sidebar_position: [integer]
---

# Page Title

## Learning Objectives (for chapters only)
- [ ] Objective 1
- [ ] Objective 2

## Introduction/Context
[Engaging introduction; 100-150 words]

## Main Content Section 1
[Content; 200-400 words]

### Subsection 1a
[Details]

### Subsection 1b
[Details]

## Main Content Section 2
[Content; 200-400 words]

## Real-World Example
[Practical application; 150-200 words]

## Hands-On Exercise (for chapters only)
[Instructions and code examples; max 2 examples]

## Key Takeaways (for chapters only)
- [ ] Takeaway 1
- [ ] Takeaway 2

## Next Steps (for chapters only)
[Link to next chapter]

## Glossary
[List of new terms from this page with definitions]

## Troubleshooting (if applicable)
[Q&A format for common issues]
```

---

## Markdown & Link Structure

### Internal Link Convention

All internal links use **relative paths**:

```markdown
# Good examples:
[Chapter 2](./chapter-2-nodes-topics.md)
[Glossary](/docs/glossary.md)
[Introduction](../introduction/what-is-physical-ai.md)

# Avoid:
[Chapter 2](/module1/chapter-2-nodes-topics.md)  # Absolute paths
[Chapter 2](https://example.com/module1/chapter-2)  # External
```

### Cross-File References

```markdown
# Linking to a glossary term from a page:
[ROS 2](../glossary.md#ros-2) — Read the definition in the glossary

# Linking to another chapter:
**Next**: [Chapter 2: Nodes, Topics, and Services](./chapter-2-nodes-topics.md)
```

### Sidebar Navigation Configuration (sidebars.js)

```javascript
'module1/index',
'module1/chapter-1-middleware',
'module1/chapter-2-nodes-topics',
'module1/chapter-3-python-agents',
'module1/chapter-4-urdf',
```

---

## Validation Rules for All Content

### Every Page Must Have

- [x] Unique title
- [x] Valid slug (lowercase, kebab-case)
- [x] Description (50–100 chars)
- [x] At least one H1 heading (title)
- [x] Proper heading hierarchy (no skipping levels)
- [x] Short paragraphs (2–4 sentences max)
- [x] Active voice where possible
- [x] Zero undefined jargon
- [x] All technical terms linked to glossary

### Every Chapter Must Have

- [x] Learning objectives (4–6)
- [x] Real-world example or application
- [x] Hands-on exercise (0–2 code examples max)
- [x] Key takeaways (checklist format)
- [x] Link to next chapter (except last chapter)
- [x] Glossary section with new terms
- [x] 1,500–2,500 words
- [x] 20–40 minutes reading time

### Every Code Example Must

- [x] Be syntactically valid Python
- [x] Run without errors
- [x] Include comments (every 3–4 lines)
- [x] Show expected output
- [x] Use rclpy or standard library only
- [x] Be tested before inclusion
- [x] Include explanation before code block

---

## File System Organization

```
docusaurus-book/
├── docs/
│   ├── index.md                        # Homepage
│   ├── title-page.md                   # Title page (special)
│   │
│   ├── introduction/
│   │   ├── what-is-physical-ai.md
│   │   ├── evolution-of-systems.md
│   │   └── why-this-matters.md
│   │
│   ├── foundations/
│   │   ├── ai-robotics-connection.md
│   │   ├── hardware-overview.md
│   │   └── software-overview.md
│   │
│   ├── approach/
│   │   ├── hands-on-philosophy.md
│   │   ├── prerequisites.md
│   │   └── how-to-use-this-book.md
│   │
│   ├── applications/
│   │   └── use-cases.md
│   │
│   ├── module1/
│   │   ├── index.md
│   │   ├── chapter-1-middleware.md
│   │   ├── chapter-2-nodes-topics.md
│   │   ├── chapter-3-python-agents.md
│   │   └── chapter-4-urdf.md
│   │
│   ├── ethics/
│   │   ├── responsible-ai.md
│   │   └── future-directions.md
│   │
│   ├── glossary.md
│   ├── writing-guidelines.md
│   │
│   └── img/
│       ├── [diagrams to be created]
│       └── [screenshots if needed]
│
├── static/
│   └── [static assets if needed]
│
├── sidebars.js
├── docusaurus.config.js
└── package.json
```

---

## State Transitions (Publishing Workflow)

```
Draft → Review → Ready → Published

Draft: Initial content written (incomplete, may have TODOs)
Review: Peer-reviewed, approved for publication
Ready: All checks passed, verified locally
Published: Live on production site
```

---

## Success Criteria for Data Model

- [x] All 14+ glossary terms defined
- [x] All 4 chapters scoped with word counts and code examples
- [x] All pages follow template structure
- [x] All links are internal (relative paths)
- [x] All frontmatter consistent (title, description, slug)
- [x] No validation rule violations
- [x] File structure matches sidebar configuration
- [x] Content relationships clearly defined

---

**Status**: ✅ **DATA MODEL COMPLETE**

**Next**: Phase 1 continues with quickstart.md setup guide.
