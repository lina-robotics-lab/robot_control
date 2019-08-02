#!/usr/bin/env python
import time
import rospy
import os
from rospy.core import logdebug
import numpy as np
from numpy import pi, sin, cos
from math import floor

from std_msgs.msg import String
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Twist
# from nav_msgs.msg import Odometry
# from geometry_msgs.msg import Pose, Twist

from CalXY import CalXY
from get_robot_pose import getPose
from tf.transformations import euler_from_quaternion
import matplotlib.pyplot as plt


#*************** CONSTANTS ******************#
BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

class turtlebot():

    def __init__(self):
        #Creating our publisher and subscriber
        self.pose = Pose()
        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        # self.pose_subscriber = rospy.Subscriber('odom', Odometry, self.callback)
        self.pose_subscriber = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.callback)
        self.rate = rospy.Rate(2)
        # rospy.spin()

    #Callback function implementing the pose value received
    def callback(self, data):
        self.pose = pose_with_cov_stamped.pose.pose
        # self.pose = data.pose.pose
        # self.pose.position.x = round(self.pose.position.x, 4)
        # self.pose.position.y = round(self.pose.position.y, 4)
        # print(x[idx])
        # print "x_r: ", x_r[idx]
        # print "z_r: ", z_r[idx]
        # print(x[idx] - x_r[idx])

    # **************** HELPER FUNCTIONS ******************* #
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

    # ***************** ONLINE TRACKING ALGORITHM ******************* #
    def setParameters(self):
        L = .16 # length of robot
        T_sim = 45 # total amount of time (seconds)
        dt = 0.5 # time it takes to sample
        print("Parameters Set")
        return L, T_sim, dt

    def setPath(self, T_sim, dt):
        N = int(round(T_sim/dt)) # total number of steps
        N_sim = int(floor(2*N)) # total number of trajectory samples
                
        # Desired Reference Path (circle)
        path = np.linspace(0,4*pi,N_sim)
        radius = 1
        z_r = 0.05*(16*sin(path)**3) - self.pose.position.y
        x_r = 0.05*(13*cos(path)-5*cos(2*path) - 2*cos(3*path) - cos(4*path) - 6.581) - self.pose.position.x
#        x_r = radius * np.sin(path)
#        z_r = - radius * np.cos(path) + radius
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
            v,w = CalXY(dt, x_r, z_r, x[idx], z[idx], theta[idx], idx) 
            print "linear velocity = ", v
            print "angular velocity = ", w

            # **** Publish Velocity **** #
            self.publishTwist(v,w)
            self.rate.sleep()
            # print((x[idx] - x[idx-1]) / 0.1)
            idx = idx + 1
            # print(idx)

        # **** Stop Velocity **** #
        self.stopTwist()


        # **** Plotting **** #
        fig = plt.figure()
        plt.plot(x,z)
        plt.plot(x_r,z_r)
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
        print(vel_msg)
        self.velocity_publisher.publish(vel_msg)

    def stopTwist(self):
        vel_msg = self.getTwist(0,0)
        print(vel_msg)
        self.velocity_publisher.publish(vel_msg)

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
