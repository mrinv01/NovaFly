from app.dao.base import BaseDAO
from app.models.plane import Plane


class PlaneDAO(BaseDAO):
    model = Plane