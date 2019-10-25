#!/usr/bin/env python
import pdb
import time
import rospy
import os
from rospy.core import logdebug
import numpy as np
from numpy import pi
from math import floor

from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Pose, Twist

from CalXY import CalXY
from get_robot_pose import getPose
from tf.transformations import euler_from_quaternion
import matplotlib.pyplot as plt

#*************** CONSTANTS ******************#
BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84
# WAFFLE_MAX_LIN_VEL = 0.26
# WAFFLE_MAX_ANG_VEL = 1.82
# LIN_VEL_STEP_SIZE = 0.01
# ANG_VEL_STEP_SIZE = 0.1

# BURGER_MAX_LIN_VEL = 100
# BURGER_MAX_ANG_VEL = 100

class turtlebot():

    def __init__(self):
        #Creating our publisher and subscriber
        self.pose = Pose()
        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('gazebo/model_states', ModelStates, self.callback)
        self.rate = rospy.Rate(10)
        # rospy.spin()

    #Callback function implementing the pose value received
    def callback(self, data):
        self.pose = data.pose[1]
        self.pose.position.x = round(self.pose.position.x, 4)
        self.pose.position.y = round(self.pose.position.y, 4)

    # **************** HELPER FUNCTIONS ******************* #
    def constrain(self, input, low, high):
        if input < low:
          input = low
        elif input > high:
          input = high
        else:
          input = input
        return input

    def linearVelocity(self, v):
        if turtlebot3_model == "burger":
          v = constrain(v, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
        elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
          v = constrain(v, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
        else:
          v = constrain(v, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
        return v

    def angularVelocity(self, w):
        if turtlebot3_model == "burger":
          w = constrain(w, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
        elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
          w = constrain(w, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
        else:
          w = constrain(w, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
        return w

    def getTwist(self, v, w):
        v = self.constrain(v, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
        w = self.constrain(w, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
        twist = Twist()
        twist.linear.x = v
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = w
        return twist

    # ***************** ONLINE TRACKING ALGORITHM ******************* #
    def setParameters(self):
        L = .16 # length of robot
        # samplen = 100
        # T_con = 1000
        T_sim = 30 # total amount of time (seconds)
        dt = 0.3 # time it takes to sample
        print("Parameters Set")
        return L, T_sim, dt

    def setPath(self, T_sim, dt):
        # total number of samples
        N = int(round(T_sim/dt))
        N_sim = int(floor(1.8*N))
                
        # Desired Reference Path (circle)
        path = np.linspace(0,3*pi,N_sim)
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

        # For plotting purposes only
        # fig = plt.figure()
        x_idx = []
        z_idx = []
        x_r_idx = []
        z_r_idx = []

        while (idx < N) and (not rospy.core.is_shutdown()):
            now = rospy.get_rostime()
            x[idx] = self.pose.position.x
            z[idx] = self.pose.position.y
            qw = self.pose.orientation.w
            qx = self.pose.orientation.x
            qy = self.pose.orientation.y
            qz = self.pose.orientation.z
            (roll, pitch, yaw) = euler_from_quaternion((qx, qy, qz, qw))
            theta[idx] = yaw

            # DEBUGGING
            # print(x[idx])
            # print(self.pose)
            # print "x: ", x[idx]
            # print "z: ", z[idx]
            # print "x_r: ", x_r[idx]
            # print "z_r: ", z_r[idx]
            # print "theta: ", theta[idx]
            # x_idx.append(x[idx])
            # z_idx.append(z[idx])
            # x_r_idx.append(x_r[idx])
            # z_r_idx.append(z_r[idx])
            # plt.scatter(x_idx, z_idx)
            # plt.scatter(x_r_idx, z_r_idx)
            # plt.pause(0.001)
            # pdb.set_trace()
            # print(x[idx] - x_r[idx])
            # print "theta: ", yaw


            # **** Calculate velocity for the next time step **** #
            v,w,x_ol,y_ol = CalXY(dt, x_r, z_r, x[idx], z[idx], theta[idx], idx) 
            # print "linear velocity = ", v
            # print "angular velocity = ", w
            # print("linear velocity = %d", v)
            # print("angular velocity = %d", w)

            # **** Publish Velocity **** #
            self.publishTwist(0,w)
            time.sleep(dt)
            self.publishTwist(v,0)
            time.sleep(dt)
            self.publishTwist(0,0)
            # self.publishTwist(v,w)
            # self.rate.sleep()
            # print((x[idx] - x[idx-1]) / 0.1)
            idx = idx + 1
            # print(idx)

        # plt.show()

        # **** Stop Velocity **** #
        self.stopTwist()

        # **** Plotting **** #
        fig = plt.figure()
        plt.plot(x,z)
        plt.plot(x_r,z_r)
        plt.plot(x_ol,y_ol)
        # for i in range(len(x)):
        #     x_idx.append(x[i])
        #     z_idx.append(z[i])
        #     x_r_idx.append(x_r[i])
        #     z_r_idx.append(z_r[i])
        #     plt.scatter(x_idx, z_idx)
        #     plt.scatter(x_r_idx, z_r_idx)
        #     plt.pause(0.0001)
        plt.show()

    #**************** Publish *******************#
    def publishTwist(self, v, w):
        vel_msg = self.getTwist(v,w)
        # print(vel_msg)
        self.velocity_publisher.publish(vel_msg)

    def stopTwist(self):
        vel_msg = self.getTwist(0,0)
        self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    rospy.init_node('turtlebot_controller', anonymous=True)
    x = turtlebot()
    # def spin():
    """
    Blocks until ROS node is shutdown. Yields activity to other threads.
    @raise ROSInitException: if node is not in a properly initialized state
    """
    if not rospy.core.is_initialized():
        raise rospy.exceptions.ROSInitException("client code must call rospy.init_node() first")
    logdebug("node[%s, %s] entering spin(), pid[%s]", rospy.core.get_caller_id(), rospy.core.get_node_uri(), os.getpid())        
    try:
        while not rospy.core.is_shutdown():
            x.onlineTracking()
            rospy.core.signal_shutdown("tracking ended")
    except KeyboardInterrupt:
        logdebug("keyboard interrupt, shutting down")
        rospy.core.signal_shutdown('keyboard interrupt')