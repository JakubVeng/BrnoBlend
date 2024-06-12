from typing import TYPE_CHECKING

from sqlalchemy.ext.declarative import declarative_base

if TYPE_CHECKING:
    Base = object
else:
    Base = declarative_base()
