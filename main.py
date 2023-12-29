from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

# Mount the 'frontend' directory
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check_post")
async def check_post(message: str = Form(...)):
    # Redirect to the /result route with the status as a query parameter
    status = "говно" not in message.lower()
    return RedirectResponse(url=f"/result?status={status}")

@app.get("/result")
async def show_result(request: Request, status: bool):
    # Convert the 'status' query parameter to a boolean and render the template
    return templates.TemplateResponse("result.html", {"request": request, "status": status})
