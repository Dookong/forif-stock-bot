# 더 많은 기술적 지표를 구할 때는 https://github.com/bukosabino/ta 라이브러리 활용 추천!
from pykrx import stock
import pandas as pd
import numpy


# start = '20220101', end = '20230508',ticker = '005930'
def get_ohlc(start, end, ticker):
    df = stock.get_market_ohlcv(start, end, ticker)
    df.drop(['거래량', '거래대금', '등락률'], axis=1, inplace=True)
    print(df)
    return df


# 이동평균선 - 첫번째: ohlc, 두번째: 기간
def get_ma(ohlc, period):
    close = ohlc["종가"]
    ma = close.rolling(period).mean()
    return pd.Series(ma)


# RSI - 첫번째: ohlc, 두번째: 기간
def get_rsi(ohlc, period):
    delta = ohlc["종가"].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)))


# 볼린저 밴드 - 첫번째: ohlc, 두번째: 기간, 세번째: 기준 날짜
def get_bollinger_band(ohlc, period, unit=2.0):
    dict_bb = {}

    ohlc['center'] = ohlc['종가'].rolling(window=period).mean()  # 20일 이동평균
    ohlc['stddev'] = ohlc['종가'].rolling(window=period).std()  # 20일 이동표준편차

    dict_bb['upper'] = ohlc['center'] + unit * ohlc['stddev']  # 상단밴드
    dict_bb['lower'] = ohlc['center'] - unit * ohlc['stddev']  # 하단밴드
    dict_bb['center'] = ohlc['center']

    ohlc.drop(['stddev', 'center'], axis=1, inplace=True)

    return dict_bb


# get_ohlc('20220101', '20230508', '005930')