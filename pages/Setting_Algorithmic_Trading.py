from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st



##############################################################
# Main func ~
##############################################################

def initMainUI() :
    st.header('ALGORITHMIC TRADING SETTINGS')
    initRiskSlider()
    

    return


def initRiskSlider() :
    st.subheader('Risk Percent')
    st.slider('', min_value=0, max_value=100)
    st.caption('The closer to 100, the higher the risk.')
    return

initMainUI()

