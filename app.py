import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(
    page_title="지역별/연도별 경제활동 데이터 조회",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(to right, #89CFF0, #FFB6C1);
    }
    .st-sidebar {
        background-color: #FFB6C1;
    }
</style>
""", unsafe_allow_html=True)


st.title("지역별/연도별 경제활동 데이터 조회")

# Load data
script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir, "경제활동_통합.csv")
df = pd.read_csv(csv_path)

# Data manipulation
df['지역'] = df['지역'].replace('계', '전국')

# Sidebar
st.sidebar.title("년도 선택")
years = sorted(df['년도'].unique())
selected_year = st.sidebar.selectbox("년도를 선택하세요.", years)

# Filter data
filtered_df = df[df['년도'] == selected_year]

# Display data
st.write(f"### {selected_year}년 경제활동인구 통계")
st.dataframe(filtered_df)