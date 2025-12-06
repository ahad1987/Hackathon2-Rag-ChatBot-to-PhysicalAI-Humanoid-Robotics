# Preset: CleanStyle

## Purpose
Audit module content for Markdown syntax consistency, brand voice alignment, and formatting standards. Optionally apply fixes automatically or report issues for manual review.

## Subagents Called
1. **MarkdownCleaner** — Identifies and fixes Markdown syntax issues, frontmatter, code blocks, links
2. **QualityGuard** — Reviews brand voice, tone consistency, and pedagogical soundness
3. **ContentValidator** — Checks formatting against Docusaurus standards
4. **BookWriter** — (Optional) Suggests tone improvements for non-compliant sections

## Skills Used
1. **CleanMarkdown** — Applies strict Markdown/Docusaurus standards
2. **VisionaryTone** — Identifies tone mismatches; suggests visionary rewrites
3. **ConsistencyCheck** — Validates alignment with Module 3 patterns
4. **GlossaryIntegration** — Ensures terms are bolded consistently

## Input Signature
```yaml
scope: string               # "module" | "chapter" | "file" (e.g., "module4" or "docs/module4/chapter-2-*.md")
check_type: list           # Checks to run: ["markdown", "brand_voice", "glossary", "links", "all"]
action: string             # "report_only" | "fix_automatically" | "suggest_revisions"
exclude_patterns: list     # Patterns to skip (optional, e.g., ["code_examples", "debug_section"])
```

## Output Format
```yaml
scope_checked: string           # What was audited
issues_found: integer          # Total count of issues
issues_by_severity:
  critical: integer            # Must fix (e.g., invalid syntax)
  warning: integer             # Should fix (e.g., inconsistent heading levels)
  suggestion: integer          # Nice-to-have (e.g., tone could be more visionary)
issues_detail: list           # List of issues with location and suggested fix
files_affected: list          # Files with at least one issue
action_taken: string          # "report_only" | "fixes_applied" | "revisions_suggested"
fixes_applied: integer        # Count of automatic fixes (if action=fix_automatically)
validation_passed: boolean    # All critical issues resolved?
```

## Safety Rules

1. **Report first, act carefully** — When action=fix_automatically, show report first; never auto-fix without user review for critical issues
2. **Preserve content** — Fixes should only touch formatting/spacing, never remove or reword substantial content
3. **Respect code blocks** — Never reformat Python code examples; only check syntax (language tags, indentation)
4. **Brand voice is subjective** — When suggesting tone improvements, show before/after with rationale
5. **Validate after fixes** — Re-run checks after auto-fixes to ensure no new issues introduced

## Workflow Steps

### Step 1: Scope Analysis
- MarkdownCleaner scans all files in scope (module/chapter/single file)
- Identify all Markdown syntax issues, code blocks, links, frontmatter

### Step 2: Multi-Check Auditing
- **Markdown Check**: Validate heading hierarchy, code block language tags, link format, HTML entities
- **Brand Voice Check**: QualityGuard reviews intro, conclusion, section titles for consistency with VisionaryTone
- **Glossary Check**: Verify all technical terms are bolded, defined in context
- **Link Check**: ContentValidator verifies all cross-module links, ensures no broken references

### Step 3: Issue Categorization
- Classify issues by severity: Critical (breaks build), Warning (inconsistent), Suggestion (style improvement)
- Generate detailed issue list with file locations, line numbers, current text, suggested fix

### Step 4: Action Based on Input
- **If report_only**: Output detailed audit report
- **If fix_automatically**: Apply non-critical fixes (Markdown formatting, typos, spacing); suggest critical fixes for user review
- **If suggest_revisions**: Provide before/after examples for tone/wording changes

### Step 5: Validation & Summary
- Re-run checks on fixed files to ensure no regressions
- Output summary with file count, issue count, action taken, next steps

## Example Invocation

### Command
```
CleanStyle --scope module4 --check_type ["markdown", "brand_voice", "glossary"] --action report_only
```

