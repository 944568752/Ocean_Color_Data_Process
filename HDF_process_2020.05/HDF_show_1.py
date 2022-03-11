import sys
import csv
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
import base64
import io
import zipfile
import math
import time
import re

class multidict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def Get_Measure_Data(all_data):
    out_data = multidict()
    out_units = multidict()
    data_index = 0
    for i in range(len(all_data)):
        all_data[i] = all_data[i].strip('\n')
        if '/fields' in all_data[i]:
            all_fileds = all_data[i].split('=')[1]
            fields = all_fileds.split(',')
        if '/units' in all_data[i]:
            all_units = all_data[i].split('=')[1]
            units = all_units.split(',')
        if '/end_header' in all_data[i]:
            data_index = i
        if i > data_index:
            all_data[i] = all_data[i].split(' ')
    data = np.array(all_data[data_index+1:])
    measure_date = list(data[:,0])
    measure_time = list(data[:,1])
    for i in range(2,len(fields),1):
        out_data[fields[i]] = list(data[:,i])
        out_units[fields[i]] = units[i]
    return measure_date,measure_time,out_data,out_units

def Get_Seconds(times):
    match_time = []
    for time in times:
        match_time.append(int(str(time)[0:2]) * 3600 + int(str(time)[2:4]) * 60 + int(str(time)[4:6]))
    return match_time

cocts_wave = [412,443,490,520,565,670,750,865]


Sta_Name = 'Dongou'
# Sta_Name = 'YanTai_3'
# Sta_Name = 'Dongou'
Start_Date = '2020-04-15'
End_Date = '2020-04-15'
Data_Type = 'aot'

