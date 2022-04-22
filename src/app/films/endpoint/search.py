from fastapi import APIRouter

search_router = APIRouter()


@search_router.get('/')
async def get_film():
    return {"message": "Hello World"}
