import ccxt
import time
import pandas as pd
import pprint
       
import myBinance
import ende_key  #암복호화키
import my_key    #업비트 시크릿 액세스키

import json
import log
 

logger = log.get_logger("bot")
#암복호화 클래스 객체를 미리 생성한 키를 받아 생성한다.
simpleEnDecrypt = myBinance.SimpleEnDecrypt(ende_key.ende_key)


#암호화된 액세스키와 시크릿키를 읽어 복호화 한다.
Binance_AccessKey = simpleEnDecrypt.decrypt(my_key.binance_access)
Binance_ScretKey = simpleEnDecrypt.decrypt(my_key.binance_secret)


# binance 객체 생성
binanceX = ccxt.binance(config={
    'apiKey': Binance_AccessKey, 
    'secret': Binance_ScretKey,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})


#선물 마켓에서 거래중인 모든 코인을 가져옵니다.
Tickers = binanceX.fetch_tickers()


#나의 코인
LovelyCoinList = ['BTC/USDT']

#모든 선물 거래가능한 코인을 가져온다.
for ticker in Tickers:

    try: 

   
        #하지만 여기서는 USDT 테더로 살수 있는 모든 선물 거래 코인들을 대상으로 돌려봅니다.
        if "/USDT" in ticker:
            Target_Coin_Ticker = ticker

            #러블리 코인이 아니라면 스킵! 러블리 코인만 대상으로 한다!!
            if myBinance.CheckCoinInList(LovelyCoinList,ticker) == False:
                continue

            
            time.sleep(0.1)

            Target_Coin_Symbol = ticker.replace("/", "")

                        
            leverage = 20 #레버리지 10
            test_amt = 0.03 #테스트할 수량!


            

            #################################################################################################################
            #영상엔 없지만 레버리지를 3으로 셋팅합니다! 
            try:
                logger.debug(binanceX.fapiPrivate_post_leverage({'symbol': Target_Coin_Symbol, 'leverage': leverage}))
            except Exception as e:
                logger.debug("error: %s", e)
            #앱이나 웹에서 레버리지를 바뀌면 바뀌니깐 주의하세요!!
            #################################################################################################################

            #잔고 데이타 가져오기 
            balance = binanceX.fetch_balance(params={"type": "future"})
            time.sleep(0.1)

            amt_s = 0 
            amt_b = 0
            entryPrice_s = 0 #평균 매입 단가. 따라서 물을 타면 변경 된다.
            entryPrice_b = 0 #평균 매입 단가. 따라서 물을 타면 변경 된다.


            isolated = True #격리모드인지 


            stop_target_rate = 0.02 #목표 손절
            limit_target_rate = 0.01 #목표 수익

            time.sleep(0.1)
            #print("------")
            #숏잔고
            for posi in balance['info']['positions']:
                if posi['symbol'] == Target_Coin_Symbol and posi['positionSide'] == 'SHORT':
                    #print(posi)
                    amt_s = float(posi['positionAmt'])
                    entryPrice_s= float(posi['entryPrice'])
                    leverage = float(posi['leverage'])
                    isolated = posi['isolated']
                    break
            logger.debug("-###########################################")
            logger.debug(" -------------- short balance --------------")
            logger.debug("-###########################################")
            logger.debug("amt_s: %s" , amt_s)
            logger.debug("entryPrice_s: %s",  entryPrice_s)
            logger.debug("leverage: %s",  leverage)
            logger.debug("isolated: %s",  isolated)
            logger.debug(" -------------------------------------------")
            
            time.sleep(0.1)
            #롱잔고
            for posi in balance['info']['positions']:
                if posi['symbol'] == Target_Coin_Symbol and posi['positionSide'] == 'LONG':
                    #print(posi)
                    amt_b = float(posi['positionAmt'])
                    entryPrice_b = float(posi['entryPrice'])
                    leverage = float(posi['leverage'])
                    isolated = posi['isolated']
                    break
            logger.debug("-###########################################")
            logger.debug(" --------------- long balance --------------")
            logger.debug("-###########################################")
            logger.debug("amt_b: %s ",amt_b)
            logger.debug("entryPrice_b: %s",entryPrice_b)
            logger.debug("leverage: %s",leverage)
            logger.debug("isolated: %s",isolated)
            logger.debug(" -------------------------------------------")

            time.sleep(0.1)

            #캔들 정보 가져온다 여기서는 15분봉을 보지만 자유롭게 조절 하세요!!!
            #df = myBinance.GetOhlcv(binanceX,Target_Coin_Ticker, '15m')
            df = myBinance.GetOhlcv(binanceX,Target_Coin_Ticker, '1h')

            #최근 3개의 종가 데이터
            logger.debug("Price[-3] : %s",df['close'][-3])
            logger.debug("Price[-2] : %s",df['close'][-2])
            logger.debug("Price[-1] : %s",df['close'][-1])
            #최근 3개의 5일선 데이터
            logger.debug("5ma[-3] : %s",myBinance.GetMA(df, 5, -3))
            logger.debug("5ma[-2] : %s",myBinance.GetMA(df, 5, -2))
            logger.debug("5ma[-1] : %s",myBinance.GetMA(df, 5, -1))
            #최근 3개의 RSI14 데이터
            logger.debug("RSI14[-3] : %s",myBinance.GetRSI(df, 14, -3))
            logger.debug("RSI14[-2] : %s",myBinance.GetRSI(df, 14, -2))
            logger.debug("RSI14[-1] : %s",myBinance.GetRSI(df, 14, -1))

            time.sleep(0.1)
            #최근 5일선 3개를 가지고 와서 변수에 넣어준다.
            ma5_before3 = myBinance.GetMA(df, 5, -4)
            logger.debug("ma5_before3 : %s",ma5_before3)
            ma5_before2 = myBinance.GetMA(df, 5, -3)
            logger.debug("ma5_before2 : %s",ma5_before2)
            ma5 = myBinance.GetMA(df, 5, -2)
            logger.debug("ma5 : %s",ma5)

            #20일선을 가지고 와서 변수에 넣어준다.
            ma20 = myBinance.GetMA(df, 20, -2)
            logger.debug("ma20 : %s",ma20)

            #RSI14 정보를 가지고 온다.
            rsi14 = myBinance.GetRSI(df, 14, -1)
            logger.debug("rsi14 : %s",rsi14)

            #################################################################################################################
            #영상엔 없지만 격리모드가 아니라면 격리모드로 처음 포지션 잡기 전에 셋팅해 줍니다,.
            if isolated == False:
                try:
                    logger.debug(binanceX.fapiPrivate_post_margintype({'symbol': Target_Coin_Symbol, 'marginType': 'ISOLATED'}))
                except Exception as e:
                    logger.debug("error: %s", e)
            #################################################################################################################    

            
            #해당 코인 가격을 가져온다.
            coin_price = myBinance.GetCoinNowPrice(binanceX, Target_Coin_Ticker)
            logger.debug("coin_price : %s", coin_price)

            #레버리지에 따른 최대 매수 가능 수량
            Max_Amount = round(myBinance.GetAmount(float(balance['USDT']['total']),coin_price,1) * leverage ,3)  
            half_amount = Max_Amount / 2
            logger.debug("Max_Amount : %s", Max_Amount)
            logger.debug("half_amount : %s", half_amount)

            time.sleep(0.1)

            #롱 포지션이 없을 경우
            if abs(amt_b) == 0:
                logger.debug("----------------------------none long position ----------------------------")
                if ma5 < ma20 and ma5_before3 > ma5_before2 and ma5_before2 < ma5 and rsi14 <= 65.0:
                    #롱 시장가 주문!
                    params = {
                        'positionSide': 'LONG'
                    }
                    #data = binanceX.create_market_buy_order(Target_Coin_Ticker, test_amt, params)
                    data = binanceX.create_order(Target_Coin_Ticker, 'market', 'buy', test_amt, None, params)
                    logger.debug(data)

                    #예로 1% 상승한 가격에 지정가 주문으로 롱 포지션 종료하려면..
                    #target_price = data['price'] * (1.0 + limit_target_rate)
                                

                    #롱 포지션 지정가 종료 주문!!     
                    #params = {
                    #     'positionSide': 'LONG'
                    #}
                    # #binanceX.create_limit_sell_order(Target_Coin_Ticker, data['amount'], target_price, params)
                    #binanceX.create_order(Target_Coin_Ticker, 'limit', 'sell', test_amt, target_price, params)

                    stop_price = data['price'] * (1.0 - stop_target_rate)
                    logger.debug("stop_price : %s", stop_price)
                    time.sleep(0.5)
                                    
                    #스탑로스!
                    myBinance.SetStopLossLongPrice(binanceX,Target_Coin_Ticker,stop_price)


            else:
                #롱 포지션이 있는 경우
                if abs(amt_b) > 0:
                    logger.debug("----------------------------current long position ----------------------------")
                    logger.debug("current long position amt = %s", amt_b)
                    #롱 수익율을 구한다!
                    revenue_rate_b = (coin_price - entryPrice_b) / entryPrice_b * 100.0

                    logger.debug("revenue_rate_b : %s", revenue_rate_b)

                    #레버리지를 곱한 실제 수익율
                    leverage_revenu_rate_b = revenue_rate_b * leverage
                    logger.debug("leverage_revenu_rate_b : %s", leverage_revenu_rate_b)
                    
                    if ma5 > ma20 and ma5_before3 < ma5_before2 and ma5_before2 > ma5:
                        #if leverage_revenu_rate_b >= 20:
                        params = {
                            'positionSide': 'LONG'
                        }
                        #binanceX.create_limit_sell_order(Target_Coin_Ticker, data['amount'], target_price, params)
                        data = binanceX.create_order(Target_Coin_Ticker, 'market', 'sell', abs(amt_b), None, params)
                        logger.debug("LONG Close : %s", data)

                    if ma5 < ma20 and ma5_before3 > ma5_before2 and ma5_before2 < ma5:   
                        if leverage_revenu_rate_b <= -10:
                            if amt_b <= half_amount:
                                params = {
                                    'positionSide': 'LONG'
                                }
                                #binanceX.create_limit_sell_order(Target_Coin_Ticker, data['amount'], target_price, params)
                                data = binanceX.create_order(Target_Coin_Ticker, 'market', 'buy', test_amt, None, params)
                                logger.debug("LONG water : %s", data)
                                time.sleep(0.5)
                                for posi in balance['info']['positions']:
                                    if posi['symbol'] == Target_Coin_Symbol and posi['positionSide'] == 'LONG':
                                        entryPrice_b = float(posi['entryPrice'])
                                        break

                                stop_price = entryPrice_b * (1.0 - stop_target_rate)
                                logger.debug("stop_price : %s", stop_price)
                                #스탑로스!
                                myBinance.SetStopLossLongPrice(binanceX,Target_Coin_Ticker,stop_price)

            #숏 포지션이 없을 경우
            if abs(amt_s) == 0:
                logger.debug("----------------------------none short position ----------------------------")
                if ma5 > ma20 and ma5_before3 < ma5_before2 and ma5_before2 > ma5 and rsi14 >= 35.0:
                    #숏 시장가 주문!
                    params = {
                        'positionSide': 'SHORT'
                    }
                    #data = binanceX.create_market_sell_order(Target_Coin_Ticker, test_amt,params)
                    data = binanceX.create_order(Target_Coin_Ticker, 'market', 'sell', test_amt, None, params)

                    #예로 1% 상승한 가격에 지정가 주문으로 숏 포지션 종료하려면..
                    #target_price = data['price'] * (1.0 - target_rate)

                    #logger.debug("short target_price : %s", target_price)
                                
                    #롱 포지션 지정가 종료 주문!!                 
                    # params = {
                    #     'positionSide': 'SHORT'
                    # }
                    # #binanceX.create_limit_buy_order(Target_Coin_Ticker, data['amount'], target_price ,params)
                    # binanceX.create_order(Target_Coin_Ticker, 'limit', 'buy', test_amt, target_price, params)


                    stop_price = data['price'] * (1.0 + stop_target_rate)
                    logger.debug("stop_price : %s", stop_price)
                    time.sleep(0.5)

                    #스탑로스!
                    myBinance.SetStopLossShortPrice(binanceX,Target_Coin_Ticker,stop_price)

            else:
                #숏 포지션이 있는 경우
                if abs(amt_s) > 0:
                    logger.debug("----------------------------current short position ----------------------------")
                    logger.debug("current short position amt = %s", amt_s)
                    #숏 수익율을 구한다!
                    revenue_rate_s = (entryPrice_s - coin_price) / entryPrice_s * 100.0

                    logger.debug("revenue_rate_s : %s", revenue_rate_s)

                     #레버리지를 곱한 실제 수익율
                    leverage_revenu_rate_s = revenue_rate_s * leverage
                    logger.debug("leverage_revenu_rate_s : %s", leverage_revenu_rate_s)

                    if ma5 < ma20 and ma5_before3 > ma5_before2 and ma5_before2 < ma5:
                        #if leverage_revenu_rate_s >= 20:
                        params = {
                            'positionSide': 'SHORT'
                        }
                        #binanceX.create_limit_buy_order(Target_Coin_Ticker, data['amount'], target_price ,params)
                        data = binanceX.create_order(Target_Coin_Ticker, 'market', 'buy', abs(amt_s), None, params)
                        logger.debug("SHORT close : %s", data)

                    if ma5 > ma20 and ma5_before3 < ma5_before2 and ma5_before2 > ma5:
                        if leverage_revenu_rate_s < -10:
                            if abs(amt_s) <= half_amount:
                                params = {
                                    'positionSide': 'SHORT'
                                }
                                #data = binanceX.create_market_sell_order(Target_Coin_Ticker, test_amt,params)
                                data = binanceX.create_order(Target_Coin_Ticker, 'market', 'sell', test_amt, None, params)
                                logger.debug("SHORT water : %s", data)
                                time.sleep(0.5)
                                for posi in balance['info']['positions']:
                                    if posi['symbol'] == Target_Coin_Symbol and posi['positionSide'] == 'SHORT':
                                        entryPrice_s= float(posi['entryPrice'])
                                        break

                                stop_price = entryPrice_s * (1.0 + stop_target_rate)
                                logger.debug("stop_price : %s", stop_price)
                                #스탑로스!
                                myBinance.SetStopLossShortPrice(binanceX,Target_Coin_Ticker,stop_price)
    except Exception as e:
        logger.debug("error: %s", e)








