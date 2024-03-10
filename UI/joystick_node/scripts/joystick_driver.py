#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoyToTwist:
    def __init__(self):
        # Initialize the node
        rospy.init_node('joy_to_twist_node')

        # Create a publisher for the /cmd_vel topic
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Create a subscriber for the /joy topic
        rospy.Subscriber('/joy', Joy, self.joystick_callback)

	# Controller variables
	self.SCALE = 0.5
	self.SCALING_FACTOR = 0.05

    def joystick_callback(self, data):
        # Instantiate a Twist message
        twist = Twist()

	# increase SCALE if UP BUTTON is pressed
	if data.axes[5] > 0.9 and self.SCALE < 1.0:
		self.SCALE = self.SCALE + self.SCALING_FACTOR

	# reduce SCALE if DOWN BUTTON is pressed
	if data.axes[5] < -0.9 and self.SCALE > 0.0:
		self.SCALE = self.SCALE - self.SCALING_FACTOR

	if self.SCALE > 1.0:
		self.SCALE = 1.0
	if self.SCALE < -1.0:
		self.SCALE = -1.0

        # These indices might need adjustment depending on your joystick

        twist.linear.x = (data.buttons[7] - data.buttons[6]) * self.SCALE  # Scale as necessary
	if twist.linear.x > 1.0:
		twist.linear.x = 1.0
	if twist.linear.x < -1.0:
		twist.linear.x = -1.0
        
	twist.angular.z = data.axes[0] * (-self.SCALE)  # Scale as necessary
	if twist.angular.z > 1.0:
		twist.angular.z = 1.0
	if twist.angular.z < -1.0:
		twist.angular.z = -1.0

        # Publish the Twist message to the /cmd_vel topic
        self.velocity_publisher.publish(twist)
        rospy.loginfo("Published velocity command: [%0.2f, %0.2f]" % (twist.linear.x, twist.angular.z))

if __name__ == '__main__':
    try:
        joy_to_twist = JoyToTwist()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
