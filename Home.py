from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np

import requests
import json

##############################################################
# API ~
##############################################################
baseHeaders = {"accept":"application/json"}
server_url = 'http://127.0.0.1:8000'

def getMarketAllKey(isTrue: bool):
    print('=====================~')
    response = requests.get(server_url +"/market/all/"+str(isTrue))

    marketList = []
    for crypto in eval(response.text):
        marketList.append(crypto['market'])
        #if crypto['market_warning'] == 'NONE' and crypto['market'].startswith('KRW'):
    
    return marketList

##############################################################
# Main View ~
##############################################################

def initMainUI() :
    st.header('to Search')
    st.selectbox('selected Coin', getMarketAllKey(True)) # todo : insert coin list
    initTabGraph()
    initTabPriceInfo()
    return

def initTabGraph() :
    tab_time, tab_day, tab_week, tab_month, = st.tabs(["time", "day", "week", "month"])

    with tab_time:
        initGraph()
    with tab_day:
        initGraph()
    with tab_week:
        initGraph()
    with tab_month:
        initGraph()
    return

def initGraph() : # todo : insert data
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows

    progress_bar.empty()

def initTabPriceInfo() :
    tab_bid_ask, tab_order, tab_stock = st.tabs(["bid-ask price", "order", "stock price"])

    with tab_bid_ask:
        initInfoColumn()
    with tab_order:
        initInfoColumn()
    with tab_stock:
        initInfoColumn()
    return

def initInfoColumn() :
    df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5)))

    st.table(df)
    return 



initMainUI()

st.caption('https://app-example-cmnc7aszgrlrlcwhqyjey2.streamlit.app/')