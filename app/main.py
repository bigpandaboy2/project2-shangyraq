from fastapi import FastAPI
from .database import Base, engine
from .routers import users, listings, comments

from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shanyraq.kz MVP",
    version="1.0.0",
    description="A marketplace for real estate in Kazakhstan (MVP)."
)

app.include_router(users.router)
app.include_router(listings.router)
app.include_router(comments.router)
