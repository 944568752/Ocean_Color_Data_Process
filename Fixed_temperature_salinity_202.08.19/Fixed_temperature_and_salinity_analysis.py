# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 20:03:28 2022

@author: 94456
"""


# Fixed temperature and salinity analysis


import warnings
warnings.filterwarnings('ignore')


import os
import sys
import numpy as np
import pandas as pd


file_path=r'./Fixed_salinity.xlsx'


# 多表（Sheet）:True
# 单表（Sheet）:False
multi_sheet_flag=True
# 取值间隔
interval=1


def get_mean_std(m,data):
    m_index=set(m[:,0])
    result=[]
    
    for i in m_index: 
        m_mean=np.mean(data[m[:,0]==i,1])
        m_rmse=np.sqrt(np.mean((data[m[:,0]==i,1]-m_mean)**2))
        result.append([data[m[:,0]==i,0][0],m_mean,m_rmse])
        
    result=np.array(result,dtype=np.float32)
    return result


if multi_sheet_flag:
    datas=pd.read_excel(file_path,header=None,dtype=np.float32,sheet_name=None)
    
    Multi_sheet_writer=pd.ExcelWriter(r'./Multi_sheet_result.xlsx')
    for i,j in datas.items():
        datas[i]=np.array(j)
        datas[i]=datas[i][np.argsort(datas[i][:,0])]
        
        result=datas[i].copy()
        result[:,0]=result[:,0]//interval
        result=get_mean_std(result,datas[i])
        result=result[np.argsort(result[:,0])]
        result=pd.DataFrame(result)
        result.to_excel(Multi_sheet_writer,index=False,header=False,sheet_name=i)
    Multi_sheet_writer.save()
    Multi_sheet_writer.close()
        
else:
    data=pd.read_excel(file_path,header=None,dtype=np.float32)
    
    data=np.array(data)
    data=data[np.argsort(data[:,0])]
    
    result=data.copy()
    result[:,0]=result[:,0]//interval
    result=get_mean_std(result,data)
    result=result[np.argsort(result[:,0])]
    result=pd.DataFrame(result)
    result.to_excel(r'./Single_sheet_result.xlsx',index=False,header=False)
    
    
    
    
    
    
    
    
    