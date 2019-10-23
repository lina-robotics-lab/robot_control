#!/usr/bin/env python
# Generated with SMOP  0.41
# from smop.libsmop import *
from numpy import sqrt,prod,exp,log,dot,multiply,inf,zeros,linspace,pi
from math import floor
from Cal_dJdx import Cal_dJdx
from Cal_dJdy import Cal_dJdy
from cal_ang_vel import *
# CalXY.m

    
def CalXY(dt_con=None,xr=None,yr=None,x_now=None,y_now=None,a_now=None,idx=None):
    #------- cost ------#

    # -- tracking error -- #
    c_x=1
    c_y=1
    c_a=1
    
    # -- velocity effort -- #
    c_v=dot(0.01,(dt_con) ** 2)
    c_w=dot(0.100,(dt_con) ** 2)
    
    # ------- step size ------- #
    # Lx = 0.1
    # Ly = 0.1
    Lx=0.0015
    Ly=0.0015

    ## ================== Online Control Algorithm ===========================
    
    # ------- prediction window ------- #
    W=80
    K_inner=int(floor((W - 1) / 2)) # inner iteration number

    # ------- initial for online decision variables ------- #
    x_ol=zeros(1 + W)
    y_ol=zeros(1 + W)
    a_ol=zeros(1 + W)

    ## Run Online Algorithm
    
    # 1 - initial (fixed)
    x_ol[0]=x_now
    y_ol[0]=y_now
    
    # initial with the last iteration results
    x_ol[1:W + 1]=xr[idx:idx + W]
    y_ol[1:W + 1]=yr[idx:idx + W]

    # 2 - gradient
    for i in range(0,K_inner):
        W_temp=3 + W - dot(2,i+1)
        dJdx=Cal_dJdx(x_ol[0:W_temp], y_ol[0:W_temp], c_x, c_y, c_v, c_w, dt_con, xr[idx-1:idx+W_temp-1])
        dJdy=Cal_dJdy(x_ol[0:W_temp], y_ol[0:W_temp], c_x, c_y, c_v, c_w, dt_con, yr[idx-1:idx+W_temp-1])
        x_ol[1:W_temp - 2]=x_ol[1:W_temp - 2] - dot(Lx,dJdx)
        y_ol[1:W_temp - 2]=y_ol[1:W_temp - 2] - dot(Ly,dJdy)
    
    # 3 - calculate control decision
    # tangential velocity
    v_real=dot(1/dt_con, sqrt((x_ol[1] - x_ol[0]) ** 2 + (y_ol[1] - y_ol[0]) ** 2))


    # angular velocity
    w_real=cal_ang_vel(x_ol[0:2], y_ol[0:2], a_now,dt_con)

    print "x_ol: ", x_ol[1], x_ol[0]
    print "y_ol: ", y_ol[1], y_ol[0]
    print "v_real", v_real
    print "w_real", w_real

    return v_real,w_real
    
if __name__ == '__main__':
    pass
    # dt_con = 0.1
    # xr = linspace(0,2*pi,120)
    # yr = xr + (pi/2)
    # x_now = 1
    # y_now = 1
    # a_now = 1
    # idx = 1
    # CalXY = CalXY(dt_con,xr,yr,x_now,y_now,a_now,idx)
