import json

from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# для тестирования использовать Chrome, другие браузеры как то странно кэшируют файлы с кодом и не обновляют их


# cntrl + shift + r чтобы обновить


@app.put("/add_pair")
def add_pair(body=Body()):
    data = json.loads(body)
    print(data)


@app.put("/delete_pair")
def delete_pair(body=Body()):
    data = json.loads(body)
    print(data)


@app.put("/replace_pair")
def replace_pair(body=Body()):
    data = json.loads(body)
    print(data)


@app.put("/get_occup")
def get_occup_pair(body=Body()):
    data = json.loads(body)
    print(data)


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
