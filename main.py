from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeChat
from dotenv import find_dotenv, load_dotenv
import asyncio
import os

# ================================
from database import db
from comands.comand_list import Private
from comands.comand_list import Group
from hendlers.admin import router_user_admin
from hendlers.users import router_user
from hendlers.group import router_group
# --------------------------------

load_dotenv(find_dotenv())

Allowed_updates = ['message', 'edited_message', 'callback_query']

GROUP_ID = int(os.getenv("GROUP_ID"))
bot = Bot(token=os.getenv('TOKEN_API'))
dp = Dispatcher()

router = Router()

dp.include_router(router_user)
dp.include_router(router_user_admin)
dp.include_router(router_group)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        print('Updates were skipped successfully')
    except Exception as e:
        print(e)
    await db.init_db()
    await db.create_application()
    await db.create_email()
    await db.create_user()
    await db.completion_email()
    await bot.set_my_commands(commands=Private, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=Group, scope=BotCommandScopeChat(chat_id=GROUP_ID))
    await dp.start_polling(bot, allowed_updates=Allowed_updates)

asyncio.run(main())
