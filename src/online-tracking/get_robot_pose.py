#!/usr/bin/env python
import rospy
import numpy as np
# TESTING ONLY! #

from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Pose
#from geometry_msgs.msg import PoseWithCovarianceStamped


def poseAMCLCallback(pose):    
    robot_pose = pose.pose[0]
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
    return robot_pose

def getPose(): 
    rospy.init_node('robot_pose', anonymous=True)
    rospy.Subscriber('gazebo/model_states', ModelStates, poseAMCLCallback)
    #rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, poseAMCLCallback)
    rospy.spin()

if __name__=="__main__":
    getPose()