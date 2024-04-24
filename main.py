import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import TG_TOKEN


async def main():

    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(f'Привет {message.from_user.username}')

    @dp.message()
    async def get_data(message: Message):
        pass

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
