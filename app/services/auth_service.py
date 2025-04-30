from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import SUserRegister
from app.repositories.user_repository import UserRepository
from app.security.hash import verify_password
from app.security.jwt import create_access_token, create_refresh_token
from app.config import settings
from app.exceptions.AuthExceptions import *

class AuthService:

    @staticmethod
    async def register_user(user_data: SUserRegister) -> dict:
        existing_user = await UserRepository.find_one_or_none(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException

        user_data_dict = user_data.model_dump()
        user_data_dict.pop('confirm_password', None)
        await UserRepository.add(**user_data_dict)

        return {'message': 'Вы успешно зарегистрированы!'}

    @staticmethod
    async def login_user(form_data: OAuth2PasswordRequestForm) -> dict:
        user = await UserRepository.find_one_or_none(email=form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            raise IncorrectEmailOrPasswordException

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def refresh_token(refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user_id: int = payload.get("sub")
            if user_id is None:
                raise NoUserIdException
        except JWTError:
            raise TokenExpiredException

        new_access_token = create_access_token({"sub": user_id})
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
        }
