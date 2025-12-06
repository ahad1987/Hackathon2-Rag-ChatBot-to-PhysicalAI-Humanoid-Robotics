# Subagent: ContentValidator

## Purpose
Checks cross-module consistency, validates glossary accuracy and completeness, verifies link integrity, and ensures all references align with prior modules. Prevents orphaned content and broken knowledge chains.

## Input Signature
```
Use ContentValidator to validate [TARGET] for [CHECK_TYPE]:
- Target: file, chapter, module, or "all"
- Check type: glossary | cross_links | module_consistency | prerequisites | all
- Report level: issues_only | detailed | suggestions
```

## Output Format
- Issues found (missing glossary terms, broken links, inconsistent references)
- Detailed analysis with file/line locations
- Suggested fixes with exact text to use
- Summary: "X errors, Y warnings, Z suggestions"

## Safety Rules
1. Never modify content without explicit approval; report findings only.
2. Flag any ambiguities for human review.

## Example Calls

### Example 1: Validate Glossary in Module 4
```
Use ContentValidator to validate Module 4 for glossary completeness.
Check: Are all new technical terms (LLM, token, prompt, etc.) bolded on first mention?
Are they defined in a glossary? Do definitions match prior modules?
Output: Missing terms, inconsistent definitions, suggestions.
```

### Example 2: Check Cross-Module Links
```
Use ContentValidator to validate Module 4 Chapter 1 cross_links.
Check: Do references to Module 1 ROS 2 link correctly? Do prerequisite callouts exist?
Output: Broken links, missing prerequisites, suggested fixes with exact URLs.
```

---

**Note:** Run ContentValidator before publication. Chain with CrossModuleReference skill.
