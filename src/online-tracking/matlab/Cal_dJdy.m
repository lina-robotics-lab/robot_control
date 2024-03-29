function  dJdy = Cal_dJdy (x,y,cx,cy,cv,cw,h,yr)
%
    T = length(y);
    
    dJdy = zeros(T,1); 
    
    dJdy(2) = 2*cv/h^2*(y(2)-y(1)) ...
            - 2*cw/h^2*( atan((y(3)-y(2))/(x(3)-x(2))) - atan((y(2)-y(1))/(x(2)-x(1))))...
              *( (x(3)-x(2))/((x(3)-x(2))^2+(y(3)-y(2))^2 ) +  (x(2)-x(1))/((x(2)-x(1))^2+(y(2)-y(1))^2 ) )...
            + 2*cy*(y(2)-yr(2)) + 2*cv/h^2*(y(2)-y(3))...
            + 2*cw/h^2*( atan((y(4)-y(3))/(x(4)-x(3))) - atan((y(3)-y(2))/(x(3)-x(2))))...
              *( (x(3)-x(2))/((x(3)-x(2))^2+(y(3)-y(2))^2) );
    
    for t = 3:T-2
        
        dJdy(t) = 2*cy*(y(t)-yr(t)) ...
                + 2*cw/h^2*( atan((y(t)-y(t-1))/(x(t)-x(t-1))) - atan((y(t-1)-y(t-2))/(x(t-1)-x(t-2))))...
                  *( (x(t)-x(t-1))/((x(t)-x(t-1))^2+(y(t)-y(t-1))^2 )  )...
                - 2*cw/h^2*( atan((y(t+1)-y(t))/(x(t+1)-x(t))) - atan((y(t)-y(t-1))/(x(t)-x(t-1))))...
                  *( (x(t+1)-x(t))/((x(t+1)-x(t))^2+(y(t+1)-y(t))^2 ) +  (x(t)-x(t-1))/((x(t)-x(t-1))^2+(y(t)-y(t-1))^2 ) )...
                +  2*cv/h^2*(y(t)-y(t-1)) + 2*cv/h^2*(y(t)-y(t+1))...
                + 2*cw/h^2*( atan((y(t+2)-y(t+1))/(x(t+2)-x(t+1))) - atan((y(t+1)-y(t))/(x(t+1)-x(t))))...
                  *( (x(t+1)-x(t))/((x(t+1)-x(t))^2+(y(t+1)-y(t))^2) );
        
    end
    
    dJdy = dJdy(2:T-2);

end
