from typing import Optional

from fastapi.params import Form
from pydantic import BaseModel


class Event(BaseModel):
    brno_id: int
    name: str
    text: str
    tickets: str
    tickets_info: str
    image_url: str
    event_url: str
    categories: str
    latitude: float
    longitude: float
    date_from: str
    date_to: str
    first_image: str
    coordinates_0: float
    coordinates_1: float
    parent_festivals_url: Optional[str]
    organizer_email: Optional[str]
    tickets_url: Optional[str]
    name_en: Optional[str]
    text_en: Optional[str]
    event_url_en: Optional[str]
    tickets_url_en: Optional[str]

    class Config:
        orm_mode = True


class PreferencesForm(BaseModel):
    # TODO: add preferences questions
    category: str
    location: str
    date: str

    @classmethod
    def as_form(
        cls, category: str = Form(...), location: str = Form(...), date: str = Form(...)
    ) -> "PreferencesForm":
        return cls(category=category, location=location, date=date)
