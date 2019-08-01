function res = rotx( angle )
%rotx the 3D rotation around x axis
%angle is the rotation
res=[1 0 0;0 cos(angle) -sin(angle);0 sin(angle) cos(angle)];
end

