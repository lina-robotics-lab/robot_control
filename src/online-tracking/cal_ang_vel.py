#!/usr/bin/env python
# converted from cal_ang_vel.m

# from smop.libsmop import *
from math import atan, pi, copysign

def sign(a):
    return copysign(1,a)

def cal_ang_vel( x, y, a, dt):

    angle_next = atan((y[1]-y[0])/(x[1]-x[0]))  
    sign_x = sign(x[1]-x[0])
    sign_y = sign(y[1]-y[0])

    
    if sign_x >= 0:
        if sign_y >= 0: # 1 area
            pass
#             angle_next = angle_next;
        else:           # 4 area
            angle_next = 2*pi + angle_next
    else:
        if sign_y >= 0: # 2 area
            angle_next = pi + angle_next
        else:           # 3 area
            angle_next = pi + angle_next
    
    angle_now = (abs(a))%(2*pi) # transform to (0,2*pi)

    if a < 0:
       angle_now = 2*pi - angle_now
    
    angle_diff = angle_next - angle_now
    if angle_diff >= pi:
        angle_diff = angle_diff - 2*pi
    else:
        if angle_diff <= -pi:
            angle_diff = angle_diff + 2*pi

    print "angle_now: ", angle_now
    print "angle next: ", angle_next
    print "angle_diff: " , angle_diff
    w = 1/dt*( angle_diff )

    return w


if __name__ == '__main__':
    pass
    # x = [5,3]
    # y = [6,5]
    # a = 2
    # dt = 0.1
    # w = cal_ang_vel( x, y, a, dt)
    # print(w)

