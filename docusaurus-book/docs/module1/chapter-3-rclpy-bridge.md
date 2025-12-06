---
title: Chapter 3 - Bridging Python Agents to ROS Controllers
description: Connect Python-based AI agents to ROS 2 robot controllers using rclpy.
slug: /module1/chapter-3-rclpy-bridge
sidebar_position: 3
---

# Chapter 3: Bridging Python Agents to ROS Controllers

## Learning Objectives

By the end of this chapter, you will:

- [ ] Understand how AI agents connect to robot controllers
- [ ] Write Python agents that send ROS 2 commands
- [ ] Create state managers for robot coordination
- [ ] Debug communication between agent and controller
- [ ] Know when to use services vs. topics in control loops

## Overview

In Chapter 2, you learned how nodes communicate through topics and services.

Now you'll see how an **AI agent** (decision-making code) communicates with a **robot controller** (action-executing code).

This is where intelligence meets action.

An AI agent might decide: "Pick up the object at location X."

The controller executes this decision by sending motor commands to the robot arm.

Both run as ROS 2 nodes. The agent publishes decisions. The controller subscribes and acts.

## Understanding the Agent-Controller Pattern

An agent makes decisions. A controller executes them.

**Agent responsibilities**:
- Process sensor data
- Run decision-making logic (machine learning, planning)
- Publish high-level commands

**Controller responsibilities**:
- Subscribe to commands from the agent
- Execute low-level motor control
- Monitor safety limits
- Report status back to the agent

## Real-World Example

A humanoid robot picks up a coffee mug:

1. **Vision agent** analyzes camera images, detects the mug, computes grasp point
2. **Agent publishes**: "Grasp position X, Y, Z"
3. **Arm controller** subscribes to grasp commands
4. **Controller runs motion planning**: Calculate joint angles needed
5. **Controller publishes**: Motor commands to arm actuators
6. **Sensors report back**: Gripper force, joint positions
7. **Loop repeats**: Agent monitors and adjusts if needed

All happens in milliseconds.

## Coding Example 1: Simple Decision Agent

This agent makes periodic decisions and sends commands.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class DecisionAgent(Node):
    def __init__(self):
        super().__init__('decision_agent')
        # Publish decisions to controller
        self.command_pub = self.create_publisher(
            String, 'robot_commands', 10)
        # Subscribe to sensor feedback
        self.sensor_sub = self.create_subscription(
            String, 'sensor_data', self.sensor_callback, 10)
        # Timer for decision-making loop
        self.timer = self.create_timer(1.0, self.make_decision)
        self.get_logger().info('Agent started')

    def sensor_callback(self, msg):
        self.get_logger().info(f'Sensor update: {msg.data}')

    def make_decision(self):
        # AI decision: randomly pick action
        actions = ['move_forward', 'turn_left', 'stop']
        decision = random.choice(actions)

        msg = String()
        msg.data = decision
        self.command_pub.publish(msg)
        self.get_logger().info(f'Decision: {decision}')

def main(args=None):
    rclpy.init(args=args)
    agent = DecisionAgent()
    rclpy.spin(agent)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Expected output**: "Decision: move_forward" every second (with random variation)

## Coding Example 2: Reactive Controller

This controller executes commands from the agent.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        # Subscribe to agent commands
        self.command_sub = self.create_subscription(
            String, 'robot_commands', self.execute_command, 10)
        # Publish status back to agent
        self.status_pub = self.create_publisher(
            String, 'controller_status', 10)
        self.get_logger().info('Controller ready')

    def execute_command(self, msg):
        command = msg.data
        self.get_logger().info(f'Executing: {command}')

        # Execute based on command
        if command == 'move_forward':
            self.move_forward()
        elif command == 'turn_left':
            self.turn_left()
        elif command == 'stop':
            self.stop()

        # Report completion
        status = String()
        status.data = f'Completed {command}'
        self.status_pub.publish(status)

    def move_forward(self):
        self.get_logger().info('Moving forward...')
        # Simulate motor control

    def turn_left(self):
        self.get_logger().info('Turning left...')
        # Simulate motor control

    def stop(self):
        self.get_logger().info('Stopped')
        # Simulate motor control

def main(args=None):
    rclpy.init(args=args)
    controller = RobotController()
    rclpy.spin(controller)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Expected output**: "Executing: move_forward" (matches agent decisions)

## Key Takeaways

- [ ] Agents make decisions; controllers execute them
- [ ] Agents and controllers are separate ROS 2 nodes
- [ ] Topics carry commands and feedback between them
- [ ] Separation of concerns keeps code modular
- [ ] Real robots follow this agent-controller pattern

## Next Chapter

Ready to describe robot structure? [Chapter 4: Robot Description Format (URDF)](./chapter-4-urdf.md)

## Glossary

**Agent**: A ROS 2 node that makes decisions based on sensor input and AI logic.

**Controller**: A ROS 2 node that executes commands and manages hardware actuators.

**Command**: A message published by an agent for the controller to execute.

**Feedback**: Status or sensor data published by the controller back to the agent.

**Reactive**: Responding immediately to incoming commands without planning ahead.

## Troubleshooting

**Q: My controller doesn't receive agent commands?**

A: Make sure the agent node is running and publishing to the correct topic. Use `ros2 topic echo robot_commands` to verify messages are flowing.

**Q: How do I ensure safe execution?**

A: Add safety checks in the controller. Verify commands are valid before executing. Use e-stops and timeout mechanisms.

**Q: Can the agent and controller run on different computers?**

A: Yes! ROS 2 handles distributed communication automatically. Just ensure they're on the same network.
