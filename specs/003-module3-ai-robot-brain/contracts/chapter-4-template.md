---
title: Chapter 4: Nav2 – Path Planning for Bipedal Humanoid Movement
description: Configure the ROS 2 Navigation Stack for autonomous path planning and obstacle avoidance on bipedal humanoid robots.
slug: chapter-4-nav2-path-planning
sidebar_position: 4
---

## Introduction

[Hook: How do autonomous robots navigate from point A to B safely?]

[Problem statement: Path planning is critical for autonomous movement]

[Learning objective: Configure Nav2 for bipedal humanoid path planning]

[Practical motivation: Complete the autonomous system (perception + planning + motion)]

**This chapter covers**:
- Path planning fundamentals
- Global and local planning algorithms
- Nav2 stack architecture
- Cost maps and obstacle representation
- Bipedal robot constraints
- Behavior trees for complex navigation
- Hands-on Nav2 configuration exercise

**Time estimate**: 50–60 minutes

---

## Path Planning Overview

[Section placeholder: Why path planning matters]

### The Navigation Problem

[Subsection: Planning collision-free routes in unknown environments]

### Global vs. Local Planning

[Subsection: Route finding vs. real-time steering]

### Integration with Perception

[Subsection: Using perception (Chapter 3) for localization]

**Key takeaway**: [One-sentence summary]

---

## Global Planning Algorithms

[Section placeholder: Computing routes from start to goal]

### Dijkstra's Algorithm

[Subsection: Optimal pathfinding with uniform costs]

### A* Search

[Subsection: Efficient heuristic-guided search]

```python
# [Code: A* pseudocode or implementation]
```

### Rapidly-Exploring Random Trees (RRT)

[Subsection: Sampling-based planning for complex spaces]

### RRT* and Other Variants

[Subsection: Improvements for optimality and efficiency]

### Algorithm Comparison

| Algorithm | Completeness | Optimality | Speed | Versatility |
|-----------|--------------|-----------|-------|-------------|
| Dijkstra | ✓ | ✓ | Medium | Low |
| A* | ✓ | ✓ | Fast | Medium |
| RRT | ✓ | ✗ | Fast | High |
| RRT* | ✓ | ✓ | Medium | High |

**Key takeaway**: [One-sentence summary]

---

## Local Planning Algorithms

[Section placeholder: Real-time steering and velocity control]

### Dynamic Window Approach (DWA)

[Subsection: Sampling-based velocity selection]

```python
# [Code: DWA velocity selection]
```

### Timed Elastic Band (TEB)

[Subsection: Trajectory optimization with time parameterization]

### Model Predictive Control (MPC)

[Subsection: Optimal control with prediction horizons]

### Algorithm Comparison

| Algorithm | Speed | Smoothness | Responsiveness |
|-----------|-------|-----------|----------------|
| DWA | ✓✓✓ | ✓✓ | ✓✓✓ |
| TEB | ✓✓ | ✓✓✓ | ✓✓ |
| MPC | ✓ | ✓✓✓ | ✓✓ |

**Key takeaway**: [One-sentence summary]

---

## Nav2 Architecture

[Section placeholder: Understanding the ROS 2 navigation stack]

### Stack Overview

[Subsection: Core components and design]

### Behavior Composition

[Subsection: Composing behaviors with behavior trees]

### ROS 2 Integration

[Subsection: Action servers, publishers, subscribers]

**Key takeaway**: [One-sentence summary]

---

## Cost Maps and Obstacle Representation

[Section placeholder: How robots represent the environment for planning]

### Occupancy Grid Maps

[Subsection: Probabilistic grid representation]

### Static Obstacles

[Subsection: Pre-mapped obstacles]

### Dynamic Obstacles

[Subsection: Moving people and objects]

### Inflation Layers

```python
# [Code: Inflation computation for safety margins]
```

### Cost Propagation

[Subsection: Spreading costs from obstacles]

**Key takeaway**: [One-sentence summary]

---

## Bipedal Robot Constraints

[Section placeholder: Adapting planning for legged robots]

### Footprint Configuration

[Subsection: Defining robot base shape for collision detection]

```yaml
# [YAML: Example footprint for humanoid robot]
```

### Step Height Limitations

[Subsection: Maximum stair/obstacle heights]

### Balance and Stability

[Subsection: Center of mass constraints]

### Velocity and Acceleration Limits

[Subsection: Legged robots have different dynamics than wheeled]

**Key takeaway**: [One-sentence summary]

---

## Global Path Planning Workflow

[Section placeholder: Computing routes end-to-end]

### Goal Reception

[Subsection: Accepting navigation goals]

### Path Computation

[Subsection: Running global planner algorithm]

### Collision Checking

[Subsection: Validating paths against obstacles]

