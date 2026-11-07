from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import router
from handlers.database import init_db

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router)


async def main():
    init_db()
    bot = Bot(token=TOKEN)

    print("bot started")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



