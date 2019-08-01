function [v_real, w_real] = CalXY(dt_con, xr, yr,  x_now, y_now, a_now, idx)



% -------- cost
c_x = 1;    c_y = 1;      c_a = 1;   % tracking error
c_v = 1*(dt_con)^2;       c_w = 1*(dt_con)^2;     % velocity effort

% ------- step size
Lx = 0.0015;   Ly = 0.0015;

%% ================== Online Control Algorithm ===========================

% ------- prediction window 
W = 40;
K_inner = floor((W-1)/2);   % inner iteration number

% ------- initial for online decision variables
x_ol = zeros(1+W,1);   y_ol = zeros(1+W,1);    a_ol = zeros(1+W,1);

%% Run Online Algorithm

% 1 - initial
x_ol(1) = x_now;      y_ol(1) = y_now;  % fixed 

% initial with the last iteration results
x_ol(2:W+1) = xr(idx+1:idx+W);
y_ol(2:W+1) = yr(idx+1:idx+W);
    
% 2 - gradient 
for i = 1:K_inner  
        
        W_temp = 3+W-2*i;
        
        dJdx = Cal_dJdx (x_ol(1:W_temp),y_ol(1:W_temp),c_x,c_y,c_v,c_w,dt_con,xr(idx:idx+W_temp-1));
        dJdy = Cal_dJdy (x_ol(1:W_temp),y_ol(1:W_temp),c_x,c_y,c_v,c_w,dt_con,yr(idx:idx+W_temp-1));
        
        % update
        x_ol(2:W_temp-2) = x_ol(2:W_temp-2)- Lx*dJdx;
        y_ol(2:W_temp-2) = y_ol(2:W_temp-2)- Ly*dJdy;
        
end
        
% 3 - calculate control decision
% tangential velocity
v_real = 1/dt_con*sqrt((x_ol(2)-x_ol(1))^2  + (y_ol(2)-y_ol(1))^2 );
    
% angular velocity
w_real = cal_ang_vel( x_ol(1:2), y_ol(1:2), a_now, dt_con);
        



end

