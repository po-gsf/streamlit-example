from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st


##############################################################
# example
##############################################################
def initView() :
    st.title('ChatGSF')
    st.header('My header')
    st.subheader('My sub')
    st.text('Fixed width text')
    st.caption('Balloons. Hundreds of them...')
    st.code('for i in range(8): foo()')
    return 

def initComponent() :
    st.button('Button')
    st.checkbox('')
    st.radio('', ['yes','no'])
    st.selectbox('', [1,2,3])
    st.multiselect('', [1,2,3])
    st.slider('', min_value=0, max_value=10)
    st.text_input('EditBox')
    st.number_input('Enter a number')
    st.text_area('Area for textual entry')
    st.date_input('캘린더')
    st.time_input('Time Picker?') 
    st.file_uploader('파일 업로드 다이얼로그') 
    st.camera_input("카메라 열기") 
    st.color_picker('색상 선택 Picker')
    return

def initComponent2() :
    for i in range(int(st.number_input('Num:'))): foo()
    if st.sidebar.selectbox('I:',['f']) == 'f': b()
    my_slider_val = st.slider('Quinn Mallory', 1, 88)
    st.write(slider_val)
    st.slider('Pick a number', 0, 100, disabled=True)
    return

def connectDataSource() :
    st.experimental_connection('pets_db', type='sql')
    conn = st.experimental_connection('sql')
    conn = st.experimental_connection('snowpark')
    class MyConnection(ExperimentalBaseConnection[myconn.MyConnection]):
        def _connect(self, **kwargs) -> MyConnection:
            return myconn.connect(**self._secrets, **kwargs)
        def query(self, query):
            return self._instance.query(query)
    return

def displayData() :
    st.dataframe(my_dataframe)
    st.table(data.iloc[0:10])
    st.json({'foo':'bar','fu':'ba'})
    st.metric(label="Temp", value="273 K", delta="1.2 K")
    return

def displayMedia() :
    st.image('./header.png')
    st.audio(data)
    st.video(data)
    return

def columns() :
    col1, col2 = st.columns(2)
    col1.write('Column 1')
    col2.write('Column 2')

    # Three columns with different widths
    col1, col2, col3 = st.columns([3,1,1])
    with col1:
        st.write('column 1')
    with col2:
        st.write('column 2')
    with col3:
        st.write('column 3')
    return 

def tap() :
    # Insert containers separated into tabs:
    tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
    tab1.write("this is tab 1")
    tab2.write("this is tab 2")

    with tab1:
        st.radio('Select one:', [1, 2])
    return

def controlFlow() :
    st.stop()
    st.experimental_rerun()

    with st.form(key='my_form'):
        username = st.text_input('Username')
        password = st.text_input('Password')
        st.form_submit_button('Login')
    return

def personalize_Apps_For_Users ():
    if st.user.email == 'jane@email.com':
        initView()
    elif st.user.email == 'adam@foocorp.io':
        initView()
    else:
        st.write("Please contact us to get access!")
    return

def build_chat_based_apps ():
    with st.chat_message("user"):
        st.write("Hello 👋")
        st.line_chart(np.random.randn(30, 3))
    
    st.chat_input("Say something")
    return

def mutate_data ():
    element = st.dataframe(df1)
    element.add_rows(df2)
    element = st.line_chart(df1)
    element.add_rows(df2)
    return

def displayCode() :
    st.echo()
    with st.echo():
        st.write('Code will be executed and printed')
    return

def placeholders_help_and_options():
    element = st.empty()
    element.line_chart(...)
    element.text_input(...)
    
    elements = st.container()
    elements.line_chart(...)
    st.write("Hello")
    elements.text_input(...)

    st.help(pandas.DataFrame)
    st.get_option(key)
    st.set_option(key, value)
    st.set_page_config(layout='wide')
    st.experimental_show(objects)
    st.experimental_get_query_params()
    st.experimental_set_query_params(**params)
    return

def optimize_performance():
    @st.cache_data
    def foo(bar):
        return bar
    d1 = foo(ref1)
    d2 = foo(ref1)
    d3 = foo(ref2)
    foo.clear()
    st.cache_data.clear()
    return

def optimize_performance_cache():
    @st.cache_resource
    def foo(bar):
        return session
    s1 = foo(ref1)
    s2 = foo(ref1)
    s3 = foo(ref2)
    foo.clear()
    st.cache_resource.clear()
    return

def display_progress_and_status():
    with st.spinner(text='In progress'):
        time.sleep(3)
        st.success('Done')

    bar = st.progress(50)
    time.sleep(3)
    bar.progress(100)

    st.balloons()
    st.snow()
    st.toast('Mr Stay-Puft')
    st.error('Error message')
    st.warning('Warning message')
    st.info('Info message')
    st.success('Success message')
    st.exception(e)
    return

##############################################################
# 정상동작 되는 함수들
initView()
initComponent()
columns()
tap()
controlFlow()
displayCode()






