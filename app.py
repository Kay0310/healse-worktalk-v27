
import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import base64
import os

st.set_page_config(layout="centered")

st.markdown("### 사진 1장 업로드 ➜ 질문 4개 응답 ➜ 저장 ➜ 다음 사진 순서대로 진행해 주세요.")

# 로고 표시
st.image("WORK_TALK_small.png", use_container_width=True)

if "responses" not in st.session_state:
    st.session_state["responses"] = []

with st.form(key="work_form"):
    name = st.text_input("이름")
    department = st.text_input("부서")

    uploaded_file = st.file_uploader("📷 작업 사진 업로드", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, use_column_width=True)
        question1 = st.text_input("어떤 작업을 하고 있는 건가요?")
        question2 = st.text_input("이 작업은 왜 위험하다고 생각하나요?")
        question3 = st.radio("이 작업은 얼마나 자주 하나요?", ["연 1-2회", "반기 1-2회", "월 2-3회", "주 1회 이상", "매일"])
        question4 = st.radio(
            "이 작업은 얼마나 위험하다고 생각하나요?",
            [
                "약간의 위험: 일회용 밴드 치료 필요 가능성 있음",
                "조금 위험: 병원 치료 필요. 1-2일 치료 및 휴식",
                "위험: 보름 이상의 휴식이 필요한 중상 가능성 있음",
                "매우 위험: 불가역적 장애 또는 사망 가능성 있음"
            ]
        )

    submitted = st.form_submit_button("💾 저장하기")

    if submitted and uploaded_file:
        response = {
            "날짜": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "이름": name,
            "부서": department,
            "사진파일명": uploaded_file.name,
            "질문1": question1,
            "질문2": question2,
            "질문3": question3,
            "질문4": question4,
        }
        st.session_state["responses"].append(response)

        with open(os.path.join("uploaded", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("💾 저장 완료! 다음 사진을 입력해 주세요.")

# 응답 저장
if st.session_state["responses"]:
    df = pd.DataFrame(st.session_state["responses"])
    df.to_excel("응답_결과.xlsx", index=False)

    with open("응답_결과.xlsx", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="응답_결과.xlsx">📥 응답 결과 다운로드</a>'
        st.markdown(href, unsafe_allow_html=True)
    