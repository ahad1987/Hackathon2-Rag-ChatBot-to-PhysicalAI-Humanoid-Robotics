# Skill: ConsistencyCheck

## Purpose
Validates alignment with project constitution, established patterns from Modules 1-3, naming conventions, and formatting standards. Ensures every new piece of content feels cohesive with the whole.

## Usage Examples

### Example 1: Check Chapter Structure Consistency
**Module 3, Chapter 1 structure:**
- Introduction with learning objectives
- 8-10 theory sections
- 2 code examples
- 3 real-world applications
- 1 hands-on exercise
- Debugging section
- Summary with glossary

**New content (Module 4, Chapter 1):**
- Should follow the same pattern
- Verify: Same number of sections? Same types? Same naming?

### Example 2: Check Naming Conventions
**Module 3 format:** `chapter-1-advanced-perception-training.md`
**Module 4 format:** `chapter-1-llm-robotics-convergence.md`
**Check:** Hyphenated, lowercase, descriptive? ✅

## Required Constraints

1. **File naming:** `chapter-N-descriptive-title.md` (lowercase, hyphens, no underscores)
2. **Heading hierarchy:** Intro as ##, subsections as ###, never skip levels
3. **Module patterns:** Every module follows 4-chapter + introduction + glossary structure
4. **Cross-links:** All references to prior modules use consistent `/docs/moduleX/` format
5. **Code examples:** Always 2 per lesson, always have expected output
6. **Real-world applications:** Always 3+ examples per chapter
7. **Glossary integration:** New terms bolded, defined in context

## Quality Check
- ✅ Does this match the pattern of Module 3?
- ✅ Are file names consistent with naming convention?
- ✅ Do cross-links follow Docusaurus format?
- ✅ Is the glossary integration consistent?

---

**Implementation Note:** ConsistencyCheck is applied before QualityGuard final review.
