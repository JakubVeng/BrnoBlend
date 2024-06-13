import requests

from src.app.constants import DATA_URL_DOWNLOAD
from src.app.db.models import Event


def parse_event(event: dict) -> dict:
    properties = event["properties"]
    geometry = event["geometry"]
    return {
        "brno_id": properties["ID"],
        "name": properties["name"],
        "text": properties["text"],
        "tickets": properties["tickets"],
        "tickets_info": properties["tickets_info"],
        "image_url": properties["images"],
        "event_url": properties["url"],
        "categories": properties["categories"],
        "parent_festivals_url": properties.get("parent_festivals"),
        "organizer_email": properties.get("organizer_email"),
        "tickets_url": properties.get("tickets_url"),
        "name_en": properties.get("name_en"),
        "text_en": properties.get("text_en"),
        "event_url_en": properties.get("url_en"),
        "tickets_url_en": properties.get("tickets_url_en"),
        "latitude": properties["latitude"],
        "longitude": properties["longitude"],
        "date_from": properties["date_from"],
        "date_to": properties["date_to"],
        "first_image": properties["first_image"],
        "coordinates_0": geometry["coordinates"][0],
        "coordinates_1": geometry["coordinates"][1],
    }


def get_events(url: str) -> list[dict]:
    response = requests.get(url)
    response.raise_for_status()

    result = []
    for record in response.json()["features"]:
        result.append(parse_event(record))

    return result


def load_events_to_db(url: str = DATA_URL_DOWNLOAD):
    for event in get_events(url):
        Event.create_or_update(**event)
