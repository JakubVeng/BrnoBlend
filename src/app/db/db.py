import logging
from contextlib import contextmanager
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def get_pg_url() -> str:
    return (
        f"postgresql+psycopg2://{getenv('POSTGRESQL_USER')}"
        f":{getenv('POSTGRESQL_PASSWORD')}@{getenv('POSTGRESQL_HOST', 'postgres')}"
        f":{getenv('POSTGRESQL_PORT', '5432')}/{getenv('POSTGRESQL_DATABASE')}"
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
