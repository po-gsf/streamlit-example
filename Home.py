from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import datetime

import requests
import json

##############################################################
# API ~
##############################################################
baseHeaders = {"accept":"application/json"}
server_url = 'http://127.0.0.1:8000'

timeStamp = [] #시간
openningPrice = [] #시가
highPrice = [] #고가
lowPrice = [] #저가
tradePrice = [] #종가
candleTradePrice = [] # 거래 총금액
candleTradeVolume = [] # 거래 총량
changePrice = [] # 가격 변화량
changeRate = [] # 변화%

def getMarketAll_API(isTrue: bool):
    print("=========getMarketAll_API======")
    try:
        response = requests.get(server_url +"/market/all/"+str(isTrue))

        marketList = []
        for crypto in eval(response.text):
            marketList.append(crypto['market'])
        
        return marketList
    except Exception as e:
        print("Error occurred: ", e)
    return

def getTicker_API(market: str):
    print("=========getTicker_API======")
    print("market:"+market)
    try:
        response = requests.get(server_url +"/ticker/"+market)
        response.text
    except Exception as e:
        print("Error occurred: ", e)
    return 

def clearCandleData():
    timeStamp.clear()
    openningPrice.clear()
    highPrice.clear()
    lowPrice.clear()
    tradePrice.clear()
    candleTradePrice.clear()
    candleTradeVolume.clear()
    changePrice.clear()
    changeRate.clear()
    return

def getCandles_API(period: str, market: str, count: str):
    print("=========getCandles_API======")
    print("period:"+period+", market:"+market+", count:"+count)
    try:
        response = requests.get(server_url +"/candles/"+ period + "/" + market + "/" +count)
        print(response.text)
        clearCandleData()
        
        for crypto in eval(response.text):
            timeStamp.append(datetime.datetime.fromtimestamp(crypto['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S'))
            openningPrice.append(crypto['opening_price'])
            highPrice.append(crypto['high_price'])
            lowPrice.append(crypto['low_price'])
            tradePrice.append(crypto['trade_price'])
            candleTradePrice.append(crypto['candle_acc_trade_price'])
            candleTradeVolume.append(crypto['candle_acc_trade_volume'])

            if period == 'days' :
                changePrice.append(crypto['change_price'])
                changeRate.append(crypto['change_rate'])
    except Exception as e:
        print("Error occurred: ", e)

    return 

def getOrderbook_API(market: str):
    print("=========getOrderbook_API======")
    print("market:"+market)
    try:
        response = requests.get(server_url +"/orderbook/"+ market)
    except Exception as e:
        print("Error occurred: ", e)
    return response.text

##############################################################
# Main View ~
##############################################################

def initMainUI() :
    st.header('to Search')
    selectedMarket = st.selectbox(label='selected Coin', options=getMarketAll_API(True))
    initSelectedUI(selectedMarket)
    
    return

def initSelectedUI(selectedMarket: str):
    col1, col2 = st.columns(2)

    with col1: 
        initPeriodType(selectedMarket)
    with col2: 
        selected = st.radio(label='selected Price', 
                        options=('openning Price', 'High Price', 'Low Price',
                                 'tradePrice', 'candleTradePrice', 'candleTradeVolume',
                                 'changePrice', 'changeRate'))
    initGraph(initPriceType(selected))
    initInfoColumn()
        
    return

def initPeriodType(selectedMarket: str) :
    selected = st.radio(label='selected period', options=('day', 'week', 'month'))

    if selected == 'day':
        getCandles_API("days", selectedMarket, str(100))
    if selected == 'week':
        getCandles_API("weeks", selectedMarket, str(100))
    if selected == 'month':
        getCandles_API("months", selectedMarket, str(100))
    else :
        getCandles_API("days", selectedMarket, str(100))
    return

def initPriceType(selected: any) :
    if selected == 'openning Price': return openningPrice
    if selected == 'High Price': return highPrice
    if selected == 'Low Price': return lowPrice
    if selected == 'tradePrice': return tradePrice
    if selected == 'candleTradePrice': return candleTradePrice
    if selected == 'candleTradeVolume': return candleTradeVolume
    if selected == 'changePrice': return changePrice
    if selected == 'changeRate': return changeRate
    else : return openningPrice

def initGraph(dataArr: [str]) : 
    chart_data = pd.DataFrame(
        dataArr
    )

    chart = st.line_chart()
    chart.add_rows(chart_data)
    return

def initInfoColumn() :
    df = pd.DataFrame(
        {
            "timeStamp data": timeStamp,
            "openning Price data": openningPrice,
            "High Price data": highPrice,
            "Low Price data": lowPrice,
            "tradePrice data": tradePrice,
            "candleTradePrice": candleTradePrice,
            "candleTradeVolume data": candleTradeVolume,
            "changePrice data": changePrice,
            "changeRate data": changeRate
        }
    )
        
    st.dataframe(
        df,
        column_config={
            "timeStamp data": "time Stamp",
            "openning Price data": "openning Price",
            "High Price data": "High Price",
            "Low Price data": "Low Price",
            "tradePrice data": "tradePrice",
            "candleTradePrice": "candleTradePrice",
            "candleTradeVolume data": "candleTradeVolume",
            "changePrice data": "changePrice",
            "changeRate data": "changeRate",
        },
        hide_index=True,
        height=2000
    )
    return 

initMainUI()

st.caption('https://app-example-cmnc7aszgrlrlcwhqyjey2.streamlit.app/')