from typing import Optional
from pydantic import BaseModel, EmailStr


class Messages(BaseModel):
    messages: str


class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]


class FilmReelId(BaseModel):
    id_film_reel: int
