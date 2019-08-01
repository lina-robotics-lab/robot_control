function res= R2ABG( R )
%R2ABG Calculate the alpha,beta and gamma from rotation matrix
%R is a rotation matrix, 3x3
res(2)=atan2(-R(3,1),sqrt(R(1,1)^2+R(2,1)^2));
res(1)=atan2(R(2,1)/cos(res(2)),R(1,1)/cos(res(2)));
res(3)=atan2(R(3,2)/cos(res(2)),R(3,3)/cos(res(2)));
end

