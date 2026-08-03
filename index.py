import pymorphy3
import spacy
from pathlib import Path
from bs4 import BeautifulSoup
from whoosh.fields import Schema, ID, TEXT
import os.path
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from rapidfuzz import process, fuzz, utils
import shutil

nlp = spacy.load("ru_core_news_sm")
morph = pymorphy3.MorphAnalyzer()

names = {
    "extra.html": "Важные ссылки",
    "main.html": "Главная страница",
    "registration_contract.html": "Заключение договора",
    "registration_sources.html": "Электронные ресурсы",
    "registration_main.html": "Оформление преподавателей",
    "marks_eval.html": "Выставление оценок",
    "marks_exams.html": "Сессия",
    "marks_main.html": "Оценивание студентов",
    "marks_cheating.html": "Списывание",
    "marks_retake.html": "Пересдачи и отчисление",
    "marks_skip.html": "Пропуск форм контроля",
    "assistants_main.html": "Учебные ассистенты",
    "assistants_booking.html": "Бронирование УА",
    "assistants_duties.html": "Обязанности УА",
    "assistants_coordinators.html": "Старшие ассистенты",
    "classes_consultations.html": "Консультации и присутственные часы",
    "classes_page.html": "Страница курса",
    "classes_computers.html": "Компьютерные классы",
    "classes_communication.html": "Коммуникация со студентами",
    "classes_main.html": "Проведение занятий",
    "classes_timetable.html": "Расписание",
    "smartlms_main.html": "Работа с SmartLMS",
    "smartlms_marks.html": "Оценки в SmartLMS",
    "smartlms_materials.html": "Материалы в SmartLMS",
    "smartlms_midterm-1.html": "Создание форм контроля в SmartLMS",
    "smartlms_midterm-2.html": "Отображение форм контроля в SmartLMS",
    "smartlms_users.html": "Группы и пользователи в SmartLMS",
    "team_project.html": "Проектный офис",
    "team_coordinators.html": "Методический отдел",
    "team_main.html": "Команда проекта",
    "iads_main.html": "Независимые экзамены",
    "iads_levels.html": "Уровни экзаменов",
    "iads_recalculate.html": "Перезачет",
    "iads_what.html": "Что такое НЭ?"
}


def textPreprocess(text):
    """
    This function tokenizes text via spacy and lemmatize each token
    via pymorphy. In addition, whitespaces and punctuation is deleted.
    :param text: a string of the text
    :returns: a string of the preprocessed text
    """
    processedText = [
        morph.parse(token.text)[0].normal_form
        for token in nlp(text)
        if not token.is_punct and not token.is_space
    ]
    return " ".join(processedText)


def htmlParser():
    """
    This function is a parser of the html-content from the website.
    It extracts the text from each page that is placed in html dir
    and preprocessed it for further indexation.
    There are no parameters.
    :returns: a dictionary where key is name of the file and values
    are tuples that consists of page title, processed text and
    original text from html.
    """
    pages = {}
    path = Path.cwd() / "html"
    for file in Path(path).rglob("*.html"):
        if "main" not in file.name:
            soup = BeautifulSoup(open(file).read(), "html.parser")
            pages[file.name] = (
                names[file.name],
                textPreprocess(soup.get_text()),
                soup.get_text(),
            )
    return pages


def buildIndex():
    """
    This function creates indexation of html pages for further
    searching via whoosh.
    There are no parameters.
    :returns: 0 when the code is succesfully executed
    """
    pages = htmlParser()
    schema = Schema(
        title=TEXT(stored=True),
        path=ID(stored=True),
        content=TEXT(stored=True),
        text=TEXT(stored=True),
    )

    if os.path.exists("indexDir"):
        shutil.rmtree("indexDir")

    os.mkdir("indexDir")
    ix = create_in("indexDir", schema)

    writer = ix.writer()

    for page in pages:
        writer.add_document(
            title=pages[page][0],
            path=f"/{page.split('_')[0]}",
            content=pages[page][1],
            text=pages[page][2],
        )
    writer.commit()

    return 0


def search(userQuery):
    """
    This function is an implementation of the search via whoosh. Before
    searching, each token is preprocessed and checked on the issue of
    typos via rapidfuzz.
    :param userQuery: string, query from the user
    :returns: a dictionary, where key is a tuple of the page's title and path on the website
    and value is a list with strings. Each string is a preview of the page's text with highlighted
    tokens from query.
    """
    ix = open_dir("indexDir")

    output = {}

    with ix.searcher() as searcher:
        vocabulary = {term.decode("utf-8") for term in searcher.lexicon("content")}

        userQueryChecked = []

        for word in userQuery.split():
            checkedWord, ratio, _ = process.extractOne(
                word, vocabulary, scorer=fuzz.QRatio, processor=utils.default_process
            )
            if ratio > 80:
                userQueryChecked.append(checkedWord)

        userQueryLemmatized = textPreprocess(" ".join(userQueryChecked))
        query = QueryParser("content", ix.schema).parse(userQueryLemmatized)
        results = searcher.search(query)

        for r in results:
            output[(r["title"], r["path"])] = []
            for lemma in userQueryLemmatized.split():
                splittedText = r["text"].split()
                for i in range(len(splittedText)):
                    if lemma == textPreprocess(splittedText[i]):
                        preview = f"...{' '.join(splittedText[max(0, i-5):i])} <mark style='color: #2300fa;''>{splittedText[i]}</mark> {' '.join(splittedText[i + 1:min(i+6, len(splittedText))])}..."
                        output[(r["title"], r["path"])].append(preview)
        return output


# Run this function if the content of the pages has changed and index must be rebuilt.
buildIndex()
