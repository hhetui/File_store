clc;
clear;
t=[2,1,4]';
r=[3,4,5]';
[dist,path_min]=dtw(t,r)
function [dist,path_min] = dtw(t,r)
n = size(t,1);
m = size(r,1);

d = zeros(n,m);
path_min=[];
for i = 1:n
for j = 1:m
d(i,j) = (t(i,:)-r(j,:)).^2;
end
end
d
D = ones(n,m) * realmax;
D(1,1) = d(1,1);

for i = 1:n
    for j = 1:m
        if i==1&&j==1
        continue;
        end
        if i>1
        D1 = D(i-1,j);
        else
        D1 = realmax;
        end
        if j>1&&i>1
        D2 = D(i-1,j-1);
        else D2 = realmax;
        end
        if j>1
        D3 = D(i,j-1);
        else
        D3 = realmax;
        end
        [min_D,path_now]=min([D1,D2,D3]);
        D(i,j) = d(i,j) + min_D;
        path_all(i,j)=path_now;
    end
end
dist = D(n,m);
path_min=huisu(path_all);
end
function path_true=huisu(P)
  sizeP=size(P);
  n=sizeP(1);
  m=sizeP(2);
  path_min=[];
  i=n;
  j=m;
  while(i>1 || j>1)
      if(P(i,j)==1)
          path_min=[path_min,1];
          i=i-1;
          continue
      elseif(P(i,j)==2)
          path_min=[path_min,2];
          i=i-1;
          j=j-1;
          continue
      else
          path_min=[path_min,3];
          j=j-1;
          continue
      end
  end
  path_true=[];
  for i=1:length(path_min)
     path_true=[path_true,path_min(length(path_min)-i+1)-2];
  end
end