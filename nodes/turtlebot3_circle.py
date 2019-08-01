#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import math

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

# WAFFLE_MAX_LIN_VEL = 0.26
# WAFFLE_MAX_ANG_VEL = 1.82

# LIN_VEL_STEP_SIZE = 0.01
# ANG_VEL_STEP_SIZE = 0.1

def constrain(input, low, high):
	if input < low:
		input = low
	elif input > high:
		input = high
	else:
		input = input
	return input

def linearVelocity(v):
	if turtlebot3_model == "burger":
		v = constrain(v, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
	elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
		v = constrain(v, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
	else:
		v = constrain(v, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
	return v

def angularVelocity(w):
	if turtlebot3_model == "burger":
		w = constrain(w, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
	elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
		w = constrain(w, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
	else:
		w = constrain(w, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
	return w

def getTwist(v, w):
	v = constrain(v, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
	w = constrain(w, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
	twist = Twist()
	twist.linear.x = v
	twist.linear.y = 0.0
	twist.linear.z = 0.0
	twist.angular.x = 0.0
	twist.angular.y = 0.0
	twist.angular.z = w
	return twist

def commandTwist(v, w):
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	rospy.init_node('controller', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		try:
			twist = getTwist(v, w)
			rospy.loginfo(twist)
			pub.publish(twist)
		except:
			print('error')

		rate.sleep()

if __name__=="__main__":
	try:
		commandTwist(.1, .6)
	except rospy.ROSInterruptionException:
		pass
    
    

