# Skill: GenerateLessonFormat

## Purpose
Structures all lesson sections consistently to maximize learning: intro → learning objectives → theory → code examples → real-world applications → hands-on exercise → debugging → summary. This predictable format helps learners know what to expect.

## Usage Examples

### Example 1: Lesson Template (Module 3, Chapter 2)
```
## Chapter 2: Isaac Sim and Synthetic Data

### Introduction (Why This Matters)
Hook: "Why do robots need digital twins?"
Problem statement, learning goals, time estimate.

### Learning Objectives
- [ ] Understand Gazebo physics simulation
- [ ] Create synthetic datasets from simulation
- [ ] Train ML models on synthetic data

### Theory (20-30% of content)
Concept explanation with diagrams, step-by-step progression.

### Code Examples (15-20% of content)
1-2 Python + rclpy examples with expected output.

### Real-World Applications (15% of content)
2-3 industry examples (Tesla, Boston Dynamics, etc.).

### Hands-On Exercise (20-30% of content)
Step-by-step guide, testable success criteria.

### Debugging & Troubleshooting (10% of content)
3-5 common errors with solutions.

### Summary & Glossary (5-10% of content)
Recap, new terms, preview of next chapter.
```

### Example 2: Time Allocation for 1-Hour Lesson
- Reading (40 min): Intro + Theory + Examples + Real-World
- Hands-On (15 min): Guided exercise
- Review (5 min): Debugging + Summary

## Required Constraints

1. **Intro must hook:** Answer "Why should I care?"
2. **Objectives are testable:** Use action verbs (Understand, Implement, Explain)
3. **Theory is conceptual:** No implementation details yet
4. **Examples work in isolation:** Learner can copy-paste and run
5. **Exercise is guided:** Step-by-step with expected output
6. **Summary ties everything together:** "You now know how to..."

## Quality Check
- ✅ Does each section have a clear purpose?
- ✅ Are learning objectives testable?
- ✅ Is the time allocation realistic for 45-60 minutes?
- ✅ Would a complete beginner follow this structure?

---

**Implementation Note:** GenerateLessonFormat is applied to all BookWriter sections.
