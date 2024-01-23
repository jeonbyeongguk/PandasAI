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
            st.warning("Unsupported file format. Please upload a CSV or Excel file.")
            st.stop()
    except UnicodeDecodeError:
        st.error("Error decoding the file. Please check the file's encoding.")
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
