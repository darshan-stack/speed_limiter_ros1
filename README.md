# ROS1 Speed Zone Limiter

Zone-based speed limiter for ROS1 Noetic navigation stack with TurtleBot3.

## Overview

This package implements a speed zone limiter that monitors robot position and caps velocity when the robot enters predefined polygonal zones. It integrates seamlessly with the ROS navigation stack.

## Features

- **Polygon-based zones**: Define speed zones using arbitrary polygons
- **Shapely integration**: Accurate point-in-polygon detection
- **Navigation integration**: Works with move_base and AMCL
- **Bidirectional limiting**: Handles both forward and backward motion
- **Graceful degradation**: Continues operating even without localization

## Repository Structure

```
catkin_ws/
├── LAUNCH.md                    # Launch instructions
└── src/
    └── speed_zone_limiter/
        ├── scripts/
        │   ├── speed_zone_limiter_node.py  # Main node (Shapely-based)
        │   └── speed_zone_limiter.py       # Alternative implementation
        ├── launch/
        │   ├── speed_zone_complete.launch  # Complete system launch
        │   ├── speed_zone_limiter.launch   # Individual component launch
        │   └── gazebo_headless.launch      # Headless Gazebo simulation
        ├── config/
        │   ├── zones.yaml                  # Zone configuration
        │   └── speed_zone.yaml             # Alternative config
        ├── CMakeLists.txt
        ├── package.xml
        └── README.md
```

## Requirements

- ROS Noetic (Ubuntu 20.04)
- TurtleBot3 packages
- Python 3
- Shapely library

## Installation

```bash
# Install dependencies
sudo apt install ros-noetic-turtlebot3 ros-noetic-turtlebot3-simulations
sudo apt install ros-noetic-navigation python3-pip
pip3 install shapely

# Clone repository
cd ~/catkin_ws/src
git clone https://github.com/darshan-stack/speed_limiter_ros1.git .

# Build
cd ~/catkin_ws
catkin_make

# Source workspace
source devel/setup.bash
```

## Configuration

Edit `config/zones.yaml` to define your speed zones:

```yaml
speed_zone_limiter:
  zone:
    name: loading_bay
    max_speed: 0.10          # m/s
    polygon:                 # [x0, y0, x1, y1, ...]
      - 1.2
      - 0.5
      - 3.4
      - 0.5
      - 3.4
      - 2.1
      - 1.2
      - 2.1
```

## Usage

### Quick Start (One Command)

```bash
export TURTLEBOT3_MODEL=burger
roslaunch speed_zone_limiter speed_zone_complete.launch
```

This launches:
- TurtleBot3 Fake Node (simulation)
- Map Server
- AMCL Localization
- Move Base Navigation
- Speed Zone Limiter
- CMD Vel Relay

### Individual Components

See `LAUNCH.md` for detailed launch instructions.

## How It Works

1. **Position Monitoring**: Subscribes to `/amcl_pose` for robot localization
2. **Velocity Interception**: Listens to `/cmd_vel_raw` from move_base
3. **Zone Detection**: Uses Shapely to check if robot is inside polygon
4. **Speed Limiting**: Caps linear velocity to `max_speed` when in zone
5. **Safe Publishing**: Outputs limited velocity to `/cmd_vel_safe`
6. **Relay**: Topic relay forwards `/cmd_vel_safe` → `/cmd_vel`

## Topics

- **Subscribed:**
  - `/amcl_pose` (geometry_msgs/PoseWithCovarianceStamped)
  - `/cmd_vel_raw` (geometry_msgs/Twist)

- **Published:**
  - `/cmd_vel_safe` (geometry_msgs/Twist)

## Parameters

- `zone/name` (string): Zone identifier
- `zone/max_speed` (double): Maximum speed in m/s
- `zone/polygon` (double array): Flat list of polygon vertices

## Testing

Use RViz to set navigation goals:
1. Start the complete launch file
2. Open RViz (shows map and robot)
3. Use "2D Nav Goal" to send robot to different locations
4. Monitor velocity with: `rostopic echo /cmd_vel`

**Expected behavior:**
- Outside zone: Normal speed (~0.22 m/s)
- Inside zone: Limited speed (0.10 m/s)

## License

MIT

## Author

Darshan - [GitHub](https://github.com/darshan-stack)

## References

- [TurtleBot3 Documentation](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
- [ROS Navigation Stack](http://wiki.ros.org/navigation)
- [Shapely Documentation](https://shapely.readthedocs.io/)
