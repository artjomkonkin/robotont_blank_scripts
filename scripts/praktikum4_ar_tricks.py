#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker
from math import atan2, sqrt
import tf
import numpy as np

last_heartbeat = 0

MAX_X_SPEED = 0.5
MAX_Y_SPEED = 0.5
MAX_Z_SPEED = 2


# IMPLEMENT THESE FUNCTIONS OR COPY FROM LAST TASK

# TASK 1


def keep_distance(x, y, z, roll, pitch, yaw, twist):

    return twist

# TASK 2


def keep_center(x, y, z, roll, pitch, yaw, twist):

    return twist

# TASK 3


def turn_towards_ar(x, y, z, roll, pitch, yaw, twist):

    return twist


def callback(data):
    global marker, last_heartbeat
    if len(data.markers) > 0:
        marker = data.markers[0]
        last_heartbeat = rospy.get_time()


def timer_callback(event):
    global last_heartbeat, marker
    if (rospy.get_time() - last_heartbeat) >= 1:
        marker = AlvarMarker()
        marker.id = -1


def ar_demo():

    # Initialize this ROS node
    rospy.init_node('ar_demo', anonymous=True)
    global marker
    # Create publisher for command velocity
    global cmd_vel_pub
    cmd_vel_pub = rospy.Publisher('/robotont/cmd_vel', Twist, queue_size=1)
    # initialize heartbeat
    global last_heartbeat
    last_heartbeat = rospy.get_time()
    # Set up subscriber for /ar_pose_marker
    rospy.loginfo("Subscribing to /ar_pose_marker")
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
    # Register heartbeat timer
    t = rospy.Timer(rospy.Duration(0.1), timer_callback)
    marker = AlvarMarker()
    marker.id = -1
    step = 0

    while(not rospy.is_shutdown()):

        #rospy.loginfo(rospy.get_caller_id() + " I heard %s", marker)
        x = marker.pose.pose.position.x
        y = marker.pose.pose.position.y
        z = marker.pose.pose.position.z
        twist_msg = Twist()
        angle = atan2(y, x)
        rospy.loginfo("Marker ID: %s", marker.id)
        rospy.loginfo("Marker: X %s Y %s Z %s", x, y, z)
        rospy.loginfo("Direction from camera: %s", angle)
        quaternion = (
            marker.pose.pose.orientation.x,
            marker.pose.pose.orientation.y,
            marker.pose.pose.orientation.z,
            marker.pose.pose.orientation.w)
        euler = tf.transformations.euler_from_quaternion(quaternion)
        roll = euler[0]
        pitch = euler[1]
        yaw = euler[2]
        rospy.loginfo("RPY: %s %s %s", roll, pitch, yaw)
        # YOUR CODE HERE

        if marker.id == 5:
           
            for i in range (0,4):
                for i in range(0,70):
                    twist_msg.linear.x = 0.2
                    twist_msg.linear.y = 0
                    twist_msg.angular.z = 0
                    cmd_vel_pub.publish(twist_msg)
                    rospy.sleep(0.05)

                for i in range(0,60):
                     twist_msg.linear.x = 0
                     twist_msg.linear.y = 0
                     twist_msg.angular.z = 1
                     cmd_vel_pub.publish(twist_msg)
                     rospy.sleep(0.05)

        if marker.id == 1:
            if x > 0.5:
                twist_msg.linear.x = 0.2
                twist_msg.linear.y = 0
                twist_msg.angular.z = 0
                cmd_vel_pub.publish(twist_msg)
                rospy.sleep(0.05)

            else:
                twist_msg.linear.x = -0.2
                twist_msg.linear.y = 0
                twist_msg.angular.z = 0
                cmd_vel_pub.publish(twist_msg)
                rospy.sleep(0.05)

        # YOUR CODE HERE END
        # limiting
        twist_msg.linear.x = min(twist_msg.linear.x, MAX_X_SPEED) if twist_msg.linear.x > 0 else max(
            twist_msg.linear.x, -MAX_X_SPEED)
        twist_msg.linear.y = min(twist_msg.linear.y, MAX_Y_SPEED) if twist_msg.linear.y > 0 else max(
            twist_msg.linear.y, -MAX_Y_SPEED)
        twist_msg.angular.z = min(twist_msg.angular.z, MAX_Z_SPEED) if twist_msg.angular.z > 0 else max(
            twist_msg.angular.z, -MAX_Z_SPEED)
        cmd_vel_pub.publish(twist_msg)
        rospy.sleep(0.05)


if __name__ == '__main__':
    try:
        ar_demo()
    except rospy.ROSInterruptException:
        pass
