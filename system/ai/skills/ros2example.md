# Skill: ROS2Example

## Purpose
Generates correct, tested, production-quality Python + rclpy code snippets that demonstrate ROS 2 concepts. All examples follow Module 1 patterns, are runnable in isolation, and include expected output.

## Usage Examples

### Example 1: Simple Subscriber Node
```python
import rclpy
from geometry_msgs.msg import Twist

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('velocity_listener')

    def callback(msg):
        print(f"Received velocity: linear.x={msg.linear.x}")

    sub = node.create_subscription(Twist, '/cmd_vel', callback, 10)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```

**Expected Output:**
```
Received velocity: linear.x=0.5
Received velocity: linear.x=0.25
```

**Common Error & Fix:**
- **Error:** "Topic '/cmd_vel' not available"
- **Fix:** Ensure another node is publishing to `/cmd_vel` (e.g., teleop node)

### Example 2: Service Server (Module 1 pattern)
```python
import rclpy
from example_interfaces.srv import AddTwoInts

def add_callback(request, response):
    response.sum = request.a + request.b
    return response

def main():
    rclpy.init()
    node = rclpy.create_node('add_two_ints_server')
    srv = node.create_service(AddTwoInts, 'add_two_ints', add_callback)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```

## Required Constraints

1. **Python 3.10+** — Use modern syntax
2. **rclpy only** — No rospy, no rosbag, no third-party abstractions
3. **Maximum 30 lines** — Keep examples bite-sized
4. **Runnable in isolation** — Learner can copy-paste directly
5. **Include expected output** — Show what they should see
6. **Follow Module 1 patterns** — node.create_node(), create_subscription(), etc.
7. **Add comments** — Explain non-obvious lines only

## Quality Check
- ✅ Is this runnable as-is?
- ✅ Does it match Module 1 conventions?
- ✅ Is the expected output realistic?
- ✅ Are common errors documented?

---

**Implementation Note:** CodeAgent validates all ROS2Example code before publishing.
