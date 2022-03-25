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

def select_stocks():
    data = finance.get_stock_list()
    code_list = data['code'].to_list()[:-10]
    num = len(code_list)
    select_list = []
    pos = 0
    num_got = 0
    for item in code_list:
        if check_stock(item):
            select_list.append(item)
            num_got = num_got + 1
        pos = pos + 1
        print(str(pos) + '/' + str(num) + '  ' + str(num_got) + 'got')
        
    select_data = []
    for item in select_list:
        data = finance.get_stock_basic(item)
        data['recommend'] = get_recommend_price(item)
        select_data.append(data)

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

def get_recommend_price(stock_code):
    df = finance.get_stock_kline(stock_code)
    price = df['close'].to_list()[-1]
    gs_data = trendline.golden_snipe(df)
    for i in range(5):
        if price > gs_data[6 - i]:
            return gs_data[6 - i]
    return 0

if __name__ == '__main__':
    select_stocks()