def Plt_Out(Sta_Name,Start_Date,End_Date,Data_Type):
    OutPut = multidict()
    OutPut['Status'] = 1
    OutPut['Error'] = ''
    if Sta_Name == 'YanTai_1':
        OutPut['Type'] = ['AOT','nLw','Rrs']
        Data_Path = r'D:\Data\HOCVAL\All\H1591TV12OC'
        Measure_Data = {
            'aotdate' : [],
            'aottime' : [],
            'ocrdate': [],
            'ocrtime': [],
            'AOT1020': [],
            'AOT865': [],
            'AOT779': [],
            'AOT667': [],
            'AOT620': [],
            'AOT560': [],
            'AOT510': [],
            'AOT490': [],
            'AOT442': [],
            'AOT412': [],
            'AOT400': [],
            'nLw1020': [],
            'nLw865': [],
            'nLw779': [],
            'nLw667': [],
            'nLw620': [],
            'nLw560': [],
            'nLw510': [],
            'nLw490': [],
            'nLw442': [],
            'nLw412': [],
            'nLw400': [],
            'Rrs1020': [],
            'Rrs865': [],
            'Rrs779': [],
            'Rrs667': [],
            'Rrs620': [],
            'Rrs560': [],
            'Rrs510': [],
            'Rrs490': [],
            'Rrs442': [],
            'Rrs412': [],
            'Rrs400': [],
        }
        Measure_units =  {
            'AOT1020': '1/m',
            'AOT865': '1/m',
            'AOT779': '1/m',
            'AOT667': '1/m',
            'AOT620': '1/m',
            'AOT560': '1/m',
            'AOT510': '1/m',
            'AOT490': '1/m',
            'AOT442': '1/m',
            'AOT412': '1/m',
            'AOT400': '1/m',
            'nLw1020': 'W/m².sr.nm',
            'nLw865': 'W/m².sr.nm',
            'nLw779': 'W/m².sr.nm',
            'nLw667': 'W/m².sr.nm',
            'nLw620': 'W/m².sr.nm',
            'nLw560': 'W/m².sr.nm',
            'nLw510': 'W/m².sr.nm',
            'nLw490': 'W/m².sr.nm',
            'nLw442': 'W/m².sr.nm',
            'nLw412': 'W/m².sr.nm',
            'nLw400': 'W/m².sr.nm',
            'Rrs1020': '1/Sr',
            'Rrs865': '1/Sr',
            'Rrs779': '1/Sr',
            'Rrs667': '1/Sr',
            'Rrs620': '1/Sr',
            'Rrs560': '1/Sr',
            'Rrs510': '1/Sr',
            'Rrs490': '1/Sr',
            'Rrs442': '1/Sr',
            'Rrs412': '1/Sr',
            'Rrs400': '1/Sr',
        }

    elif Sta_Name == 'YanTai_2':
        OutPut['Type'] = ['AOT']
        Data_Path = r'D:\Data\HOCVAL\All\H1626TS'
        Measure_Data = {
            'aotdate': [],
            'aottime': [],
            'ocrdate': [],
            'ocrtime': [],
            'AOT1020': [],
            'AOT870': [],
            'AOT675': [],
            'AOT440': [],
            'AOT500': [],
            'AOT380': [],
            'AOT340': []
        }
        Measure_units = {
            'date': [],
            'time': [],
            'AOT1020': '1/m',
            'AOT870': '1/m',
            'AOT675': '1/m',
            'AOT440': '1/m',
            'AOT500': '1/m',
            'AOT380': '1/m',
            'AOT340': '1/m'
        }

    elif Sta_Name == 'Dongou':
        OutPut['Type'] = ['AOT', 'nLw', 'Rrs']
        Data_Path = r'D:\Data\HOCVAL\All\H1562TV12OC'
        Measure_Data = {
            'aotdate': [],
            'aottime': [],
            'ocrdate': [],
            'ocrtime': [],
            'AOT1020': [],
            'AOT865': [],
            'AOT779': [],
            'AOT667': [],
            'AOT620': [],
            'AOT560': [],
            'AOT510': [],
            'AOT490': [],
            'AOT442': [],
            'AOT412': [],
            'AOT400': [],
            'nLw1020': [],
            'nLw865': [],
            'nLw779': [],
            'nLw667': [],
            'nLw620': [],
            'nLw560': [],
            'nLw510': [],
            'nLw490': [],
            'nLw442': [],
            'nLw412': [],
            'nLw400': [],
            'Rrs1020': [],
            'Rrs865': [],
            'Rrs779': [],
            'Rrs667': [],
            'Rrs620': [],
            'Rrs560': [],
            'Rrs510': [],
            'Rrs490': [],
            'Rrs442': [],
            'Rrs412': [],
            'Rrs400': [],
        }
        Measure_units = {
            'AOT1020': '1/m',
            'AOT865': '1/m',
            'AOT779': '1/m',
            'AOT667': '1/m',
            'AOT620': '1/m',
            'AOT560': '1/m',
            'AOT510': '1/m',
            'AOT490': '1/m',
            'AOT442': '1/m',
            'AOT412': '1/m',
            'AOT400': '1/m',
            'nLw1020': 'W/m².sr.nm',
            'nLw865': 'W/m².sr.nm',
            'nLw779': 'W/m².sr.nm',
            'nLw667': 'W/m².sr.nm',
            'nLw620': 'W/m².sr.nm',
            'nLw560': 'W/m².sr.nm',
            'nLw510': 'W/m².sr.nm',
            'nLw490': 'W/m².sr.nm',
            'nLw442': 'W/m².sr.nm',
            'nLw412': 'W/m².sr.nm',
            'nLw400': 'W/m².sr.nm',
            'Rrs1020': '1/Sr',
            'Rrs865': '1/Sr',
            'Rrs779': '1/Sr',
            'Rrs667': '1/Sr',
            'Rrs620': '1/Sr',
            'Rrs560': '1/Sr',
            'Rrs510': '1/Sr',
            'Rrs490': '1/Sr',
            'Rrs442': '1/Sr',
            'Rrs412': '1/Sr',
            'Rrs400': '1/Sr',
        }

    elif Sta_Name == 'YanTai_3':
        OutPut['Type'] = ['Lw','ES','Rrs']
        Data_Path = r'D:\Data\HOCVAL\All\Cruise'

    Start_Date_tmp = datetime.datetime.strptime(Start_Date, '%Y-%m-%d')
    End_Date_tmp = datetime.datetime.strptime(End_Date, '%Y-%m-%d')

    Data_Years = os.listdir(Data_Path)
    # OutPut = multidict()
    if Sta_Name == 'YanTai_3':
        end_time = []
        end_date = []
        end_data = []
        for Year in Data_Years:
            Data_Dates = os.listdir(os.path.join(Data_Path, Year))
            for Data_Date in Data_Dates:
                Measure_Data_tmp = datetime.datetime.strptime(Year + Data_Date, '%Y%m%d')
                if Measure_Data_tmp >= Start_Date_tmp and Measure_Data_tmp <= End_Date_tmp:
                    if os.path.isfile(os.path.join(os.path.join(os.path.join(Data_Path, Year),Data_Date),'ASS_STATION001_' + Year + Data_Date + '.txt')):
                        f = open(os.path.join(os.path.join(os.path.join(Data_Path, Year),Data_Date),'ASS_STATION001_' + Year + Data_Date + '.txt'),'r',encoding='utf-8')
                        File_Datas = f.readlines()
                        f.close()
                        if len(File_Datas) > 0:
                            if File_Datas[-1] == '/end_header\n':
                                pass
                            else:
                                flag = File_Datas.index('/end_header\n')
                                fields = File_Datas[flag - 4].strip('\n').split('=')[1].split(',')
                                units = File_Datas[flag - 3].strip('\n').split('=')[1].split(',')
                                all_datas = File_Datas[flag + 1:]
                                for i in range(len(all_datas)):
                                    all_datas[i] = list(map(float, all_datas[i].strip('\n').split(' ')))

                                all_datas = np.array(all_datas)
                                ocr_data = all_datas[:, 2:]
                                measure_time = all_datas[:, 0]
                                measure_date = all_datas[:, 1]
                                measure_time_flag = list(map(int, measure_time))
                                time_flags = np.array(Get_Seconds(measure_time_flag))
                                tmp_index = 0
                                while tmp_index != len(time_flags):
                                    start = time_flags[tmp_index]
                                    find_index = np.where((time_flags < (start + 900)) & (time_flags >= start))
                                    if start > 32400 and start < 57600:
                                        end_time.append(measure_time[tmp_index])
                                        end_date.append(measure_date[tmp_index])
                                        tmp = ocr_data[find_index]
                                        tmp_mean = tmp.mean(axis=0)
                                        end_data.append(list(tmp_mean))
                                    tmp_index = np.max(find_index[0]) + 1
        if Start_Date == End_Date:
            plt_wave = np.arange(325,945,1)
            fig = plt.figure()
            plt.xlabel('WaveLength(nm)')
            plt.ylabel('Rrs(1/sr)')
            plt.title(Start_Date)
            Color_ID = 1
            for i in range(len(end_data)):
                plt.plot(plt_wave, end_data[i][1240:], color=(1, ( Color_ID) / len(end_data), 1),label=str(int(end_date[i])) + str(int(end_time[i])))
                # plt.scatter(plt_wave, end_data[i][1240:], s = 10,color=(1, (Color_ID) / 19, 1))
                Color_ID += 1
                plt.legend(fontsize=7)
                canvas = fig.canvas
                buffer = io.BytesIO()
                canvas.print_png(buffer)
                data = buffer.getvalue()
                Img_64 = base64.b64encode(data)
                Img_64_Str = Img_64.decode()
                buffer.close()
                OutPut['Pic']['Spec_Rrs'] = Img_64_Str
            # plt.savefig(r'C:\Users\86152\Desktop\333.jpg')
            fig = plt.figure()
            plt.xlabel('WaveLength(nm)')
            plt.ylabel('Lw(mW/m^2/nm/sr)')
            plt.title(Start_Date)
            Color_ID = 1
            for i in range(len(end_data)):
                plt.plot(plt_wave, end_data[i][0:620], color=(1, (Color_ID) / len(end_data), 1),
                         label=str(int(end_date[i])) + str(int(end_time[i])))
                # plt.scatter(plt_wave, end_data[i][1240:], s = 10,color=(1, (Color_ID) / 19, 1))
                Color_ID += 1
                plt.legend(fontsize=7)
                canvas = fig.canvas
                buffer = io.BytesIO()
                canvas.print_png(buffer)
                data = buffer.getvalue()
                Img_64 = base64.b64encode(data)
                Img_64_Str = Img_64.decode()
                buffer.close()
                OutPut['Pic']['Spec_Lw'] = Img_64_Str
            # plt.savefig(r'C:\Users\86152\Desktop\444.jpg')
            fig = plt.figure()
            plt.xlabel('WaveLength(nm)')
            plt.ylabel('Es(mW/m^2/nm)')
            plt.title(Start_Date)
            Color_ID = 1
            for i in range(len(end_data)):
                plt.plot(plt_wave, end_data[i][620:1240], color=(1, (Color_ID) / len(end_data), 1),
                         label=str(int(end_date[i])) + str(int(end_time[i])))
                # plt.scatter(plt_wave, end_data[i][1240:], s = 10,color=(1, (Color_ID) / 19, 1))
                Color_ID += 1
                plt.legend(fontsize=7)
                canvas = fig.canvas
                buffer = io.BytesIO()
                canvas.print_png(buffer)
                data = buffer.getvalue()
                Img_64 = base64.b64encode(data)
                Img_64_Str = Img_64.decode()
                buffer.close()
                OutPut['Pic']['Spec_Es'] = Img_64_Str
            # plt.savefig(r'C:\Users\86152\Desktop\555.jpg')
        else:
            end_data = np.array(end_data)
            plt_date = np.array(list(map(lambda x: datetime.datetime.strptime(x, '%Y%m%d'), list(map(str,map(int,end_date))))))
            series = ['Lw','ES','Rrs']
            for wave in cocts_wave:
                for serie in series:
                    index = fields.index(serie + str(float(wave)))
                    plt_data = end_data[:,index-2]
                    fig = plt.figure(figsize=(10, 4))
                    plt.xlim(datetime.datetime.strptime(Start_Date, '%Y-%m-%d'),
                             datetime.datetime.strptime(End_Date, '%Y-%m-%d'))
                    plt.ylabel(serie + str(wave) + '(' + units[index] + ')')
                    plt.xlabel('Date')
                    plt.title(Sta_Name + ':' + Start_Date + '-' + End_Date + '(' + serie + str(wave) + ')')
                    plt.plot(plt_date, plt_data, linewidth=0.4, color='silver')
                    plt.scatter(plt_date, plt_data, marker='.', s=4, color='k')
                    # plt.savefig()
                    path = os.path.join(r'C:\Users\86152\Desktop', serie + str(wave) + '.png')
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
                    OutPut['Pic'][serie + str(wave)] = Img_64_Str
        for k in list(OutPut['Pic'].keys()) :
            if k == 'Spec':
                pass
            elif Data_Type not in k:
                del OutPut['Pic'][k]
        return OutPut

    else:
        for Year in Data_Years:
            Data_Dates = os.listdir(os.path.join(Data_Path,Year))
            for Data_Date in Data_Dates:
                Measure_Data_tmp = datetime.datetime.strptime(Year + Data_Date, '%Y%m%d')
                if Measure_Data_tmp >= Start_Date_tmp and Measure_Data_tmp <= End_Date_tmp:
                    Data_files = os.listdir(os.path.join(os.path.join(Data_Path,Year),Data_Date))
                    if len(Data_files) > 0:
                        for Data_file in Data_files:
                            if 'CEAOT' in Data_file:
                                f = open(os.path.join(os.path.join(os.path.join(Data_Path,Year),Data_Date),Data_file),'r',encoding='utf-8')
                                Measure_File_Datas= f.readlines()
                                f.close()
                                date,time,data,units = Get_Measure_Data(Measure_File_Datas)
                                Measure_Data['aotdate'] = Measure_Data['aotdate'] + date
                                Measure_Data['aottime'] = Measure_Data['aottime'] + time
                                for k in data:
                                    Measure_Data[k] = Measure_Data[k] + data[k]
                                    Measure_units[k] = units[k]
                            if 'CEOCR' in Data_file:
                                f = open(os.path.join(os.path.join(os.path.join(Data_Path, Year), Data_Date), Data_file), 'r',encoding='utf-8')
                                Measure_File_Datas = f.readlines()
                                f.close()
                                date, time, data,units = Get_Measure_Data(Measure_File_Datas)
                                Measure_Data['ocrdate'] = Measure_Data['ocrdate'] + date
                                Measure_Data['ocrtime'] = Measure_Data['ocrtime'] + time
                                for k in data:
                                    Measure_Data[k] = Measure_Data[k] + data[k]
                                    Measure_units[k] = units[k]
                    else:
                        pass


        Plt_aot_Date = np.array(Measure_Data['aotdate'])
        Plt_ocr_Date = np.array(Measure_Data['ocrdate'])
        Plt_aot_Time = np.array(Measure_Data['aottime'])
        Plt_ocr_Time = np.array(Measure_Data['ocrtime'])
        if Start_Date == End_Date:
            Plt_aot_Date = np.array(list(map(lambda x,y: datetime.datetime.strptime(x+'-' + y,'%Y%m%d-%H%M%S'),Plt_aot_Date,Plt_aot_Time)))
            Plt_ocr_Date = np.array(list(map(lambda x,y: datetime.datetime.strptime(x+'-'+y,'%Y%m%d-%H%M%S'),Plt_ocr_Date,Plt_ocr_Time)))
        else:
            Plt_aot_Date = np.array(list(map(lambda x: datetime.datetime.strptime(x, '%Y%m%d'), Plt_aot_Date)))
            Plt_ocr_Date = np.array(list(map(lambda x: datetime.datetime.strptime(x, '%Y%m%d'), Plt_ocr_Date)))
        # Plt_Date = datetime.datetime.strptime(Plt_Date, '%Y%m%d')

        for k in Measure_Data:
            if 'date' in k or 'time' in k:
                pass
            elif 'AOT' in k:
                fig = plt.figure(figsize=(10, 4))
                # plt.ylim(0, 0.8)
                if Start_Date == End_Date:
                    plt.xlim(datetime.datetime.strptime(Start_Date + '-000000', '%Y-%m-%d-%H%M%S'),datetime.datetime.strptime(End_Date + '-235959', '%Y-%m-%d-%H%M%S'))
                else:
                    plt.xlim(datetime.datetime.strptime(Start_Date, '%Y-%m-%d'), datetime.datetime.strptime(End_Date, '%Y-%m-%d'))
                plt.ylabel(k + '(' + Measure_units[k]+')')
                plt.xlabel('Date')
                plt.title(Sta_Name + ':'+ Start_Date + '-' + End_Date + '(' +k+')')
                plt.plot(Plt_aot_Date, np.array(list(map(float,Measure_Data[k]))), linewidth=0.4, color='silver')
                plt.scatter(Plt_aot_Date, np.array(list(map(float,Measure_Data[k]))), marker='.', s=4, color='k')
                # plt.savefig()
                # path = os.path.join(r'C:\Users\86152\Desktop', k + '.png')
                # plt.savefig(path)
                plt.close(fig)
                plt.cla()
                canvas = fig.canvas
                buffer = io.BytesIO()
                canvas.print_png(buffer)
                data = buffer.getvalue()
                Img_64 = base64.b64encode(data)
                Img_64_Str = Img_64.decode()
                buffer.close()
                OutPut['Pic'][k] = Img_64_Str
            else:
                fig = plt.figure(figsize=(10, 4))
                # plt.ylim(0, 0.8)
                if Start_Date == End_Date:
                    plt.xlim(datetime.datetime.strptime(Start_Date + '-000000', '%Y-%m-%d-%H%M%S'),
                             datetime.datetime.strptime(End_Date + '-235959', '%Y-%m-%d-%H%M%S'))
                else:
                    plt.xlim(datetime.datetime.strptime(Start_Date, '%Y-%m-%d'),
                             datetime.datetime.strptime(End_Date, '%Y-%m-%d'))
                plt.ylabel(k+ '(' + Measure_units[k]+')')
                plt.xlabel('Date')
                plt.title(Sta_Name + ':'+ Start_Date + '-' + End_Date + '(' +k+')')
                plt.plot(Plt_ocr_Date, np.array(list(map(float, Measure_Data[k]))), linewidth=0.4, color='silver')
                plt.scatter(Plt_ocr_Date, np.array(list(map(float, Measure_Data[k]))), marker='.', s=4, color='k')
                # plt.savefig()
                # path = os.path.join(r'C:\Users\86152\Desktop', k + '.png')
                # plt.savefig(path)
                plt.close(fig)
                plt.cla()
                canvas = fig.canvas
                buffer = io.BytesIO()
                canvas.print_png(buffer)
                data = buffer.getvalue()
                Img_64 = base64.b64encode(data)
                Img_64_Str = Img_64.decode()
                buffer.close()
                OutPut['Pic'][k] = Img_64_Str
        if Start_Date == End_Date and (Sta_Name == 'YanTai_1' or Sta_Name == 'Dongou'):
            fig = plt.figure()
            plt.xlabel('WaveLength(nm)')
            plt.ylabel('Rrs(1/sr)')
            plt.title(Start_Date)
            waves = []
            for k in Measure_Data:
                if 'Rrs' in k:
                    waves.append(int(re.findall("\d+", k)[0]))
            waves = np.array(waves)
            plt_data = []
            for wave in waves:
                plt_data.append(Measure_Data['Rrs' + str(wave)])
            plt_data = np.array(plt_data).T
            Color_ID = 1
            for i in range(len(plt_data)):

                plt.plot(waves, np.array(list(map(float,plt_data[i,:]))), color=(1, (len(plt_data) - Color_ID) / len(plt_data), 1), label=Measure_Data['ocrdate'][i] +Measure_Data['ocrtime'][i])
                plt.scatter(waves, np.array(list(map(float,plt_data[i,:]))), color=(1, (len(plt_data) - Color_ID) / len(plt_data), 1))
                Color_ID += 1
                plt.legend(fontsize=7)
                canvas = fig.canvas
                buffer = io.BytesIO()
                canvas.print_png(buffer)
                data = buffer.getvalue()
                Img_64 = base64.b64encode(data)
                Img_64_Str = Img_64.decode()
                buffer.close()
                OutPut['Pic']['Spec'] = Img_64_Str
            # plt.savefig(r'C:\Users\86152\Desktop\222.jpg')
        if Data_Type == 'aot':
            Data_Type = 'AOT'
        for k in list(OutPut['Pic'].keys()) :
            if k == 'Spec':
                pass
            elif Data_Type not in k:
                del OutPut['Pic'][k]
        return OutPut
if __name__ == "__main__":
    Result = Plt_Out(Sta_Name,Start_Date,End_Date,Data_Type)
    print('pause')
