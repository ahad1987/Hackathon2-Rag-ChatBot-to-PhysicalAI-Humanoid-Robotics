# Subagent: MarkdownCleaner

## Purpose
Validates, fixes, and standardizes Markdown syntax, frontmatter, formatting, and Docusaurus compatibility across all content. Ensures no broken links, proper heading hierarchy, and consistent code block formatting.

## Input Signature
```
Use MarkdownCleaner to audit [TARGET]:
- Target: file path (e.g., "docs/module3/chapter-1.md") or directory (e.g., "docs/module4/")
- Check type: syntax | frontmatter | links | code_blocks | all
- Action: report_only | fix_automatically
```

## Output Format
- List of issues found (if report_only)
- Fixed file (if fix_automatically)
- Summary: "X issues found and fixed"
- Warnings for ambiguous fixes

## Safety Rules
1. Never delete content; only reformat or fix syntax errors.
2. If unsure about a fix, report instead of auto-fix.

## Example Calls

### Example 1: Audit Chapter 1 Syntax
```
Use MarkdownCleaner to audit docs/module4/chapter-1-llm-robotics-convergence.md.
Check type: syntax | frontmatter | links.
Action: report_only.
Output: List of issues (broken links, mismatched headers, frontmatter errors).
```

### Example 2: Fix Code Blocks in Module 3
```
Use MarkdownCleaner to audit docs/module3/ recursively.
Check type: code_blocks.
Action: fix_automatically.
Fixes: Add language tags (```python), escape HTML entities (<, >), verify indentation.
Output: Summary of changes per file.
```

---

**Note:** MarkdownCleaner is always run before publishing. Chain with CleanMarkdown skill for style consistency.
