from fastapi import FastAPI
from config.db import engine
from routes.user import user
from routes.auth import auth_
from routes.calendar import calendar
from routes.events import events
from models.user import Base
from core.config import settings
app = FastAPI(
    version="0.0.1",
    title="API Edu"
)
print(settings.DATABASE_URL)
Base.metadata.create_all(bind=engine)

app.include_router(auth_)
app.include_router(user)
app.include_router(events)
app.include_router(calendar)

