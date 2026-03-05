#!/usr/bin/env python3

import math
from typing import List, Tuple, Optional

import rospy
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped


Point = Tuple[float, float]


class SpeedZoneLimiter(object):
  def __init__(self):
    self.node_name = rospy.get_name()

    zone_param_name = "~zone"
    if not rospy.has_param(zone_param_name):
      rospy.logerr("%s: required param '%s' is missing", self.node_name, zone_param_name)
      raise rospy.ROSInitException("zone configuration not found on parameter server")

    zone = rospy.get_param(zone_param_name)

    try:
      self.zone_name = str(zone.get("name", "unnamed_zone"))
      self.max_speed = float(zone["max_speed"])
      polygon_list = zone["polygon"]
      self.polygon: List[Point] = [(float(p[0]), float(p[1])) for p in polygon_list]
    except (KeyError, TypeError, ValueError) as exc:
      rospy.logerr("%s: invalid zone configuration: %s", self.node_name, exc)
      raise rospy.ROSInitException("invalid zone configuration") from exc

    if len(self.polygon) < 3:
      rospy.logerr("%s: polygon must have at least 3 vertices", self.node_name)
      raise rospy.ROSInitException("zone polygon too small")

    self.current_pose: Optional[Point] = None

    self.cmd_vel_sub = rospy.Subscriber(
      "/cmd_vel", Twist, self.cmd_vel_callback, queue_size=10
    )
    self.cmd_vel_pub = rospy.Publisher(
      "/cmd_vel_safe", Twist, queue_size=10
    )

    self.pose_sub = rospy.Subscriber(
      "/amcl_pose", PoseWithCovarianceStamped, self.pose_callback, queue_size=10
    )

    rospy.loginfo(
      "%s: initialized with zone '%s', max_speed=%.3f m/s, %d vertices",
      self.node_name,
      self.zone_name,
      self.max_speed,
      len(self.polygon),
    )

  def pose_callback(self, msg: PoseWithCovarianceStamped) -> None:
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    self.current_pose = (x, y)

  def cmd_vel_callback(self, msg: Twist) -> None:
    twist_out = Twist()
    twist_out.linear.x = msg.linear.x
    twist_out.linear.y = msg.linear.y
    twist_out.linear.z = msg.linear.z
    twist_out.angular.x = msg.angular.x
    twist_out.angular.y = msg.angular.y
    twist_out.angular.z = msg.angular.z

    if self.current_pose is None:
      self.cmd_vel_pub.publish(twist_out)
      return

    if self.is_inside_zone(self.current_pose):
      original_speed = twist_out.linear.x
      if original_speed > self.max_speed:
        twist_out.linear.x = self.max_speed
      elif original_speed < -self.max_speed:
        twist_out.linear.x = -self.max_speed

    self.cmd_vel_pub.publish(twist_out)

  def is_inside_zone(self, point: Point) -> bool:
    x, y = point
    inside = False
    n = len(self.polygon)

    for i in range(n):
      x1, y1 = self.polygon[i]
      x2, y2 = self.polygon[(i + 1) % n]

      intersects = ((y1 > y) != (y2 > y)) and (
        x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1
      )
      if intersects:
        inside = not inside

    return inside


def main():
  rospy.init_node("speed_zone_limiter", anonymous=False)
  try:
    SpeedZoneLimiter()
    rospy.spin()
  except rospy.ROSInitException:
    pass


if __name__ == "__main__":
  main()

