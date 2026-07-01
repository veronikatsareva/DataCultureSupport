import streamlit as st

st.html(open("html/team/team_main.html").read())

tab1, tab2 = st.tabs(["Проектный офис", "Методический отдел"])

with tab1:
    st.html(open("html/team/team_project.html").read())

with tab2:
    st.html(open("html/team/team_coordinators.html").read())
