# Preset: ValidateCrossModule

## Purpose
Check cross-module consistency, verify all links resolve correctly, validate glossary alignment, and ensure prerequisite callouts are accurate. Comprehensive validation before publishing.

## Subagents Called
1. **ContentValidator** — Checks link integrity, glossary consistency, cross-module references
2. **MarkdownCleaner** — Validates Markdown link syntax, frontmatter, hierarchy
3. **QualityGuard** — Reviews prerequisites are appropriate and prerequisites callouts are clear
4. **StructureAgent** — Verifies file paths match sidebar configuration

## Skills Used
1. **CrossModuleReference** — Validates inter-module links and prerequisite callouts
2. **GlossaryIntegration** — Ensures glossary terms are consistent across modules
3. **ConsistencyCheck** — Verifies content aligns with established patterns
4. **CleanMarkdown** — Validates link formatting and Markdown syntax

## Input Signature
```yaml
scope: string               # "all" | "module" | "chapter" | "file" (e.g., "module4" or specific file path)
check_type: list           # Checks to run: ["links", "glossary", "prerequisites", "consistency", "all"]
strict_mode: boolean       # If true, fail on any warning (default: false)
report_format: string      # "summary" | "detailed" | "json"
```

## Output Format
```yaml
scope_validated: string                 # What was checked
validation_passed: boolean              # All checks passed?
total_issues: integer                   # Count of all issues found
issues_by_type:
  broken_links: integer                 # Links that don't resolve
  glossary_conflicts: integer           # Term definition mismatches
  missing_prerequisites: integer        # Prerequisites not called out
  consistency_violations: integer       # Pattern deviations
  syntax_errors: integer                # Markdown/link format issues
issues_detail: list                     # Detailed list with locations
files_affected: integer                 # Count of files with issues
recommendations: list                   # Suggested fixes
```

## Safety Rules

1. **Report all issues** — Never hide potential problems; surface everything
2. **Cross-module links must resolve** — Every link to another module must point to actual file
3. **Glossary must be consistent** — Same term can't have different definitions across modules
4. **Prerequisites must be clear** — If chapter requires Module X knowledge, callout must be present
5. **Don't auto-fix critical issues** — Report and require user approval before modifying links

## Workflow Steps

### Step 1: Scope Analysis
- Determine which files/modules to validate based on scope parameter
- ContentValidator creates list of all files to check

### Step 2: Link Validation
- MarkdownCleaner scans all cross-module links (format: `[text](/docs/moduleX/chapter-name)`)
- ContentValidator verifies each link points to actual file that exists
- Flag broken links, relative paths (should be Docusaurus format), malformed links
- Check sidebar.ts to ensure all linked files are properly indexed

### Step 3: Glossary Consistency Check
- GlossaryIntegration scans all glossary files (docs/glossary.md, docs/moduleX/glossary.md)
- Extract all defined terms and their definitions
- Check for conflicting definitions (same term defined differently across modules)
- Verify all bolded terms in chapters have corresponding glossary entries
- Flag undefined terms (bolded but no glossary entry)

