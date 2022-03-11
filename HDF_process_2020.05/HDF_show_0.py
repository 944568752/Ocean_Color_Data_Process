import os
#处理文件和目录
import re
#正则表达式库
import csv
#处理csv文件
import numpy as np
#用于数组运算
import datetime
#用来处理时间与日期
import matplotlib
#数据可视化库
matplotlib.use('Agg')
#不画图，只写文件
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
#绘图函数的相关函数
import base64
#二进制数据转换为普通字符串
import io
#用来进行输入输出操作
import h5py
#操作HDF5文件
from netCDF4 import Dataset
#解析nc文件分析其数据结构

class multidict(dict):
    #多重字典类
    def __getitem__(self, item):
        #获得项目
        try:
            return dict.__getitem__(self, item)
            #让对象实现迭代功能
        except KeyError:
            value = self[item] = type(self)()
            return value


Data_Attr = {'Chlor_a': {'ARONET_Name' : 'hlorophyll-a','Unit':'(mg/m^3)' },
             'aot': {'ARONET_Name' : 'erosol_Optical_Depth','Unit':'' },
            'nLw': {'ARONET_Name' : 'wn_f','Unit':'(mw/(cm^2 sr um))' },
            'Rrs': {'ARONET_Name' : 'wn_f','Unit':'(1/sr)' }
             }
#字典Data_Attr

F0 = {
    '1020': 68.9267,
    '870': 97.0437,
    '865':95.9955,
    '779': 116.9842,
    '709': 139.6457,
    '681': 147.4890,
    '675': 148.7164,
    '667': 151.7730,
    '620': 167.4744,
    '560': 176.7558,
    '555': 188.2640,
    '551': 186.1380,
    '532': 190.0784,
    '531': 191.4176,
    '510': 189.8667,
    '500': 193.3927,
    '490': 202.6040,
    '443': 195.4065,
    '440': 182.4854,
    '412': 167.2800,
    '400': 173.9175,
    '380': 117.1379,
    '340': 107.8918

}
#字典F0


font1 = {
'size'   : 15,
}
#字典font1

#检验数据是否有效
#输入：数据属性字典，数据
#输出：数据有效为1  无效为0
def Check_Data(Data):
    Inval = str('-999.')
    # Data = np.array(list(map(float, Data)))
    if np.sum(Data == Inval) == len(Data):
        #np.sum求数组元素之和
        return 0
    else:
        return 1

#按照名称读取ARONET文件
def Get_Sta_file(Import_name,Data_Path):
    Sta_file_Path = []
    files = os.listdir(Data_Path)
    #返回指定文件夹包含的文件的列表
    for file in files:
        if Import_name in file:
            tmp = file.split('(')
            name = tmp[0]
            Location = tmp[1]
            Sta_file_Path.append(os.path.join(Data_Path,file))
            #路径拼接并存入数组中
            lat = round(float(re.findall("\d+\.?\d+",Location.split(',')[0])[0]),3)
            lon = round(float(re.findall("\d+\.?\d+",Location.split(',')[1])[0]),3)
            #round返回浮点数的四舍五入值
    return Sta_file_Path,lon,lat

