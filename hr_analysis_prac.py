import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');

    /* 앱 전체 텍스트 */
    * {
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="퇴직율 대시보드", layout="wide")
sns.set_theme(style="whitegrid", font='Noto Sans KR')

# 1) 데이터 로드
@st.cache_data
def load_df(path:str ="HR Data.csv") -> pd.DataFrame:
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except: 
        return df 
    df["퇴직"] = df["퇴직여부"].map({"Yes":1, "No":0}).astype("int8")
    df.drop(['직원수', '18세이상'], axis=1, inplace=True)
    return df

df = load_df()
if df.empty:
    st.error("데이터가 없습니다. 'HR Data.csv' 파일을 확인하세요.")
    st.stop()

# ===== KPI  =====
# 1) 헤더 & KPI
st.title("퇴직율 분석 및 인사이트")
n = len(df); quit_n = int(df["퇴직"].sum())
quit_rate = df["퇴직"].mean()*100
stay_rate = 100 - quit_rate
k1,k2,k3,k4 = st.columns(4)
k1.metric("전체 직원 수", f"{n:,}명")
k2.metric("퇴직자 수", f"{quit_n:,}명")
k3.metric("유지율", f"{stay_rate:.1f}%")
k4.metric("퇴직율", f"{quit_rate:.1f}%")

dept_rate = df.groupby('부서')['퇴직'].mean().sort_values(ascending=False)
k1,k2 = st.columns(2)
k1.metric(f"가장 높은 퇴직율 부서: {dept_rate.index[0]}", f"{dept_rate.iloc[0]*100:.1f}%")
k2.metric(f"가장 낮은 퇴직율 부서: {dept_rate.index[-1]}", f"{dept_rate.iloc[-1]*100:.1f}%")

# 4) 그래프 2/3를 두 칼럼으로
c1, c2 = st.columns(2)

# (좌) 연령대와 퇴직율
if "나이" in df.columns:
    tmp = df[["나이","퇴직"]].dropna().copy()
    tmp['연령대'] = pd.cut(tmp['나이'], bins=[18, 29, 39, 49, 59, 69], labels=['20대', '30대', '40대', '50대', '60대'])
    age = tmp.groupby("연령대")["퇴직"].mean()*100
    with c1:
        st.subheader("연령대와 퇴직율")
        fig2, ax2 = plt.subplots(figsize=(6.5,4))
        sns.lineplot(x=age.index, y=age.values, marker="o", ax=ax2)
        ax2.set_xlabel("연령대"); 
        ax2.set_ylabel("퇴직율(%)")
        st.pyplot(fig2)

# (우) 야근정도별 퇴직율 (Yes/No 막대)
col_name = "결혼여부"
if col_name in df.columns:
    ot = (df.groupby(col_name)["퇴직"].mean()*100)
#    ot.index = ot.index.map({"No":"없음","Yes":"있음"}).astype(str)
    with c2:
        st.subheader("결혼 여부 별 퇴직율")
        fig3, ax3 = plt.subplots(figsize=(6.5,4))
        sns.barplot(x=ot.index, y=ot.values, ax=ax3)
        ax3.set_ylabel("퇴직율(%)"); 
        ax3.bar_label(ax3.containers[0], fmt="%.1f")
        st.pyplot(fig3)
