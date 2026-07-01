import streamlit as st

st.html(open("html/classes/classes_main.html").read())

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Расписание",
        "Страница курса",
        "Коммуникация со студентами",
        "Компьютерные классы",
        "Консультации и присутственные часы",
    ]
)

with tab1:
    st.html(open("html/classes/classes_timetable.html").read())

with tab2:
    st.html(open("html/classes/classes_page.html").read())

with tab3:
    st.html(open("html/classes/classes_communication.html").read())

with tab4:
    st.html(open("html/classes/classes_computers.html").read())

with tab5:
    st.html(open("html/classes/classes_consultations.html").read())
