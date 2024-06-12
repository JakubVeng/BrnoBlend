from datetime import date

from pydantic import BaseModel


class EventCreate(BaseModel):
    name: str
    description: str
    date: date
    location: str


class Event(BaseModel):
    id: int
    name: str
    description: str
    date: date
    location: str

    class Config:
        orm_mode = True
