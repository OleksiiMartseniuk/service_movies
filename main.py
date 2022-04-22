from fastapi import FastAPI

from src.routers import films

app = FastAPI()


# app.include_router(films)
