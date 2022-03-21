import requests
import pandas as pd
import datetime
import time

def get_stock_list():
    result = []
    url = f'https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=10000&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    data = requests.get(url, headers = headers).json()['data']['list']
    for item in data:
        stock_data = {
            'code' : item['symbol'],
            'name' : item['name'],
            'price' : item['current'],
            'change' : item['chg'],
            'percent' : item['percent'],
            'volume' : item['volume'],
            'amount' : item['amount'],
            'capital' : item['market_capital']
        }
        result.append(stock_data)
    result = pd.DataFrame(result)
    return result

def get_stock_code(stock_name):
    result = {}
    url = f'https://xueqiu.com/query/v1/suggest_stock.json?q={stock_name}&count=5'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    session = requests.Session()
    session.get(url = "https://xueqiu.com", headers = headers)
    data = session.get(url, headers = headers).json()
    if data['code'] == 200:
        data = data['data']
        for item in data:
            if item['query'] == stock_name:
                return item['code'][2:]
    else:
        return None

def get_stock_now(stock_code):
    stock_code = get_stock_type(stock_code)
    url = f'https://stock.xueqiu.com/v5/stock/realtime/pankou.json?symbol={stock_code}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    data = requests.get(url, headers = headers).json()['data']
    time = data['timestamp']
    time = datetime.datetime.fromtimestamp(time / 1000)
    result = {}
    result['code'] = data['symbol']
    result['time'] = str(time)
    for i in range(1, 6):
        list = []
        list.append(data['sp' + str(i)])
        list.append(data['sc' + str(i)] / 100)
        result['sell' + str(i)] = list
    for i in range(1, 6):
        list = []
        list.append(data['bp' + str(i)])
        list.append(data['bc' + str(i)] / 100)
        result['buy' + str(i)] = list
    return result

def get_stock_basic(stock_code):
    stock_code = get_stock_type(stock_code)
    url = f'https://stock.xueqiu.com/v5/stock/quote.json?symbol={stock_code}&extend=detail'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    session = requests.Session()
    session.get(url = "https://xueqiu.com", headers = headers)
    data = session.get(url, headers = headers).json()['data']['quote']
    result = {
        'name' : data['name'],
        'code' : data['symbol'][2:],
        'price' : data['current'],
        'change' : data['chg'],
        'percent' : data['percent'],
        'high' : data['high'],
        'low' : data['low'],
        'up_limit' : data['limit_up'],
        'down_limit' : data['limit_down'],
        'last_close' : data['last_close'],
        'float_shares' : data['float_shares']
    }
    return result

def get_stock_minute(stock_code):
    stock_code = get_stock_type(stock_code)
    url = f'https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol={stock_code}&period=1d'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    session = requests.Session()
    session.get(url = "https://xueqiu.com", headers = headers)
    data = session.get(url, headers = headers).json()['data']['items']
    result = []
    for item in data:
        time = item['timestamp']
        time = datetime.datetime.fromtimestamp(time / 1000)
        
        minute_data = {
            'price' : item['current'],
            'volume' : int(item['volume'] / 100),
            'average': item['avg_price'], 
            'change' : item['chg'],
            'percent' : item['percent'], 
            'timestamp' : item['timestamp'],
            'time' : str(time)
        }
        result.append(minute_data)
    result = pd.DataFrame(result)
    return result

def get_stock_kline(stock_code, type = 'day', length = 284):
    stock_code = get_stock_type(stock_code)
    url = f'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={stock_code}&begin={str(round(time.time() * 1000))}&period={type}&type=before&count=-{str(length)}&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    session = requests.Session()
    session.get(url = "https://xueqiu.com", headers = headers)
    data = session.get(url, headers = headers).json()['data']['item']
    result = []
    for item in data:
        line_time = item[0]
        line_time = datetime.datetime.fromtimestamp(line_time / 1000)
        line_time = line_time.strftime('%Y-%m-%d')
        
        minute_data = {
            'open' : item[2],
            'high' : item[3],
            'low' : item[4],
            'close' : item[5],
            'volume' : item[1] / 100,
            'change' : item[6],
            'percent' : item[7], 
            'time' : line_time
        }
        result.append(minute_data)
    result = pd.DataFrame(result)
    return result

def get_trade_now(stock_code, num = 1):
    stock_code = get_stock_type(stock_code)
    url = f'https://stock.xueqiu.com/v5/stock/history/trade.json?symbol={stock_code}&count={num}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    session = requests.Session()
    session.get(url = "https://xueqiu.com", headers = headers)
    data = session.get(url, headers = headers).json()['data']['items']
    result = []
    for item in data:
        time = item['timestamp']
        time = datetime.datetime.fromtimestamp(time / 1000)
        time = time.strftime('%H:%M:%S')

        if item['side'] < 0:
            type = 'S'
        elif item['side'] > 0:
            type = 'B'
        else:
            type = 'N'

        trade_data = {
            'code' : item['symbol'],
            'time' : time,
            'price' : item['current'],
            'volume' : int(item['trade_volume'] / 100),
            'type' : type
        }
        result.append(trade_data)
    result = pd.DataFrame(result)
    return result

def get_market_now():
    url = f'https://xueqiu.com/service/v5/stock/batch/quote?symbol=SH000001%2CSZ399001%2CSZ399006%2CSH000688&_={str(round(time.time() * 1000))}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    market_list = requests.get(url, headers = headers).json()['data']['items']
    result = []
    for market in market_list:
        market_data = market['quote']
        data_time = market_data['timestamp']
        data_time = datetime.datetime.fromtimestamp(data_time / 1000)
        
        minute_data = {
            'code': market_data['symbol'],
            'name': market_data['name'],
            'value': market_data['current'], 
            'change' : market_data['chg'],
            'percent' : market_data['percent'], 
            'time' : str(data_time)
        }
        result.append(minute_data)
    result = pd.DataFrame(result)
    return result

def get_market_status():
    url = f'https://xueqiu.com/service/v5/stock/batch/quote?symbol=SH000001%2CSZ399001%2CSZ399006%2CSH000688&_={str(round(time.time() * 1000))}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    data = requests.get(url, headers = headers).json()['data']['items'][0]['market']['status']
    return data

def get_stock_type(stock_code):
    sh_head = ("50", "51", "60", "90", "110", "113",
               "132", "204", "5", "6", "9", "7")
    if stock_code.startswith(("SH", "SZ")):
        return stock_code
    else:
        return "SH" + stock_code if stock_code.startswith(sh_head) else "SZ" + stock_code

if __name__ == '__main__':
    #print(get_trade_now('SZ002221', 10).values)
    #print(get_market_now())
    #print(get_stock_kline('SZ002221')['close'].to_list()[::-1])
    #print(len(get_stock_list()))
    #print(get_stock_code('东华能源'))
    #print(get_stock_minute('SZ002221'))
    #import pyqtgraph.examples
    #pyqtgraph.examples.run()
    #print(get_market_status())
    #print(get_stock_basic('SZ002221'))
    print(datetime.datetime.now().weekday())