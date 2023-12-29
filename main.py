from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from backend.shitpost_classifier import is_shitpost

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/check_post")
async def check_post(message: str = Form(...)):
    return {"status": "true" if is_shitpost(message) else "false"}


@app.get("/result")
async def show_result(request: Request, status: str):
    status_bool = status.lower() == "true"
    return templates.TemplateResponse("result.html", {"request": request, "status": status_bool})
