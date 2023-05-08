import json
import pandas as pd
from tabulate import tabulate


def per_pbr_total(market='코스피'):
    financial_file_path = "../data/FinancialKOSPI.json" if market == '코스피' else "../data/FinancialKOSDAQ.json"

    with open(financial_file_path, 'r', encoding="UTF-8") as f:
        dicts = json.load(f)

    df = pd.DataFrame(dicts)
    condition = (df.PBR >= 0) & (df.PBR <= 2) & (df.PER >= 0) & (df.PER <= 12) & (df.시가총액 >= 500)

    df = df[condition]
    print(tabulate(df, headers=df.keys(), tablefmt='psql'))
    return df

