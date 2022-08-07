# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 13:28:03 2022

@author: 94456
"""


# Data analysis


import warnings
warnings.filterwarnings('ignore')


import os
import glob
import numpy as np





Data_dir=r'C:\Users\94456\Desktop\2022-03\Result 8'
Result_dir=r'C:\Users\94456\Desktop\2022-03\Result'


for data_dir_name in os.listdir(Data_dir):
    
    result_path=os.path.join(Result_dir,fr'{data_dir_name}.txt')
    
    TXT_record=open(result_path,'a') 
    TXT_record.writelines(f' Name , Mean \n')
    
    Mean_cache=[]
    
    for data_path in glob.glob(os.path.join(Data_dir,data_dir_name,'*.txt')):
        
        data_name=os.path.basename(data_path).split('.')[0]
        
        with open(data_path,'r') as f:
            data_info=f.readlines()
            if len(data_info)==0:
                continue
            elif len(data_info)==1:
                data_info=data_info[0]
            else:
                print('!!!')
            
        data_info=np.array(data_info.split(','),dtype=np.float32)
        data_info_mean=np.mean(data_info)
        
        Mean_cache.append(data_info_mean)
        TXT_record.writelines(f'{data_name},{data_info_mean:.7f}\n')
        
    
    Data_MSE=np.mean((Mean_cache-np.mean(Mean_cache))**2)
    
    
    TXT_record.writelines(f'\nMean:{np.mean(Mean_cache)}\nMSE:{Data_MSE}\n')
    TXT_record.close()
        
        
        
        
        
        
        
        
        