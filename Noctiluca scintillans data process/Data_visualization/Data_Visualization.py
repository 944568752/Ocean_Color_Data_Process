# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 09:51:12 2022

@author: 94456
"""


# Data Visualization


import warnings
warnings.filterwarnings('ignore')


import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt



Data_path=r'./raw_data'
Result_path=r'./result'


Threshold_DN=21
Back_ground_DN=4



Dir_paths=os.listdir(Data_path)
for dir_path in Dir_paths:
    Sub_result_path=os.path.join(Result_path,dir_path)
    
    if not os.path.exists(Sub_result_path):
        os.makedirs(Sub_result_path)
    
    Dat_paths=glob.glob(os.path.join(Data_path,dir_path,'*.dat'))
    
    for Dat_path in Dat_paths:
        try:
            Data_info=np.loadtxt(Dat_path,delimiter=',',usecols=np.arange(11,70,1,dtype=np.int),dtype=np.int)
        except IndexError:
            print(f'IndexError: {Dat_path}')
            
            
        Dat_name=os.path.basename(Dat_path).split('.')[0]
        
        
        Data_info=Data_info.flatten()
        
        Data_info=Data_info-Back_ground_DN
        
        Data_info=np.where(Data_info>0,Data_info,0)
        
        
        New_data_info=Data_info.copy()
        
        
        Continuity_start_0_location=0
        Continuity_end_0_location=0
        Continuity_start_1_location=0
        Continuity_end_1_location=0
        Left_0_Peak_flag=-1
        Left_1_Peak_flag=-1
        
        Image_count=0
        
        Peak_count=0
        
            
        for i in range(1,len(New_data_info)-1):
            if New_data_info[i]>New_data_info[i-1] and New_data_info[i]>New_data_info[i+1]:
                
                Start_location=0
                End_location=0
                
                Step_count=1
                Peak_flag=1
                
                # Forward traversal
                Step=i-1
                while Step>0:
                    Step_count=Step_count+1
                    if New_data_info[Step]>New_data_info[Step-1]:
                        Step=Step-1
                    elif New_data_info[Step]==0:
                        Step=Step+1
                        break
                    else:
                        Peak_flag=0
                        break
                    
                    
                if Step_count<4 or Step_count>14:
                    continue
                if Peak_flag==0:
                    continue
                
                Start_location=Step
                
                # Backward traversal
                Step=i+1
                while Step<len(New_data_info)-1:
                    Step_count=Step_count+1
                    if New_data_info[Step]>New_data_info[Step+1]:
                        Step=Step+1
                    elif New_data_info[Step]==0:
                        Step=Step-1
                        break
                    else:
                        Peak_flag=0
                        break
                
                End_location=Step
                
                # Conditional screening
                if Peak_flag==1 and Step_count<=120 and New_data_info[i]<(10000/1.46):
                    Peak_count=Peak_count+1
                    
                elif Peak_flag==0 and Step_count<=120 and New_data_info[i]<(10000/1.46):

                    if Left_1_Peak_flag==1 and Left_0_Peak_flag==0:
                        
                        if np.max(Data_info[Continuity_start_1_location:Continuity_end_1_location])>21:
                            if np.max(Data_info[Continuity_start_0_location:Continuity_end_0_location])>15:
                                if np.max(Data_info[Start_location:End_location])>15:
                                    
                                    if Continuity_end_0_location-Continuity_start_0_location>7:
                                        if Continuity_end_1_location-Continuity_start_1_location>7:
                                            if End_location-Start_location>7:
                                                
                                                Image_count=Image_count+1
                                                Continuity_Data_info=Data_info[Continuity_start_0_location:End_location]
                                                fig=plt.figure()
                                                plt.plot(np.arange(0,Continuity_Data_info.shape[0],1)/60,Continuity_Data_info*1.46*10**7,color='blue')
                                                y_ticks=np.array(plt.yticks()[0])
                                                new_y_ticks=list(map(lambda x:f'{x:e}'.split('e'),y_ticks))
                                                new_y_ticks=list(map(lambda x:f'${float(x[0])}*{{10}}^{{{int(x[1])}}}$',new_y_ticks))
                                                # new_y_ticks[0]='0'
                                                plt.ylim(bottom=0)
                                                # plt.yticks(y_ticks,new_y_ticks)
                                                
                                                plt.xlabel(' Time(s) ')
                                                plt.ylabel('$ Bioluminescence Intensity (photons s^{-1}) $')
                                                plt.savefig(os.path.join(Sub_result_path,f'{Dat_name}_{Image_count}.png'))
                                                plt.clf()
                                                
                                                
                        
                                                print('Yes 1')
                    elif Left_1_Peak_flag==0 and Left_0_Peak_flag==1:
                        if np.max(Data_info[Continuity_start_0_location:Continuity_end_0_location])>21:
                            if np.max(Data_info[Continuity_start_1_location:Continuity_end_1_location])>15:
                                if np.max(Data_info[Start_location:End_location])>15:
                                    
                                    if Continuity_end_0_location-Continuity_start_0_location>7:
                                        if Continuity_end_1_location-Continuity_start_1_location>7:
                                            if End_location-Start_location>7:
                                                
                                                Image_count=Image_count+1
                                                Continuity_Data_info=Data_info[Continuity_start_0_location:End_location]
                                                fig=plt.figure()
                                                plt.plot(np.arange(0,Continuity_Data_info.shape[0],1)/60,Continuity_Data_info*1.46*10**7,color='blue')
                                                y_ticks=np.array(plt.yticks()[0])
                                                new_y_ticks=list(map(lambda x:f'{x:e}'.split('e'),y_ticks))
                                                new_y_ticks=list(map(lambda x:f'${float(x[0])}*{{10}}^{{{int(x[1])}}}$',new_y_ticks))
                                                # new_y_ticks[0]='0'
                                                plt.ylim(bottom=0)
                                                # plt.yticks(y_ticks,new_y_ticks)
                                                
                                                plt.xlabel(' Time(s) ')
                                                plt.ylabel('$ Bioluminescence Intensity (photons s^{-1}) $')
                                                plt.savefig(os.path.join(Sub_result_path,f'{Dat_name}_{Image_count}.png'))
                                                plt.clf()
                                                
                                                print('Yes 2')
                                        

                Left_0_Peak_flag=Left_1_Peak_flag
                Continuity_start_0_location=Continuity_start_1_location
                Continuity_end_0_location=Continuity_end_1_location
                
                Left_1_Peak_flag=Peak_flag
                Continuity_start_1_location=Start_location
                Continuity_end_1_location=End_location
                    

                        
                        
                    

                        
                    
                    
                    
                    
                    
        
        # if Peak_count>1:
        #     fig=plt.figure()
        #     plt.plot(np.arange(0,Data_info.shape[0],1),Data_info)
        #     plt.xlabel(' Time(s) ')
        #     plt.ylabel('$ Bioluminescence Intensity (photons s^-1) $')
        #     plt.savefig(os.path.join(Sub_result_path,f'{Dat_name}.png'))
        #     plt.clf()
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        