def Get_Valid_Range(date1,date2,csv_data,Data_type):
    csv_Example_Arrribute = csv_data[0, :]
    csv_Example = csv_data[1:, :]
    All_Invalid_Data_Index = []
    for i in range(5,len(csv_Example[0]),1):
        if not(Check_Data(csv_Example[:,i])):
            All_Invalid_Data_Index.append(i)

    # All_Invalid_Data_Index = np.where(np.array(csv_Example) == str('-999.'))
    Valid_Sta_Data = np.delete(csv_data, list(All_Invalid_Data_Index), axis=1)
    #删除指定列
    csv_Data_Attributes = Valid_Sta_Data[0, :]
    Valid_Sta_Data = Valid_Sta_Data[1:, :]

    All_Plt_Data_Column = []
    for Data_Attribute in csv_Data_Attributes:
        if Data_Attr[Data_type]['ARONET_Name'] in Data_Attribute:
            All_Plt_Data_Column.append(np.argwhere(csv_Data_Attributes == Data_Attribute)[0][0])
            #返回非零的数组元素的索引
    Start_Date_tmp = datetime.datetime.strptime(date1, '%Y-%m-%d')
    End_Date_tmp = datetime.datetime.strptime(date2, '%Y-%m-%d')
    #日期格式转化为字符串格式

    All_Sta_Date = list(Valid_Sta_Data[:, 1])
    Sta_Date_Tran = []
    Plt_Date = []
    All_Sta_Time = Valid_Sta_Data[:, 2]
    for i in range(len(All_Sta_Date)):
        Date_Tran = datetime.datetime.strptime(All_Sta_Date[i], '%d:%m:%Y')
        Plt_Date.append(Date_Tran)
        if Date_Tran >= Start_Date_tmp and Date_Tran <= End_Date_tmp:
            Sta_Date_Tran.append(i)
    if len(Sta_Date_Tran) == 0:
        All_Plt_Data_Row = []
        Data_Range = []
    else:
        All_Plt_Data_Row = [min(Sta_Date_Tran), max(Sta_Date_Tran)]
        if Start_Date == End_Date:
            Data_Range = np.array(All_Sta_Time[All_Plt_Data_Row[0]:All_Plt_Data_Row[1]+1])
            #创建数组
        else:
            Data_Range = np.array(Plt_Date[All_Plt_Data_Row[0]:All_Plt_Data_Row[1]+1])
    return All_Plt_Data_Row,All_Plt_Data_Column,Valid_Sta_Data,csv_Data_Attributes,Data_Range

#在只显示一天的时候，需要将时间准换成小数形式作为坐标轴
def Get_Day_Time(Times):
    Plt_time = []
    for time in Times:
        tmp = time.split(':')
        hour = int(tmp[0])
        minute = float(tmp[1])
        second = float(tmp[2])
        Plt_time.append(round(hour + (minute * 60 + second)/3600,2))
    Plt_time = np.array(Plt_time)
    return Plt_time

#读取计算Rrs需要的F0
def Get_F0(F0_Dir,wave,Plt_Sta_Data):
    All_F0_Data = open(F0_Dir, 'r').readlines()
    #打开F0_Dir，读取所有行并返回链表
    Index = All_F0_Data.index('/end_header\n')
    #检查字符串中是否包含子字符串
    F0_Data = np.array(All_F0_Data[Index + 1:])
    F0_Wave = []
    F0_D = []
    for F0_Single in F0_Data:
        F0_Single = F0_Single.rstrip('\n')
        #去掉字符串右边的"\n"
        tmp = F0_Single.split(' ')
        #按空格分割
        F0_Wave.append(int(tmp[0]))
        F0_D.append(float(tmp[1]))
    Index_Wave = F0_Wave.index(wave)
    F0_Y = F0_D[Index_Wave]
    Plt_Sta_Data = Plt_Sta_Data / F0_Y
    return Plt_Sta_Data
    # 读取对应波长的F0，将ARONET-OC的nl数据转成Rrs



Sta_Name = 'Galata_Platform'
Start_Date = '2019-03-08'
End_Date = '2019-03-08'
Data_Type = 'Rrs'

