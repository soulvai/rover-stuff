#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray

class JoyToTwist:
	def __init__(self):
        # Initialize the node
		rospy.init_node('joy_to_twist_node')

        # Create a publisher for the /cmd_vel topic
		self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Create a publisher for the /joint_angles topic
		self.joint_publisher = rospy.Publisher('/joint_angles', Int32MultiArray, queue_size=10)

        # Create a subscriber for the /joy topic
		rospy.Subscriber('/joy', Joy, self.joystick_callback)
		# Controller variables
		self.SCALE = 0.5
		self.SCALING_FACTOR = 0.05

	def joystick_callback(self, data):
		# Instantiate a Twist message
		twist = Twist()
		arm_array = Int32MultiArray()

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

		twist.linear.x = (data.buttons[7] - data.buttons[6]) * self.SCALE * 255 # Scale as necessary
		if twist.linear.x > 1.0*255:
			twist.linear.x = 1.0*255
		if twist.linear.x < -1.0*255:
			twist.linear.x = -1.0*255
		
		twist.angular.z = data.axes[0] * (-self.SCALE) *255 # Scale as necessary
		if twist.angular.z > 1.0*255:
			twist.angular.z = 1.0*255
		if twist.angular.z < -1.0*255:
			twist.angular.z = -1.0*255

		# Control for base
		base = (data.buttons[4] * -1) + data.buttons[5]
		shoulder = int(data.axes[2])
		elbow = (data.buttons[2] * -1) + data.buttons[0]
		arm_array.data = [base, shoulder, elbow]


	# Publish the Twist message to the /cmd_vel topic
		self.velocity_publisher.publish(twist)
		self.joint_publisher.publish(arm_array)

if __name__ == '__main__':
    try:
        joy_to_twist = JoyToTwist()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
