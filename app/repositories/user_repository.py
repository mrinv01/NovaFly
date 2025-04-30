from app.repositories.base_repository import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository):
    model = User

