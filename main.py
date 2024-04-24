import asyncio
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import TG_TOKEN, DB_HOST, DB_PORT, DB_COLLECTION, DB_NAME

from util import find_data

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                               '[%(asctime)s] - %(name)s - %(message)s')
    client = AsyncIOMotorClient(DB_HOST, DB_PORT)
    collection = client.get_database(DB_NAME).get_collection(DB_COLLECTION)
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        """Функция для отправки ответа на комманду Start"""
        await message.answer(f'Привет {message.from_user.username}')

    @dp.message()
    async def get_data(message: Message):
        """Функция для отправки данных за выбранный период"""
        logger.info(message.text)
        dct = eval(message.text)
        res = await find_data(dct["dt_from"],
                              dct["dt_upto"],
                              dct["group_type"],
                              collection)
        await message.answer(str(res).replace("'", '"'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
