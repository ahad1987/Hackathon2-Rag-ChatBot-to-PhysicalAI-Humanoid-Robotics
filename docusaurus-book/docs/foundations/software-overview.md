---
title: Software Overview
description: Software frameworks and tools that power physical AI systems.
slug: /foundations/software-overview
sidebar_position: 3
---

# Software Overview

Modern robots run sophisticated software stacks. Here's the landscape.

## Operating Systems

**Linux**:
- Industry standard for robots
- Open-source and free
- Excellent support for ROS 2
- Ubuntu is the preferred distribution

**Real-Time Linux**:
- Guarantees timing for critical control tasks
- Preempt-RT kernel modifications
- Used in safety-critical applications

**Windows/macOS**:
- Less common in robotics
- Good for development and simulation

## Middleware (ROS 2)

**ROS 2 (Robot Operating System 2)** is the central nervous system.

- Manages communication between robot components
- Provides standardized interfaces for sensors and actuators
- Enables code reuse across projects
- Supports distributed systems (multiple computers)

**Why ROS 2?**
- Industry standard used by thousands of robots worldwide
- Backed by Open Robotics (nonprofit organization)
- Mature ecosystem with extensive libraries
- Beginner-friendly documentation

We'll dive deep into ROS 2 starting in Module 1.

## AI Frameworks

**Machine Learning**:
- **TensorFlow**: General-purpose deep learning
- **PyTorch**: Research and production AI
- **JAX**: High-performance numerical computing

**Computer Vision**:
- **OpenCV**: Classical and modern vision algorithms
- **YOLO**: Real-time object detection
- **ROS 2 vision_opencv**: Integration with ROS 2

**Planning & Control**:
- **MoveIt**: Robotic arm motion planning
- **Navigation2**: Autonomous navigation and path planning

## Programming Languages

**Python**:
- Beginner-friendly
- Rapid development
- Excellent AI/ML libraries
- Used in this book (rclpy = ROS 2 Python)

**C++**:
- High performance
- Real-time control
- More complex syntax

**Both together**:
- Python for AI and high-level logic
- C++ for low-level control and performance

---

**Next:** [How to Learn - Hands-On Philosophy](../approach/hands-on-philosophy.md)
