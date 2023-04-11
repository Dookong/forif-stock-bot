from pykis import *
from prettytable import PrettyTable
import helper.commons as commons

kis = PyKis(
    appkey = commons.get_app_key(),
    appsecret = commons.get_app_secret(),
    virtual_account=False,
)
# 계좌 스코프 생성
account = kis.account(commons.get_account_no() + commons.get_product_code()) # 계좌번호 ex) 50071022-01 또는 5007102201

def get_balance():
    # 잔고 조회
    balance = account.balance_all()
    # 결과출력
    print(f'예수금: {balance.dnca_tot_amt:,}원 평가금: {balance.tot_evlu_amt:,} 손익: {balance.evlu_pfls_smtl_amt:,}원')
    # 리턴
    return balance

def print_balance():
    balance = get_balance()
    table = PrettyTable(field_names=['상품번호', '상품명', '보유수량', '매입금액', '현재가', '평가손익율', '평가손익',], align='r')

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
        table='상승', # '상승', '하락', '거래상위'
        # 시장 구분
        market=market, # '전체', '코스피', '코스닥', '코넥스'
        # 수정주가 적용
        proc=True,
        # 정렬 기준
        sort='자동', # '자동', '등락율', '거래량', '거래대금'
        # 기준에 반대 차순 정렬
        reverse=False,
    )[:10]
    
    table = PrettyTable(field_names=['순위', '종목코드', '종목명', '등락율', '거래량', '거래대금(만)'], align='r')
    for i, item in enumerate(rank):
        table.add_row([
            i+1,
            item.isu_cd,
            item.isu_abbrv,
            item.fluc_rt,
            item.acc_trdvol,
            item.acc_trdval / 10000 if True else item.acc_trdval // 10000
        ])
    print(table)
    return [i.isu_cd for i in rank]
    
if __name__ == '__main__':
    print(is_market_open())
    get_hot_tickers("코스닥")
    # 네이버 1주 20만원에 매수
    # order = buy_limit_order("035420", 1, 200000)
    
