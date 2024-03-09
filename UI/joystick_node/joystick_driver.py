#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Twist

class JoyToTwist:
    def __init__(self):
        # Initialize the node
        rospy.init_node('joy_to_twist_node')

        # Create a publisher for the /cmd_vel topic
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Create a subscriber for the /joy topic
        rospy.Subscriber('/joy', Joy, self.joystick_callback)

    def joystick_callback(self, data):
        # Instantiate a Twist message
        twist = Twist()

        # These indices might need adjustment depending on your joystick
        twist.linear.x = (data.buttons[7] - data.buttons[6]) * 0.5  # Scale as necessary
        twist.angular.z = data.axes[0] * (-0.5)  # Scale as necessary

        # Publish the Twist message to the /cmd_vel topic
        self.velocity_publisher.publish(twist)
        rospy.loginfo("Published velocity command: [%0.2f, %0.2f]" % (twist.linear.x, twist.angular.z))

if __name__ == '__main__':
    try:
        joy_to_twist = JoyToTwist()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
