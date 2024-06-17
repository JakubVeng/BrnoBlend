import html
import logging
from typing import Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import inspect

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
    categories = db_session.query(EventModel.categories).distinct().all()
    unique_categories = set()
    for category in categories:
        if category.categories:
            unique_categories.update(category.categories.split(", "))
    return list(unique_categories)


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


def model_to_dict(obj):
    """
    Convert SQLAlchemy model instance to dictionary.
    """
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


# TODO: yes forms in FastAPI needs to be as post requests. If something breaks or is not working
# or u think u can do better, replace <form> in html with javascript to create form and
# send it to /results as get with body. I ain't doing the js part...
@app.post("/results", response_class=HTMLResponse)
async def get_results(
    request: Request,
    categories: list[str] = Form(...),
    # location: str = Form(...),
    date: Optional[str] = Form(None),
    limit: int = Form(...),
):
    preferences_form = PreferencesForm(categories=categories, date=date, limit=limit)
    matcher = Preferencator3000(preferences_form)

    events = matcher.match_events()

    # Format the html-encoded titles...
    for event in events:
        event.name = html.unescape(event.name)

    # Convert events to dictionaries for the #results-map to decode them
    events_dicts = [model_to_dict(event) for event in events]

    return templates.TemplateResponse(
        "results.html", {"request": request, "events": events_dicts}
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
