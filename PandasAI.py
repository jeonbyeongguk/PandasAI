from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd 
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import time

load_dotenv()

API_KEY = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(api_token=API_KEY)

# 페이지 기본 설정
st.set_page_config(
    page_icon="🐼",
    page_title="PandasAI prompt data analysis",
    layout="wide",
)


st.title("🐼[PandasAI] prompt data analysis")

uploaded_file = st.file_uploader("'CSV' 또는 'xlsx' 파일 업로드하세요!!", type=['csv', 'xlsx'])


if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_extension == 'csv':
            #csv 파일 읽기
            df = pd.read_csv(uploaded_file)

        elif file_extension == 'xlsx':
            # Excel 파일 읽기
            df = pd.read_excel(uploaded_file)
        else:
            st.warning("지원하지 않는 파일 포맷입니다. CSV or Excel 파일을 올려주세요.")
            st.stop()
    except UnicodeDecodeError:
        st.error("이 형식의 파일은 업로드가 되지 않습니다. .xlsx 파일로 변환해서 올려주세요.")
        st.error("변환 사이트: https://convertio.co/kr/csv-xlsx/")
        st.stop()
    
    # 데이터 프레임 확장
    st.dataframe(df.head(100), use_container_width=True)

    num_rows, um_columns = df.shape

    columns = df.columns.tolist()

    st.write(f"행 개수: {num_rows} |  열 개수 : {um_columns}")
    
    st.write(f"열이름: {columns}")

    prompt = st.text_area("Enter your prompt")

    if st.button("Generate"):
        start_time = time.time()

        if prompt:
            st.write("PandasAI is generating an answer, please wait...")
            query_engine = SmartDataframe(df, config={"llm": llm})
            answer = query_engine.chat(prompt)
            st.write(answer)
        else:
            st.warning("Please enter a prompt.")
        end_time = time.time()

        execution_time = end_time - start_time

        st.write(f"코드실행 시간: {execution_time:.1f}초")
