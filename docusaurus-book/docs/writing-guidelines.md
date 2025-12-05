---
title: Writing Guidelines
description: Internal guide for maintaining consistency and quality standards across the book.
slug: /writing-guidelines
sidebar_position: 100
---

# Writing Guidelines for Physical AI & Humanoid Robotics

**Internal Document**: This page documents standards for all contributors. Readers don't need to read this.

## Brand Voice Standards

### Tone

- **Simple English**: No jargon without explanation; short sentences; active voice
- **Visionary**: Forward-looking; exciting possibilities without hype
- **Human-Centered**: Focus on impact to people and society; not technology for its own sake
- **Engaging**: Tell stories; use examples; never condescending
- **Never Boring**: Every section has a reason for existing; content connects to reader interests

### Sentence & Paragraph Rules

- **Sentence length**: Maximum 20 words per sentence
- **Paragraph length**: 2–4 sentences maximum; visual breaks with subheadings or lists
- **Active voice**: Prefer "AI learns patterns" over "Patterns are learned by AI"
- **Clarity**: Short words when possible; explain technical terms on first use

## Content Structure

### Chapter Template (MANDATORY)

Every chapter MUST follow this structure:

```markdown
---
title: [Chapter Title]
description: [50-100 char description]
slug: /module1/[chapter-name]
sidebar_position: [number]
---

# Chapter Title

## Learning Objectives

[4-6 checkbox items]

## Overview

[100-150 word engaging introduction]

## [Core Concept Section 1]

[200-300 word explanation]

## [Core Concept Section 2]

[200-300 word explanation]

## Real-World Example

[150-200 word practical application]

## Coding Example 1

[Description of code]

\`\`\`python
# Code here (max 50 lines, commented, tested)
\`\`\`

## Coding Example 2

[Description - IF NEEDED, max 2 examples per chapter]

\`\`\`python
# Code here (max 50 lines, commented)
\`\`\`

## Key Takeaways

[4-5 checkbox items]

## Next Chapter

[Link to next chapter]

## Glossary

[New terms with definitions]

## Troubleshooting

[Q&A format for common issues]
```

## Markdown Formatting Rules

### Headings

- **H1** (chapter title): Use once per file with `# Title`
- **H2** (sections): Use for major topics with `## Section Name`
- **H3** (subsections): Use for supporting topics with `### Subsection Name`
- **Never skip levels**: Go H1 → H2 → H3, not H1 → H3

### Links

- **Internal links**: Use relative paths: `[text](./chapter-2-ros2-basics.md)` or `../glossary.md`
- **All links tested**: Before publishing, verify every link works

### Code Blocks

- **Language specified**: Always use ` ```python `, ` ```bash `, ` ```xml `, etc.
- **Comments**: Include comments every 3-4 lines
- **Expected output**: Show what the code should print

### Lists

- **Bullet format**: Use `- ` for bulleted lists (not `* ` or `+ `)
- **Ordered lists**: Use `1. `, `2. `, `3. ` for numbered lists
- **Consistency**: Don't mix formats within a section

### Emphasis

- **Bold**: Use `**bold**` for key terms and important phrases
- **Italic**: Use `*italic*` for book titles, tool names, and subtle emphasis
- **Avoid**: Don't use CAPS, except for acronyms like ROS 2, AI, URDF

## Content Standards

### Technical Accuracy

- Every claim must be accurate for ROS 2 Humble or newer
- No speculation or "might someday" claims
- Cite sources for statistics or complex claims

### Beginner-Friendly Language

| ❌ Avoid | ✅ Use |
|---------|--------|
| "Utilize asynchronous pub/sub paradigms" | "Send messages between robot parts" |
| "URDF is the standard" | "URDF (robot description format) defines robot structure" |
| "The middleware, which manages communication between nodes in a distributed system architecture, enables real-time data exchange" | "Middleware sends messages between robot parts in real time." |
| "Robots employ sophisticated control mechanisms" | "A robot arm uses motors to pick up objects" |

### Code Examples

- **Max 2 per chapter**: Strictly enforced
- **Tested**: Every code example must run without errors
- **Beginner-friendly**: Avoid advanced Python features
- **Commented**: Explain every 3-4 lines of code
- **Output**: Show what the code should print or display

### Jargon Management

- **Define on first use**: "URDF (Unified Robot Description Format) is..."
- **Add to glossary**: Every new term goes in `glossary.md`
- **Link to glossary**: Use `[term](/docs/glossary.md#term)` if helpful
- **Consistency**: Always use the same term; don't alternate between synonyms

## File Naming Conventions

- **All lowercase**: `chapter-1-middleware.md`, not `Chapter1Middleware.md`
- **Hyphens only**: `chapter-1-middleware.md`, not `chapter_1_middleware.md`
- **No spaces**: `writing-guidelines.md`, not `writing guidelines.md`
- **Descriptive**: Names should indicate content (`chapter-1-middleware.md`, not `ch1.md`)

## Quality Checklist for Every Section

Before publishing, verify:

- [ ] **Clarity**: Can a beginner understand this on first read?
- [ ] **Accuracy**: Are all facts correct and current?
- [ ] **Engagement**: Does this connect to reader interests?
- [ ] **Progression**: Does it build on prior material without assuming advanced knowledge?
- [ ] **Jargon**: All technical terms explained and in glossary?
- [ ] **Length**: Sentences < 20 words? Paragraphs < 4 sentences?
- [ ] **Links**: All internal links work and are relative paths?
- [ ] **Code**: Examples tested, commented, < 50 lines each?
- [ ] **Tone**: Consistent with brand voice (never boring, practical, visionary)?
- [ ] **Format**: Proper Markdown, frontmatter, heading hierarchy?

## Example: Well-Written Section

```markdown
## What is Middleware?

Middleware connects robot parts together. It handles messages between sensors, processors, and motors.

Think of it like a postal system for robots. Messages get delivered. Tasks get coordinated. Everything works together.

Without middleware, each robot part would need custom code to talk to every other part. That's complex and error-prone.

With middleware, parts publish data or send requests. The middleware routes messages automatically. This keeps code simple and reusable.

**Why does this matter?** Robot systems need coordination. Sensors stream data constantly. Motors need commands quickly. Processors must make decisions in real time.

Middleware makes all of this work smoothly together.
```

## Consistency Standards

- **Glossary is source of truth**: All terms must be defined the same way across chapters
- **Examples are current**: Use ROS 2 Humble features; don't reference deprecated versions
- **Images have alt-text**: Every image includes descriptive alt-text for accessibility
- **Terminology aligned**: Use "machine learning" not "ML", "robot" not "bot", consistently

---

**Questions?** Refer back to this guide or discuss with the project team.

