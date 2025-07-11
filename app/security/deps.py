from fastapi import Request, HTTPException, status, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer(auto_error=False)

from app.security.jwt import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.exceptions.AuthExceptions import ForbiddenException

def get_token_from_header(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> str:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

async def get_current_user(token: str = Security(get_token_from_header)):
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserRepository.find_one_or_none_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role.id in [2]:
        return current_user
    raise ForbiddenException
