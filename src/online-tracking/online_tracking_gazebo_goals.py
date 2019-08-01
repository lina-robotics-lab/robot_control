#!/usr/bin/env python
import time
import os
from rospy.core import logdebug

import numpy as np
from numpy import pi
from math import floor

import rospy
import actionlib
from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

from CalPos import CalPos
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import matplotlib.pyplot as plt


#*************** CONSTANTS ******************#
BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84
# WAFFLE_MAX_LIN_VEL = 0.26
# WAFFLE_MAX_ANG_VEL = 1.82
# LIN_VEL_STEP_SIZE = 0.01
# ANG_VEL_STEP_SIZE = 0.1

class online_tracking_client():

    def __init__(self):
        #Creating our publisher and subscriber
        self.goal_number = 0
        self.goal = MoveBaseGoal()
        # self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('gazebo/model_states', ModelStates, self.callback)
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        self.rate = rospy.Rate(1)
        # rospy.spin()

    def callback(self, pose_with_cov_stamped):    
        self.pose = pose_with_cov_stamped.pose.pose
        # print(robot_pose)
        # rospy.loginfo(pose)
        # poseAMCL = np.zeros(7)
        # poseAMCL[0] = pose.position.x
        # poseAMCL[1] = pose.position.y
        # poseAMCL[2] = pose.position.z
        # poseAMCL[3] = pose.orientation.w
        # poseAMCL[4] = pose.orientation.x
        # poseAMCL[5] = pose.orientation.y
        # poseAMCL[6] = pose.orientation.z
        # rospy.loginfo(poseAMCL)

    def sendGoal(self, x, y, theta):

        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.goal.target_pose.pose.position.x = x
        self.goal.target_pose.pose.position.y = y
        self.goal.target_pose.pose.position.z = 0
        quaternion = quaternion_from_euler(0, 0, theta)
        self.goal.target_pose.pose.orientation.w = quaternion[3]
        self.goal.target_pose.pose.orientation.x = quaternion[0]
        self.goal.target_pose.pose.orientation.y = quaternion[1]
        self.goal.target_pose.pose.orientation.z = quaternion[2]

        self.client.send_goal(self.goal)
        self.goal_number += 1
        self.client.wait_for_result()
        return self.client.get_result()

        # ***************** ONLINE TRACKING ALGORITHM ******************* #
    def setParameters(self):
        L = .16 # length of robot
        # samplen = 100
        # T_con = 1000
        T_sim = 30 # total amount of time (seconds)
        dt = 1 # time it takes to sample
        print("Parameters Set")
        return L, T_sim, dt

    def setPath(self, T_sim, dt):
        # total number of samples
        N = int(round(T_sim/dt))
        N_sim = int(floor(2*N))
                
        # Desired Reference Path (circle)
        path = np.linspace(0,4*pi,N_sim)
        radius = 1
        x_r = radius * np.sin(path)
        z_r = - radius * np.cos(path) + radius
        # path =  np.linspace(0,30*0.16,N_sim)
        # x_r = path
        # z_r = path 
        # xdot_r = np.diff(x_r)
        # zdot_r = np.diff(z_r)
        # theta_r = np.arctan2(zdot_r, xdot_r)
        # theta_r = np.insert(theta_r, 0, pi/2.)
        # w_r = np.diff(theta_r)
        # v_r = np.sqrt(xdot_r**2 + zdot_r**2)

        # initialize arrays
        # x = np.zeros(N)
        # z = np.zeros(N)
        # theta = np.zeros(N)           
        print("Path Set")
        return x_r, z_r, N

    def onlineTracking(self):
        L, T_sim, dt = self.setParameters()
        x_r, z_r, N = self.setPath(T_sim, dt)

        # initialize arrays 
        x = np.zeros(N)
        z = np.zeros(N)
        theta = np.zeros(N) 
        idx = 1

        while (idx < N) and (not rospy.core.is_shutdown()):
            # print(self.pose)
            now = rospy.get_rostime()
            x[idx] = self.pose.position.x
            z[idx] = self.pose.position.y
            # print(x[idx])
            # print "x_r: ", x_r[idx]
            # print "z_r: ", z_r[idx]
            # print(x[idx] - x_r[idx])
            qw = self.pose.orientation.w
            qx = self.pose.orientation.x
            qy = self.pose.orientation.y
            qz = self.pose.orientation.z
            (roll, pitch, yaw) = euler_from_quaternion((qx, qy, qz, qw))
            theta[idx] = yaw
            # print "theta: ", yaw


            # **** Calculate velocity for the next time step **** #
            x_goal,z_goal,theta_goal = CalPos(dt, x_r, z_r, x[idx], z[idx], theta[idx], idx) 

            # **** Publish Velocity **** #
            self.sendGoal(x_goal, z_goal, theta_goal)
            self.rate.sleep()
            
        fig = plt.figure()
        plt.plot(x,z)
        plt.plot(x_r,z_r)
        plt.show()

if __name__ == '__main__':
    try:
        rospy.init_node('move_base_client')
        x = online_tracking_client()
        result = x.onlineTracking()
        if result:
            rospy.loginfo("great job")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation Test Finished")


