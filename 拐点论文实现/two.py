import numpy as np
import copy
import math
import random
import matplotlib.pyplot as plt

def a_alpha(G,alpha):
    G=np.array(G)
    #print(G)
    medG=np.median(G)
    G_sorted=sorted(G)
    #print(medG)
    i=0
    a=0
    #print(len(G))
    while(i<len(G)):
        if(G_sorted[i]<=medG):
            #print(i)
            f1=sum((G_sorted[i]<=G)&(G<=medG))#card
            f2=math.exp(-alpha*abs(medG-G_sorted[i]))
            if(f1*f2>a):
                a=G_sorted[i]
            i=i+1
        else:
            break
    return a

def b_alpha(G,alpha):
    G=np.array(G)
    
    medG=np.median(G)
    
    len_G=len(G)
    G_sorted=sorted(G,reverse=True)
    i=0
    b=0
    while(i<len(G)):
        if(G_sorted[i]>=medG ):
            f1=sum((G_sorted[i]>=G)&(G>=medG))#card
            f2=math.exp(-alpha*abs(medG-G_sorted[i]))
            if(f1*f2>b):
                b=G_sorted[i]
            i=i+1
        else:
            break
    return b

def Vol(G):
    #计算积分 离散方式计算的 因为自定义的函数
    gap=0.02
    alpha=gap/2
    vol=0
    for i in range(int(1/gap)-1):
        vol=vol+gap*abs(b_alpha(G,alpha)-a_alpha(G,alpha))
        alpha=alpha+gap
    return vol

def PSO(L,G,lamda=10):
    w=0.9
    c1=2
    c2=2
    L=L-1
    #s=np.array(sorted(np.random.choice(len(G),L)))+1
    S=np.zeros((lamda,L))
    #print(np.shape(S))
    #print(S[0,:])
    for i in range(lamda):
        #S[i,:]=(np.array(sorted(random.sample(range(len(G)-1),L))))+1
        S[i,:]=np.array([len(G)/(L+1)*j for j in range(1,L+1)])
    S=S.astype(int)
    #print(type(S[0,0]))
    V=np.random.randn(lamda,L)*2
    B=copy.copy(S)
    P=copy.copy(S[1,:])
    Num=0
    while(Num<100):
        #print(Num)
        V=w*V+c1*np.random.rand(lamda,1)*(B-S)+c2*np.random.rand(lamda,1)*(P-S)
        S=S+V
        S_now=np.round(S)
        S_now=S.astype(int)
        #print('S\n',S)
        #print("V\n",V)
        for i in range(lamda):
            if(cal_VOL(G,S_now[i,:])!=None):
                if(cal_VOL(G,S_now[i,:])<cal_VOL(G,B[i,:])):
                    B[i,:]=copy.copy(S_now[i,:])
                if(cal_VOL(G,B[i,:])<cal_VOL(G,P)):
                    P=copy.copy(B[i,:])
                    print("P\n",P,cal_VOL(G,P))
                Num=Num+1
            else:
                S[i,:]=np.array([len(G)/(L+1)*j for j in range(1,L+1)])
        
        
    return P

def cut(G,s):
    s=np.array(s)-1
    s=s.astype(int)
    if(s[len(s)-1]>=len(G)-1):
        #print("分割点越界或者不足！\n")
        #print(len(G),'\n',s)
        return 0
    else:
        cut_G=[]
        for i in range(len(s)):
            if i==0:
                cut_G.append(G[0:s[i]+1])
            else:
                cut_G.append(G[s[i-1]+1:s[i]+1])
        cut_G.append(G[s[len(s)-1]+1:len(G)])
        #print(cut_G)
        return cut_G

def cal_VOL(G,s):
    cut_G=cut(G,s)
    if cut_G==0:
        return None
    else:
        return sum(Vol(g) for g in cut_G)

def f(a):
    a=[2,3]
    return a


G=[5,8,12,48,52,53,56,60,65,70,80,85,109,110,120,130,131,132,133,134,135,136,137]
#print(sum([f(i) for i in G ]))
#print(PSO(3,G))
#s=[1,4]
#print(s)
#print(type(s[0]))
#print(cut(G,s))
#print(cal_VOL(G,s))
print(PSO(3,G)) 
#print(cal_VOL(G,[3,5]))
plt.plot(G)
plt.show()
