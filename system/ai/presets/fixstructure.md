# Preset: FixStructure

## Purpose
Reorganize module content, refactor chapter hierarchies, update sidebars, and ensure consistent file naming and directory structure.

## Subagents Called
1. **StructureAgent** — Plans and executes directory reorganization, validates file naming
2. **MarkdownCleaner** — Fixes Markdown heading hierarchy and frontmatter
3. **ContentValidator** — Updates all cross-module links after file moves
4. **QualityGuard** — Validates that refactoring doesn't break pedagogical structure

## Skills Used
1. **ConsistencyCheck** — Ensures naming conventions and structure match established patterns
2. **CleanMarkdown** — Fixes heading levels and Markdown formatting after reorganization
3. **CrossModuleReference** — Updates all links to reflect new file paths
4. **GlossaryIntegration** — Verifies glossary references still valid after restructuring

## Input Signature
```yaml
action: string              # "reorganize_module" | "refactor_chapters" | "rename_files" | "update_sidebar"
scope: string               # Module/chapter identifier (e.g., "module4" or "module3/chapter-2")
plan_only: boolean          # If true, show plan but don't execute
target_structure: object    # (Optional) Desired directory tree layout
naming_convention: string   # (Optional) File naming pattern to enforce
```

## Output Format
```yaml
action_taken: string            # Which reorganization was performed
files_moved: list              # Files renamed/moved with old→new paths
links_updated: integer         # Count of cross-module links fixed
sidebar_changes: string        # Updated sidebars.ts content (if modified)
validation_passed: boolean     # All checks passed?
warnings: list                 # Non-critical issues (e.g., "moved file referenced 3 places")
issues: list                   # Critical issues requiring human review
rollback_available: boolean    # Can be undone? (git-based)
```

## Safety Rules

1. **Always show plan first** — Never reorganize without user approval of proposed changes
2. **Preserve content** — No file deletions; moves only (with backups via git)
3. **Update all cross-references** — Every link, include, and reference must be updated
4. **Validate sidebar.ts** — If moving chapters, update sidebars.ts and verify syntax
5. **Test in isolation** — Reorganization should not break build or validation checks

## Workflow Steps

### Step 1: Analysis & Planning
- StructureAgent analyzes current directory structure, identifies inconsistencies
- ConsistencyCheck compares current structure against Module 3 patterns
- StructureAgent generates proposed reorganization plan (ASCII tree showing before/after)

### Step 2: Impact Assessment
- ContentValidator scans all files for references (includes, links, cross-module references)
- StructureAgent identifies all files that would be affected by proposed changes
- QualityGuard checks if reorganization affects pedagogical flow or prerequisites

### Step 3: User Approval (if plan_only=true)
- Output proposed changes as ASCII tree with file counts and link impact
- Wait for user confirmation before proceeding to Step 4

### Step 4: Execution (if plan_only=false)
- StructureAgent creates new directory structure
- MarkdownCleaner ensures all heading hierarchies are correct after moves
- ContentValidator updates all cross-module links (search-replace across all .md files)
- If sidebar.ts changes are needed, update entries for moved chapters

### Step 5: Validation & Cleanup
- ContentValidator re-scans all files to verify no broken references
- CleanMarkdown validates Markdown syntax in all affected files
- Confirm sidebars.ts has valid TypeScript syntax
- Output summary of changes with before/after comparison

## Example Invocation

### Command
```
FixStructure --action reorganize_module --scope module3 --plan_only true
```

### Expected Output (Plan Only)
```yaml
action_taken: reorganize_module
plan_only: true

Proposed Changes (Module 3):
==============================================================

CURRENT STRUCTURE:
docs/module3/
├── introduction.md (195 lines)
├── chapter-1-advanced-perception.md (842 lines)
├── chapter-2-isaac-sim-synthetic.md (756 lines)
├── chapter-3-data-pipeline-ml.md (892 lines)
└── chapter-4-nav2-path-planning.md (1043 lines)

PROPOSED STRUCTURE (no changes needed):
docs/module3/
├── _category_.json (exists, valid)
├── introduction.md (195 lines) ✓
├── chapter-1-advanced-perception-training.md (842 lines) ✓
├── chapter-2-isaac-sim-synthetic-data.md (756 lines) ✓
├── chapter-3-data-pipeline-ml-integration.md (892 lines) ✓
└── chapter-4-nav2-path-planning-navigation.md (1043 lines) ✓

Impact Analysis:
- Files to move: 0
- Files to rename: 0
- Cross-module links to update: 0
- Sidebar.ts changes: 0

Validation: ✓ Module 3 structure is already consistent with patterns

Conclusion: No changes required. Module 3 follows established naming and structure conventions.
```

### Command (with actual reorganization)
```
FixStructure --action refactor_chapters --scope module4 --plan_only false
```

### Expected Output (Execution)
```yaml
action_taken: refactor_chapters
files_moved:
  - "docs/module4/chapter-1-llm-robotics.md → docs/module4/chapter-1-llm-robotics-convergence.md"
  - "docs/module4/chapter-2-voice-action.md → docs/module4/chapter-2-voice-to-action-whisper.md"
links_updated: 12
sidebar_changes: |
  export const sidebar = [
    {
      type: 'category',
      label: 'Module 4: LLM & Humanoid Robotics',
      items: [
        { type: 'doc', id: 'module4/introduction' },
        { type: 'doc', id: 'module4/chapter-1-llm-robotics-convergence' },
        { type: 'doc', id: 'module4/chapter-2-voice-to-action-whisper' },
        ...
      ],
    },
  ];
validation_passed: true
warnings:
  - "File 'chapter-1-llm-robotics-convergence.md' is referenced in 3 external files; all updated"
issues: []
rollback_available: true
```

## Quality Checks
- ✅ Does proposed structure match established patterns (Module 3)?
- ✅ Are all cross-module links updated with no broken references?
- ✅ Is sidebars.ts valid TypeScript after changes?
- ✅ Do file names follow `chapter-N-descriptive-title.md` convention?
- ✅ Does reorganization preserve pedagogical flow?
- ✅ Can changes be rolled back via git?

---

**Implementation Note:** FixStructure is used for maintaining consistency and refactoring modules. Always run with `--plan_only true` first to review proposed changes. After execution, run ValidateCrossModule to verify no links were broken by reorganization.
