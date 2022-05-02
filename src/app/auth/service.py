from fastapi import HTTPException, status

from src.app.auth import auth
from src.app.auth.tokenizator import create_token
from src.service.CRUD import ServiceCRUD
from src.app.auth import models, schemas


class ServiceAuth(ServiceCRUD):
    model = models.User
    get_schema = schemas.User

    async def auth(self, username: str, password: str) -> dict:
        user = await auth.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return create_token(user.id)

    async def create(self, schema, **kwargs) -> schemas.User:
        # Валидатор пароля
        auth.is_password(schema.hashed_password)
        # Хеширования пароля
        hashed_password = auth.get_password_hash(schema.hashed_password)
        schema.hashed_password = hashed_password

        obj = await self.model.create(**schema.dict(exclude_unset=True))
        return await self.get_schema.from_tortoise_orm(obj)


user_s = ServiceAuth()
