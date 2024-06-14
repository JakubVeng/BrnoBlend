import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
    Home page of the app.
    """
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/preferences", response_class=HTMLResponse)
async def get_preferences(request: Request):
    """
    Preferences page of the app.
    """
    return templates.TemplateResponse("preferences.html", {"request": request})


# TODO: yes forms in FastAPI needs to be as post requests. If something breaks or is not working
# or u think u can do better, replace <form> in html with javascript to create form and
# send it to /results as get with body. I ain't doing the js part...
@app.post("/results", response_class=HTMLResponse)
async def get_results(
    request: Request,
    preferences_form: PreferencesForm = Depends(PreferencesForm.as_form),
):
    """
    Render the results page with the events to display according preferences.
    """
    matcher = Preferencator3000(preferences_form)
    # TODO: ta data co jsou z databaze brane tak maji uplne zle kodovani... jak to opravit?
    events = matcher.match_events()
    return templates.TemplateResponse(
        "results.html", {"request": request, "events": events}
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
