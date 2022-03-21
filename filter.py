# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:08:33 2020

@author: admin
"""
import finance
import trendline
import pandas as pd
import time
import json
import os

def select_stocks():
    data = finance.get_stock_list()
    code_list = data['code'].to_list()[:-10]
    num = len(code_list)
    select_list = []
    #pos = 0
    #num_got = 0
    for item in code_list:
        if check_stock(item):
            select_list.append(item)
            #num_got = num_got + 1
        #pos = pos + 1
        #print(str(pos) + '/' + str(num) + '  ' + str(num_got) + 'got')
        
    select_data = []
    for item in select_list:
        select_data.append(finance.get_stock_basic(item))

    #print(select_data)
    present_time = time.strftime("%Y-%m-%d", time.localtime())
    select_data = {'date':str(present_time), 'data':select_data}
    with open('select.json', 'w') as file:
        json.dump(select_data, file)

def check_stock(stock_code):
    stock_data = finance.get_stock_basic(stock_code)
    if stock_data['name'].startswith('ST') or stock_data['name'].startswith('*ST'):
        return False
    if stock_code.startswith('SH688'):
        return False
    if stock_data['price'] > 40 or stock_data['price'] < 9:
        return False
    if stock_data['float_shares'] < 100000000:
        return False
    df = finance.get_stock_kline(stock_code)
    if(len(df) < 200):
        return False
    close_data = df['close'].to_list()[::-1]
    if (close_data[0] - close_data[3]) / close_data[3] > 0.2:
        return False
    mf_data = trendline.mainforce_monitor(df).to_list()
    if mf_data[0] < 50 or mf_data[0] < mf_data[1]:
        return False
    if mf_data[0] < 100 and mf_data[0] - mf_data[1] < 1:
        return False
    if mf_data[1] < mf_data[2] and (close_data[0] - close_data[2]) / close_data[2] > 0.1:
        return False
    gs_data = trendline.golden_snipe(df)
    if stock_data['price'] > gs_data[1] or stock_data['price'] < gs_data[6]:
        return False
    gs_range = gs_data[0] - gs_data[7]
    if (close_data[0] - close_data[3]) / gs_range > 0.35:
        return False
    if gs_range / gs_data[0] < 0.25:
        return False
    pos = (stock_data['price'] - gs_data[7]) / gs_range
    gs_list = [[0.809, 0.70], [0.618, 0.55], [0.5, 0.43], [0.382, 0.30]]
    for item in gs_list:
        if pos < item[0] and pos > item[1]:
            return False
    return True
    
def selected_evaluate(select_time):
    df = pd.read_excel('./selected/' + select_time + '.xlsx', index_col = 0, converters = {'code':str})
    current_list = []
    success_list = []
    percent_list = []
    num = 0
    #price = ts.get_realtime_quotes('600000')
    #price = '{:.2f}'.format(float(price['price'][0]))
    #print(price)
    #print(df['code'][1])
    #bar = Bar('Processing', max=len(df))
    for index,row in df.iterrows():
        code = df['code'][index]
        data = ts.get_realtime_quotes(code)
        current = '{:.2f}'.format(float(data['price'][0]))
        p_min = '{:.2f}'.format(float(data['low'][0]))
        if float(p_min) < float(df['price'][index]):
            percent = '{:.2f}'.format((float(current) - float(df['price'][index])) / float(df['price'][index]) * 100)
            if float(percent) < 0:
                success = 'N'
            else:
                success = 'Y'
                num = num + 1
        else:
            success = 'N'
            percent = 0
        if float(p_min) == 0:
            percent = 0
        current_list.append(current)
        success_list.append(success)
        percent_list.append(percent)
        #bar.next()
    df['current'] = current_list
    df['success'] = success_list
    df['percent'] = percent_list
    #bar.finish()
    print(str(num) + '/' + str(len(df)) + ' ' + str('{:.2f}'.format((num / len(df)) * 100)) + '%')
    present_time = time.strftime("%Y-%m-%d", time.localtime())
    df.to_excel('./evaluate/' + select_time + '--' + present_time + '.xlsx')

def evaluate_all():
    file_dir = './evaluate/'
    name_list = []
    present_time = time.strftime("%Y-%m-%d", time.localtime())
    for files in os.listdir(file_dir):
        file_name = os.path.splitext(files)[0]
        name_list.append(file_name)
    #print(name_list)
    for item in name_list:
        time_list = item.split('--', 1)
        if time_list[1] != present_time:
            df = pd.read_excel('./evaluate/' + item + '.xlsx', index_col = 0, converters = {'code':str})
            num = 0
            for index,row in df.iterrows():
                if df['percent'][index] != 0:
                    code = df['code'][index]
                    data = ts.get_realtime_quotes(code)
                    current = '{:.2f}'.format(float(data['price'][0]))
                    percent = '{:.2f}'.format((float(current) - float(df['price'][index])) / float(df['price'][index]) * 100)
                    if float(percent) > 0:
                        num = num + 1
                    df['current'][index] = current
                    df['percent'][index] = percent
            df.to_excel('./evaluate/' + time_list[0] + '--' + present_time + '.xlsx')
            print(time_list[0] + ':' + str(num) + '/' + str(len(df)) + ' ' + str('{:.2f}'.format((num / len(df)) * 100)) + '%')
    
                    
if __name__ == '__main__':
    select_stocks()
