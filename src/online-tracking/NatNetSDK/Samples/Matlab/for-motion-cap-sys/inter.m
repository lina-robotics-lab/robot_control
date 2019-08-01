function d = inter (f,g,u)
    %Interpolation using bilinear algorithm
    x1=floor(f)
    x2=ceil(f);
    y1=floor(g);
    y2=ceil(g);
    if (x1==x2 && y1==y2)
        d=u(f,g);
    else if(x1==x2)
        d=((y2-g)/(y2-y1))*u(f,y1)+((g-y1)/(y2-y1))*u(f,y2);
    else if(y1==y2)
        d=((x2-f)/(x2-x1))*u(x1,g)+((f-x1)/(x2-x1))*u(x2,g);
        else
        d=(1/((x2-x1)*(y2-y1)))*(u(x1,y1)*(x2-f)*(y2-g)+u(x2,y1)*(f-x1)*(y2-g)+u(x1,y2)*(x2-f)*(g-y1)+u(x2,y2)*(f-x1)*(g-y1));
        end
        end
    end
  

    
