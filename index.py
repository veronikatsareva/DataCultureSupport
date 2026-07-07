import pymorphy3
import spacy
from pathlib import Path
from bs4 import BeautifulSoup
from whoosh.fields import Schema, ID, TEXT
import os.path
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
import shutil

nlp = spacy.load("ru_core_news_sm")
morph = pymorphy3.MorphAnalyzer()

names = {
    "extra.html": "Важные ссылки",
    "main.html": "Главная",
    "registration_contract.html": "Заключение договора",
    "registration_sources.html": "Электронные ресурсы",
    "registration_main.html": "Оформление преподавателей",
    "marks_eval.html": "Выставление оценок",
    "marks_exams.html": "Сессия",
    "marks_main.html": "Оценивание студентов",
    "marks_cheating.html": "Списывание",
    "marks_retake.html": "Пересдачи и отчисление",
    "marks_skip.html": "Пропуск форм контроля",
    "assistants_main.html": "Учебные Ассистенты",
    "assistants_booking.html": "Бронирование УА",
    "assistants_duties.html": "Обязанности УА",
    "classes_consultations.html": "Консультации и присутственные часы",
    "classes_page.html": "Страница курса",
    "classes_computers.html": "Компьютерные классы",
    "classes_communication.html": "Коммуникация со студентами",
    "classes_main.html": "Проведение занятий",
    "classes_timetable.html": "Расписание",
    "smartlms_main.html": "Работа с SmartLMS",
    "team_project.html": "Проектный офис",
    "team_coordinators.html": "Методический отдел",
    "team_main.html": "Команда проекта",
    "iads_main.html": "Независимые экзамены",
}


def textPreprocess(text):
    """ """
    processedText = [
        morph.parse(token.text)[0].normal_form
        for token in nlp(text)
        if not token.is_punct and not token.is_space
    ]
    return " ".join(processedText)


def htmlParser():
    """ """
    pages = {}
    path = "/Users/veronikatsareva/Desktop/DataCultureSupport/html"
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
    """ """
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
    """ """
    ix = open_dir("indexDir")

    output = {}

    with ix.searcher() as searcher:
        userQueryLemmatized = textPreprocess(userQuery)
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


# buildIndex()
