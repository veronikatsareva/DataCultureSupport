import streamlit as st

st.html(open("html/iads/iads_main.html").read())

tab1, tab2, tab3 = st.tabs(["Что это?", "Уровни экзаменов", "Перезачет"])

with tab1:
    st.html(open("html/iads/iads_what.html").read())

with tab2:
    st.html(open("html/iads/iads_levels.html").read())

with tab3:
    st.html(open("html/iads/iads_recalculate.html").read())