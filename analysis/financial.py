import json
import pandas as pd
from tabulate import tabulate
financial_file_path = "../data/FinancialInfo.json"

with open(financial_file_path, 'r', encoding="UTF-8") as f:
    dicts = json.load(f)

filtered = list(filter(lambda x: 2 >= x['PBR'] >= 0 and 12 >= x['PER'] >= 0 and x['시가총액'] >= 500, dicts))
print(filtered)

# df = pd.DataFrame(dicts)
# condition = (df.PBR >= 0) & (df.PBR <= 2) & (df.PER >= 0) & (df.PER <= 12) & (df.시가총액 >= 500)
#
# df = df[condition]
# print(tabulate(df, headers=df.keys(), tablefmt='psql'))


