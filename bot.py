import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.engine import URL

from tgbot.models.database.base import Database
from tgbot.data.config import load_config
from tgbot.data.directories import DIRECTORY_TGBOT_DATA
from tgbot.data.locale import LocaleManager, Lang
from tgbot.filters.auth import AuthFilter
from tgbot.filters.admin import AdminFilter
from tgbot.middlewares.db import DbMiddleware
from tgbot import handlers

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(AuthFilter)


def register_all_handlers(dp):
    handlers.register.register_admin(dp)
    handlers.register.register_client(dp)
    handlers.user.register.register_client_function(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',

    )
    logger.info("Starting bot")
    config = load_config(".env")

    if config.tg_bot.use_redis:
        storage = RedisStorage2(config.tg_bot.redis_host)
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    db = Database()

    scheduler = AsyncIOScheduler(
         timezone='Asia/Aqtobe'
    )
    await db.create_pool(
        URL(
            drivername="mysql+asyncmy",
            username=config.db.user,
            password=config.db.password,
            host=config.db.host,
            database=config.db.database,
            query={},
            port=3306
        )
    )

    dp = Dispatcher(bot, storage=storage)
    redis = await storage.redis()

    bot['config'] = config
    bot['pool'] = db.pool

    bot['redis'] = redis

    LocaleManager.add_locale(
        DIRECTORY_TGBOT_DATA / 'locales' / 'local.xlsx',
        col_locale=1,
        locale_name=Lang.RUS
    )
    LocaleManager.add_locale(
        DIRECTORY_TGBOT_DATA / 'locales' / 'local.xlsx',
        col_locale=2,
        locale_name=Lang.UZB
    )

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    bot_me = await bot.me
    logging.info(
        f'starting bot: @{bot_me.username}'
    )

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")