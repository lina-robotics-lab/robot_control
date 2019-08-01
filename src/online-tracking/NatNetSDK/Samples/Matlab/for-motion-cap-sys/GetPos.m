function [pos1,pos2]=GetPos(data1,data2)
%GetPos this function get the current position of the quadrotor
%data is a structure. it includes the rotation and the position
%curPos is a 3x1 vector.It is the current position.The unit is milimeter
pos1=[data1(1).pos(1) data1(1).pos(2) data1(1).pos(3)]'*1000;%the unit is milimeter
pos1=[-1 0 0;0 0 1;0 1 0]*pos1;
pos2=[data2(1).pos(1) data2(1).pos(2) data2(1).pos(3)]'*1000;
pos2=[-1 0 0;0 0 1;0 1 0]*pos2;

end