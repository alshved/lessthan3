import json

from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
import uvicorn
from DBApi import DataBase
from quickstart import GoogleApi

google_api = GoogleApi()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# для тестирования использовать Chrome, другие браузеры как то странно кэшируют файлы с кодом и не обновляют их


# cntrl + shift + r чтобы обновить


@app.put("/add_pair")
def add_pair(body=Body()):
    """
    Функция для обработки запроса с сайта о добавлении пары в базу данных и гугл календарь
    :param body: тело запроса
    :return: None
    """
    data = json.loads(body)
    db = DataBase("LessonsDB.db")
    print(data)
    db.add_lesson(data['cabinet'], data['group'], data['teacher'],
                  data['start_time'], data['end_time'], data['subject'], data['date'],
                  data['type'] == 'one')
    pair = dict()
    pair['subject'] = data['subject']
    pair['cabinet'] = data['cabinet']
    pair['date'] = data['date']
    pair['time_start'] = data['start_time']
    pair['time_finish'] = data['end_time']
    pair['teacher'] = data['teacher']
    pair['group'] = data['group']
    google_api.load_one_pair(pair)


@app.put("/delete_pair")
def delete_pair(body=Body()):
    """
    Функция для обработки запроса с сайта об удалении пары в базе данных и гугл календаре
    :param body: тело запроса
    :return: None
    """
    data = json.loads(body)
    print(data)
    pair = dict()
    pair['subject'] = data['subject']
    pair['cabinet'] = data['cabinet']
    pair['date'] = data['date']
    pair['time_start'] = data['start_time']
    pair['time_finish'] = data['end_time']
    pair['teacher'] = data['teacher']
    pair['group'] = data['group']
    google_api.delete_one_pair(pair)
    db = DataBase("LessonsDB.db")
    db.delete_lesson(data['cabinet'], data['start_time'], data['date'])


@app.put("/replace_pair")
def replace_pair(body=Body()):
    """
    Функция для обработки запроса с сайта об изменении пары в базе данных и гугл календаре.
    :param body: тело запроса
    :return: None
    """
    data = json.loads(body)
    print(data)
    pair_old = dict()
    pair_old['subject'] = data['subject_before']
    pair_old['cabinet'] = data['cabinet_before']
    pair_old['date'] = data['date_before']
    pair_old['time_start'] = data['start_time_before']
    pair_old['time_finish'] = data['end_time_before']
    pair_old['teacher'] = data['teacher_before']
    pair_old['group'] = data['group_before']

    pair_new = dict()
    pair_new['subject'] = data['subject_after']
    pair_new['cabinet'] = data['cabinet_after']
    pair_new['date'] = data['date_after']
    pair_new['time_start'] = data['start_time_after']
    pair_new['time_finish'] = data['end_time_after']
    pair_new['teacher'] = data['teacher_after']
    pair_new['group'] = data['group_after']

    google_api.update_one_pair(pair_old, pair_new)
    db = DataBase("LessonsDB.db")
    db.delete_lesson(data['cabinet_before'], data['start_time_before'], data['date_before'])
    db.add_lesson(data['cabinet_after'], data['group_after'], data['teacher_after'],
                  data['start_time_after'], data['end_time_after'], data['subject_after'], data['date_after'],
                  data['type'] == 'one')
    print("succesfully replaced")


@app.put("/get_occup")
def get_occup_pair(body=Body()):
    """
    Функция для обработк запроса с сайта о занятости какого-либо кабинета.
    :param body: тело запроса
    :return: None
    """
    data = json.loads(body)
    print(data)
    db = DataBase("LessonsDB.db")
    res = db.is_lesson_in_table(data['cabinet'], data['start_time'], data['date'])
    return Response(content="get_occup", media_type="text/plain", headers={"result": str(res)})


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.put("/sync")
def sync_db():
    """
    Функция для синхронизации базы данных и гугл календаря.
    :return: None
    """

    # Ищет в базе данных пары, которые не опубликованы в гугл календаре (у таких пар нет google_id),
    # и добавляет их в гугл календарь.
    
    db = DataBase("LessonsDB.db")
    data = db.select_all()
    for pair in data:
        # если нет google-id, то значит пары нет в гугл календаре
        if not pair['google_id']:
            google_api.load_one_pair(pair)


if __name__ == "__main__":
    # поставить reload=False для прода
    uvicorn.run("main:app", reload=False)
    google_api = GoogleApi()
