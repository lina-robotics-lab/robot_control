#!/usr/bin/env python
# Generated with SMOP  0.41
# from smop.libsmop import *

from math import atan
from numpy import sqrt,prod,exp,log,dot,multiply,inf,zeros
# Cal_dJdx.m

    
def Cal_dJdx(x=None,y=None,cx=None,cy=None,cv=None,cw=None,h=None,xr=None):
    T=len(x)
    dJdx=zeros(T)
    dJdx[1]=dot(dot(2,cv) / h ** 2,(x[1] - x[0])) \
          + dot(dot(dot(2,cw) / h ** 2,(atan((y[2] - y[1]) / (x[2] - x[1])) - atan((y[1] - y[0]) / (x[1] - x[0])))) \
           ,((y[2] - y[1]) / ((x[2] - x[1]) ** 2 + (y[2] - y[1]) ** 2) + (y[1] - y[0]) / ((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2))) \
          + dot(dot(2,cx),(x[1] - xr[1])) + dot(dot(2,cv) / h ** 2,(x[1] - x[2])) \
          - dot(dot(dot(2,cw) / h ** 2,(atan((y[3] - y[2]) / (x[3] - x[2])) - atan((y[2] - y[1]) / (x[2] - x[1])))) \
           ,((y[2] - y[1]) / ((x[2] - x[1]) ** 2 + (y[2] - y[1]) ** 2)))
    
    for t in range(2,T - 2): # BE CAREFUL. FORLOOPS END ONE LOOP SOONER THAN MATLAB
        dJdx[t]=dot(dot(2,cx),(x[t] - xr[t])) \
              + dot(dot(dot(2,cw) / h ** 2,(atan((y[t] - y[t - 1]) / (x[t] - x[t - 1])) - atan((y[t - 1] - y[t - 2]) / (x[t - 1] - x[t - 2])))) \
               ,(- (y[t] - y[t - 1]) / ((x[t] - x[t - 1]) ** 2 + (y[t] - y[t - 1]) ** 2))) \
              + dot(dot(dot(2,cw) / h ** 2,(atan((y[t + 1] - y[t]) / (x[t + 1] - x[t])) - atan((y[t] - y[t - 1]) / (x[t] - x[t - 1])))) \
               ,((y[t + 1] - y[t]) / ((x[t + 1] - x[t]) ** 2 + (y[t + 1] - y[t]) ** 2) + (y[t] - y[t - 1]) / ((x[t] - x[t - 1]) ** 2 + (y[t] - y[t - 1]) ** 2))) \
              + dot(dot(2,cv) / h ** 2,(x[t] - x[t - 1])) + dot(dot(2,cv) / h ** 2,(x[t] - x[t + 1])) \
              - dot(dot(dot(2,cw) / h ** 2,(atan((y[t + 2] - y[t + 1]) / (x[t + 2] - x[t + 1])) - atan((y[t + 1] - y[t]) / (x[t + 1] - x[t])))) \
               ,((y[t + 1] - y[t]) / ((x[t + 1] - x[t]) ** 2 + (y[t + 1] - y[t]) ** 2)))    
    
    dJdx=dJdx[1 : T - 2]

    return dJdx
    
if __name__ == '__main__':
    pass
    # x=[1,2,3,4,5,4,3,2,1,8,7,10]
    # y=[1,2,3,4,5,6,7,8,9,9,9,9]
    # cx=1
    # cy=1
    # cv=1
    # cw=1
    # h=0.1
    # xr=[2,3,4,5,6,7,8,9,10,5,6,2]
    # dJdx = Cal_dJdx(x,y,cx,cy,cv,cw,h,xr)
    # print(dJdx)

    
    