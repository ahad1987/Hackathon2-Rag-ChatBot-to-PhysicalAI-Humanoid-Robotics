---
title: Chapter 2 - ROS 2 Nodes, Topics, and Services
description: Learn core ROS 2 communication patterns - nodes, topics, and services.
slug: /module1/chapter-2-ros2-basics
sidebar_position: 2
---

# Chapter 2: ROS 2 Nodes, Topics, and Services – Core Communication Patterns

## Learning Objectives

By the end of this chapter, you will:

- [ ] Understand what a node is and how nodes communicate
- [ ] Master the pub/sub (topics) pattern
- [ ] Understand the request/reply (services) pattern
- [ ] Create simple ROS 2 nodes using Python
- [ ] Know when to use topics vs. services

## Overview

In Chapter 1, you learned that ROS 2 is middleware for robots.

Now let's see HOW it works.

ROS 2 has three main concepts: nodes, topics, and services.

**Nodes** are small programs. Each node does one thing.

**Topics** are message channels. Nodes publish or subscribe to topics.

**Services** are for request/reply interactions. One node asks. Another answers.

Together, these three concepts make robot systems work.

## Understanding Nodes

A node is a computational unit. Think of it as a small program that runs continuously.

One node might read sensor data. Another processes that data. A third sends motor commands.

Each node is independent. Nodes communicate via topics and services.

Why split into multiple nodes? Because it keeps code simple. Each node focuses on one job. Node A doesn't need to know how Node B works.

## Understanding Topics (Pub/Sub)

Topics are message channels. Many nodes can subscribe to the same topic.

Think of a radio station. The station publishes (broadcasts). Listeners subscribe (tune in). Multiple listeners can tune to the same station.

With ROS 2 topics, publishers send data continuously. Subscribers receive the latest data.

**When to use topics?** For streams of data. Sensor readings. Motor commands. Status updates.

## Understanding Services (Request/Reply)

Services are different from topics. With services, one node sends a request. Another node sends back a reply.

Think of a phone call. You call (request). Someone answers (reply). The conversation is one-way then another-way, not continuous.

**When to use services?** For one-time requests. "Start the robot." "Is the battery low?" "Calculate the path."

## Real-World Example

A humanoid robot arm picking up an object:

- **Sensor node** publishes camera images (topic)
- **Vision node** subscribes to images, publishes detected objects (topic)
- **Planning node** requests a grasp plan from the planning service (service)
- **Control node** publishes motor commands (topic)

All nodes work together. ROS 2 routes the messages automatically.

## Coding Example 1: Create a Publisher Node

This node publishes sensor data continuously.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        self.publisher_ = self.create_publisher(Float32, 'sensor_data', 10)
        self.timer = self.create_timer(1.0, self.publish_data)
        self.get_logger().info('Sensor node started')

    def publish_data(self):
        msg = Float32()
        msg.data = 42.5  # Simulated sensor reading
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Expected output**: "Published: 42.5" every second

## Coding Example 2: Create a Subscriber Node

This node listens to sensor data.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class ListenerNode(Node):
    def __init__(self):
        super().__init__('listener_node')
        self.subscription = self.create_subscription(
            Float32, 'sensor_data', self.callback, 10)
        self.get_logger().info('Listener node started')

    def callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = ListenerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Expected output**: "Received: 42.5" every second (when running with the publisher)

## Key Takeaways

- [ ] Nodes are small programs that do one task each
- [ ] Topics are for continuous data streams (publish/subscribe pattern)
- [ ] Services are for one-time requests and replies
- [ ] Multiple nodes can communicate through ROS 2 automatically
- [ ] Understanding nodes and topics is essential for robot programming

## Next Chapter

Ready to write AI code that controls robots? [Chapter 3: Bridging Python Agents to ROS Controllers](./chapter-3-rclpy-bridge.md)

## Glossary

**Node**: A computational unit in ROS 2; each node performs one task.

**Topic**: A named channel for publishing and subscribing to messages (pub/sub pattern).

**Publisher**: A node that sends messages to a topic.

**Subscriber**: A node that receives messages from a topic.

**Service**: A ROS 2 communication pattern for request/reply interactions.

**Message**: Data sent between nodes; for example, sensor readings.

## Troubleshooting

**Q: My subscriber node doesn't receive messages?**

A: Make sure the publisher node is running first. Subscribers won't receive past messages, only new ones.

**Q: How do I see what topics are available?**

A: Run `ros2 topic list` in your terminal. You'll see all active topics.

**Q: What's the difference between topics and services?**

A: Topics are for continuous streams (like a radio station). Services are for one-time requests (like a phone call).
