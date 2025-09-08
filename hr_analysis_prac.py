import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
# plt.rcParams['font.family'] = 'AppleGothic' # Mac
# plt.rcParams['font.family'] = 'NanumGothic' # Linux / Nanum 설치 시

# 그래프 예시
tips = sns.load_dataset("tips")
fig, ax = plt.subplots()
sns.barplot(x="day", y="total_bill", data=tips, ax=ax)
ax.set_title("요일별 총 지출")  # 한글 제목
ax.set_xlabel("요일")
ax.set_ylabel("총 지출")

st.pyplot(fig)
