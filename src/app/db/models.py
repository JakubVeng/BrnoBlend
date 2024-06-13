from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from .db import sa_session_transaction

if TYPE_CHECKING:
    Base = object
else:
    Base = declarative_base()


# description of attributes is here
# https://data.brno.cz/datasets/mestobrno::akce-events/about
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)

    # match events from brno DB by this id
    brno_id = Column(Integer, index=True)
    name = Column(String)
    text = Column(Text)
    # no idea what they mean by this... it's just some string
    tickets = Column(String)
    tickets_info = Column(String)
    image_url = Column(String)
    event_url = Column(String)
    categories = Column(String)
    parent_festivals_url = Column(String, nullable=True)
    organizer_email = Column(String, nullable=True)
    tickets_url = Column(String, nullable=True)
    name_en = Column(String, nullable=True)
    text_en = Column(Text, nullable=True)
    event_url_en = Column(String, nullable=True)
    tickets_url_en = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date_from = Column(String)
    date_to = Column(String)
    first_image = Column(String)

    # TODO: split this... and split more of the above
    coordinates_0 = Column(Float)
    coordinates_1 = Column(Float)

    @classmethod
    def create(
        cls,
        brno_id: int,
        name: str,
        text: str,
        tickets: str,
        tickets_info: str,
        image_url: str,
        event_url: str,
        categories: str,
        parent_festivals_url: str,
        organizer_email: str,
        tickets_url: str,
        name_en: str,
        text_en: str,
        event_url_en: str,
        tickets_url_en: str,
        latitude: float,
        longitude: float,
        date_from: str,
        date_to: str,
        first_image: str,
        coordinates_0: float,
        coordinates_1: float,
    ):
        with sa_session_transaction(commit=True) as session:
            event = cls()
            event.brno_id = brno_id
            event.name = name
            event.text = text
            event.tickets = tickets
            event.tickets_info = tickets_info
            event.image_url = image_url
            event.event_url = event_url
            event.categories = categories
            event.parent_festivals_url = parent_festivals_url
            event.organizer_email = organizer_email
            event.tickets_url = tickets_url
            event.name_en = name_en
            event.text_en = text_en
            event.event_url_en = event_url_en
            event.tickets_url_en = tickets_url_en
            event.latitude = latitude
            event.longitude = longitude
            event.date_from = date_from
            event.date_to = date_to
            event.first_image = first_image
            event.coordinates_0 = coordinates_0
            event.coordinates_1 = coordinates_1
            session.add(event)
            return event
