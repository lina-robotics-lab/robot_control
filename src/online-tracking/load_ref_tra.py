# Generated with SMOP  0.41
from libsmop import *
# load_ref_tra.m

    
@function
def load_ref_tra(index=None,*args,**kwargs):
    varargin = load_ref_tra.varargin
    nargin = load_ref_tra.nargin

    if 1 == index:
        dt_con=1
# load_ref_tra.m:7
        T_con=dot(30,pi)
# load_ref_tra.m:8
        t_con=arange(0,T_con,dt_con)
# load_ref_tra.m:9
        nT_con=length(t_con)
# load_ref_tra.m:10
        radius=10
# load_ref_tra.m:12
        wr=0.1
# load_ref_tra.m:13
        vr=dot(radius,wr)
# load_ref_tra.m:13
        xr=dot(radius,cos(dot(wr,t_con)).T)
# load_ref_tra.m:14
        yr=dot(radius,sin(dot(wr,t_con)).T)
# load_ref_tra.m:15
        ar=dot(wr,t_con.T) + pi / 2
# load_ref_tra.m:16
        disp('load fast circle successfully!')
    else:
        if 2 == index:
            dt_con=0.1
# load_ref_tra.m:21
            T_con=dot(30,pi)
# load_ref_tra.m:22
            t_con=arange(0,T_con,dt_con)
# load_ref_tra.m:23
            nT_con=length(t_con)
# load_ref_tra.m:24
            radius=10
# load_ref_tra.m:26
            wr=0.1
# load_ref_tra.m:27
            vr=dot(radius,wr)
# load_ref_tra.m:27
            xr=dot(radius,cos(dot(wr,t_con)).T)
# load_ref_tra.m:28
            yr=dot(radius,sin(dot(wr,t_con)).T)
# load_ref_tra.m:29
            ar=dot(wr,t_con.T) + pi / 2
# load_ref_tra.m:30
            disp('load slow circle successfully!')
        else:
            if 3 == index:
                dt_con=1
# load_ref_tra.m:33
                T_con=100
# load_ref_tra.m:34
                t_con=arange(0,T_con,dt_con)
# load_ref_tra.m:35
                nT_con=length(t_con)
# load_ref_tra.m:36
                xr=zeros(nT_con,1)
# load_ref_tra.m:37
                yr=zeros(nT_con,1)
# load_ref_tra.m:37
                ar=zeros(nT_con,1)
# load_ref_tra.m:37
                xr[arange(1,21)]=arange(0,20,1)
# load_ref_tra.m:38
                xr[arange(22,41)]=dot(20,ones(20,1))
# load_ref_tra.m:39
                yr[arange(22,41)]=arange(1,20,1)
# load_ref_tra.m:39
                ar[arange(22,41)]=dot(pi / 2,ones(20,1))
# load_ref_tra.m:39
                xr[arange(42,61)]=20 - (arange(1,20,1))
# load_ref_tra.m:40
                yr[arange(42,61)]=dot(20,ones(20,1))
# load_ref_tra.m:40
                ar[arange(42,61)]=dot(pi,ones(20,1))
# load_ref_tra.m:40
                yr[arange(62,81)]=20 - (arange(1,20,1))
# load_ref_tra.m:41
                ar[arange(62,81)]=dot(dot(3 / 2,pi),ones(20,1))
# load_ref_tra.m:41
                xr[arange(82,101)]=arange(1,20,1)
# load_ref_tra.m:42
                disp('load fast square successfully!')
            else:
                if 4 == index:
                    dt_con=0.1
# load_ref_tra.m:45
                    T_con=100
# load_ref_tra.m:46
                    t_con=arange(0,T_con,dt_con)
# load_ref_tra.m:47
                    nT_con=length(t_con)
# load_ref_tra.m:48
                    xr=zeros(nT_con,1)
# load_ref_tra.m:49
                    yr=zeros(nT_con,1)
# load_ref_tra.m:49
                    ar=zeros(nT_con,1)
# load_ref_tra.m:49
                    xr[arange(1,201)]=arange(0,20,0.1)
# load_ref_tra.m:50
                    xr[arange(202,401)]=dot(20,ones(200,1))
# load_ref_tra.m:51
                    yr[arange(202,401)]=arange(0.1,20,0.1)
# load_ref_tra.m:52
                    ar[arange(202,401)]=dot(pi / 2,ones(200,1))
# load_ref_tra.m:53
                    xr[arange(402,601)]=20 - (arange(0.1,20,0.1))
# load_ref_tra.m:54
                    yr[arange(402,601)]=dot(20,ones(200,1))
# load_ref_tra.m:55
                    ar[arange(402,601)]=dot(pi,ones(200,1))
# load_ref_tra.m:56
                    yr[arange(602,801)]=20 - (arange(0.1,20,0.1))
# load_ref_tra.m:57
                    ar[arange(602,801)]=dot(dot(3 / 2,pi),ones(200,1))
# load_ref_tra.m:58
                    xr[arange(802,1001)]=arange(0.1,20,0.1)
# load_ref_tra.m:59
                    disp('load slow square successfully!')
                else:
                    if 5 == index:
                        dt_con=0.1
# load_ref_tra.m:63
                        T_con=60
# load_ref_tra.m:64
                        t_con=arange(0,T_con,dt_con)
# load_ref_tra.m:65
                        nT_con=length(t_con)
# load_ref_tra.m:66
                        t=linspace(- 6,6,601)
# load_ref_tra.m:67
                        xr=dot(16,(sin(t)) ** 3)
# load_ref_tra.m:68
                        yr=dot(13,cos(t)) - dot(5,cos(dot(2,t))) - dot(2,cos(dot(3,t))) - cos(dot(4,t))
# load_ref_tra.m:69
                        ar=zeros(nT_con,1)
# load_ref_tra.m:70
                        for i in arange(1,nT_con - 1).reshape(-1):
                            ar[i]=atan((yr(i + 1) - yr(i)) / (xr(i + 1) - xr(i)))
# load_ref_tra.m:72
                        disp('load heart successfully!')
                    else:
                        disp('please select a correct type number')
    
    return dt_con,T_con,t_con,nT_con,xr,yr,ar
    
if __name__ == '__main__':
    pass
    