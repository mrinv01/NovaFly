from fastapi import APIRouter, Depends
from app.schemas.user_schema import SUserRegister, SUserAuth
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['Аутентификация'])

@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: SUserRegister) -> dict:
    return await AuthService.register_user(user_data)

@router.post("/login", summary="Получение токена")
async def login_for_access_token(form_data: SUserAuth = Depends()) -> dict:
    return await AuthService.login_user(form_data)

