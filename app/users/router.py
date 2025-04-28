from fastapi import APIRouter, Depends, HTTPException, status
from app.users.dao import UserDAO
from app.users.schemas import UserResponseSchema
from app.security.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/me", response_model=UserResponseSchema)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user
