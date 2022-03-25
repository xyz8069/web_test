import finance

df = finance.get_stock_kline('002221')
print(df['close'].to_list()[-1])