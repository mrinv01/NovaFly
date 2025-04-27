from app.dao.base import BaseDAO
from app.models.user import User
from app.database import async_session_maker
from sqlalchemy import select

class UserDAO(BaseDAO):
    model = User

