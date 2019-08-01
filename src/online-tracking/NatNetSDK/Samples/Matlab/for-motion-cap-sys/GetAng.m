function [ang,quat]=GetAng(data)
%GetAng this function get the Euler angle for the quadrotor
%data is a structure
%ang is a 3x1 vector,including the roll,pitch and yaw angle
q=[data(1).quat(1) data(1).quat(2) data(1).quat(3) data(1).quat(4)];%the last element is the angle term

%this method is borrowed from Sayan's work. It's different from my previous
%method
% quat=quat/norm(quat,2);
% q_v=quat(1,1:3);
% q_0=quat(1,4);
% k=q_v'/norm(q_v);
% th=2*atan2(norm(q_v),q_0);
% R=KTh2R([k;th]);
% angTemp=R2ABG(R);
% ang=[-angTemp(1,3);angTemp(1,1);angTemp(1,2)];%for the capture system, there are some differences

qx = q(1);
qy = q(2);
qz = q(3);
qw = q(4);



% Mei
% disp('Mei')
yaw = atan2(2*qy*qw-2*qx*qz , 1-2*qy^2-2*qz^2);
pitch = asin(2*qx*qy+ 2*qz*qw);
roll = atan2(2*qx*qw-2*qy*qz,1-2*qx^2-2*qz^2);
ang=[roll;pitch;yaw];
end
