%% function: send signal from xbee to xbee in m3pi
% editor: Yan Ou
% date: 20140730

function pc2xbee(s,lm,rm)
lm = lm*100;
rm = rm*100;
% transfer value
speed = int2ascii(lm,rm);
% send value
fprintf(s,speed);
end

%% function: transfer integer value to ascii value
% editor: Yan Ou
% date: 20140730

function speed = int2ascii(lm,rm)
speed='lrlrlrpppppp';
% limit the max speed to be 0.3
for i = 1:length(lm)
speed(2*(i-1)+1)=round(abs(lm(i)))+40;
speed(2*(i-1)+2)=round(abs(rm(i)))+40;
if lm(i) < 0
    speed(2*(i-1)+7)='n';
end
if rm(i) < 0
    speed(2*(i-1)+8)='n';
end
end
end