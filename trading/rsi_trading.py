from helper import trading_center as tc
import json
import pandas as pd
import pprint

rsi_stock_list = []
file_path = "../data/RSIStockList.json"

try:
    with open(file_path, 'r') as json_file:
        rsi_stock_list = json.load(json_file)

except Exception as e:
    print("File not yet")

if tc.is_market_open():
    for stock in rsi_stock_list:
        tc.buy_market_order(stock, 1)
