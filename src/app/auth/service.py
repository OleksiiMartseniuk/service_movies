from fastapi import HTTPException, status

from src.app.auth.auth import authenticate_user
from src.app.auth.tokenizator import create_token
from src.service.CRUD import ServiceCRUD
from src.app.auth import models, schemas


class ServiceUser(ServiceCRUD):
    model = models.User
    get_schema = schemas.User

    async def auth(self, username: str, password: str) -> dict:
        user = await authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return create_token(user.id)


user_s = ServiceUser()
