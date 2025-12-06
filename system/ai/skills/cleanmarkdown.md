# Skill: CleanMarkdown

## Purpose
Applies strict Markdown and Docusaurus formatting standards. Ensures proper heading hierarchy, consistent code block formatting, correct link syntax, proper list indentation, and HTML entity escaping for special characters.

## Usage Examples

### Example 1: Fix Code Block Formatting
**Before:**
```
Look at this example:
import rclpy
node = rclpy.init()
```

**After (CleanMarkdown):**
\`\`\`python
import rclpy
node = rclpy.init()
\`\`\`

### Example 2: Escape HTML Entities in Tables
**Before:**
```
| Metric | Target |
|--------|--------|
| Latency | <12 seconds |
```

**After (CleanMarkdown):**
```
| Metric | Target |
|--------|--------|
| Latency | &lt;12 seconds |
```

## Required Constraints

1. **Heading hierarchy:** # only for page title, ## for sections, ### for subsections (never skip levels)
2. **Code blocks:** Always include language tag (```python, ```bash, etc.)
3. **Inline code:** Backticks for technical terms (`rclpy`, `node`, `topic`)
4. **Links:** Docusaurus format `[text](/path/to/page)` not `[text](../path)`
5. **Special characters:** Escape `<`, `>` as `&lt;`, `&gt;` in tables/lists
6. **Lists:** 2-space indentation for nested items
7. **Blockquotes:** `>` for callouts and notes

## Quality Check
- ✅ All code blocks have language tags?
- ✅ No broken link references?
- ✅ Heading hierarchy is consistent?
- ✅ Special characters properly escaped?

---

**Implementation Note:** CleanMarkdown runs automatically before MarkdownCleaner's final validation.
