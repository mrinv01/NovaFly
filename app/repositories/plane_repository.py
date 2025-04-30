from app.repositories.base_repository import BaseDAO
from app.models.plane import Plane


class PlaneDAO(BaseDAO):
    model = Plane