from fastapi import APIRouter, HTTPException, status
from app.security.hash import get_password_hash
from app.users.dao import UserDAO
from app.users.schemas import SUserRegister, SUserAddDB


router = APIRouter(prefix='/auth', tags=['Аутентификация'])

@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_data_dict = user_data.model_dump()
    user_data_dict.pop('confirm_password', None)
    await UserDAO.add( **user_data_dict)
    return {'message': 'Вы успешно зарегистрированы!'}