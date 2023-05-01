import helper.commons as commons
import time as t
import requests
from fake_useragent import UserAgent
from tqdm import tqdm
from prettytable import PrettyTable
from pykis import *
from pprint import pprint

kis: PyKis = PyKis(
    appkey=commons.get_app_key(),
    appsecret=commons.get_app_secret(),
    virtual_account=False,
)
# 계좌 스코프 생성
account: KisAccountScope = kis.account(
    commons.get_account_no() + commons.get_product_code())  # 계좌번호 ex) 50071022-01 또는 5007102201


def get_balance():
    # 잔고 조회
    balance = account.balance_all()
    # 결과출력
    print(f'예수금: {balance.dnca_tot_amt:,}원 평가금: {balance.tot_evlu_amt:,} 손익: {balance.evlu_pfls_smtl_amt:,}원')
    # 리턴
    return balance


def print_balance():
    balance = get_balance()
    table = PrettyTable(field_names=['상품번호', '상품명', '보유수량', '매입금액', '현재가', '평가손익율', '평가손익', ], align='r')

    # 잔고를 테이블에 추가
    for stock in balance.stocks:
        table.add_row([
            stock.pdno,
            stock.prdt_name,
            f'{stock.hldg_qty:,}주',
            f'{stock.pchs_amt:,}원',
            f'{stock.prpr:,}원',
            f'{stock.evlu_pfls_rt:.2f}%',
            f'{stock.evlu_pfls_amt:,}원',
        ])

    print(table)


def get_stock_info(ticker):
    return kis.stock(ticker)


def get_stock_name(ticker):
    return kis.stock(ticker).name


def print_stock_info(stock):
    price = stock.price()

    print(f'[{stock.code} {stock.name}]')
    print(f'전일대비율: {price.prdy_ctrt:.2f}%')
    print(f'현재가: {price.stck_prpr:,}원')
    print(f'최저가: {price.stck_lwpr:,}원')
    print(f'최고가: {price.stck_hgpr:,}원')
    print(f'전일대비: {price.prdy_vrss:,}원')
    print(f'전일대비거래량비율: {price.prdy_vrss_vol_rate:.2f}%')
    print(f'거래대금: {price.acml_tr_pbmn:,}원')


def buy_limit_order(ticker, qty, price):
    return account.buy(code=ticker, qty=qty, unpr=price)


def buy_market_order(ticker, qty):
    return account.buy(code=ticker, qty=qty, unpr=0)


def sell_limit_order(ticker, qty, price):
    return account.sell(code=ticker, qty=qty, unpr=price)


def sell_market_order(ticker, qty):
    return account.sell(code=ticker, qty=qty, unpr=0)


def cancle_all_order(_order):
    return account.cancel(order=_order, qty=None)


def is_market_open():
    KRXMarketOpen.set_service_key(commons.get_service_key())
    return KRXMarketOpen.daily_open()[0]


def get_hot_tickers(market="코스피"):
    rank = KRXFluctRank.fetch(
        # 날짜가 None인 경우 마지막 장 운영일을 기준으로 조회한다.
        start_date=None,
        # 날짜가 None인 경우 마지막 장 운영일을 기준으로 조회한다.
        end_date=None,
        # 테이블명
        table='상승',  # '상승', '하락', '거래상위'
        # 시장 구분
        market=market,  # '전체', '코스피', '코스닥', '코넥스'
        # 수정주가 적용
        proc=True,
        # 정렬 기준
        sort='자동',  # '자동', '등락율', '거래량', '거래대금'
        # 기준에 반대 차순 정렬
        reverse=False,
    )[:10]

    table = PrettyTable(field_names=['순위', '종목코드', '종목명', '등락율', '거래량', '거래대금(만)'], align='r')
    for i, item in enumerate(rank):
        table.add_row([
            i + 1,
            item.isu_cd,
            item.isu_abbrv,
            item.fluc_rt,
            item.acc_trdvol,
            item.acc_trdval / 10000 if True else item.acc_trdval // 10000
        ])
    print(table)
    return [i.isu_cd for i in rank]


# PyKIS 미지원 기능 -> 직접 API 호출
def get_financial_info(ticker):
    t.sleep(0.5)

    # 허위 주문 생성 및 취소 -> 토큰 발급
    try:
        cancle_all_order(buy_limit_order("035420", 1, 10000))
    except Exception as e:
        pass

    user_agent = UserAgent()
    headers = {}
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{commons.get_url_base()}/{PATH}"

    # Request Header
    headers = {
        "User-Agent": user_agent.random,
        "Content-Type": "application/json",
        "authorization": f"Bearer {kis.client.token.token}",
        "appKey": commons.get_app_key(),
        "appSecret": commons.get_app_secret(),
        "tr_id": "FHKST01010100"
    }

    # Query Parameter
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": ticker
    }

    # Call
    res = requests.get(URL, headers=headers, params=params)
    # pprint(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == '0':
        result = res.json()['output']

        # 종목 상태 구분 코드
        # 00 : 그외
        # 51 : 관리종목
        # 52 : 투자의견
        # 53 : 투자경고
        # 54 : 투자주의
        # 55 : 신용가능
        # 57 : 증거금 100%
        # 58 : 거래정지
        # 59 : 단기과열
        financial_dict = {
            '번호': ticker,
            '이름': get_stock_name(ticker=ticker),
            '시장': result['rprs_mrkt_kor_name'],
            '상태': result['iscd_stat_cls_code']
        }

        try:
            financial_dict['현재가'] = int(result['stck_prpr'])  # 현재가
        except Exception as e:
            financial_dict['현재가'] = 0

        try:
            financial_dict['업종'] = result['bstp_kor_isnm']  # 업종
        except Exception as e:
            financial_dict['StockDistName'] = ""

        try:
            financial_dict['시가총액'] = float(result['hts_avls'])  # 시가총액
        except Exception as e:
            financial_dict['StockMarketCap'] = 0

        try:
            financial_dict['PER'] = float(result['per'])  # PER
        except Exception as e:
            financial_dict['PER'] = 0.0

        try:
            financial_dict['PBR'] = float(result['pbr'])  # PBR
        except Exception as e:
            financial_dict['PBR'] = 0.0

        try:
            financial_dict['EPS'] = float(result['eps'])  # EPS
        except Exception as e:
            financial_dict['EPS'] = 0.0

        try:
            financial_dict['BPS'] = float(result['bps'])  # BPS
        except Exception as e:
            financial_dict['BPS'] = 0.0

        return financial_dict
    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return res.json()["msg_cd"]


if __name__ == '__main__':
    print(is_market_open())

    dicts = []
    for ticker in tqdm(get_hot_tickers("코스닥")):
        dicts.append(get_financial_info(ticker))

    # 코스피 전체 종목은 900개 이상 -> 3시간 넘게 소요..
    # for stock in tqdm(kis.market.kospi.all()):
    #     dicts.append(get_financial_info(stock.mksc_shrn_iscd))

    # 파일 저장
    financial_file_path = "../data/FinancialInfo.json"
    with open(financial_file_path, 'w', encoding="UTF-8") as outfile:
        json.dump(dicts, outfile, ensure_ascii=False)
