import streamlit as st

st.html(open("html/smartlms/smartlms_main.html").read())

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Группы и пользователи", "Оценки", "Загрузка материалов в оболочку", "Создание форм контроля в курсе", "Отображение форм контроля"])

with tab1:
    st.html(open("html/smartlms/smartlms_users.html").read())

with tab2:
    st.html(open("html/smartlms/smartlms_marks.html").read())

with tab3:
    st.html(open("html/smartlms/smartlms_materials.html").read())

with tab4:
    st.html(open("html/smartlms/smartlms_midterm-1.html").read())

with tab5:
    st.html(open("html/smartlms/smartlms_midterm-2.html").read())
