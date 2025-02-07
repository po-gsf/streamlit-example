#-*-coding:utf-8 -*-
import myUpbit   #우리가 만든 함수들이 들어있는 모듈
import time
import pyupbit

import ende_key  #암복호화키
import my_key    #업비트 시크릿 액세스키

'''
강의에서 만든 존버 봇 입니다.

60분 기준의 RSI지표를 보지만
서버의 크론탭에는 15분마다 돌게 설정해 분할 매수 합니다.

*/15 * * * * python3 /var/autobot/upbit_auto_bot.py

이렇게 등록하면 되지만 사실 어느 캔들(몇분 봉)을 보고 몇 분마다 돌릴지는 여러분 자유입니다.


'''


#암복호화 클래스 객체를 미리 생성한 키를 받아 생성한다.
simpleEnDecrypt = myUpbit.SimpleEnDecrypt(ende_key.ende_key)

#암호화된 액세스키와 시크릿키를 읽어 복호화 한다.
Upbit_AccessKey = simpleEnDecrypt.decrypt(my_key.upbit_access)
Upbit_ScretKey = simpleEnDecrypt.decrypt(my_key.upbit_secret)

#업비트 객체를 만든다
upbit = pyupbit.Upbit(Upbit_AccessKey, Upbit_ScretKey)

#내가 매수할 총 코인 개수
MaxCoinCnt = 5.0

#처음 매수할 비중(퍼센트)
FirstRate = 10.0
#추가 매수할 비중 (퍼센트)
WaterRate = 5.0

#내가 가진 잔고 데이터를 다 가져온다.
balances = upbit.get_balances()

TotalMoeny = myUpbit.GetTotalMoney(balances) #총 원금
TotalRealMoney = myUpbit.GetTotalRealMoney(balances) #총 평가금액

#내 총 수익율
TotalRevenue = (TotalRealMoney - TotalMoeny) * 100.0/ TotalMoeny

#코인당 매수할 최대 매수금액
CoinMaxMoney = TotalMoeny / MaxCoinCnt


#처음에 매수할 금액 
FirstEnterMoney = CoinMaxMoney / 100.0 * FirstRate 

#그 이후 매수할 금액 
WaterEnterMoeny = CoinMaxMoney / 100.0 * WaterRate

print("-----------------------------------------------")
print ("Total Money:", myUpbit.GetTotalMoney(balances))
print ("Total Real Money:", myUpbit.GetTotalRealMoney(balances))
print ("Total Revenue", TotalRevenue)
print("-----------------------------------------------")
print ("CoinMaxMoney : ", CoinMaxMoney)
print ("FirstEnterMoney : ", FirstEnterMoney)
print ("WaterEnterMoeny : ", WaterEnterMoeny)



#거래대금이 많은 탑코인 30개의 리스트
TopCoinList = myUpbit.GetTopCoinList("week",30)

#구매 제외 코인 리스트
OutCoinList = ['KRW-MARO','KRW-TSHP','KRW-PXL','KRW-BTC']

#나의 코인
LovelyCoinList = ['KRW-BTC','KRW-ETH','KRW-DOGE','KRW-DOT']


Tickers = pyupbit.get_tickers("KRW")


