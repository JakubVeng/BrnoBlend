#!/usr/bin/python3
from typing import Optional

import click

# CLI tool to invoke commands to the application and database from commandline


@click.group()
def manage():
    pass


@manage.command()
@click.option("--url", default=None, help="URL to fetch events from")
def refresh_events(url: Optional[str] = None):
    """
    Refresh events in the database.

    The URL link refresh often so if the fetching won't be dynamic,
     put the URL to the command.
    """
    from src.app.db.data_loader import load_events_to_db

    if url:
        load_events_to_db(url)
    else:
        load_events_to_db()


if __name__ == "__main__":
    manage()
