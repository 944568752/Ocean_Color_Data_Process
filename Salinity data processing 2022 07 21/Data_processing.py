# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 13:36:36 2022

@author: 94456
"""


# Data processing



import warnings
warnings.filterwarnings('ignore')


import os
import sys
import glob
import numpy as np
import pandas as pd


excel_dir=r'./'
excel_paths=glob.glob(os.path.join(excel_dir,r'*.xlsx'))


def get_mean(m,n):
    m_index=set(m[:,0])
    result=[]
    
    for i in m_index:
        m_1=np.mean(n[m[:,0]==i,0])
        m_2=np.mean(m[m[:,0]==i,1])
        m_3=np.mean(m[m[:,0]==i,2])
        rmse=np.sqrt(np.sum((m[m[:,0]==i,2]-m_3)**2)/(m[m[:,0]==i,1].shape[0]+1e-7))
        
        result.append([m_1,m_2,m_3,rmse])
        
        
    result=np.array(result,dtype=np.float32)
    return result


for excel_path in excel_paths:
    excel_result_name=os.path.basename(excel_path).split('.')[0]+'_result.xlsx'
    excel_result_path=os.path.join(excel_dir,excel_result_name)
    
    s_data=pd.read_excel(excel_path,header=None,dtype=np.float32)
    
    s_data=np.array(s_data,dtype=np.float32)
    
    s_data=np.sort(s_data,axis=0)
    
    s_original=s_data.copy()
    
    s_data[:,0]=s_data[:,0]//1
    
    s_result=get_mean(s_data,s_original)
    
    s_result[:,0]=s_result[:,0]/1
    
    s_result=np.sort(s_result,axis=0)
    
    
    # s_result_cache=[]
    # for i in s_original[:,0]:
    #     s_result_cache.append([
    #         i,
    #         s_result[s_result[:,0]==i//1,1],
    #         s_result[s_result[:,0]==i//1,2],
    #         s_result[s_result[:,0]==i//1,3]
    #         ])    
    # s_result_cache=np.array(s_result_cache,dtype=np.float32)
    
    # s_result=s_result_cache.copy()
    
    
    s_result=pd.DataFrame(s_result)
    
    s_result.to_excel(excel_result_path,header=None,index=None)
    
    
    
    
    
    
    