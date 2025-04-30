from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserResponseSchema
from app.security.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/me", response_model=UserResponseSchema)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user
