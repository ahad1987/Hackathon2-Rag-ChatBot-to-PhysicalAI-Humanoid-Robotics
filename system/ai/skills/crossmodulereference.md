# Skill: CrossModuleReference

## Purpose
Creates accurate inter-module links and prerequisite callouts. Ensures learners understand what prior knowledge they need, can navigate between related concepts, and won't encounter broken references.

## Usage Examples

### Example 1: Link to ROS 2 Concepts from Module 4
**Reference in Module 4, Chapter 2:**
"Recall from [Module 1: ROS 2 Nodes](/docs/module1/chapter-1-middleware)—a node is a ROS 2 process. Our voice listener is a node that subscribes to `/microphone_input`."

**Correct format:**
- Use Docusaurus format: `[Link Text](/docs/moduleX/chapter-name)`
- Not `../` relative paths
- Always provide context (why they need this prior knowledge)

### Example 2: Prerequisite Callout
**Module 4, Chapter 3 (before teaching task planning):**
```
> ⚠️ **Prerequisite:** This chapter assumes you have completed Module 3, Chapter 4 (Nav2 Path Planning).
> Review [Module 3: Navigation](/docs/module3/chapter-4-nav2-path-planning) if needed.
```

## Required Constraints

1. **Link format:** `[text](/docs/moduleX/chapter-name)` (Docusaurus style, not relative)
2. **Prerequisite callouts:** Use blockquote (>) at chapter start if needed
3. **Context always:** Explain why you're linking (not just bare links)
4. **Verify before publishing:** Test that all links resolve
5. **Avoid forward references:** Don't link to content not yet written
6. **Use consistent language:** "Module 3, Chapter 1" not "Ch3-1" or "Module III"

## Quality Check
- ✅ Do all links use correct Docusaurus format?
- ✅ Are prerequisite callouts placed at the start?
- ✅ Does each link have context (why it's relevant)?
- ✅ Are no forward references present?

---

**Implementation Note:** CrossModuleReference is validated by ContentValidator's link checker.
