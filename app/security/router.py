from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.users.dao import UserDAO
from app.users.schemas import SUserRegister
from app.security.hash import verify_password
from app.security.jwt import create_access_token, create_refresh_token
from app.config import settings
from app.exceptions.AuthExceptions import *




router = APIRouter(prefix='/auth', tags=['Аутентификация'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_data_dict = user_data.model_dump()
    user_data_dict.pop('confirm_password', None)
    await UserDAO.add( **user_data_dict)
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post("/login", summary="Получение токена")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserDAO.find_one_or_none(email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise IncorrectEmailOrPasswordException
    print(user)
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/refresh")
async def refresh_token(refresh_token: str = Depends(oauth2_scheme)):
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