from aiogram import types, Dispatcher
from tgbot.database.functions.db_requests import DbRequests


async def bot_start(message: types.Message, db_request: DbRequests):
    user = await db_request.get_user(user_id=message.from_user.id)
    await message.answer(f'Привет {user.full_name}')


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
