---
title: "Module 2: The Digital Twin (Gazebo & Unity)"
description: "Learn to build virtual robot simulations with physics and high-fidelity rendering."
slug: /module2
sidebar_position: 0
sidebar_label: "Module 2 Overview"
---

# Module 2: The Digital Twin (Gazebo & Unity)

## Welcome to the Digital Twin

In **Module 1**, you learned how to control robots using ROS 2—the communication framework that connects AI software to robot hardware.

In **Module 2**, you'll learn to **simulate robots virtually** before deploying code to expensive, physical hardware.

**A digital twin** is a virtual replica of a physical robot. You'll learn to build digital twins using:

- **Gazebo**: Open-source physics simulation (gravity, collisions, forces)
- **Unity**: Professional 3D rendering engine (realistic visuals)
- **ROS 2 Integration**: Your simulations connect directly to Module 1 code

---

## Why Digital Twins Matter

### 🛡️ **Safety First**
Test risky behaviors in simulation before physical deployment. No broken robots. No safety hazards.

### 💰 **Cost Savings**
A physical humanoid robot costs $100,000+. Simulate thousands of scenarios for free before hardware purchase.

### 🚀 **Faster Development**
Debug perception algorithms, control behaviors, and sensor configurations without waiting for hardware availability.

### 🧪 **Reproducible Testing**
Same simulation, same results, every time. Perfect for validating algorithms.

---

## Learning Path: Chapter-by-Chapter

### **Chapter 1: Physics Simulation and Environment Building**
Learn Gazebo basics. Build virtual environments with robots, obstacles, and gravity.

**What you'll build**: A Gazebo world with a robot that falls and collides realistically.

### **Chapter 2: Simulating Physics, Gravity, and Collisions**
Master physics parameters (gravity, mass, friction, damping). Predict how robots behave in realistic conditions.

**What you'll build**: A robot arm that picks up objects with realistic physics.

### **Chapter 3: High-Fidelity Rendering in Unity**
Create visually realistic robots in Unity. Connect them to ROS 2 commands for real-time control visualization.

**What you'll build**: A beautiful humanoid robot in Unity that responds to your ROS 2 control commands.

### **Chapter 4: Simulating Sensors (LiDAR, Depth Cameras, IMUs)**
Simulate realistic sensor data. Test perception algorithms before hardware deployment.

**What you'll build**: A complete robot with sensors producing realistic measurements.

---

## How This Module Connects to Module 1

Your **ROS 2 code from Module 1** will run against simulated robots in this module.

**Example**:
```python
# From Module 1: Python ROS 2 code to control a robot arm
import rclpy
from my_robot_interface import RobotArm

arm = RobotArm()
arm.move_to(x=0.5, y=0.3, z=0.8)  # Move arm to position
```

In **Module 2**, you'll:
1. Simulate a robot arm in Gazebo
2. Connect your Module 1 ROS 2 code to the simulated arm
3. Watch it move realistically in the simulation
4. Debug physics and perception without physical hardware

**Your code stays the same.** Only the robot changes (simulated → physical).

---

## What You'll Learn

✅ **Physics fundamentals**: gravity, mass, friction, collisions
✅ **Gazebo simulation**: building worlds, configuring physics, debugging behavior
✅ **3D rendering**: creating realistic robot visuals in Unity
✅ **Sensor simulation**: LiDAR, depth cameras, IMUs with realistic noise
✅ **ROS 2 integration**: controlling simulated robots with ROS 2 code
✅ **Sim-to-real transfer**: preparing simulation for physical robot deployment

---

## Prerequisites

**You should have completed**:
- Module 1: The Robotic Nervous System (ROS 2)
- Basic understanding of ROS 2 topics, services, and Python rclpy

**You do NOT need**:
- 3D modeling experience (Chapter 3 starts from scratch)
- Advanced physics knowledge (all concepts explained)
- Graphics programming knowledge

---

## Setup & Environment

All chapters use a **Docker environment** with:
- ROS 2 (latest)
- Gazebo (physics simulation)
- Python + rclpy (ROS 2 Python client library)
- Unity (for Chapter 3)

**One-command setup**:
```bash
docker run -it ros2-gazebo-unity:latest bash
```

See [Chapter setup instructions](#) for details.

---

## Time Commitment

**Per chapter**: 30-50 minutes (reading + hands-on exercises)

**Total module**: 3-4 hours to complete all 4 chapters

---

## Real-World Applications

- **Manufacturing**: Tesla and Boston Dynamics use Gazebo to test robot movements before deployment
- **Autonomous vehicles**: Self-driving cars simulate LiDAR, cameras, and collision detection
- **Space exploration**: NASA simulates rovers before sending them to Mars
- **Healthcare**: Surgical robots validate movements in simulation before patient contact

---

## Let's Begin

Ready to build your first digital twin?

→ **[Start with Chapter 1: Physics Simulation and Environment Building](/module2/chapter-1-environment)**

---

## Glossary & References

**Quick Glossary**:
- **Digital Twin**: Virtual replica of a physical robot
- **Gazebo**: Physics simulation engine
- **RViz**: ROS 2 visualization tool
- **ROS 2**: Robot Operating System (from Module 1)
- **Unity**: 3D rendering engine

See the [complete glossary](#) for all terms introduced in Modules 1 and 2.

---

**Happy simulating!** 🚀
