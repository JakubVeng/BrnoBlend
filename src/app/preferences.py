from src.app.db.db import sa_session_transaction
from src.app.db.models import EventModel
from src.app.schema import Event


class Preferencator3000:
    # TODO: please implement me
    def __init__(self, preferences):
        self.preferences = None

    def match_events(self) -> list[Event]:
        with sa_session_transaction() as session:
            return session.query(EventModel).limit(5).all()
