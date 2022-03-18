# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:08:33 2020

@author: admin
"""
import trendline
import pandas as pd
import time
import os
#from progress.bar import Bar

def select_stocks(required_score):
    #code_list = stocks.get_all_code()
    data_list = ts.get_stock_basics()
    code_list = []
    for index,row in data_list.iterrows():
        name = row[0]
        outstanding = row[4]
        datas = (index,name,outstanding)
        code_list.append(datas)
    num = len(code_list)
    stock_selected = []
    pos = 0
    num_got = 0
    for item in code_list:
        score = 0
        pos = pos + 1
        recommend = 0
        print(str(pos) + '/' + str(num) + '  ' + str(num_got) + 'got')
        if item[1].find('ST') != -1:
            continue
        try:
            df = ts.get_hist_data(item[0])
            if df is None:
                continue
            if len(df) < 50:
                continue
            price = df['close'][0]
            mainforce = trendline.mainforce_monitor(df)
            goldenline = trendline.golden_snipe(df)
            if mainforce[0] > mainforce[1]:
                score = score + 5
            else:
                continue
            for item1 in goldenline:
                if price - item1 < 0:
                    continue
                if (price - item1) / price < 0.01:
                    score = score + 7
                    recommend = item1
                    break
                elif (price - item1) / price < 0.015:
                    score = score + 6
                    recommend = item1
                    break
                elif (price - item1) / price < 0.02:
                    score = score + 5
                    recommend = item1
                    break
                elif (price - item1) / price < 0.025:
                    score = score + 4
                    recommend = item1
                    break
                elif (price - item1) / price < 0.03:
                    score = score + 3
                    recommend = item1
                    break
            if recommend < 2:
                continue
            if recommend < 20:
                score = score + 2
            elif recommend < 30:
                score = score + 1
            else:
                continue
            if item[2] <= 5:
                score = score + 5
            elif item[2] <= 10:
                score = score + 3
            if score < required_score:
                continue
            #name = ts.get_realtime_quotes(item)
            #name = name['name'][0]
            stock_selected.append({'code':item[0], 'name':item[1], 'price':recommend, 'score':score})
            df_selected = pd.DataFrame(stock_selected)
            num_got = num_got + 1
        except ConnectionError as err:
            print(err)
    print(df_selected)
    present_time = time.strftime("%Y-%m-%d", time.localtime())
    df_selected.to_excel('./selected/' + present_time + '.xlsx')

def test_stocks(stock_code):
    data_list = ts.get_stock_basics()
    outstanding = data_list['outstanding'][stock_code]
    score = 0
    recommend = 0
    df = ts.get_hist_data(stock_code)
    price = df['close'][0]
    mainforce = trendline.mainforce_monitor(df)
    goldenline = trendline.golden_snipe(df)
    if mainforce[0] > mainforce[1]:
        score = score + 5
    for item1 in goldenline:
        if price - item1 < 0:
            continue
        if (price - item1) / price < 0.01:
            score = score + 7
            recommend = item1
            break
        elif (price - item1) / price < 0.015:
            score = score + 6
            recommend = item1
            break
        elif (price - item1) / price < 0.02:
            score = score + 5
            recommend = item1
            break
        elif (price - item1) / price < 0.025:
            score = score + 4
            recommend = item1
            break
        elif (price - item1) / price < 0.03:
            score = score + 3
            recommend = item1
            break
    if recommend < 20:
        score = score + 2
    elif recommend < 30:
        score = score + 1
    if outstanding <= 5:
        score = score + 5
    elif outstanding <= 10:
        score = score + 3
    print(score)
    
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
    data_list = ts.get_stock_basics()
    #select_stocks(19)
    #test_stocks('000952')
    #selected_evaluate('2020-04-29')
    #evaluate_all()