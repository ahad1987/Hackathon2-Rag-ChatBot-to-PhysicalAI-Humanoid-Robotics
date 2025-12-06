---
title: AI & Robotics Connection
description: How AI and robotics work together to create intelligent physical systems.
slug: /foundations/ai-robotics-connection
sidebar_position: 1
---

# How AI and Robotics Connect

AI and robotics are two distinct fields that combine to create Physical AI.

## Robotics: The Hardware

Robotics focuses on the **physical machine**:
- Motors and actuators that move
- Sensors that gather data
- Mechanical structures (arms, wheels, grippers)
- Low-level control systems that execute commands

Think of robotics as the **body**.

## AI: The Intelligence

AI focuses on **decision-making and learning**:
- Computer vision to understand images
- Natural language processing to understand speech
- Machine learning to recognize patterns
- Planning algorithms to decide what to do next

Think of AI as the **brain**.

## When They Connect

A robot becomes intelligent when:

1. **Sensors feed data to AI**: Camera images → AI processes them
2. **AI makes decisions**: "I see an object I should pick up"
3. **Decisions become actions**: Motor commands execute the grasp

Example: A robot sees a coffee mug (robotics + sensors), recognizes it using AI (computer vision), and decides to pick it up (AI reasoning), then commands its arm to grasp it (robotics + motors).

## The Physical AI Loop

```
Sense → Think → Act → Learn
 ↑                      ↓
 └──────────────────────┘
```

1. **Sense**: Cameras and sensors collect data
2. **Think**: AI processes data and makes decisions
3. **Act**: Robots execute commands in the real world
4. **Learn**: Systems improve from experience

This loop repeats thousands of times per second.

## Why Separate Them?

Separating AI from robotics allows:
- Roboticists to focus on mechanical design and control
- AI researchers to focus on learning algorithms
- Middleware (like ROS 2) to connect them cleanly

---

**Next:** [Hardware Overview](./hardware-overview.md)
