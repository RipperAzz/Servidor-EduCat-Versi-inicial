from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from config.db import SessionLocal
from core.secure import get_current_user
from models.events import EventsTable
from datetime import datetime, time
calendar = APIRouter()

def start_of_day(date) -> datetime:
    return datetime.combine(date, time.min)  # 00:00:00
    
def end_of_day(date) -> datetime:
    return datetime.combine(date, time.max)  # 23:59:59.999999

@calendar.get("/calendar", tags=["Calendar"])
def get_all_events(user=Depends(get_current_user)):
    with SessionLocal() as db:
        events = db.query(EventsTable).all()
        if not events:
            return {"message": "No events yet"}
        return events


@calendar.get("/calendar/day/{day}", tags=["Calendar"]) 
def get_events_by_day(day: datetime,user=Depends(get_current_user)):
    with SessionLocal() as db:
        events = db.query(EventsTable).filter(and_(start_of_day(day) <= EventsTable.date_finish, 
            EventsTable.date_finish <= end_of_day(day))).all()
        if not events:
            return {"message":"Sin eventos previos"}
        return events

@calendar.get("/calendar/month/{start}/{end}", tags=["Calendar"])
def get_events_by_month(start: datetime, end: datetime,user=Depends(get_current_user)):
    with SessionLocal() as db:
        events = db.query(EventsTable).filter(and_(
            EventsTable.date_finish >= start_of_day(start), end_of_day(end) >=
            EventsTable.date_finish)).all()
        if not events:
            return {"message":"Sin eventos previos"}
        return events