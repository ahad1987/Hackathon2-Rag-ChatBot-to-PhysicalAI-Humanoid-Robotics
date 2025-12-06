---
title: Chapter 4 - URDF (Robot Description Format)
description: Define robot structure, joints, and links using URDF XML files.
slug: /module1/chapter-4-urdf
sidebar_position: 4
---

# Chapter 4: URDF (Robot Description Format)

## Learning Objectives

By the end of this chapter, you will:

- [ ] Understand what URDF is and why robots need it
- [ ] Learn the structure of a URDF file
- [ ] Create a simple robot description
- [ ] Visualize robots using URDF
- [ ] Understand links, joints, and frames

## Overview

How does ROS 2 know what your robot looks like?

How does it calculate if a move is possible? How does it know if something will collide?

The answer: **URDF** (Unified Robot Description Format).

URDF is an XML file that describes your robot's structure.

It defines:
- **Links**: Physical parts (body, arm, wheel, gripper)
- **Joints**: Connections between links (hinge, slide, fixed)
- **Coordinate frames**: Where each part is in 3D space
- **Mass and inertia**: Physics properties for simulation

ROS 2 tools read URDF files to understand your robot.

## Understanding Links

A link is a rigid body part.

Examples:
- Robot base (the chassis)
- Arm segments (upper arm, forearm)
- End effector (gripper or tool)
- Wheel

Each link has:
- **Name**: Unique identifier
- **Mass**: Weight (for physics)
- **Geometry**: Shape for visualization and collision detection
- **Inertia**: Rotation properties

## Understanding Joints

A joint connects two links and defines movement.

**Types**:
- **Fixed**: No movement (bolted together)
- **Revolute**: Rotates around an axis (like a hinge)
- **Prismatic**: Slides along an axis (like a piston)
- **Continuous**: Rotates infinitely (like a wheel)

Each joint has:
- **Name**: Unique identifier
- **Type**: How it moves
- **Parent link**: The link it's attached to
- **Child link**: The link it controls
- **Axis**: Direction of movement
- **Limits**: Min/max angles or distances

## Real-World Example

A simple robot arm with 3 joints:

```
Base (link)
  ↓ Fixed joint
Shoulder (link)
  ↓ Revolute joint (rotates up/down)
Upper arm (link)
  ↓ Revolute joint (rotates)
Forearm (link)
  ↓ Revolute joint (rotates)
Hand (link)
```

Each joint's movement changes the arm's position and grip location.

## Coding Example 1: Minimal URDF

Here's a simple robot with one rotating joint.

```xml
<?xml version="1.0"?>
<robot name="simple_arm">
  <!-- Base link -->
  <link name="base_link">
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.1 0.1 0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
  </link>

  <!-- Shoulder joint -->
  <joint name="shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="upper_arm"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="3.14" effort="10" velocity="1"/>
  </joint>

  <!-- Upper arm link -->
  <link name="upper_arm">
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
    <visual>
      <geometry>
        <cylinder radius="0.02" length="0.3"/>
      </geometry>
      <origin xyz="0 0 0.15"/>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
  </link>
</robot>
```

This describes a base with a rotating arm attached. ROS 2 uses this to simulate and visualize the robot.

## Coding Example 2: URDF in Python

Load and inspect a URDF file in ROS 2.

```python
import rclpy
from rclpy.node import Node
from urdf_parser_py.urdf import URDF

class URDFInspector(Node):
    def __init__(self):
        super().__init__('urdf_inspector')

        # Load URDF from parameter
        urdf_path = '/path/to/robot.urdf'
        robot = URDF.from_xml_file(urdf_path)

        # Print robot structure
        self.get_logger().info(f'Robot name: {robot.name}')
        self.get_logger().info(f'Links: {len(robot.links)}')
        self.get_logger().info(f'Joints: {len(robot.joints)}')

        # List all joints and their limits
        for joint in robot.joints:
            if hasattr(joint, 'limit'):
                self.get_logger().info(
                    f'{joint.name}: {joint.limit.lower:.2f} to '
                    f'{joint.limit.upper:.2f}')

def main(args=None):
    rclpy.init(args=args)
    inspector = URDFInspector()
    rclpy.spin(inspector)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Expected output**: Lists all links and joints with their motion limits.

## Key Takeaways

- [ ] URDF is an XML format that describes robot structure
- [ ] Links are rigid body parts; joints are connections
- [ ] ROS 2 uses URDF for visualization and collision checking
- [ ] URDF enables simulation before building physical robots
- [ ] Motion planning tools rely on accurate URDF descriptions

## Next Steps

You've completed Module 1! You now understand ROS 2 fundamentals.

Next you could:
- Build a physical robot using these concepts
- Explore advanced ROS 2 packages (MoveIt, Navigation2)
- Write AI agents that control robots
- Contribute to open-source robotics projects

## Glossary

**URDF**: XML format that describes robot structure, links, and joints.

**Link**: A rigid body part of the robot with mass, geometry, and inertia.

**Joint**: A connection between two links that defines allowed movement.

**Coordinate frame**: A 3D reference point and orientation for robot parts.

**Inertia**: Physical property that affects how a link rotates and accelerates.

**Revolute joint**: A joint that rotates around an axis (like a hinge).

**Prismatic joint**: A joint that slides along an axis (like a piston).

## Troubleshooting

**Q: How do I visualize a URDF file?**

A: Use RViz2 with: `ros2 run rviz2 rviz2`. Load the URDF and RViz will display your robot.

**Q: What if my URDF file has errors?**

A: Use `check_urdf /path/to/robot.urdf` to validate. It will report syntax errors.

**Q: Can I test a URDF without a real robot?**

A: Yes! Use Gazebo simulation with ROS 2. It loads URDF files and simulates physics.

---

**Congratulations!** You've completed Module 1: The Robotic Nervous System.

You now understand how robots communicate, from low-level node networks to high-level control architectures.

Ready to explore advanced topics? Continue with new modules or dive into open-source robotics projects.
