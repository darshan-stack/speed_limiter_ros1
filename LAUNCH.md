# Speed Zone Limiter - Launch Instructions

## ✅ Simple One-Command Launch (RECOMMENDED)

Run everything in ONE terminal:

```bash
multipass exec ros-dev -- bash -c 'source /opt/ros/noetic/setup.bash && source ~/catkin_ws/devel/setup.bash && export TURTLEBOT3_MODEL=burger && roslaunch speed_zone_limiter speed_zone_complete.launch'
```

This starts:
- ✅ TurtleBot3 Fake Node (simulation)
- ✅ Map Server
- ✅ AMCL Localization
- ✅ Move Base Navigation
- ✅ Speed Zone Limiter
- ✅ CMD Vel Relay

## 📺 RViz Visualization (for screen recording)

**Option 1: Connect via VNC**
```bash
vncviewer 10.75.192.100:5901
```
Password: `password`

Then in VNC terminal:
```bash
export DISPLAY=:1
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash  
export TURTLEBOT3_MODEL=burger
rosrun rviz rviz -d $(rospack find turtlebot3_navigation)/rviz/turtlebot3_navigation.rviz
```

**Option 2: Separate host terminal**
```bash
multipass exec ros-dev -- bash -c 'export DISPLAY=:1 && source /opt/ros/noetic/setup.bash && source ~/catkin_ws/devel/setup.bash && export TURTLEBOT3_MODEL=burger && rosrun rviz rviz -d $(rospack find turtlebot3_navigation)/rviz/turtlebot3_navigation.rviz'
```

## 🎯 Testing the Speed Limiter

In RViz:
1. Click "2D Nav Goal" button
2. Set goals outside the zone [X:1.2-3.4, Y:0.5-2.1] → Normal speed (0.22 m/s)
3. Set goals inside the zone → Limited speed (0.10 m/s)

Monitor velocity:
```bash
multipass exec ros-dev -- bash -c 'source /opt/ros/noetic/setup.bash && rostopic echo /cmd_vel'
```
