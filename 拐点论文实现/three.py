import numpy as np
import copy
import math
import random


def data_frame_diff(f,d=0.5):
    #print 'd in diff',d
    data_frame = f
    row_name_list = data_frame.columns.values.tolist()
    for row_name in row_name_list:
        row_data = data_frame[row_name].tolist()
        #print row_data
        data_frame[row_name] = diffseris(row_data,d)
        #print diffseris(row_data,d)
    return data_frame

def calculateBOLL(df,period,d = 0):
    _df = copy.copy(df)
    if(d != 0 ):
        df = data_frame_diff(df,d)
    closeArray = np.array(df['close'])
    MA,MD=[],[]
    MB, UP, DN = [], [], []
    for i in range(0,period-1):
        MA.append(np.nan)
    for i in range(0,2*period-2):
        MD.append(np.nan)
        UP.append(np.nan)
        DN.append(np.nan)
    for i in range(period-1,len(closeArray)):
        MA.append(np.mean(closeArray[i+1-period:i+1]))
    for i in range(2*period-2,len(closeArray)):
        sum_MA_C=0
        for j in range(i+1-period,i+1):
            sum_MA_C+=(closeArray[j]-MA[i])**2
        MD.append(np.sqrt(sum_MA_C/period))

    for i in range(0,period):
        MB.append(np.nan)

    for i in range(period,len(closeArray)):
        MB.append(MA[i-1])
    for i in range(2*period-2,len(closeArray)):
        UP.append(MB[i]+2*MD[i])
        DN.append(MB[i]-2*MD[i])
    _df['MB']=MB
    _df['UP'] = UP
    _df['DN'] = DN
    return _df


def FCM(Y,c,m=2,e=10**-3):
    #Y需要是1xlen(Y)的向量
    v=np.random.rand(1,c)
    U=np.random.rand(c,len(Y))
    U=U/sum(U)
    U_old=np.random.rand(c,len(Y))
    U_old=U_old/sum(U_old)
    while(np.max(abs(U-U_old))>e):
        U_old=copy.copy(U)
        v=np.sum((U**m)*Y,1)/np.sum(U**m,1)
        Yv=np.zeros([c,len(Y)])
        for i in range(c):
            Yv[i,:]=abs(Y-v[i])#可以更换距离函数
        U=(Yv**(2/(m-1))*(np.sum(Yv**(-2/(m-1)),1)))**-1

    return v

def trimf(x,a,b,c):
    return max(0,min((x-a)/(b-a),(c-x)/(c-b)))

def trapmf(x,a,b,c,d):
    return max(0,min((x-a)/(b-a),1,(d-x)/(d-c)))


