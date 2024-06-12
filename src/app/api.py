import logging

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
template_response = templates.TemplateResponse


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "events": []})


@app.post("/events")
async def find_events(
    request: Request,
    event_type: str = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    preferences: str = Form(...),
):
    events = [
        {
            "name": "Concert A",
            "description": "A great concert.",
            "date": "2024-07-01",
            "location": "Brno",
        },
        {
            "name": "Exhibition B",
            "description": "An amazing exhibition.",
            "date": "2024-07-02",
            "location": "Brno",
        },
    ]
    return templates.TemplateResponse(
        "index.html", {"request": request, "events": events}
    )
