import asyncio
import logging
from aiogram import Dispatcher, Bot
from config import TOKEN
from handlers.start import router as start_router

async def main():

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Closing bot')

