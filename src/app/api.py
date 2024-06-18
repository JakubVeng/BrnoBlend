import html
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.app.db.data_loader import get_events
from src.app.db.db import sa_session_transaction
from src.app.db.models import EventModel
from src.app.preferences import Preferencator3000
from src.app.schema import PreferencesForm

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
template_response = templates.TemplateResponse


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page of the apsp.
    """
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.post("/update-events")
def update_events():
    try:
        with sa_session_transaction() as session:
            events_from_api = get_events()

            # Convert API events to a dictionary with event IDs as keys for quick lookup
            api_event_dict = {event["brno_id"]: event for event in events_from_api}

            # Delete events not present in the API response
            events_to_delete = (
                session.query(EventModel)
                .filter(~EventModel.brno_id.in_(api_event_dict.keys()))
                .all()
            )
            for event in events_to_delete:
                session.delete(event)

            # Create or update events from the API response
            for event in events_from_api:
                EventModel.create_or_update(**event)

            session.commit()

            return {"message": "Database updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_categories_from_db(db_session):
    categories = db_session.query(EventModel.categories_en).distinct().all()
    unique_categories = set()
    for category in categories:
        if category.categories_en:
            unique_categories.update(category.categories_en.split(", "))
    return sorted(list(unique_categories))


@app.get("/preferences", response_class=HTMLResponse)
async def get_preferences(request: Request):
    """
    Preferences page of the app.
    """
    with sa_session_transaction() as session:
        categories = get_categories_from_db(session)
        return templates.TemplateResponse(
            "preferences.html", {"request": request, "categories": categories}
        )



# TODO: yes forms in FastAPI needs to be as post requests. If something breaks or is not working
# or u think u can do better, replace <form> in html with javascript to create form and
# send it to /results as get with body. I ain't doing the js part...
@app.post("/results", response_class=HTMLResponse)
async def get_results(
    request: Request,
    categories: list[str] = Form(...),
    date: Optional[str] = Form(None),
    limit: int = Form(...),
):
    preferences_form = PreferencesForm(categories=categories, date=date, limit=limit)
    matcher = Preferencator3000(preferences_form)

    events = matcher.match_events()

    # Format the html-encoded titles...
    for event in events:
        event.name = html.unescape(event.name)
        event.date_from = datetime.utcfromtimestamp(
            int(event.date_from) // 1000
        ).strftime("%d.%m.%Y")
        event.date_to = datetime.utcfromtimestamp(int(event.date_to) // 1000).strftime(
            "%d.%m.%Y"
        )

    def eval_event_text(event):
        if event.text_en is None and event.text is None:
            return "Description unavailable."

        return event.text_en or "Description available only in Czech: " + str(event.text)

    # Convert events to dictionaries for the results-map to decode them
    # Filter out only the required fields
    events_dicts = [
        {
            "date_from": event.date_from,
            "date_to": "-" if event.date_to == "31.12.2050" else event.date_to,
            "name": html.unescape(event.name_en or event.name),
            "categories": html.unescape(event.categories_en),
            "text": html.unescape(eval_event_text(event)),
            "latitude": event.latitude,
            "longitude": event.longitude,
        }
        for event in events
    ]

    return templates.TemplateResponse(
        "results.html", {"request": request, "events": events_dicts}
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