def Plt_Out(Sta_Name,Start_Date,End_Date,Data_Type):
    OutPut = multidict()
    OutPut['Status'] = 1
    OutPut['Error'] = ''

    Data_Path = r'D:\Data\HOCVAL\All'
    F0_Dir = r'D:\Data\HOCVAL\F0.dat'
    aot_dir = r'D:\Data\卫星中心\out\out\tmp'



    All_Sta_Files,Lon,Lat = Get_Sta_file(Sta_Name,Data_Path)
    OutPut['Location'] = [Lon,Lat]
    for Sta_File in All_Sta_Files:
        with open(Sta_File, encoding='utf-8') as f:
            csv_Data = []
            reader = csv.reader(f)
            #创建并读取一个csv文件
            for Row in reader:
                if len(Row) > 5:
                    csv_Data.append(Row)
            csv_Data = np.array(csv_Data)
            Valid_Row_Range , Valid_Columns ,All_Data ,Data_Attributes,Plt_Date= Get_Valid_Range(Start_Date,End_Date,csv_Data,Data_Type)
            if len(Valid_Row_Range) == 0:
                OutPut['Status'] = 0
                OutPut['Error'] = 'No Satisfactory Data  '
            else:
                if Start_Date == End_Date:
                    # Plt_Date = Get_Day_Time(Plt_Date)
                    Day_Datas = All_Data[Valid_Row_Range[0]:Valid_Row_Range[1]+1]
                    fig = plt.figure()
                    plt.xlabel('WaveLength(nm)')
                    plt.ylabel('Rrs(1/sr)')
                    plt.title(Start_Date)
                    Color_ID = 1
                    for Day_Data in Day_Datas:

                        wave_plt = []
                        data_plt = []
                        for column in Valid_Columns:
                            wave = int(re.findall("\d+", Data_Attributes[column])[0])
                            wave_plt.append(wave)
                            data = (float(Day_Data[column]) / F0[str(wave)]) /10
                            data_plt.append(data)
                        # plt.plot(wave_plt, data_plt, color=(1, (19 - Color_ID) / 19, 1), label=Day_Data[2])
                        # plt.scatter(wave_plt, data_plt,color=(1,(19 - Color_ID) /19,1))
                        plt.plot(wave_plt, data_plt, color=(1, (len(Day_Datas) - Color_ID) / len(Day_Datas), 1), label=Day_Data[2])
                        plt.scatter(wave_plt, data_plt, color=(1, (len(Day_Datas) - Color_ID) / len(Day_Datas), 1))
                        Color_ID += 1
                        plt.legend(fontsize = 7)
                        canvas = fig.canvas
                        buffer = io.BytesIO()
                        canvas.print_png(buffer)
                        data = buffer.getvalue()
                        Img_64 = base64.b64encode(data)
                        Img_64_Str = Img_64.decode()
                        buffer.close()
                        OutPut['Pic']['Spec'] = Img_64_Str
                    plt.savefig(r'C:\Users\86152\Desktop\222.jpg')

                elif Sta_Name == 'Platform_Dongou' and Data_Type == 'aot':
                    aot_column = [4,13,14,16]
                    aot_wave = [412,443,490,1020]
                    aot_name = ['aot_412','aot_443','aot_490','aot_1020']
                    with open(aot_dir, encoding='utf-8') as f1:
                        aot_data = []
                        reader = csv.reader(f1)
                        for Row in reader:
                            aot_data.append(Row)
                        aot_data = np.array(aot_data)
                        aot_time = aot_data[:,0]
                        aot_time = list(aot_time)
                        Plt_Date = []
                        for i in range(len(aot_time)):
                            Date_Tran = datetime.datetime.strptime(aot_time[i], '%d:%m:%Y')
                            Plt_Date.append(Date_Tran)
                        Plt_Date = np.array(Plt_Date)
                        for i in range(len(aot_column)):
                            plt_data = aot_data[:,aot_column[i]]
                            index = np.where(plt_data != 'N/A')
                            aot_plt_data = plt_data[index]
                            aot_plt_time_tmp = Plt_Date[index]
                            aot_plt_data = np.array(list(map(float,aot_plt_data)))
                            fig = plt.figure(figsize=(10, 4))
                            plt.ylim(0,0.8)
                            plt.xlim(datetime.datetime.strptime(Start_Date, '%Y-%m-%d'),datetime.datetime.strptime(End_Date, '%Y-%m-%d'))
                            plt.ylabel('aot')
                            plt.xlabel('Date')
                            plt.title(Sta_Name + ':(aot)' + Start_Date + '-' + End_Date + '(' + str(aot_wave[i]) + 'nm)')
                            plt.plot(aot_plt_time_tmp, aot_plt_data, linewidth=0.4, color='silver')
                            plt.scatter(aot_plt_time_tmp, aot_plt_data, marker='.', s=4, color='k')
                            # plt.savefig()
                            path = os.path.join(r'C:\Users\86152\Desktop', 'aot'+ str(aot_wave[i]) + '.png')
                            plt.savefig(path)
                            plt.close(fig)
                            plt.cla()
                            canvas = fig.canvas
                            buffer = io.BytesIO()
                            canvas.print_png(buffer)
                            data = buffer.getvalue()
                            Img_64 = base64.b64encode(data)
                            Img_64_Str = Img_64.decode()
                            buffer.close()
                            OutPut['Pic'][aot_name[i]] = Img_64_Str
                else:
                    Name = []
                    for column in Valid_Columns:
                        Plt_Data = All_Data[Valid_Row_Range[0]:Valid_Row_Range[1]+1,column]
                        Plt_Data = np.array(list(map(float,Plt_Data)))
                        Plt_Valid_Index = np.where(Plt_Data == -999)
                        if len(Plt_Valid_Index[0]) == len(Plt_Data):
                            pass
                        else:
                            fig = plt.figure(figsize=(10, 4))

                            Data_Name = Data_Attributes[column]
                            if Data_Type == 'Chlor_a':
                                pass
                                Data_Wave = ''
                                plt.title(Sta_Name + ':(' + Data_Type + ')' + Start_Date + '-' + End_Date  + Data_Name)
                            else:
                                Data_Wave = int(re.findall("\d+", Data_Name)[0])
                                plt.title(Sta_Name + ':(' + Data_Type + ')' + Start_Date + '-' + End_Date + '(' + str(Data_Wave) + 'nm)')
                            Plt_Valid_Data = np.delete(Plt_Data, list(Plt_Valid_Index), axis=0)
                            if 'Rrs' in Data_Type:
                                Plt_Valid_Data = Get_F0(F0_Dir,Data_Wave,Plt_Valid_Data)
                                # Data_Name = 'Lwn_f/Q[' + str(Data_Wave).zfill(4) + 'nm]'
                                Data_Name = 'Rrs_' + str(Data_Wave)
                            if 'aot' in Data_Type:
                                Plt_Valid_Data = Get_F0(F0_Dir, Data_Wave, Plt_Valid_Data)
                                Data_Name = 'aot_' + str(Data_Wave)
                            Plt_Valid_Date = np.delete(Plt_Date, list(Plt_Valid_Index), axis=0)
                            if 'Chlor_a' == Data_Type:
                                Plt_Valid_Data = np.log10(Plt_Valid_Data)
                            else:
                                limit = np.max(Plt_Valid_Data)
                                Ndelta, Xdelta = np.histogram(Plt_Valid_Data, range=(0, limit), bins=500)
                                Index = np.argwhere(Ndelta == np.max(Ndelta))[0, 0]
                                ylim = Xdelta[Index + 1] * 1.5
                                plt.ylabel(Data_Attr[Data_Type]['Unit'])
                                ymax = ylim *5
                                if  ymax<0.05:
                                    ymax = 0.05

                            if Start_Date == End_Date:
                                plt.xlabel('Time')
                                plt.xlim(0,24)
                            else:
                                plt.xticks(rotation=15)
                                plt.xlim(datetime.datetime.strptime(Start_Date, '%Y-%m-%d'),
                                                  datetime.datetime.strptime(End_Date, '%Y-%m-%d'))
                            # plt.plot(Plt_Valid_Date, Plt_Valid_Data, linewidth=0.4, color='silver')
                            if Sta_Name == 'Platform_Dongou':
                                plt.ylim(-0.05, 0.1)
                                Plt_Valid_Data = Plt_Valid_Data / 10
                                plt.plot(Plt_Valid_Date, Plt_Valid_Data, linewidth=0.4, color='silver')
                                plt.scatter(Plt_Valid_Date, Plt_Valid_Data, label='Dongou',marker='.', s = 4,color='k')
                            else:
                                # plt.ylim(-0.05, ymax)
                                plt.plot(Plt_Valid_Date, Plt_Valid_Data, linewidth=0.4, color='silver')
                                plt.scatter(Plt_Valid_Date, Plt_Valid_Data, label='AERONET-OC', marker='.', s=4, color='k')


                            plt.legend()
                            canvas = fig.canvas
                            buffer = io.BytesIO()
                            canvas.print_png(buffer)
                            data = buffer.getvalue()
                            Img_64 = base64.b64encode(data)
                            Img_64_Str = Img_64.decode()
                            buffer.close()
                            OutPut['Pic'][Data_Name] = Img_64_Str
                            path = os.path.join(r'C:\Users\86152\Desktop',str(Data_Wave) + '.jpg')
                            plt.savefig(path)
                            plt.close(fig)
                            plt.cla()
                            print(Data_Name + ':Single Data Time Series Picture Drawing Completed')

    return OutPut

if __name__ == "__main__":
    Result = Plt_Out(Sta_Name,Start_Date,End_Date,Data_Type)