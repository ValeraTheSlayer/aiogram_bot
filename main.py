import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app import handlers
from app.models import db, User, MessageTemplate, ScheduledMessage
from configs.config import Config, load_config

config: Config = load_config()
bot = Bot(token=config.tg_bot.token)


async def main() -> None:
    storage = RedisStorage.from_url(url='redis://redis:6379/0')

    dp = Dispatcher(storage=storage)

    dp.include_router(handlers.router)

    db.connect()
    db.create_tables([User, MessageTemplate, ScheduledMessage])

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
