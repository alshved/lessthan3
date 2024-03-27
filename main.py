from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="D:\\vueproject1\\api\\.venv\\Scripts"))


# для тестирования использовать Chrome, другие браузеры как то странно кэшируют файлы с кодом и не обновляют их
@app.post("/test")
def test():
    return HTMLResponse(content="<h2>this is test post request</h2>")


@app.put("/test")
def get_info(data=Body()):
    print("received put request from front. Request info:")
    print(data)
    return data


@app.get("/")
def root():
    return FileResponse("index.html")


@app.get("/StyleSheet.css")
def get_css():
    return FileResponse("StyleSheet.css")


@app.get("/main.js")
def get_js():
    print("s")
    return FileResponse("main.js")


if __name__ == "__main__":
    # поставить reload=True для обновления страницы при обновлении
    # кода во время разработки
    uvicorn.run("main:app", reload=True)
