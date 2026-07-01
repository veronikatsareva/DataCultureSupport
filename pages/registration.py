import streamlit as st

st.html(open("html/registration/registration_main.html").read())

tab1, tab2 = st.tabs(["Заключение договора", "Электронные ресурсы"])

with tab1:
    st.html(open("html/registration/registration_contract.html").read())

with tab2:
    st.html(open("html/registration/registration_sources.html").read())