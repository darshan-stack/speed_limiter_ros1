cmake_minimum_required(VERSION 3.0.2)
project(speed_zone_limiter)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  nav_msgs
  std_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(
  PROGRAMS
    scripts/speed_zone_limiter.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

