from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

# Монтируем статические файлы из каталога frontend на корень /frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check_post")
async def check_post(message: str = Form(...)):
    return {"status": "true" if "говно" not in message.lower() else "false"}

@app.get("/result")
async def show_result(request: Request, status: str):
    status_bool = status.lower() == "true"  # Преобразование строки в булево значение
    return templates.TemplateResponse("result.html", {"request": request, "status": status_bool})
