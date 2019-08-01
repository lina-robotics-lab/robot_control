function res = Q2R( quaternion )
%Q2R calculate the quaternion to the rotation matrix 
%quaternion is a 4x1 vector. the first element is the angle
%res is a 3x1 vector includes roll pitch yaw(alpha, beta and gamma) 
q1=quaternion(1);
q2=quaternion(2);
q3=quaternion(3);
q4=quaternion(4);
R(1,1)=1-2*q3*q3-2*q4*q4;
R(1,2)=2*(q2*q3-q4*q1);
R(1,3)=2*(q2*q4+q3*q1);
R(2,1)=2*(q2*q3+q4*q1);
R(2,2)=1-2*q2^2-2*q4^2;
R(2,3)=2*(q3*q4-q2*q1);
R(3,1)=2*(q2*q4-q3*q1);
R(3,2)=2*(q3*q4+q2*q1);
R(3,3)=1-2*q2*q2-2*q3*q3;
res=R;

end

