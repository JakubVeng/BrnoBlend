import logging
from contextlib import contextmanager
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def get_pg_url() -> str:
    return (
        f"postgresql+psycopg2://{getenv('POSTGRES_USER')}"
        f":{getenv('POSTGRES_PASSWORD')}"
        f"@{getenv('POSTGRES_HOST')}"
        f":{getenv('POSTGRES_PORT', '5432')}"
        f"/{getenv('POSTGRES_DB')}"
    )


engine = create_engine(get_pg_url())
Session = sessionmaker(engine)


@contextmanager
def sa_session_transaction(commit: bool = False) -> SQLAlchemySession:
    with Session() as session:
        if not commit:
            yield session
        else:
            with session.begin():
                yield session
