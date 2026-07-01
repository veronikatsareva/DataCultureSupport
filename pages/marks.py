import streamlit as st

st.html(open("html/marks/marks_main.html").read())

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Выставление оценок", "Сессия", "Пересдачи и отчисление", "Списывание", "Пропуск форм контроля"])

with tab1:
    st.html(open("html/marks/marks_eval.html").read())

with tab2:
    st.html(open("html/marks/marks_exams.html").read())

with tab3:
    st.html(open("html/marks/marks_retake.html").read())

with tab4:
    st.html(open("html/marks/marks_cheating.html").read())