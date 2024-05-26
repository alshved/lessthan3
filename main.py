import json

from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
import uvicorn
from DBApi import DataBase

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# для тестирования использовать Chrome, другие браузеры как то странно кэшируют файлы с кодом и не обновляют их


# cntrl + shift + r чтобы обновить


@app.put("/add_pair")
def add_pair(body=Body()):
    data = json.loads(body)
    db = DataBase("LessonsDB.db")
    print(data)
    db.add_lesson(data['cabinet'], data['group'], data['teacher'],
                  data['start_time'], data['end_time'], data['subject'], data['date'],
                  data['type'] == 'one')


@app.put("/delete_pair")
def delete_pair(body=Body()):
    data = json.loads(body)
    print(data)
    db = DataBase("LessonsDB.db")
    db.delete_lesson(data['cabinet'], data['start_time'], data['date'])


@app.put("/replace_pair")
def replace_pair(body=Body()):
    data = json.loads(body)
    print(data)
    db = DataBase("LessonsDB.db")
    db.delete_lesson(data['cabinet_before'], data['start_time_before'], data['date_before'])
    db.add_lesson(data['cabinet_after'], data['group_after'], data['teacher_after'],
                  data['start_time_after'], data['end_time_after'], data['subject_after'], data['date_after'],
                  data['type'] == 'one')


@app.put("/get_occup")
def get_occup_pair(body=Body()):
    data = json.loads(body)
    print(data)
    db = DataBase("LessonsDB.db")
    res = db.is_lesson_in_table(data['cabinet'], data['start_time'], data['date'])
    return Response(content="get_occup", media_type="text/plain", headers={"result": str(res)})


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/sync")
def sync_db():
    print('sync')


# @app.get("/StyleSheet.css")
# def get_css():
#     return FileResponse("StyleSheet.css")#
# @app.get("/main.js")
# def get_js():
#     print("s")
#     return FileResponse("main.js")


if __name__ == "__main__":
    # поставить reload=False для прода
    uvicorn.run("main:app", reload=True)
