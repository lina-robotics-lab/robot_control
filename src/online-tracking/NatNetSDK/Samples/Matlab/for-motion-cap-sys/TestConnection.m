function TestConnection
% open port
s = serial('COM4','BaudRate',9600);
fopen(s);
% show they work
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% set value
ls = [0.5,0.5,1.0];
rs = [0.2,0.5,1.0];
% send value
pc2xbee(s,ls,rs);
disp('m3pi 1 screen should display:');
disp('l:0.0000');
disp('r:0.0000');
disp('m3pi 2 screen should display:');
disp('l:0.5000');
disp('r:0.5000');
disp('m3pi 3 screen should display:');
disp('l:1.0000');
disp('r:1.0000');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% stop
pause(4)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% set value
ls = [0,0,0];
rs = [0,0,0];
% send value
pc2xbee(s,ls,rs);
disp('m3pi 1 screen should display:');
disp('l:0.0000');
disp('r:0.0000');
disp('m3pi 2 screen should display:');
disp('l:0.0000');
disp('r:0.0000');
disp('m3pi 3 screen should display:');
disp('l:0.0000');
disp('r:0.0000');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% close port
fclose(s); 
delete(s); 
clear s;
end