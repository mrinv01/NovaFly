from sqlalchemy import select
from app.models import Role
from app.repositories.base_repository import BaseRepository
from app.database import async_session_maker


class RoleRepository(BaseRepository):
    model = Role

    @classmethod
    async def seed_roles(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            roles_result = await session.execute(query)
            roles = roles_result.scalars().all()
            if not roles:
                print("Роли не найдены. Добавление ролей user и admin.... Готово!")
                session.add_all([
                    Role(name="user"),
                    Role(name="admin"),
                ])
                await session.commit()
            else:
                print("Роли обнаружены. Ничего добавлять не требуется!")


