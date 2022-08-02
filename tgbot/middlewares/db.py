import logging

from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.database.functions.db_requests import DbRequests
from tgbot.database.models.user import User


class DbSessionMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session_pool):
        super().__init__()
        self.session_pool = session_pool

    async def pre_process(self, obj, data, *args):
        session = self.session_pool()
        data["session"] = session
        db_request = DbRequests(session)
        data["db_request"] = db_request
        tg_user: types.User = obj.from_user
        user = await session.get(User, tg_user.id)
        data["user"] = user

        if not user:
            user = await db_request.add_user(full_name=tg_user.full_name,
                                             user_id=tg_user.id,
                                             username=tg_user.username)

            logging.info(f"new user {tg_user.full_name} in db")

        if user.username != tg_user.username or \
                user.full_name != tg_user.full_name:
            await db_request.update_user(user_id=tg_user.id,
                                         updated_fields={
                                             "username": tg_user.username,
                                             "full_name": tg_user.full_name
                                         })

    async def post_process(self, obj, data, *args):
        session = data.get("session")
        if session:
            await session.close()
