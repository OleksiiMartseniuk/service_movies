from fastapi import APIRouter
from src.app.films.endpoint import search

films = APIRouter()

films.include_router(search.search_router, tags=['search'])
