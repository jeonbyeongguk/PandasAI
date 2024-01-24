## pages/1_Docs.py

import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_icon="🐼",
    page_title="Docs",
    layout="wide",
)

# 제목 생성
st.subheader("Pandas AI 코드 예시")

if st.button("소스 코드 보기"):
    code = '''
    import pandas as pd
    from pandasai import SmartDataframe
    
    # Sample DataFrame
    df = pd.DataFrame({
        "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
        "gdp": [19294482071552, 2891615567872, 2411255037952, 3435817336832, 1745433788416, 1181205135360, 1607402389504, 1490967855104, 4380756541440, 14631844184064],
        "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12]
    })
    
    # Instantiate a LLM
    from pandasai.llm import OpenAI
    llm = OpenAI(api_token="YOUR_API_TOKEN")
    
    df = SmartDataframe(df, config={"llm": llm})
    df.chat('Which are the 5 happiest countries?')
    '''
    st.code(code, language='python')
