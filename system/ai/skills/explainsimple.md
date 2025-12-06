# Skill: ExplainSimple

## Purpose
Breaks complex robotics and AI concepts into beginner-friendly language. Uses analogies, step-by-step progression, and real-world grounding. Assumes the learner has Module 1-3 knowledge but may not have specialized ML/AI background.

## Usage Examples

### Example 1: Explain LLMs Simply
**Technical version:** "Large language models use transformer architecture with multi-head attention and positional encoding to predict token sequences."

**ExplainSimple version:** "LLMs work like a next-word predictor trained on billions of examples. They learn patterns: after 'the robot moved', the word 'forward' is likely. They string predictions together to generate complete sentences—and with the right prompts, generate robot commands."

### Example 2: Explain Task Decomposition
**Technical version:** "LLM-based task planning leverages semantic understanding to decompose goals into temporally-ordered sub-tasks with dependency graphs."

**ExplainSimple version:** "When you say 'pick up the cup and move it to the table,' the LLM breaks it into steps: 1) Find the cup, 2) Move arm above cup, 3) Grasp it, 4) Move to table, 5) Release. This is how humans think about tasks—and now robots can too."

## Required Constraints

1. **Use analogies:** Compare to familiar concepts (LLM as translator, task planning as recipe, etc.)
2. **Short sentences:** Average 12-15 words, max 25 words
3. **Active examples:** Always show what it does, not just what it is
4. **Acknowledge the learner:** "You know ROS 2 nodes—think of this as..."
5. **Avoid:** math formulas, academic jargon, assumptions about prior knowledge beyond Modules 1-3

## Quality Check
- ✅ Would a non-expert understand this?
- ✅ Is there a helpful analogy?
- ✅ Does it show the "so what?" (why it matters)?

---

**Implementation Note:** ExplainSimple is used in theory sections and hands-on exercise descriptions.
