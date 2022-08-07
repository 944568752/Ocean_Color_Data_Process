# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 12:56:15 2022

@author: 94456
"""


# Data Analysis


import warnings
warnings.filterwarnings('ignore')


import os
import sys
import glob
import numpy as np
import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt


File_dir=r'C:\Users\94456\Desktop\New folder'
Result_dir=r'C:\Users\94456\Desktop\New folder/Result'



# MSE
def Loss(y_pred,y):
    loss=(y_pred-y)**2
    loss=np.mean(loss)
    loss=np.power(loss,0.5)
    return loss


# R**2
def RR(y_pred,y):
    y_mean=np.mean(y)
    y_up=np.sum((y_pred-y)**2)
    y_down=np.sum((y-y_mean)**2)
    loss=1-y_up/y_down
    return loss


def Fitting_formula_1(x,a,b):
    y=a*x+b
    return y


def Fitting_formula_2(x,a,b,c):
    y=a*(x**2)+b*x+c
    return y


data_info=[]
for csv_path in glob.glob(os.path.join(File_dir,'*.csv')):
    csv_info=np.array(pd.read_csv(csv_path,header=None,usecols=[0,1,2]))
    data_info.append(csv_info)
    
data_info=np.concatenate(data_info,axis=0,dtype=np.float32)


Light_intensity_factor=1.46e+07


data_info[:,2]=data_info[:,2]*Light_intensity_factor

  
Threshold_31=32
Threshold_35=34
Stride=0.1

# for i in np.arange(Threshold_31,Threshold_31+0.5+Stride,Stride):
#     Limit_cache=np.argwhere((data_info[:,0]>i)&(data_info[:,0]<i+Stride))
#     print(f'{i}-{i+Stride}:{Limit_cache.shape[0]}')    



  
Temperature_limit_31=np.argwhere((data_info[:,0]>32.3)&(data_info[:,0]<32.4))
Temperature_limit_35=np.argwhere((data_info[:,0]>34)&(data_info[:,0]<34.5))

Temperature_limit_31=Temperature_limit_31.reshape(Temperature_limit_31.shape[0])
Temperature_limit_35=Temperature_limit_35.reshape(Temperature_limit_35.shape[0])


Data_info_31=data_info[Temperature_limit_31,1:]
Data_info_35=data_info[Temperature_limit_35,1:]


Data_info_31[:,1]=np.log10(Data_info_31[:,1])
Data_info_35[:,1]=np.log10(Data_info_35[:,1])


All_x=Data_info_31[:,0]
All_y=Data_info_31[:,1]

All_x=All_x[np.where(All_x<12.5)]
All_y=All_y[np.where(All_x<12.5)]


Correct_limit=np.argwhere(All_x>9)
Correct_limit=Correct_limit.reshape(Correct_limit.shape[0])

All_y[Correct_limit]=np.where(All_y[Correct_limit]>9.7,np.mean(All_y[Correct_limit]),All_y[Correct_limit])


Correct_limit=np.argwhere(All_x<9)
Correct_limit=Correct_limit.reshape(Correct_limit.shape[0])
All_y[Correct_limit]=np.where(All_y[Correct_limit]<7.7,np.mean(All_y[Correct_limit]),All_y[Correct_limit])



X_cache=[]
Y_cache=[]
RMSE_cache=[]


for i in range(int(np.floor(np.min(All_x))),int(np.ceil(np.max(All_x))),1):
    
        sub_y_cache=All_y[np.where((All_x>=i)&(All_x<(i+1)))]
        y_value=np.mean(sub_y_cache)
        y_rmse=(np.mean((sub_y_cache-y_value)**2))**0.5
        if np.isnan(y_value):
            continue
        X_cache.append(i)
        Y_cache.append(y_value)
        RMSE_cache.append(y_rmse)


All_x=np.array(X_cache)
All_y=np.array(Y_cache)
RMSE_cache=np.array(RMSE_cache)


# All_x=Data_info_35[:,0]
# All_y=Data_info_35[:,1]


# 一次拟合
# optp : a,b
optp,pcov=optimize.curve_fit(f=Fitting_formula_1,xdata=All_x,ydata=All_y)
a,b=optp
print(f'optp : {optp}')

loss=RR(Fitting_formula_1(All_x,a,b),All_y)
print(f'1 Loss : {loss}',end='\n\n')
print(f'y = {a:.4f} * x + {b:.4f}')
print('-'*60)

# show_0
fig0=plt.figure(figsize=(10,6))

ax=plt.gca()
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)

# 显示中文
plt.rcParams['font.sans-serif']=['Microsoft YaHei']
# plt.title(' 在不同海域夜光藻发光强度和盐度的关系 ',fontsize=16)

x_plot=np.arange(int(np.min(All_x)),int(np.max(All_x)+1),0.1)
y_plot=np.array(list(map(lambda x:Fitting_formula_1(x,a,b),x_plot)))

# color : 线的颜色
plt.plot(x_plot,y_plot,color='blue',linewidth=3)

plt.scatter(All_x,All_y,s=12,color='red')

# print(ax.get_legend_handles_labels())

plt.legend()
# plt.grid()

# y_ticks=list(plt.yticks()[0])
# new_y_ticks=list(map(lambda x:f'${{{Base_n}}}^{{{x}}}$',y_ticks))
# # new_y_ticks=list(map(lambda x:f'{Base_n}^{x}',y_ticks))
# plt.yticks(y_ticks,new_y_ticks,fontsize=16)
# plt.xticks(fontsize=16)

# X&Y轴内容
plt.xlabel(' 温度 ',fontsize=16)
plt.ylabel(' 发光强度 ',fontsize=16)
# 存储路径
plt.savefig(os.path.join(Result_dir,'1.png'))
plt.clf()


All_x=All_x.reshape(All_x.shape[0],1)
All_y=All_y.reshape(All_y.shape[0],1)
RMSE_cache=RMSE_cache.reshape(RMSE_cache.shape[0],1)
Data_result=np.concatenate([All_x,All_y,RMSE_cache],axis=1,dtype=np.float32)
Data_result=pd.DataFrame(Data_result,dtype=np.float32)

Data_result.to_csv(os.path.join(Result_dir,'Result.csv'),header=['Temperature','Intensity','RMSE'],index=False)


    
    

