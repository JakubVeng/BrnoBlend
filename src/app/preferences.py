from datetime import datetime, timezone
from sqlalchemy import Integer, Numeric, cast, func, or_

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
                # Convert self.preferences.date string to datetime object
                date_obj = datetime.strptime(self.preferences.date, '%Y-%m-%d')

                # Convert date_obj to milliseconds since epoch
                date_timestamp = int(date_obj.replace(tzinfo=timezone.utc).timestamp() * 1000)

                # Cast EventModel.date_from and date_to to Numeric for precise comparison
                date_from_casted = cast(EventModel.date_from, Numeric)
                date_to_casted = cast(EventModel.date_to, Numeric)
                query = query.filter(date_from_casted <= date_timestamp)
                query = query.filter(date_to_casted >= date_timestamp)

            if self.preferences and self.preferences.limit:
                query = query.limit(self.preferences.limit)

            matched_events = query.all()

        return matched_events
