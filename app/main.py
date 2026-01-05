from fastapi import FastAPI
from app.api.v1.router import api_router

app =FastAPI(
    title="Deadline & Obligation Tracker",
    version="0.10"
)

app.include_router(api_router)