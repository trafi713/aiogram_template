from tgbot.database.models.user import User
from sqlalchemy import select, insert, func, update


class DbRequests:
    """"Database requests"""

    def __init__(self, session):
        self.session = session

    async def get_user(self, user_id: int):
        sql = select(User).where(User.user_id == user_id)
        request = await self.session.execute(sql)
        return request.scalar()

    async def add_user(self, user_id: int,
                       username: str,
                       full_name: str, ):
        sql = insert(User).values(user_id=user_id,
                                  username=username,
                                  full_name=full_name).returning('*')

        request = await self.session.execute(sql)
        await self.session.commit()
        return request.first()

    async def count_users(self):
        sql = select(func.count("*")).select_from(User)
        request = await self.session.execute(sql)
        await self.session.commit()
        return request.scalar()

    async def update_user(self, user_id: int, updated_fields: dict):
        sql = update(User).where(User.user_id == user_id).values(**updated_fields)
        request = await self.session.execute(sql)
        await self.session.commit()
        return request

    async def count_id_users(self):
        sql = select(User.user_id).select_from(User)
        request = await self.session.execute(sql)
        return request.scalars().all()

