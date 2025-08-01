from fastapi import FastAPI

from .router import router

app = FastAPI(
    title="Baggers API",
    description="A simple API for managing contact details and AFL membership numbers",
    version="0.1.0",
)

app.include_router(router)
