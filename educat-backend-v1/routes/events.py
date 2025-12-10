from fastapi import APIRouter, Depends, HTTPException, Response
import starlette.status as s
from config.db import SessionLocal
from sqlalchemy import and_
from models.events import EventsTable
from schemas.events import EventsCreate, EventSchema
from core.secure import require_role
events = APIRouter()

@events.post("/events",tags=["Events"])
def new_event(event: EventsCreate, user=Depends(require_role(["Admin", "teacher"]))):
    with SessionLocal() as Session:
        exists = Session.query(EventsTable).filter(EventsTable.name == event.name).first()
        if exists:
            raise HTTPException(status_code=403,detail="The event already exists")
        db_event = EventsTable(name=event.name, description=event.description, task= event.task, author= user["sub"], date_start= event.date_starts, date_finish=event.date_ends)
        Session.add(db_event)
        Session.commit()

        return {"message": "New event uploaded"}

@events.put("/events",tags=["Events"])
def event_update(Event: EventSchema, user=Depends(require_role(["Admin", "teacher"]))):
    with SessionLocal() as Session:
        print(user["sub"])
        event = Session.query(EventsTable).filter(and_(EventsTable.name == Event.name, EventsTable.author == user["sub"])).first()
        if not event:
            raise HTTPException(status_code=403,detail="The event doesn't exists")
        event.description = Event.description
        event.date_start = Event.date_start
        event.date_finish = Event.date_finish
        event.name = Event.name
        Session.commit()

        return {"message": "Event updated"}

@events.delete("/events",tags=["Events"])
def event_delete(Event: EventSchema, user=Depends(require_role(["Admin", "teacher"]))):
    with SessionLocal() as Session:
        db_del_event = Session.query(EventsTable).filter(and_(EventsTable.name == Event.name, EventsTable.author == user["sub"])).delete()
        if db_del_event == 0:
            raise HTTPException(status_code=404,detail="The event doesn't exists") 
        Session.commit()
        return Response(status_code=s.HTTP_204_NO_CONTENT)