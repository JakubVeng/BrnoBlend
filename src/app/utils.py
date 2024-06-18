# not needed?

from sqlalchemy import inspect
from datetime import datetime

def model_to_dict(obj):
    """
    Convert SQLAlchemy model instance to dictionary.
    """
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def format_unix_timestamp(timestamp):
    try:
        timestamp = int(timestamp)
        timestamp = timestamp // 1000  # Convert from milliseconds to seconds
        return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
    except (ValueError, OverflowError) as e:
        print(f"Error converting timestamp: {timestamp} - {e}")
        return None