for ticker in Tickers:
    try: 
        print("Coin Ticker: ",ticker)
  

        #이미 매수된 코인이다. 물타기!!
        if myUpbit.IsHasCoin(balances,ticker) == True:
            

            #제외할 코인이라면 스킵!!!
            if myUpbit.CheckCoinInList(OutCoinList,ticker) == True:
                continue

            print("!!!!! Target Coin!!! :",ticker)
            
            time.sleep(0.05)
            df = pyupbit.get_ohlcv(ticker,interval="minute60") #60분봉 데이타를 가져온다.

            #RSI지표를 구한다.
            rsi_min_before = myUpbit.GetRSI(df,14,-3)
            rsi_min = myUpbit.GetRSI(df,14,-2)


            print("-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            ################################새로 추가된 지표 참고용으로 필요하시면 봇에 활용해 보세요!##############################################################

            #---------------------------------------------#
            #아래 지표들 구할때 제가 현재 캔들을 -1 이 아니라 -2로 
            #이전 캔들을 -2가 아니라 -3으로 수정했습니다. 이유는 https://blog.naver.com/zacra/222567868086 참고하세요!
            #---------------------------------------------#


            #볼린저 밴드 구하는 함수는 실제 차트와 다소 오차가 존재하지만 활용하는데는 무리가 없습니다!
            #볼린저 밴드 함수는 아래와 같이 딕셔너리 형식으로 값을 리턴하며 upper가 상단, ma는 기준이 되는 이동평균선(여기선 20일선),lower가 하단이 됩니다.
            print("-----------------------------------------------")
            #이전 캔들의 볼린저 밴드 상하단
            BB_dic_before = myUpbit.GetBB(df,20,-3)
            print("before - MA:",BB_dic_before['ma'],", Upper:", BB_dic_before['upper'] ,", Lower:" ,BB_dic_before['lower'])

            print("-----------------------------------------------")
            #현재 볼린저 밴드 상하단
            BB_dic_now = myUpbit.GetBB(df,20,-2)
            print("now - MA:",BB_dic_now['ma'],", Upper:", BB_dic_now['upper'] ,", Lower:" ,BB_dic_now['lower'])



            #MACD값을 구해줍니다!
            #MACD함수는 아래와 같이 딕셔너리 형식으로 값을 리턴하며 macd는 MACD값, macd_siginal값이 시그널값, ocl이 오실레이터 값이 됩니다
            print("-----------------------------------------------")
            macd_before = myUpbit.GetMACD(df,-3) #이전캔들의 MACD
            print("before - MACD:",macd_before['macd'], ", MACD_SIGNAL:", macd_before['macd_siginal'],", ocl:", macd_before['ocl'])
            print("-----------------------------------------------")
            macd = myUpbit.GetMACD(df,-2) #현재캔들의 MACD
            print("now - MACD:",macd['macd'], ", MACD_SIGNAL:", macd['macd_siginal'],", ocl:", macd['ocl'])




            #일목균형표(일목구름) 구해줍니다!
            #일목균형표(일목구름)함수는 아래와 같이 딕셔너리 형식으로 값을 리턴하며 conversion는 전환선, base는 기준선
            #huhang_span은 후행스팬, sunhang_span_a는 선행스팬1, sunhang_span_b는 선행스판2 입니다.
            print("-----------------------------------------------")
            ic_before = myUpbit.GetIC(df,-3) #이전캔들의 일목균형표
            print("before - Conversion:",ic_before['conversion'], ", Base:", ic_before['base'],", HuHang_Span:", ic_before['huhang_span'],", SunHang_Span_a:", ic_before['sunhang_span_a'],", SunHang_Span_b:", ic_before['sunhang_span_b'])

            print("-----------------------------------------------")
            ic = myUpbit.GetIC(df,-2) #이전캔들의 일목균형표
            print("now - Conversion:",ic['conversion'], ", Base:", ic['base'],", HuHang_Span:", ic['huhang_span'],", SunHang_Span_a:", ic['sunhang_span_a'],", SunHang_Span_b:", ic['sunhang_span_b'])




            print("-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")



            #################################################################################################################
            #################################################################################################################
            #################################################################################################################
            #################################################################################################################
            #################################################################################################################

            #반드시 이 글을 읽고 수정하세요 https://blog.naver.com/zacra/222567868086
            # 지표를 활용할 때 현재 캔들 -1 과 이전 캔들 -2는 값이 같아지는 경우가 생길 수 있습니다. 
            # (봇이 캔들이 변경되는 시점에 주로 실행되기에 이 경우 현재 캔들 기준으로 구한 지표 값과 이전 캔들 기준으로 구한 지표 값이 동일해 지는 상황압니다,)
            # 따라서 이전 캔들 -2, 이이전 캔들 -3으로 조합해야 원하는 결과를 얻을 수 있습니다.
            # 쉽게 이야기해서 현재 캔들을 -2, 이전 캔들을 -3으로 보는게 좋다는 거죠. 어자피 진짜 현재 캔들 -1과 이전 캔들 -2의 값이 보통 같을테니까요. 
            # (이전 캔들의 종가와 현재 캔들의 시가가 거의 같은 경우가 많으니까요!)

            #################################################################################################################
            #################################################################################################################
            #################################################################################################################
            #################################################################################################################
            #################################################################################################################


            #수익율을 구한다.
            revenu_rate = myUpbit.GetRevenueRate(balances,ticker)


            time.sleep(0.05)
            #원화 잔고를 가져온다
            won = float(upbit.get_balance("KRW"))
            print("# Remain Won :", won)

            print("------------------------------------")
            print("Coin ticker :",ticker)
            print("- Recently RSI :", rsi_min_before, " -> ", rsi_min)
            print("- Now Revenue : ",revenu_rate)
        

            #현재 코인의 총 매수금액
            NowCoinTotalMoney = myUpbit.GetCoinNowMoney(balances,ticker)

            #60분봉 기준 RSI지표 70 이상이면서 수익권일때 분할 매도를 한다.
            if rsi_min >= 70.0 and revenu_rate >= 1.0:
                print("!!!!!!!!!!!!!!!Revenue Success Sell Coin!!!!!!!!!!!!!!!!!!!!")

                #현재 걸려있는 지정가 주문을 취소한다. 왜? 아래 매수매도 로직이 있으니깐 
                myUpbit.CancelCoinOrder(upbit,ticker)

                #최대코인매수금액의 1/4보다 작다면 전체 시장가 매도 
                if NowCoinTotalMoney < (CoinMaxMoney / 4.0):
                    #시장가 매도를 한다.
                    balances = myUpbit.SellCoinMarket(upbit,ticker,upbit.get_balance(ticker))
                #최대코인매수금액의 1/4보다 크다면 절반씩 시장가 매도 
                else:
                    #시장가 매도를 한다.
                    balances = myUpbit.SellCoinMarket(upbit,ticker,upbit.get_balance(ticker) / 2.0)

                #팔았으면 원화를 다시 가져올 필요가 있다.
                won = float(upbit.get_balance("KRW"))
               



            #내가 가진 원화가 물탈 돈보다 적다..(원금 바닥) 그런데 수익율이 - 10% 이하다? 그럼 절반 팔아서 물탈돈을 마련하자!
            if won < WaterEnterMoeny and revenu_rate <= -10.0:
                print("!!!!!!!!!!!!!!!No Money Sell Coin Half !!!!!!!!!!!!!!!!!!!!")
                #현재 걸려있는 지정가 주문을 취소한다. 왜? 아래 매수매도 로직이 있으니깐 
                myUpbit.CancelCoinOrder(upbit,ticker)
                #시장가 매도를 한다.
                balances = myUpbit.SellCoinMarket(upbit,ticker,upbit.get_balance(ticker) / 2.0)



            #할당된 최대코인매수금액 대비 매수된 코인 비율
            Total_Rate = NowCoinTotalMoney / CoinMaxMoney * 100.0

            #60분봉 기준 RSI지표 30 이하에서 빠져나왔을 때
            if rsi_min_before <= 30.0 and rsi_min > 30.0:
                #할당된 최대코인매수금액 대비 매수된 코인 비중이 50%이하일때..
                if Total_Rate <= 50.0:
                    print("!!!!!!!!!!!!!!!Water GoGo!!!!!!!!!!!!!!!!!!!!!!")
                    #현재 걸려있는 지정가 주문을 취소한다. 왜? 아래 매수매도 로직이 있으니깐 
                    myUpbit.CancelCoinOrder(upbit,ticker)

                     #시장가 매수를 한다.
                    balances = myUpbit.BuyCoinMarket(upbit,ticker,WaterEnterMoeny)


                #50%를 초과하면
                else:
                    print("!!!!!!!!!!!!!!! Water GoGo But if ",revenu_rate," Under !!!!!!!!!!!!!!!!!!!!!")
                    #수익율이 마이너스 5% 이하 일때만 매수를 진행하여 원금 소진을 늦춘다.
                    if revenu_rate <= -5.0:
                        print("!!!!!!!!!!!!!!!Water GoGo!!!!!!!!!!!!!!!!!!!!!")
                        #현재 걸려있는 지정가 주문을 취소한다. 왜? 아래 매수매도 로직이 있으니깐 
                        myUpbit.CancelCoinOrder(upbit,ticker)

                         #시장가 매수를 한다.
                        balances = myUpbit.BuyCoinMarket(upbit,ticker,WaterEnterMoeny)





        #아직 매수안한 코인
        else:

            #거래량 많은 탑코인 리스트안의 코인이 아니라면 스킵! 탑코인에 해당하는 코인만 이후 로직을 수행한다.
            if myUpbit.CheckCoinInList(TopCoinList,ticker) == False:
                continue
            #위험한 코인이라면 스킵!!!
            if myUpbit.CheckCoinInList(OutCoinList,ticker) == True:
                continue
            #나만의 러블리만 사겠다! 그 이외의 코인이라면 스킵!!!
            #if myUpbit.CheckCoinInList(LovelyCoinList,ticker) == False:
            #    continue

            print("!!!!! Target Coin!!! :",ticker)
            
            time.sleep(0.05)
            df = pyupbit.get_ohlcv(ticker,interval="minute60") #60분봉 데이타를 가져온다.

            #RSI지표를 구한다.
            rsi_min_before = myUpbit.GetRSI(df,14,-3)
            rsi_min = myUpbit.GetRSI(df,14,-2)





            print("-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            ################################새로 추가된 지표 참고용으로 필요하시면 봇에 활용해 보세요!##############################################################


            #---------------------------------------------#
            #아래 지표들 구할때 제가 현재 캔들을 -1 이 아니라 -2로 
            #이전 캔들을 -2가 아니라 -3으로 수정했습니다. 이유는 https://blog.naver.com/zacra/222567868086 참고하세요!
            #---------------------------------------------#



            #볼린저 밴드 구하는 함수는 실제 차트와 다소 오차가 존재하지만 활용하는데는 무리가 없습니다!
            #볼린저 밴드 함수는 아래와 같이 딕셔너리 형식으로 값을 리턴하며 upper가 상단, ma는 기준이 되는 이동평균선(여기선 20일선),lower가 하단이 됩니다.
            print("-----------------------------------------------")
            #이전 캔들의 볼린저 밴드 상하단
            BB_dic_before = myUpbit.GetBB(df,20,-3)
            print("before - MA:",BB_dic_before['ma'],", Upper:", BB_dic_before['upper'] ,", Lower:" ,BB_dic_before['lower'])

            print("-----------------------------------------------")
            #현재 볼린저 밴드 상하단
            BB_dic_now = myUpbit.GetBB(df,20,-2)
            print("now - MA:",BB_dic_now['ma'],", Upper:", BB_dic_now['upper'] ,", Lower:" ,BB_dic_now['lower'])



            #MACD값을 구해줍니다!
            #MACD함수는 아래와 같이 딕셔너리 형식으로 값을 리턴하며 macd는 MACD값, macd_siginal값이 시그널값, ocl이 오실레이터 값이 됩니다
            print("-----------------------------------------------")
            macd_before = myUpbit.GetMACD(df,-3) #이전캔들의 MACD
            print("before - MACD:",macd_before['macd'], ", MACD_SIGNAL:", macd_before['macd_siginal'],", ocl:", macd_before['ocl'])
            print("-----------------------------------------------")
            macd = myUpbit.GetMACD(df,-2) #현재캔들의 MACD
            print("now - MACD:",macd['macd'], ", MACD_SIGNAL:", macd['macd_siginal'],", ocl:", macd['ocl'])




            #일목균형표(일목구름) 구해줍니다! 다소 오차는 있을 수 있으나 활용하는데 무리는 없습니다.
            #일목균형표(일목구름)함수는 아래와 같이 딕셔너리 형식으로 값을 리턴하며 conversion는 전환선, base는 기준선
            #huhang_span은 후행스팬, sunhang_span_a는 선행스팬1, sunhang_span_b는 선행스팬2 입니다.
            print("-----------------------------------------------")
            ic_before = myUpbit.GetIC(df,-3) #이전캔들의 일목균형표
            print("before - Conversion:",ic_before['conversion'], ", Base:", ic_before['base'],", HuHang_Span:", ic_before['huhang_span'],", SunHang_Span_a:", ic_before['sunhang_span_a'],", SunHang_Span_b:", ic_before['sunhang_span_b'])

            print("-----------------------------------------------")
            ic = myUpbit.GetIC(df,-2) #현재캔들의 일목균형표
            print("now - Conversion:",ic['conversion'], ", Base:", ic['base'],", HuHang_Span:", ic['huhang_span'],", SunHang_Span_a:", ic['sunhang_span_a'],", SunHang_Span_b:", ic['sunhang_span_b'])




            print("-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")





            print("------------------------------------")
            print("Coin ticker :",ticker)
            print("- Recently RSI :", rsi_min_before, " -> ", rsi_min)


            #60분봉 기준 RSI지표 30 이하에서 빠져나오면서 아직 매수한 코인이 MaxCoinCnt보다 작다면 매수 진행!
            if rsi_min_before <= 30.0 and rsi_min > 30.0 and myUpbit.GetHasCoinCnt(balances) < MaxCoinCnt :
                print("!!!!!!!!!!!!!!!First Buy GoGoGo!!!!!!!!!!!!!!!!!!!!!!!!")
                 #시장가 매수를 한다.
                balances = myUpbit.BuyCoinMarket(upbit,ticker,FirstEnterMoney)



    except Exception as e:
        print("---:", e)



























