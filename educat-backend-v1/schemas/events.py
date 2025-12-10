from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import time

class EventsCreate(BaseModel):
    name : str
    task : bool
    description : str
    date_starts : Optional[datetime] = None
    date_ends : datetime

class EventSchema(BaseModel):
    pub_id: str
    name: str
    author: str
    description: str
    date_start: datetime
    date_finish: datetime

    class Config:
        orm_mode = True