### Step 4: Prerequisites Validation
- QualityGuard reviews all prerequisite callouts (blockquote format: `> ⚠️ **Prerequisite:**...`)
- Verify each prerequisite callout references an actual prior module/chapter
- Check that complex chapters have prerequisite callouts
- Flag missing prerequisites (chapters that should have callouts but don't)

### Step 5: Consistency Check
- ConsistencyCheck validates chapter structure matches Module 3 patterns
- Verify file naming conventions (chapter-N-descriptive-title.md)
- Check heading hierarchy (no skipped levels)
- Confirm all chapters have required sections (learning objectives, code examples, real-world applications, etc.)

### Step 6: Report Generation
- Aggregate all findings by severity (critical, warning, suggestion)
- Generate recommendations with specific fix examples
- Output in requested format (summary, detailed, json)

## Example Invocation

### Command
```
ValidateCrossModule --scope all --check_type ["links", "glossary", "prerequisites"] --report_format detailed
```

### Expected Output
```yaml
scope_validated: all (22 files across Modules 1-4)
validation_passed: false
total_issues: 8

issues_by_type:
  broken_links: 2
  glossary_conflicts: 1
  missing_prerequisites: 2
  consistency_violations: 2
  syntax_errors: 1

issues_detail:
  - severity: critical
    type: broken_link
    file: docs/module4/chapter-2-voice-to-action-whisper.md
    line: 145
    issue: "Link points to non-existent file"
    current: "[Module 3 Navigation](/docs/module3/chapter-5-advanced-navigation)"
    problem: "chapter-5 does not exist in Module 3 (only 4 chapters)"
    suggestion: "[Module 3 Navigation](/docs/module3/chapter-4-nav2-path-planning)"

  - severity: critical
    type: broken_link
    file: docs/module4/chapter-3-cognitive-planning-llm.md
    line: 89
    issue: "Relative path used instead of Docusaurus format"
    current: "[Previous Concepts](../module1/chapter-1.md)"
    problem: "Relative paths break in some Docusaurus configurations"
    suggestion: "[Previous Concepts](/docs/module1/chapter-1-ros2-fundamentals)"

  - severity: warning
    type: glossary_conflict
    modules: ["module1", "module3", "module4"]
    term: "**Node**"
    definitions:
      - "Module 1: A ROS 2 process that communicates via topics"
      - "Module 3: A computational unit in a neural network"
      - "Module 4: Consistently uses Module 1 definition ✓"
    issue: "Term 'Node' has conflicting definitions between modules"
    recommendation: "In Module 3, rename neural network concept to '**Neural Node**' or '**Neuron**' to avoid confusion"

  - severity: warning
    type: missing_prerequisite
    file: docs/module4/chapter-3-cognitive-planning-llm.md
    line: 1
    issue: "Chapter assumes knowledge of path planning but no prerequisite callout"
    context: "Chapter references '[Nav2 path planning](/docs/module3/chapter-4-nav2-path-planning)' multiple times"
    suggestion: "Add at top of chapter: '> ⚠️ **Prerequisite:** This chapter builds on Module 3, Chapter 4 (Nav2 Path Planning).'"

  - severity: warning
    type: missing_prerequisite
    file: docs/module4/chapter-4-autonomous-humanoid-capstone.md
    line: 1
    issue: "Capstone project assumes all prior chapters completed, but no explicit prerequisite"
    suggestion: "Add: '> ⚠️ **Prerequisite:** Complete Module 4, Chapters 1-3 and Module 1-3 entirely before starting.'"

  - severity: suggestion
    type: consistency_violation
    file: docs/module4/chapter-1-llm-robotics-convergence.md
    line: 340
    issue: "Code example block is missing Python language tag"
    current: "```\n# Missing python tag"
    suggestion: "```python\n# Add language tag for syntax highlighting"

  - severity: suggestion
    type: consistency_violation
    file: docs/module2/chapter-2-gazebo-physics.md
    line: 215
    issue: "Heading hierarchy skips level: ## to ####"
    current: "## Simulation Concepts\n#### Physics Engine Details"
    suggestion: "## Simulation Concepts\n### Physics Engine Details"

  - severity: suggestion
    type: syntax_error
    file: docs/module3/chapter-3-data-pipeline-ml.md
    line: 156
    issue: "HTML entity not escaped in table cell"
    current: "Input size <12 tokens"
    suggestion: "Input size &lt;12 tokens"

files_affected: 5 (module2/chapter-2, module3/chapter-3, module4/chapter-1, module4/chapter-2, module4/chapter-3, module4/chapter-4)

recommendations:
  1. [CRITICAL] Fix broken link in module4/chapter-2 (line 145): chapter-5 → chapter-4
  2. [CRITICAL] Fix relative path in module4/chapter-3 (line 89): use Docusaurus format
  3. [HIGH] Resolve glossary conflict: clarify "Node" definition in Module 3
  4. [HIGH] Add prerequisite callouts to module4/chapter-3 and module4/chapter-4
  5. [MEDIUM] Add Python language tag to code block in module4/chapter-1
  6. [MEDIUM] Fix heading hierarchy in module2/chapter-2 (skip level violation)
  7. [LOW] Escape HTML entity in module3/chapter-3 table
```

### Command (Strict Mode)
```
ValidateCrossModule --scope module4 --check_type all --strict_mode true
```

### Expected Output
```yaml
scope_validated: module4 (5 files: introduction.md, chapter-1.md, chapter-2.md, chapter-3.md, chapter-4.md)
validation_passed: false (strict mode: 1 critical issue blocks validation)

total_issues: 3
issues_by_type:
  broken_links: 1
  glossary_conflicts: 0
  missing_prerequisites: 1
  consistency_violations: 1
  syntax_errors: 0

validation_status: FAILED (strict mode enabled)
blocking_issues: 1 (critical: broken link in chapter-2)

Strict mode requires ALL issues to be resolved. Fix broken link and re-run.
```

## Quality Checks
- ✅ Do all cross-module links point to actual files?
- ✅ Are glossary definitions consistent across modules?
- ✅ Do complex chapters have prerequisite callouts?
- ✅ Do file names follow established naming convention?
- ✅ Are all code examples properly formatted?
- ✅ Is heading hierarchy correct throughout?

---

**Implementation Note:** Run ValidateCrossModule after WriteChapter, WriteLesson, or FixStructure to ensure no broken links or inconsistencies were introduced. Use `--strict_mode true` before publishing to ensure all issues are resolved. Can be scheduled as pre-deployment check in CI/CD pipeline.
