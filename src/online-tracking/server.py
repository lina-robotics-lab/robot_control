#!/usr/bin/env python
import rospy
import actionlib
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBase


class turtlebot_server():

	_feedback = # some navigation feedback thing
	_result = # some navigation result thing
	
	def __init__(self, name):
		self._action_name
		self._as = actionlib.SimpleActionServer(self._action_name, # navgiation msg thing, execute_callback = self.execute_callback, auto_start = False)
		self._as.start()) # delete that parentheses

	def execute_callback:
		r = rospy.Rate(1)
		success = True
		rospy.loginfo("Goal pose received")

		# start executing action
		#### NAVIGATE TO GOAL POSE ####

		# check that client has not cancelled goal
		if self._as.is_preempt_requested():
			rospy.loginfo("preempted")
			self._as.set_preempted()
			success = False

		self._as.publish_feedback(self._feedback)

		if success:
			self._result = self._feedback
			rospy.loginfo("reached goal")
			self._as.set_succeeded(self._result)