### Smoothing

[Subsection: Improving path quality and efficiency]

**Key takeaway**: [One-sentence summary]

---

## Local Planning and Obstacle Avoidance

[Section placeholder: Real-time steering around obstacles]

### Real-Time Steering

[Subsection: Velocity control loop]

### Obstacle Avoidance

[Subsection: Reactive collision avoidance]

### Replanning Triggers

[Subsection: When to recompute global path]

### Failure Recovery

[Subsection: What to do when stuck]

**Key takeaway**: [One-sentence summary]

---

## Dynamic Obstacle Handling

[Section placeholder: Navigating around moving objects]

### Moving Object Tracking

[Subsection: Prediction of dynamic obstacles]

### Predictive Collision Avoidance

[Subsection: Planning with predicted trajectories]

### Social Navigation

[Subsection: Respecting human comfort and space]

### Crowd Interaction

[Subsection: Navigating through people]

**Key takeaway**: [One-sentence summary]

---

## Behavior Trees for Complex Navigation

[Section placeholder: Composing sophisticated navigation behaviors]

### Behavior Tree Fundamentals

[Subsection: Nodes, sequences, selectors]

### Common Navigation Behaviors

[Subsection: Follow path, avoid obstacles, recover]

### Composition Examples

```xml
<!-- [Behavior tree XML example] -->
```

### Debugging and Monitoring

[Subsection: Introspection tools for behavior trees]

**Key takeaway**: [One-sentence summary]

---

## Nav2 Setup and Configuration

[Section placeholder: Getting Nav2 running]

### Installation

```bash
# [Installation commands for Nav2]
```

### Basic Configuration Files

```yaml
# [Example nav2_params.yaml]
```

### Parameter Tuning

[Subsection: Key parameters for different robots]

### Visualization with RViz

```bash
# [RViz visualization setup]
```

**Key takeaway**: [One-sentence summary]

---

## Hands-On: Configure Nav2 for Humanoid

### What You'll Learn

Configure and test Nav2 for a bipedal humanoid robot.

### Prerequisites

- ROS 2 Humble (from Module 1)
- Nav2 stack installed
- Humanoid robot URDF with footprint definition
- Map or Gazebo simulation environment

### Step 1: Define Robot Footprint

```yaml
# [URDF/YAML: Humanoid robot footprint definition]
```

### Step 2: Create Nav2 Configuration

```yaml
# [nav2_params.yaml with A*, DWA configuration]
```

### Step 3: Generate Cost Map

```python
# [Code: Load map or create cost map from sensors]
```

### Step 4: Launch Nav2

```bash
# [Launch command for Nav2 with parameters]
```

### Step 5: Send Navigation Goal

```python
# [ROS 2 Python script to send goals via action client]
```

### Step 6: Test Obstacle Avoidance

[Add obstacles and verify avoidance behavior]

### Step 7: Measure Performance

```python
# [Code to measure planning time, path length, success rate]
```

