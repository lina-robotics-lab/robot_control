function res=KTh2R(kth)
%KTh2R transform the angle axis to euler angle(fixed x,y,z)
%kth is a 4x1 vector. The first three is the vector. Reference from The
%Indroduction To Robotics Page 47.
%res is a 3x1 vector. It represents the alpha,beta and gamma
kx=kth(1);
ky=kth(2);
kz=kth(3);
theta=kth(4);
cth=cos(theta);
vth=(1-cos(theta));
sth=sin(theta);
r11=kx*kx*vth+cth;
r12=kx*ky*vth-kz*sth;
r13=kx*kz*vth+ky*sth;
r21=kx*ky*vth+kz*sth;
r22=ky*ky*vth+cth;
r23=ky*kz*vth-kx*sth;
r31=kx*kz*vth-ky*sth;
r32=ky*kz*vth+kx*sth;
r33=kz*kz*vth+cth;

res(1,1)=r11;
res(1,2)=r12;
res(1,3)=r13;
res(2,1)=r21;
res(2,2)=r22;
res(2,3)=r23;
res(3,1)=r31;
res(3,2)=r32;
res(3,3)=r33;
end