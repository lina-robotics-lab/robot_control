function res=ABG2R(input)
%ABG2R calculate the Euler Angle to the rotation matrix
%input is the Euler Angle. 3x1 matrix
alp=input(1);
bet=input(2);
gam=input(3);
ca=cos(alp);
sa=sin(alp);
cb=cos(bet);
sb=sin(bet);
cg=cos(gam);
sg=sin(gam);
r11=ca*cb;
r12=ca*sb*sg-sa*cg;
r13=ca*sb*cg+sa*sg;
r21=sa*cb;
r22=sa*sb*sg+ca*cg;
r23=sa*sb*cg-ca*sg;
r31=-sb;
r32=cb*sg;
r33=cb*cg;
res=[r11 r12 r13;r21 r22 r23;r31 r32 r33];
end