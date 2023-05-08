# from helper import trading_center as tc
import technical_indicator as ti
import json
import pandas as pd
from pprint import pprint

candidate = ['004690', '005380']
rsi_stock_list = []
file_path = "../data/RSIStockList.json"


def filter_by_rsi(ticker):
    df = ti.get_ohlc('20230101', '20230508', ticker=ticker)
    df['RSI'] = ti.get_rsi(ohlc=df, period=14)
    print(df['RSI'][-1])
    if df['RSI'][-1] < 30:
        rsi_stock_list.append(ticker)


for stock in candidate:
    filter_by_rsi(stock)

print(rsi_stock_list)
with open(file_path, 'w', encoding="UTF-8") as outfile:
    json.dump(rsi_stock_list, outfile, ensure_ascii=False)