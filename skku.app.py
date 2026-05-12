import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Hello SKKU",
    page_icon="🎓",
    layout="wide"
)

# 제목
st.title("Hello, SKKU! 🎓")

# 설명
st.write("My first Streamlit web app")

# 섹션
st.subheader("성균관대학교 Streamlit 연습")

# 성공 메시지
st.success("웹앱 실행 성공!")

# 버튼 예시
if st.button("클릭해보기"):
    st.balloons()
    st.write("버튼이 눌렸습니다!")
