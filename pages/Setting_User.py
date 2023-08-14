from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st

import requests

##############################################################
# Setting func ~
##############################################################
baseHeaders = {"accept":"application/json"}
server_url = 'http://127.0.0.1:8000'

def postPrivateKey(accessKey: str, secretKey: str):
    try:
        response = requests.post(server_url +'/postPrivatekey', 
                        json={'accessKey':accessKey,
                                'secretKey':secretKey})
        print(response.text)
    except Exception as e:
        print("Error occurred: ", e)
    return

##############################################################
# Main func ~
##############################################################
class privateKey:
    accessKey = ''
    secretKey = ''

def initMainUI() :
    st.header('USER SETTINGS')

    initAccessKey()
    initSecretKey()
    
    st.button('SETTING', on_click=setPrivateKeyInServer())
    return


def initAccessKey() :
    st.subheader('accessKey')
    AccesskeyType = st.radio(
        "What\'s your accessKey Type?",
        ('File', 'Text'))
    
    if AccesskeyType == 'File':
        FileUploader_AccessKey = st.file_uploader('accessKey_file')
        if FileUploader_AccessKey is not None:
            privateKey.accessKey = FileUploader_AccessKey.read()
    if AccesskeyType == 'Text':
        TextInput_AccessKey = st.text_input('accessKey_text') 
        privateKey.accessKey = TextInput_AccessKey
    return

def initSecretKey() :
    st.subheader('secretKey')
    SecretkeyType = st.radio(
        "What\'s your secretKey Type?",
        ('File', 'Text'))

    if SecretkeyType == 'File':
        FileUploader_SecretKey = st.file_uploader('secretKey_file') 
        if FileUploader_SecretKey is not None:
            privateKey.secretKey = FileUploader_SecretKey.read()
    if SecretkeyType == 'Text':
        TextInput_SecretKey = st.text_input('secretKey_text') 
        privateKey.secretKey = TextInput_SecretKey
    return

def setPrivateKeyInServer() :
    print('=========================')
    print(privateKey.accessKey)
    print(privateKey.secretKey)
    postPrivateKey(privateKey.accessKey, privateKey.secretKey)
    return

initMainUI()