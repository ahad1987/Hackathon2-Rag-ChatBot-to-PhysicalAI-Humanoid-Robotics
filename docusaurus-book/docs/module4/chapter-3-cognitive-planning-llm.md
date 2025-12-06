---
title: "Chapter 3: Cognitive Planning with LLMs"
description: "Use LLMs to plan multi-step robot actions. Validate plans for safety, handle errors, and refine through multi-turn interactions."
slug: chapter-3-cognitive-planning-llm
sidebar_position: 4
---

# Chapter 3: Cognitive Planning with LLMs

## Overview

This chapter teaches you how to use LLMs for task planning. Given a natural language goal like "clean the table," you'll decompose it into executable robot actions, validate for safety, and handle errors gracefully.

**Duration**: 45–55 minutes | **Difficulty**: Intermediate to Advanced

---

## Learning Objectives

By the end of this chapter, you will:

1. Decompose natural language tasks into robot actions
2. Write effective prompts for task planning
3. Validate plans for safety and feasibility
4. Handle invalid plans and recover gracefully
5. Optimize LLM API costs for robot applications

---

## Key Concepts

- **Task Decomposition**: Breaking down high-level goals into steps
- **Plan Validation**: Checking plans for safety and feasibility
- **Safety Constraints**: Rules that robot actions must follow
- **Hallucination Mitigation**: Preventing the LLM from suggesting impossible actions
- **Multi-Turn Context**: Maintaining conversation history for refinement
- **Token Efficiency**: Minimizing API calls and costs

---

## Section 1: Task Decomposition with LLMs

### The Problem

Given a goal: "Pick up the red cube and place it on the table"

A human understands:
1. Find the red cube
2. Navigate to its location
3. Position gripper above it
4. Grasp it
5. Lift it
6. Navigate to table
7. Position over table
8. Lower and release

An LLM can learn this decomposition from examples.

### Prompting for Decomposition

```python
prompt = """
You are a robot task planner. Given a high-level goal,
decompose it into a sequence of robot actions.

Available actions:
- navigate_to(location): Move to a named location
- detect_object(color, shape): Find object by properties
- grasp(force): Activate gripper with specified force
- move_arm(x, y, z): Move arm to 3D position
- release(): Open gripper

Goal: Pick up the red cube and place it on the table

Actions:
"""
```

---

## Section 2: Prompt Engineering for Planning

### Prompt Structure

A good planning prompt includes:
1. **Role Definition**: "You are a robot task planner"
2. **Context**: Available actions, environment description
3. **Constraints**: Safety rules, physical limits
4. **Examples**: Few-shot examples for better performance
5. **Output Format**: Structured response (JSON, list, etc.)

### Example: Complex Planning

```python
prompt = """
You are an autonomous robot planner. The robot has:
- Mobile base (can navigate 2D space)
- Gripper (can grasp objects up to 2 kg)
- Camera (can detect objects, colors)
- Arm (6-DOF, can reach 1.5 m)

Available actions (in order):
1. navigate_to(room)
2. locate_by_color(color)
3. approach_object()
4. grasp()
5. navigate_home()

Constraints:
- Don't request actions on objects >2kg
- Don't suggest navigation outside the building
- Always return home after task

Task: "Fetch a paper cup from the kitchen and bring it to my desk"

Generate a step-by-step plan:
"""
```

---

## Section 3: Plan Validation and Safety

### Safety Validation Framework (SAFER)

SAFER uses dual-LLM validation:

```
Task Input
    ↓
Planner LLM
(Generate candidate plan)
    ↓
Validator LLM
(Check for safety violations)
    ↓
Safe? → Execute : Ask for clarification
```

### Validation Rules

| Rule | Example | Consequence |
|------|---------|-------------|
| Robot capability | Grasp object > 5kg | Reject plan |
| Physical feasibility | Reach location outside arm range | Reject plan |
| Safety constraint | Push human off table | Reject plan |
| Environmental | Navigate through wall | Reject plan |

### Implementation

```python
def validate_plan(plan, robot_capabilities):
    """Check if plan is safe and feasible."""

    safety_rules = [
        lambda a: a['action'] != 'push_human',  # Never push humans
        lambda a: a['weight'] <= 5,  # Max grasp weight
        lambda a: a['distance'] <= robot_capabilities['reach'],
    ]

    for action in plan:
        for rule in safety_rules:
            if not rule(action):
                return False, f"Violated: {action}"

    return True, "Plan is valid"
```

---

## Section 4: Multi-Turn Interaction

### Conversation History

```python
messages = [
    {"role": "user", "content": "Pick up the red cube"},
    {"role": "assistant", "content": "[plan]"},
    {"role": "user", "content": "What if the cube is on the shelf?"},
    {"role": "assistant", "content": "[revised plan]"},
]
```

### Refinement Loop

1. User provides goal
2. LLM generates plan
3. System validates
4. If invalid, ask clarification
5. Update context, regenerate
6. Iterate until valid plan

---

## Section 5: Real-World Planning Applications

