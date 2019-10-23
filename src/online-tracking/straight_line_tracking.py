#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import rospy
import os

from rospy.core import logdebug
import numpy as np
from numpy import pi, sin, cos
from math import floor

from std_msgs.msg import String
from geometry_msgs.msg import Pose, PoseStamped, PoseWithCovarianceStamped, Twist
from nav_msgs.msg import Odometry
# from geometry_msgs.msg import Pose, Twist

from CalXY import CalXY
from get_robot_pose import getPose
from tf.transformations import euler_from_quaternion
import matplotlib.pyplot as plt

#*************** CONSTANTS ******************#
BURGER_MAX_LIN_VEL = 0.21
BURGER_MAX_ANG_VEL = 2.80

class turtlebot():

    def __init__(self):
        self.pose = Pose()
        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/vrpn_client_node/TB3_1/pose', PoseStamped, self.callback)
#        self.pose_subscriber = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.callback)
        self.freq = 2
        self.rate = rospy.Rate(self.freq)

        # log collection
        self.log = open("tracking_straight_" + str(rospy.get_rostime()) + ".txt", 'w')

    # Callback collecting pose data
    def callback(self, data):
        self.pose = data.pose



    """ Helper Functions """

    def constrain(self, input, low, high):
        if input < low:
          input = low
        elif input > high:
          input = high
        else:
          input = input
        return input

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


    """ Online Tracking Algorithm """

    def setParameters(self):
        L = .16 # length of robot
        T_sim = 25 # total amount of time (seconds)
        dt = 0.5 # time it takes to sample

        print("Parameters Set")
        self.log.write("Parameters Set \n")

        return L, T_sim, dt

    def setPath(self, T_sim, dt):
        N = int(round(T_sim/dt))    # total number of steps
        N_sim = int(floor(self.freq*N))     # total number of trajectory samples

        # Reference Trajectory - straight line

        path = np.linspace(0, 6, num=N+80)     # generate values from 0 to 1, N_sim entries
        x_r = path
        z_r = np.linspace(0, 0, num=N+80)

        print("Path Set")
        self.log.write("Path Set \n")

        return x_r, z_r, N

    def onlineTracking(self):
        L, T_sim, dt = self.setParameters()
        x_r, z_r, N = self.setPath(T_sim, dt)



        # Initialize Arrays
        x = np.zeros(N)
        z = np.zeros(N)
        theta = np.zeros(N)
        idx = 1

        print("Waiting")
        while (self.pose.position.x == 0):
            continue
        print("Going")

        # subtract the initial reference error
        x[0] = self.pose.position.x
        z[0] = self.pose.position.z
        x_dif = x_r[0]-x[0]
        z_dif = z_r[0]-z[0]
        for i in range(len(x_r)):
            x_r[i] -= x_dif
            z_r[i] -= z_dif

        while (idx < N) and (not rospy.core.is_shutdown()):
            now = rospy.get_rostime()
            self.log.write(str(now) + "\n")
            self.log.write(str(self.pose) + "\n")

            x[idx] = self.pose.position.x
            z[idx] = self.pose.position.z


#            if idx == 1
#              x_r = x_r - x[idx]
#              z_r = z_r - z[idx]
#            end

            qw = self.pose.orientation.w
            qx = self.pose.orientation.x
            qy = self.pose.orientation.y
            qz = self.pose.orientation.z

            (roll, pitch, yaw) = euler_from_quaternion((qx, qy, qz, qw))
            theta[idx] = yaw

            """ Caclulate velocity """
            self.log.write("x_r: " + str(x_r[idx]) + "\tz_r: " + str(z_r[idx]) + "\n")
            v,w = CalXY(dt, x_r, z_r, x[idx], z[idx], theta[idx], idx)

#            v = 0.05*v
#            w = 0.05*w

            print "linear velocity = ", v
            print "angular velocity = ", w
            self.log.write("lin Vel = " + str(v) + "\t ang Vel = " + str(w) + "\n")

            self.publishTwist(v, -w)
            idx = idx + 1
            self.log.write("\n")

            self.rate.sleep()

        self.stopTwist()

        fig = plt.figure()
        plt.plot(x,z)
        plt.plot(x_r[0:len(x)],z_r[0:len(z)])
        plt.ylim(-1, 1)
        plt.show()

    """ Publishing """
    def publishTwist(self, v, w):
        vel_msg = self.getTwist(v,w)
        print(vel_msg)
        self.log.write(str(vel_msg) + "\n")
        rospy.sleep(0.01)
        self.velocity_publisher.publish(vel_msg)

    def stopTwist(self):
        vel_msg = self.getTwist(0,0)
        print(vel_msg)
#        self.log.write(str(vel_msg) + "\n")
        self.log.close()
        self.velocity_publisher.publish(vel_msg)


""" Main function """
if __name__ == '__main__':
    rospy.init_node('turtlebot_controller', anonymous=True)
    x = turtlebot()

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
            rospy.core.signal_shutdown('tracking ended')
        x.stopTwist()
    except KeyboardInterrupt:
        logdebug("keyboard interrupt, shutting down")
        rospy.core.signal_shutdown('keyboard interrupt')
