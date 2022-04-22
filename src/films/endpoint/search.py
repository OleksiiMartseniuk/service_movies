from fastapi import APIRouter

search = APIRouter()


@search.get('/')
async def get_film():
    pass
