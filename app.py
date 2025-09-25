import streamlit as st
import pandas as pd
import os

# --- Page Configuration (PRD 4.2) ---
st.set_page_config(
    page_title="지역별/연도별 경제활동 데이터 분석",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
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

st.title("지역별/연도별 경제활동 데이터 분석")

# --- Data Loading and Caching (PRD 4.1, Non-functional: Performance) ---
@st.cache_data
def load_and_process_data():
    """
    Loads data from CSV, processes it, and calculates key metrics.
    - Caches the data to improve performance.
    - Uses a relative path for better portability.
    - Handles '계' to '전국' transformation.
    - Calculates unemployment and employment rates safely.
    """
    # Build a portable path to the CSV file
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, "경제활동_통합.csv")
    
    df = pd.read_csv(csv_path)
    
    # Data cleaning (PRD 4.1)
    df['지역'] = df['지역'].replace('계', '전국')

    # Calculate metrics safely (PRD 3, Non-functional: Robustness)
    # Avoid division by zero
    active_pop = df['경제활동인구 (천명)']
    
    df['실업률 (%)'] = (df['실업자 (천명)'] / active_pop * 100).where(active_pop > 0, 0)
    df['고용률 (경제활동인구 대비, %)'] = (df['취업자 (천명)'] / active_pop * 100).where(active_pop > 0, 0)
    
    return df

# Load the data using the cached function
df = load_and_process_data()


# --- Sidebar for User Input (PRD 4.2) ---
st.sidebar.title("년도 선택")
years = sorted(df['년도'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("분석할 년도를 선택하세요.", years)


# --- Main Panel Display ---
st.header(f"{selected_year}년 경제활동 데이터 분석")

# Filter data based on selected year
filtered_df = df[df['년도'] == selected_year]


# --- Display Data Table (PRD 4.2) ---
st.subheader("데이터 테이블")

# Format the rate columns for display without altering the original dataframe
display_df = filtered_df.copy()
display_df['실업률 (%)'] = display_df['실업률 (%)'].map('{:.2f}%'.format)
display_df['고용률 (경제활동인구 대비, %)'] = display_df['고용률 (경제활동인구 대비, %)'].map('{:.2f}%'.format)
st.dataframe(display_df)


# --- Display Charts (PRD 4.2) ---
st.subheader("지역별 비교 시각화")

# Prepare data for charting
chart_df = filtered_df.set_index('지역')

# Bar chart for Unemployment Rate
st.markdown("#### 지역별 실업률 (%)")
st.bar_chart(chart_df['실업률 (%)'])

# Bar chart for Employment Rate
st.markdown("#### 지역별 고용률 (경제활동인구 대비, %)")
st.bar_chart(chart_df['고용률 (경제활동인구 대비, %)'])