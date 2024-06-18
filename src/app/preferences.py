from datetime import datetime, timezone

from sqlalchemy import Numeric, cast, or_

from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.app.db.db import sa_session_transaction  # Adjust import as per your setup
from src.app.db.models import EventModel  # Adjust import as per your actual model
from src.app.schema import Event, PreferencesForm  # Adjust import as per your setup


# Simple preferences matching for testing, change as u like
class Preferencator3000:
    def __init__(self, preferences: PreferencesForm):
        self.preferences = preferences

    def match_events(self) -> List[Event]:
        with sa_session_transaction() as session:
            query = session.query(EventModel)

            if self.preferences and self.preferences.categories:
                category_filters = []
                for category in self.preferences.categories:
                    category_filters.append(
                        EventModel.categories_en.ilike(f"%{category}%")
                    )

                # Combine all category filters with "OR" logic
                query = query.filter(or_(*category_filters))

            # if self.preferences and self.preferences.location:
            #     query = query.filter(EventModel.location.ilike(f"%{self.preferences.location}%"))

            if self.preferences and self.preferences.date:
                # Convert self.preferences.date string to datetime object
                date_obj = datetime.strptime(self.preferences.date, "%Y-%m-%d")

                # Convert date_obj to milliseconds since epoch
                date_timestamp = int(
                    date_obj.replace(tzinfo=timezone.utc).timestamp() * 1000
                )

                # Cast EventModel.date_from and date_to to Numeric for precise comparison
                date_from_casted = cast(EventModel.date_from, Numeric)
                date_to_casted = cast(EventModel.date_to, Numeric)
                query = query.filter(date_from_casted <= date_timestamp)
                query = query.filter(date_to_casted >= date_timestamp)

            if self.preferences and self.preferences.limit:
                query = query.limit(self.preferences.limit)

            matched_events = query.all()

        return matched_events


class SemanticSearchEngine():
    def __init__(self, preferences: PreferencesForm):
        self.preferences = preferences

    def match_events(self) -> List[Event]:
        with sa_session_transaction() as session:
            query = session.query(EventModel)

            if self.preferences and self.preferences.date:
                # Convert self.preferences.date string to datetime object
                date_obj = datetime.strptime(self.preferences.date, "%Y-%m-%d")

                # Convert date_obj to milliseconds since epoch
                date_timestamp = int(
                    date_obj.replace(tzinfo=timezone.utc).timestamp() * 1000
                )

                # Cast EventModel.date_from and date_to to Numeric for precise comparison
                date_from_casted = cast(EventModel.date_from, Numeric)
                date_to_casted = cast(EventModel.date_to, Numeric)
                query = query.filter(date_from_casted <= date_timestamp)
                query = query.filter(date_to_casted >= date_timestamp)

            matched_events = query.all()

            if self.preferences and self.preferences.categories:
                # Prepare texts for vectorization
                event_texts = [event_to_text(event) for event in matched_events]

                # Perform TF-IDF vectorization
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(event_texts)

                # Calculate cosine similarity
                query_vector = vectorizer.transform(["[SEP]".join(self.preferences.categories)])
                similarities = cosine_similarity(tfidf_matrix, query_vector.reshape(1, -1))

                # Sort events by similarity
                similarity_scores = list(enumerate(similarities.flatten()))
                similarity_scores = [score for score in similarity_scores if score[1] >= 0.12]
                similarity_scores.sort(key=lambda x: x[1], reverse=True)

                if self.preferences and self.preferences.limit:
                    similarity_scores = similarity_scores[:self.preferences.limit]

                return [matched_events[index] for index, _ in similarity_scores]


def event_to_text(event: Event):
    categories = str(event.categories_en)
    categories = categories.replace(", ", "[SEP]")
    text = event.text_en or f"Description available only in Czech: {event.text}"
    name = event.name_en or f"Name available only in Czech: {event.name}"

    return"[SEP]".join([categories, str(text), categories ,str(name), categories])