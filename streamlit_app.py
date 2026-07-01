import streamlit as st
import time


def load_css():
    with open("styles/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.set_page_config(
    page_title="Data Culture Support", page_icon="static/icons/dc_green.svg"
)

st.logo("static/icons/dc_green.svg")

st.markdown("<h1>Data Culture Support</h1>", unsafe_allow_html=True)

pageMain = st.Page("pages/main.py", title="Главная")
pageTeam = st.Page("pages/team.py", title="Команда проекта")
pageOrg = st.Page("pages/registration.py", title="Оформление преподавателей")
pageClasses = st.Page("pages/classes.py", title="Проведение занятий")
pageAssistance = st.Page("pages/assistants.py", title="Учебные Ассистенты")
pageMarks = st.Page("pages/marks.py", title="Оценивание студентов")
pageExams = st.Page("pages/iads.py", title="Независимые экзамены")
pageLMS = st.Page("pages/smartlms.py", title="Работа с SmartLMS")
pageRef = st.Page("pages/extra.py", title="Важные ссылки")

pg = st.navigation(
    [
        pageMain,
        pageTeam,
        pageOrg,
        pageClasses,
        pageAssistance,
        pageMarks,
        pageExams,
        pageLMS,
        pageRef,
    ]
)

pg.run()