**Expected output**:
```
Nav2 initialized
Global planner: A* algorithm ready
Local planner: DWA algorithm ready
Planning time: 0.3 seconds
Path length: 12.5 meters
Collision avoidance: Success (3/3 tests)
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Path planning too slow | Reduce map resolution, tune A* parameters |
| Robot gets stuck | Increase DWA forward simulation window, adjust inflation |
| Jerky movements | Reduce DWA scaling factors, increase replanning frequency |

### Challenge Extension

Implement a custom behavior tree that patrols multiple waypoints and avoids dynamic obstacles!

---

## Parameter Tuning and Debugging

[Section placeholder: Optimizing Nav2 performance]

### Common Tuning Parameters

| Parameter | Effect | Typical Range |
|-----------|--------|---------------|
| `costmap_resolution` | Map granularity | 0.01–0.1 m |
| `inflation_radius` | Safety margin | 0.3–1.0 m |
| `planner_timeout` | Max planning time | 1–5 seconds |
| `max_vel_x` | Max forward velocity | 0.5–2.0 m/s |
| `sim_time` | DWA lookahead | 1–3 seconds |

### Performance Profiling

[Subsection: Measuring planning time, memory usage]

### Logging and Visualization

[Subsection: RViz debugging, ROS logs]

### Troubleshooting Decision Trees

[Subsection: Systematic debugging approach]

**Key takeaway**: [One-sentence summary]

---

## Deployment to Real Robots

[Section placeholder: Moving from simulation to reality]

### Sensor Integration

[Subsection: Connecting LiDAR, cameras, IMU]

### Odometry and Localization

[Subsection: Using encoder odometry or VSLAM]

### Real-World Testing

[Subsection: Gradual deployment, safety considerations]

### Lessons from Sim-to-Real Transfer

[Subsection: Common surprises in real deployment]

**Key takeaway**: [One-sentence summary]

---

## Real-World Applications

### Boston Dynamics Spot: Complex Terrain Navigation

[Problem]: How does Spot navigate uneven, complex environments?

[Solution]: Using Nav2-like planning with legged locomotion constraints...

[Lesson]: Path planning must respect robot morphology and dynamics.

### Tesla Bot: Warehouse Autonomy

[Problem]: How does Tesla Bot navigate crowded warehouse environments?

[Solution]: Using prediction and social navigation to move safely around humans...

[Lesson]: Dynamic obstacle handling is essential for human environments.

### Humanoid Robot Deployment

[Problem]: How do humanoid robots plan and execute movement?

[Solution]: Using Nav2 configured for bipedal constraints and dynamics...

[Lesson]: Specialized planning improves performance on legged robots.

---

## Debugging and Troubleshooting

### Common Issues

#### Issue: "No path found"

**Cause**: Goal is unreachable, cost map blocked

**Solution**: Verify cost map, check goal location, increase inflation

#### Issue: "Oscillating around obstacles"

**Cause**: Local planner parameters not tuned

**Solution**: Increase DWA forward simulation, adjust cost weights

#### Issue: "Path is inefficient or jerky"

**Cause**: Planner parameters suboptimal for your robot

**Solution**: Tune cost weights, increase path smoothing iterations

### Performance Tips

- Monitor CPU and memory usage during navigation
- Test in simulation before real deployment
- Use RViz to visualize cost maps and paths
- Log trajectories for post-analysis

### Getting Help

- Check [Nav2 documentation](https://nav2.org/)
- Search [Nav2 GitHub issues](https://github.com/ros-planning/navigation2/)
- Ask on [ROS Discourse](https://discourse.ros.org/) with tag `module3-chapter-4`

---

## Summary

In this chapter, you learned:

- **Path Planning**: Computing collision-free routes from start to goal
- **Global Planning**: Algorithms like A* and RRT for route finding
- **Local Planning**: Real-time steering with obstacle avoidance
- **Nav2**: ROS 2's complete navigation stack
- **Bipedal Constraints**: Adapting planning for legged robots

**You can now**:

- [ ] Explain global and local path planning algorithms
- [ ] Configure Nav2 for your robot
- [ ] Set up cost maps and obstacle layers
- [ ] Handle dynamic obstacles and moving people
- [ ] Deploy autonomous navigation on real robots

**Next steps**: Module 3 complete! You can now combine:
- **Chapter 1**: Perception (seeing obstacles, people, objects)
- **Chapter 2**: Synthetic data (training models efficiently)
- **Chapter 3**: VSLAM (knowing where you are)
- **Chapter 4**: Nav2 (planning where to go)

→ **Building complete autonomous humanoid robots!**

**Glossary terms introduced**: Navigation, Global Planner, Local Planner, Cost Map, DWA, Bipedal Locomotion, Footprint, Nav2, Behavior Tree, Teleoperation (see Module 3 Glossary)

---

## Additional Resources

### Recommended Reading

- [Nav2: Towards Optimized Navigation over Autonomous Robots](https://ieeexplore.ieee.org/document/9288415) – Nav2 paper
- [The Dynamic Window Approach to Collision Avoidance](https://www.researchgate.net/publication/3824156_The_Dynamic_Window_Approach_to_Collision_Avoidance) – DWA original paper
- [Nav2 Documentation](https://nav2.org/)

### Code Examples Index

1. Robot URDF with footprint
2. Nav2 configuration parameters
3. A* pathfinding example
4. DWA velocity selection
5. Cost map creation
6. Behavior tree definition
7. Navigation goal action client
8. RViz visualization setup

### Next Steps

- **Experiment**: Test different planning algorithms and compare
- **Extend**: Implement custom behavior trees for complex missions
- **Optimize**: Profile and tune parameters for your robot
- **Deploy**: Deploy to real humanoid robot and iterate

---

## Module 3 Complete!

Congratulations on completing the AI-Robot Brain module! You've learned:

1. **Deep learning** for perception (Chapter 1)
2. **Synthetic data generation** to train models efficiently (Chapter 2)
3. **Visual SLAM** for real-time localization (Chapter 3)
4. **Path planning** for autonomous navigation (Chapter 4)

These four skills combine to enable **fully autonomous humanoid robots**. Now you can:

- Train perception models
- Simulate training data
- Deploy perception on real robots
- Plan and execute navigation
- Build end-to-end autonomous systems

**What's next?**
- Apply these skills to a real humanoid robot project
- Explore specialized topics (manipulation, dexterous hands, etc.)
- Contribute to open-source robotics projects
- Join the robotics community!

Happy building! 🤖
