from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.schemas.user_schema import SUserRegister
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['Аутентификация'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: SUserRegister) -> dict:
    return await AuthService.register_user(user_data)

@router.post("/login", summary="Получение токена")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await AuthService.login_user(form_data)

@router.post("/refresh", summary="Обновление токена доступа")
async def refresh_token(refresh_token: str = Depends(oauth2_scheme)):
    return AuthService.refresh_token(refresh_token)
