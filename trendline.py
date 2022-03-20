# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:38:17 2020

@author: admin
"""

import finance
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt


def mainforce_monitor(data):
    data = data[::-1]
    n = 35
    m = 35
    n1 = 3
    price = pd.DataFrame()
    price['high'] = data['high'].iloc[::-1].rolling(n).max()
    price['low'] = data['low'].iloc[::-1].rolling(n).min()
    price['time'] = data['time'].iloc[::-1]
    df = pd.DataFrame()
    df = data['close']
    #p_max = price['high'].max()
    #p_min = price['low'].min()
    b1 = (price['high'] - df) / (price['high'] - price['low']) * 100 - m
    b1 = b1.dropna(axis = 0,how = 'any')
    b1 = np.around(b1, 2)
    
    b2 = sma(b1, n, 1) + 100
    b2 = np.around(b2, 2)
    b3 = (df - price['low']) / (price['high'] - price['low']) * 100
    b3 = b3.dropna(axis = 0,how = 'any')
    b3 = np.around(b3, 2)
    b4 = sma(b3, 7, 1)
    b4 = np.around(b4, 2)
    b5 = sma(b4, 5, 1) + 100
    b5 = np.around(b5, 2)
    b6 = b5 - b2
    result = b6.add(-n1) * 3.5
    result[result < 0] = 0
    result = result.iloc[::-1]
    result = result.iloc[:75]
    result = np.around(result, 2)
    return result

def mainforce_monitor_ml(data):
    n = 35
    m = 35
    n1 = 3
    price = pd.DataFrame()
    price['high'] = data['high'].iloc[::-1].rolling(n).max()
    price['low'] = data['low'].iloc[::-1].rolling(n).min()
    df = pd.DataFrame()
    df = data['close']
    #p_max = price['high'].max()
    #p_min = price['low'].min()
    b1 = (price['high'] - df) / (price['high'] - price['low']) * 100 - m
    b1 = b1.dropna(axis = 0,how = 'any')
    b1 = np.around(b1, 2)
    b2 = sma(b1, n, 1) + 100
    b2 = np.around(b2, 2)
    b3 = (df - price['low']) / (price['high'] - price['low']) * 100
    b3 = b3.dropna(axis = 0,how = 'any')
    b3 = np.around(b3, 2)
    b4 = sma(b3, 7, 1)
    b4 = np.around(b4, 2)
    b5 = sma(b4, 5, 1) + 100
    b5 = np.around(b5, 2)
    b6 = b5 - b2
    result = b6.add(-n1) * 3.5
    result = result.iloc[::-1]
    result = result.iloc[:len(data) - 99]
    result = np.around(result, 2)
    mf_result = pd.DataFrame()
    mf_result['mf_value'] = result
    trend = []
    date = []
    value1 = 0
    for index,row in mf_result.iterrows():
        date.append(index)
        if value1 > row['mf_value']:
            trend.append(1)
        else:
            trend.append(-1)
        value1 = row['mf_value']
    trend = trend[1:]
    date = date[:len(data) - 100]
    trend = trend[:len(data) - 100]
    trend_dict = {'date' : date, 'trend' : trend}
    trend_result = pd.DataFrame(trend_dict)
    trend_result = trend_result.set_index('date')
    mf_result = pd.merge(mf_result, trend_result, on='date')
    return mf_result

def ma(data, n):
    pv = pd.DataFrame()
    #pv['date'] = data['open']
    pv['ma' + str(n)] = data.iloc[::-1].close.rolling(n).mean()
    pv = np.around(pv, 2)
    return pv

def sma(data, n, m):
    df = data
    for i in range(len(data)):
        if i == 0:
            df.iloc[i] = data.iloc[i] * m / n
        else:
            df.iloc[i] = (data.iloc[i] * m + (n - m) * df.iloc[i - 1]) / n
    return df

def golden_snipe(data):
    data = data[::-1]
    price = pd.DataFrame()
    price['high'] = data['high'].iloc[3:153]
    price['low'] = data['low'].iloc[3:153]
    price['time'] = data['time'].iloc[3:153]
    p_max = price['high'].max()
    p_min = price['low'].min()
    delta_p = p_max - p_min
    p_191 = round((delta_p * 0.191 + p_min) * 100) / 100
    p_236 = round((delta_p * 0.236 + p_min) * 100) / 100
    p_382 = round((delta_p * 0.382 + p_min) * 100) / 100
    p_5 = round((delta_p * 0.5 + p_min) * 100) / 100
    p_618 = round((delta_p * 0.618 + p_min) * 100) / 100
    p_809 = round((delta_p * 0.809 + p_min) * 100) / 100
    g_list = [p_max, p_809, p_618, p_5, p_382, p_236, p_191, p_min]
    return g_list

def golden_snipe_ml(data):
    data = data[::-1]
    list_max = []
    list_809 = []
    list_618 = [] 
    list_5 = []
    list_382 = []
    list_236 = [] 
    list_191 = []
    list_min = []
    date = []
    for i in range(0, len(data)-10):
        price = pd.DataFrame()
        price['high'] = data['high'].iloc[i + 4:i + 153]
        price['low'] = data['low'].iloc[i + 4:i + 153]
        p_max = price['high'].max()
        p_min = price['low'].min()
        delta_p = p_max - p_min
        p_191 = round((delta_p * 0.191 + p_min) * 100) / 100
        p_236 = round((delta_p * 0.236 + p_min) * 100) / 100
        p_382 = round((delta_p * 0.382 + p_min) * 100) / 100
        p_5 = round((delta_p * 0.5 + p_min) * 100) / 100
        p_618 = round((delta_p * 0.618 + p_min) * 100) / 100
        p_809 = round((delta_p * 0.809 + p_min) * 100) / 100
        
        list_max.append(p_max)
        list_min.append(p_min)
        list_191.append(p_191)
        list_236.append(p_236)
        list_382.append(p_382)
        list_5.append(p_5)
        list_618.append(p_618)
        list_809.append(p_809)
    #print(p_max[:5])
    date = data.index.tolist()
    date = date[:len(data) - 100]
    g_dict = {'date' : date, 'p_max' : list_max, 'p_809' : list_809, 'p_618' : list_618, 'p_5' : list_5, 'p_382' : list_382, 'p_236' : list_236, 'p_191' : list_191, 'p_min' : list_min}
    gs_data = pd.DataFrame(g_dict)
    gs_data = gs_data.set_index('date')
    return gs_data

def mainforce_monitor_plot(data):
    ma = mainforce_monitor(data)
    ma = ma.iloc[::-1]
    ma1 = pd.DataFrame()
    ma1['kpd'] = ma
    ma1['kpcd'] = ma - 100
    ma1['kpd'][ma1['kpd'] > 100] = 100
    ma1['kpcd'][ma1['kpcd'] < 0] = 0
    ma1.plot(kind='bar', stacked = True, colormap = 'autumn_r', figsize=(12,6))
    plt.axhline(100, color='r')
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    # 将matplotlib图片转换为HTML
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd
    
if __name__ == '__main__':
    df = finance.get_stock_kline('600962')
    ma = mainforce_monitor(df)
    print(ma.to_list())
    # ma = ma[::-1]
    # # ma2 = golden_snipe(df)
    # ma1 = pd.DataFrame()
    # ma1['kpd'] = ma
    # ma1['kpcd'] = ma - 100
    # ma1['kpd'][ma1['kpd'] > 100] = 100
    # ma1['kpcd'][ma1['kpcd'] < 0] = 0
    # ma1.plot(kind='bar', stacked = True, colormap = 'autumn_r', figsize=(12,6))
    
    # plt.axhline(100, color='r')
    # plt.show()