### Google Robotics Transformer (RT-2)

RT-2 combines vision and language to execute real manipulation tasks. It learns from diverse robot data and generalizes to novel tasks.

### DeepMind's Gato

Gato is a generalist agent that handles multiple modalities (language, vision, control). It learns task structure from data and applies it across different robots.

### Tesla's Occupancy Network

Tesla uses occupancy prediction to plan paths through complex environments. The system combines vision with semantic understanding of the scene.

---

## Section 6: Handling Invalid Plans

### Error Recovery

```python
def plan_and_validate(goal):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            plan = generate_plan(goal)
            is_valid, reason = validate_plan(plan)

            if is_valid:
                return plan
            else:
                # Add constraint to context
                goal += f". Note: {reason}. Please revise."

        except Exception as e:
            logger.error(f"Planning error: {e}")

    return None, "Could not generate valid plan"
```

---

## Section 7: Hands-On Exercise – Planning System with Safety

### Objectives

- Build a task planner using LLM
- Implement safety validation
- Handle errors and ask for clarification
- Demonstrate multi-turn refinement

### Step 1: Create a Planner

```python
#!/usr/bin/env python3

from openai import OpenAI

class RobotTaskPlanner:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []

    def plan(self, goal):
        self.messages.append({"role": "user", "content": goal})

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.messages,
            system="You are a robot task planner. Generate executable action sequences."
        )

        plan = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": plan})
        return plan

    def validate(self, plan):
        """Check if plan is safe."""
        unsafe_words = ['push', 'drop', 'throw', 'break']
        if any(word in plan.lower() for word in unsafe_words):
            return False, "Plan contains unsafe actions"
        return True, "Plan validated"

    def execute_planning_loop(self, goal):
        max_attempts = 3
        for attempt in range(max_attempts):
            print(f"\n[Attempt {attempt+1}]")
            plan = self.plan(goal)
            print(f"Plan: {plan}")

            is_valid, reason = self.validate(plan)
            if is_valid:
                print(f"✓ Valid: {reason}")
                return plan
            else:
                print(f"✗ Invalid: {reason}")
                # Ask for revision
                self.messages.append({
                    "role": "user",
                    "content": f"This plan has issues: {reason}. Revise."
                })

        return None

def main():
    planner = RobotTaskPlanner()
    goal = "Pick up the red cube and place it on the table"
    plan = planner.execute_planning_loop(goal)
    if plan:
        print(f"\nFinal Plan:\n{plan}")

if __name__ == '__main__':
    main()
```

### Step 2: Test Your Planner

```bash
python3 task_planner.py
```

### Expected Output

```
[Attempt 1]
Plan: 1. Detect red cube location
      2. Navigate to cube
      3. Approach cube with gripper
      4. Grasp cube
      5. Navigate to table
      6. Place cube on table

✓ Valid: Plan validated

Final Plan:
1. Detect red cube location
2. Navigate to cube
3. Approach cube with gripper
4. Grasp cube
5. Navigate to table
6. Place cube on table
```

---

## Section 8: Cost Optimization

### Token Counting

```python
from tiktoken import encoding_for_model

def count_tokens(text):
    enc = encoding_for_model("gpt-4")
    tokens = enc.encode(text)
    return len(tokens)

prompt = "Plan this task..."
tokens = count_tokens(prompt)
cost = (tokens / 1000) * 0.03  # Cost per 1K tokens
print(f"Estimated cost: ${cost}")
```

### Cost Reduction Strategies

1. **Use smaller models**: gpt-3.5-turbo vs. gpt-4
2. **Summarize context**: Keep message history short
3. **Local models**: Use Llama 2 or Mistral for free
4. **Caching**: Store frequently used prompts

---

## Section 9: Debugging & Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Plan contains impossible actions" | LLM hallucinated | Use stricter validation rules |
| "Cost too high" | Too many API calls | Implement caching or use local model |
| "Context too long" | Conversation history grows | Summarize old messages |
| "Validation always fails" | Rules too strict | Relax constraints or clarify task |
| "LLM ignores constraints" | Poor prompt design | Add explicit constraint examples |

---

## Section 10: Summary & Glossary

### Key Takeaways

- LLMs excel at task decomposition with good prompts
- Safety validation is essential for robots
- Multi-turn refinement handles ambiguity
- Cost optimization enables production deployments

### New Glossary Terms

- **Task Decomposition**: Breaking goals into actions
- **Plan Validation**: Checking safety and feasibility
- **Safety Constraint**: Rule that actions must follow
- **Hallucination**: LLM generating impossible actions
- **Multi-Turn Context**: Conversation history for refinement
- **Token Efficiency**: Minimizing API usage

---

## What's Next?

Chapter 4 integrates everything: voice input (Chapter 2), planning (this chapter), and perception/navigation (Modules 1–3) into a complete Vision-Language-Action system.

**Next Chapter**: [Chapter 4: Autonomous Humanoid Capstone](/docs/module4/chapter-4-autonomous-humanoid-capstone)
