import streamlit as st
import index


def load_css():
    """
    This function loads css styles from styles.css for rendering htmls of the pages.
    There are no parameters.
    :returns: 0 when the code is succesfully executed.
    """
    with open("styles/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    return 0


def add_banner():
    """
    This function add a running banner to the top of the pages.
    There are no parameters.
    :returns: 0 when the code is succesfully executed.
    """
    st.markdown(
        """
        <div class="banner-header">
            <div class="banner-track">
                <img src="https://raw.githubusercontent.com/veronikatsareva/DataCultureSupport/refs/heads/main/static/%D0%B1%D0%B5%D0%B3%D1%83%D1%89%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B0.png">
                <img src="https://raw.githubusercontent.com/veronikatsareva/DataCultureSupport/refs/heads/main/static/%D0%B1%D0%B5%D0%B3%D1%83%D1%89%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B0.png">
                <img src="https://raw.githubusercontent.com/veronikatsareva/DataCultureSupport/refs/heads/main/static/%D0%B1%D0%B5%D0%B3%D1%83%D1%89%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B0.png">
                <img src="https://raw.githubusercontent.com/veronikatsareva/DataCultureSupport/refs/heads/main/static/%D0%B1%D0%B5%D0%B3%D1%83%D1%89%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B0.png">
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return 0


load_css()
add_banner()

st.set_page_config(
    page_title="Data Culture Support", page_icon="static/icons/logo_green.jpeg"
)

st.logo("static/icons/logo_green.jpeg")

pageMain = st.Page("pages/main.py", title="Главная страница")
pageTeam = st.Page("pages/team.py", title="Команда проекта")
pageOrg = st.Page("pages/registration.py", title="Оформление преподавателей")
pageClasses = st.Page("pages/classes.py", title="Проведение занятий")
pageAssistance = st.Page("pages/assistants.py", title="Учебные ассистенты")
pageMarks = st.Page("pages/marks.py", title="Оценивание студентов")
pageExams = st.Page("pages/iads.py", title="Независимые экзамены")
pageLMS = st.Page("pages/smartlms.py", title="Работа с SmartLMS")
pageRef = st.Page("pages/extra.py", title="Полезные ссылки")

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

with st.sidebar:
    st.markdown(
        "<h3 class='sidebar-title'>Справочник преподавателя проекта «Культура работы с данными» (Data Culture) <br> ФКН НИУ ВШЭ</h3><hr>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h3 style='padding-top:0;'>Поиск по сайту</h3>", unsafe_allow_html=True
    )

    query = st.text_input(
        "Запрос пользователя",
        label_visibility="collapsed",
        placeholder="Введите запрос",
    )

    if query:
        results = index.search(query)

        if not results:
            st.info("Ничего не найдено")

        for title, path in results:
            st.page_link("pages/" + path + ".py", label=f"{title}")

            for preview in results[(title, path)]:
                st.markdown(f"<p>{preview}</p>", unsafe_allow_html=True)
            st.markdown(f"<br>", unsafe_allow_html=True)

pg.run()
