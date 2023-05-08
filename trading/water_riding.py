from ..helper import trading_center as tc
from pprint import pprint


def set_invest_seed():
    # 계좌 잔고
    balance = tc.get_balance()

    # 종목 개수 - 해당 전략으로 최대 몇개의 종목을 매수할 것인가
    stock_cnt = 5

    print("--------------계좌 잔고---------------------")
    pprint(balance)

    print("--------------------------------------------")
    # 투자 비중
    invest_rate = 0.2  # 20%

    # 전체 예수금 * 투자비중 = 토탈 시드
    total_seed = float(balance.dnca_tot_amt) * invest_rate

    # 토탈 시드 / 종목 개수 = 각 종목당 투자 금액
    seed = total_seed / stock_cnt
    print("총 시드:", str(format(round(total_seed), ',')))
    print("종목별 투자 금액:", str(format(round(seed), ',')))

    # 종목에 할당된 금액을 쪼개서 물타기!
    first_money = seed / 3.0  # 첫 진입시 매수 금액!
    second_money = first_money * 2.0  # 두번째 진입시 매수 금액!

    print("first_money:", str(format(round(first_money), ',')))
    print("second_money:", str(format(round(second_money), ',')))
