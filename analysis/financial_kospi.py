from ..helper import trading_center as tc
import json
from tqdm import tqdm


dicts = []

for stock in tqdm(tc.kis.market.kospi.all()):
    dicts.append(tc.get_financial_info(stock.mksc_shrn_iscd))

# 파일 저장
financial_file_path = "../data/FinancialKOSPI.json"
with open(financial_file_path, 'w', encoding="UTF-8") as outfile:
    json.dump(dicts, outfile, ensure_ascii=False)