### Expected Output
```yaml
scope_checked: module4 (5 files: introduction.md, chapter-1.md, chapter-2.md, chapter-3.md, chapter-4.md)
issues_found: 23
issues_by_severity:
  critical: 2
  warning: 8
  suggestion: 13

issues_detail:
  - severity: critical
    file: docs/module4/chapter-2-voice-to-action-whisper.md
    line: 142
    type: markdown_syntax
    issue: "Code block missing language tag"
    current: "```\nimport rclpy"
    suggested: "```python\nimport rclpy"

  - severity: critical
    file: docs/module4/chapter-1-llm-robotics-convergence.md
    line: 89
    type: markdown_syntax
    issue: "HTML entity not escaped in table: < should be &lt;"
    current: "<12 tokens"
    suggested: "&lt;12 tokens"

  - severity: warning
    file: docs/module4/introduction.md
    line: 45
    type: heading_hierarchy
    issue: "Skipped heading level: ## to #### (should be ###)"
    current: "## Overview\n#### Deep Dive"
    suggested: "## Overview\n### Deep Dive"

  - severity: warning
    file: docs/module4/chapter-3-cognitive-planning-llm.md
    line: 201
    type: link_format
    issue: "Relative link used; should be Docusaurus format"
    current: "[Module 3](../module3/chapter-1.md)"
    suggested: "[Module 3: Advanced Perception](/docs/module3/chapter-1-advanced-perception-training)"

  - severity: suggestion
    file: docs/module4/chapter-1-llm-robotics-convergence.md
    line: 12
    type: brand_voice
    issue: "Intro could be more visionary; currently technical"
    current: "LLMs are neural networks trained on text. They predict tokens."
    suggested: "Imagine a robot that understands intent, not just words. That's what happens when we combine **Large Language Models** with robotics—machines that think, reason, and adapt to your commands."

  - severity: suggestion
    file: docs/module4/chapter-2-voice-to-action-whisper.md
    line: 78
    type: glossary
    issue: "Term 'acoustic features' used but not bolded/defined"
    current: "The model processes acoustic features..."
    suggested: "The model processes **acoustic features**—digital representations of sound patterns that capture pitch, intensity, and timing."

files_affected:
  - docs/module4/introduction.md (3 issues)
  - docs/module4/chapter-1-llm-robotics-convergence.md (7 issues)
  - docs/module4/chapter-2-voice-to-action-whisper.md (6 issues)
  - docs/module4/chapter-3-cognitive-planning-llm.md (4 issues)
  - docs/module4/chapter-4-autonomous-humanoid-capstone.md (3 issues)

action_taken: report_only
fixes_applied: 0
validation_passed: false (2 critical issues must be fixed)

Next Steps:
1. Fix 2 critical Markdown syntax issues (code block tag, HTML entity)
2. Review 8 warning issues (heading hierarchy, link formats)
3. Consider 13 tone/glossary suggestions for enhanced clarity
4. Re-run CleanStyle --action fix_automatically after addressing critical issues
```

### Command (with automatic fixes)
```
CleanStyle --scope docs/module4/chapter-2-voice-to-action-whisper.md --check_type ["markdown"] --action fix_automatically
```

### Expected Output (Execution)
```yaml
scope_checked: docs/module4/chapter-2-voice-to-action-whisper.md
issues_found: 6
issues_by_severity:
  critical: 1
  warning: 3
  suggestion: 2

action_taken: fixes_applied
fixes_applied: 3 (non-critical Markdown issues)

Fixed Issues:
  - Line 142: Added python language tag to code block
  - Line 89: Escapes < as &lt; in table
  - Line 201: Fixed heading hierarchy ## → ###

Remaining Critical Issues (requires user review):
  - Line 156: Link format needs manual update (relative → Docusaurus)

validation_passed: false (1 critical issue remains)

Recommended Next Step:
  1. Manually update relative link at line 156
  2. Run CleanStyle again to verify all issues resolved
```

## Quality Checks
- ✅ Are all critical Markdown syntax issues identified?
- ✅ Is brand voice consistent with VisionaryTone standards?
- ✅ Are all glossary terms bolded and defined?
- ✅ Do all links follow Docusaurus format?
- ✅ Are code blocks properly tagged with language?
- ✅ Is heading hierarchy correct (no skipped levels)?

---

**Implementation Note:** CleanStyle is perfect for pre-publication audits. Run `--action report_only` first to review issues, then decide whether to auto-fix or manually address critical items. After fixes, run ValidateCrossModule to ensure no broken references.
