# Skill: GlossaryIntegration

## Purpose
Identifies new technical terms, ensures they are bolded on first mention, provides clear definitions in context, and maintains a master glossary. Prevents terminology inconsistencies and orphaned terms.

## Usage Examples

### Example 1: Integrate LLM Terminology
**Before:**
"Large language models are neural networks trained on text. They predict next tokens."

**After (GlossaryIntegration):**
"**Large Language Models (LLMs)** are neural networks trained on vast text corpora to predict sequences of words (tokens). Each **token** is a unit of text—a word or subword—that the model processes. When you ask an LLM a question, it generates **tokens** sequentially, building an answer one piece at a time."

**Glossary entry:**
- **LLM:** A neural network trained on text to predict and generate language
- **Token:** A unit of text (word or subword) processed by language models
- **Inference:** The process of generating output from a trained model

### Example 2: Maintain Cross-Module Consistency
**Module 1 defined:** **Node** as "A ROS 2 process that communicates via topics"
**Module 4 reference:** Should use the same definition, not redefine

## Required Constraints

1. **Bold first mention:** `**Term** is defined as...`
2. **Define immediately:** Within 2 sentences of first use
3. **Use consistent language:** If Module 1 defines Node, use that definition
4. **Avoid re-defining:** Check prior modules before creating new definition
5. **Track in master glossary:** Every new term documented in /docs/glossary.md
6. **Simple definitions:** 1-2 sentences max

## Quality Check
- ✅ Is every technical term bolded on first mention?
- ✅ Is each definition clear for a learner with Modules 1-3 knowledge?
- ✅ Are definitions consistent with prior modules?
- ✅ Is the master glossary updated?

---

**Implementation Note:** GlossaryIntegration is checked by ContentValidator before final approval.
