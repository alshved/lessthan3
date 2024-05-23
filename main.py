from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# для тестирования использовать Chrome, другие браузеры как то странно кэшируют файлы с кодом и не обновляют их


# cntrl + shift + r чтобы обновить
@app.put("/test")
def get_info(data=Body()):
    print("received put request from front. Request info:")
    print(data)
    return data


@app.put("/add_pair")
def add_pair(data=Body()):
    print(data)


@app.put("/delete_pair")
def add_pair(data=Body()):
    print(data)


@app.put("/update_pair")
def add_pair(data=Body()):
    print(data)


@app.get("/")
def root():
    return FileResponse("static/index.html")


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
