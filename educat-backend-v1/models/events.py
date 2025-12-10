from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime, timedelta
import uuid


class EventsTable(Base):
    __tablename__ = 'Events'
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    pub_id = Column(String(), default= lambda: str(uuid.uuid4()), nullable= False)
    author = Column(String(), nullable=False)
    name = Column(String(), nullable=False)
    task = Column(Boolean(), default=True, nullable=False)
    description = Column(Text(), nullable=False)
    date_start = Column(DateTime(), default=datetime.now, nullable=False)
    date_finish = Column(DateTime(), default=datetime.now() + timedelta(days=1), nullable=True)

    def __repr__(self):
        return (
        f"<Event pub_id={self.pub_id}, "
        f"name='{self.name}', "
        f"author='{self.author}', "
        f"description='{self.description}', "
        f"date_start={self.date_start}, "
        f"date_finish={self.date_finish}>"
    )
    