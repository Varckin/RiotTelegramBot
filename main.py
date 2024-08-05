import asyncio
from aiogram import Bot, Dispatcher

from bot import commands_bot
from resources import API_KEY


async def main():
    bot = Bot(token=API_KEY.bot_token)
    dp = Dispatcher()
    dp.include_router(commands_bot.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
