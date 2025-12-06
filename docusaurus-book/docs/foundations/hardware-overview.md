---
title: Hardware Overview
description: Key hardware components that make up physical AI systems and robots.
slug: /foundations/hardware-overview
sidebar_position: 2
---

# Hardware Overview

Physical AI systems combine specialized hardware components. Here's what you need to know.

## Sensors

Sensors gather data from the environment.

**Vision**:
- **Cameras**: RGB images for object detection, face recognition
- **Depth cameras**: Lidar or structured light for 3D maps
- **Thermal cameras**: Heat detection for night vision

**Touch**:
- **Pressure sensors**: Detect force and grip strength
- **Tactile arrays**: Sense surface texture and contact

**Movement**:
- **Accelerometers**: Detect motion and orientation
- **Gyroscopes**: Measure rotation
- **Encoders**: Track joint positions and speeds

**Other**:
- **Ultrasonic**: Measure distance to obstacles
- **IMU**: Inertial measurement (acceleration, rotation)

## Actuators

Actuators make the robot move.

**Motors**:
- **Servo motors**: Precise angular control (robot arms)
- **DC motors**: General-purpose motion
- **Stepper motors**: Controlled step increments
- **Brushless motors**: Efficient and quiet

**Grippers**:
- **Parallel grippers**: Two-finger grasp
- **Dexterous hands**: Five-finger manipulation
- **Soft grippers**: Delicate object handling

## Compute

The "brain" of the robot.

**CPUs**:
- **Single-board computers**: Jetson Nano, Raspberry Pi (edge AI)
- **Industrial computers**: High performance, robust
- **Cloud servers**: For heavy computation

**GPUs**:
- Accelerate machine learning and computer vision
- Essential for real-time AI processing

## Communication

How components talk to each other.

- **CAN bus**: Reliable, industrial standard
- **Ethernet**: Fast, widely supported
- **WiFi**: Wireless connectivity
- **ROS 2**: Software layer connecting everything

---

**Next:** [Software Overview](./software-overview.md)
