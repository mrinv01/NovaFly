from app.repositories.base_repository import BaseDAO
from app.models.user import User


class UserDAO(BaseDAO):
    model = User

