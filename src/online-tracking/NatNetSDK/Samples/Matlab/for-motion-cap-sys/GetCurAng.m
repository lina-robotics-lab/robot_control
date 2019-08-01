function [ang1,ang2]=GetCurAng(data1,data2)
%GetCurAng this function gets the roll, pitch and yaw angle
%data1 and data2 are the vrpn packages
%ang1 and ang2 are two 3x1 vectors 
ang1=GetAng(data1);
ang2=GetAng(data2);
end