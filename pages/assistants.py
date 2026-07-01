import streamlit as st

st.html(open("html/assistants/assistants_main.html").read())

tab1, tab2 = st.tabs(["Обязанности УА", "Бронирование УА"])

with tab1:
    st.html(open("html/assistants/assistants_duties.html").read())

with tab2:
    st.html(open("html/assistants/assistants_booking.html").read())
