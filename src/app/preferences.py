from sqlalchemy import or_

from src.app.db.db import sa_session_transaction  # Adjust import as per your setup
from src.app.db.models import EventModel  # Adjust import as per your actual model
from src.app.schema import Event, PreferencesForm  # Adjust import as per your setup


# Simple preferences matching for testing, change as u like
class Preferencator3000:
    def __init__(self, preferences: PreferencesForm):
        self.preferences = preferences

    def match_events(self) -> list[Event]:
        with sa_session_transaction() as session:
            query = session.query(EventModel)

            if self.preferences and self.preferences.categories:
                category_filters = []
                for category in self.preferences.categories:
                    category_filters.append(
                        EventModel.categories.ilike(f"%{category}%")
                    )

                # Combine all category filters with "OR" logic
                query = query.filter(or_(*category_filters))

            # if self.preferences and self.preferences.location:
            #     query = query.filter(EventModel.location.ilike(f"%{self.preferences.location}%"))

            if self.preferences and self.preferences.date:
                query = query.filter(EventModel.date_from <= self.preferences.date)
                query = query.filter(EventModel.date_to >= self.preferences.date)

            if self.preferences and self.preferences.limit:
                query = query.limit(self.preferences.limit)

            matched_events = query.all()

        return matched_events
