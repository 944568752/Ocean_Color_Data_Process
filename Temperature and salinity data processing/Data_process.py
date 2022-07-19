# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:59:54 2022

@author: 94456
"""


# Date Process


import warnings
warnings.filterwarnings('ignore')


import os
import sys
import numpy as np
import pandas as pd


s_path=r'./s.xlsx'
t_path=r'./t.xlsx'


s_data=pd.read_excel(s_path,header=None,dtype=np.float32)
t_data=pd.read_excel(t_path,header=None,dtype=np.float32)


s_data=np.array(s_data,dtype=np.float32)
t_data=np.array(t_data,dtype=np.float32)


s_data=np.sort(s_data,axis=0)
t_data=np.sort(t_data,axis=0)


s_data[:,0]=s_data[:,0]//0.5
t_data[:,0]=t_data[:,0]//1


def get_mean(m):
    m_index=set(m[:,0])
    result=[]
    
    for i in m_index:
        result.append([i,np.mean(m[m[:,0]==i,1])])
        
    result=np.array(result,dtype=np.float32)
    return result
    

s_result=get_mean(s_data)
s_result[:,0]=s_result[:,0]/2

t_result=get_mean(t_data)


s_result=np.sort(s_result,axis=0)
t_result=np.sort(t_result,axis=0)


s_result=pd.DataFrame(s_result)
t_result=pd.DataFrame(t_result)


s_result.to_excel(r'./s_result.xlsx',index=False,header=False)
t_result.to_excel(r'./t_result.xlsx',index=False,header=False)










