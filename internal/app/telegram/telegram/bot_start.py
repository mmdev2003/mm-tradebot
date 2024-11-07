import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv('ROOT_PATH'))


from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers.register import register_router
from handlers.menu import menu_router
from routes.trade_alert import trade_alert_router

from bot_init import bot, dp

main_server = os.getenv('MAIN_SERVER')


async def on_startup(dispatcher):
    await bot.set_webhook(f'{main_server}/telegram', secret_token='secret')
    webhook_info = await bot.get_webhook_info()
    print(webhook_info)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


def main():
    dp.include_router(register_router)
    dp.include_router(menu_router)

    dp.startup.register(on_startup)
    app = web.Application()
    app.add_routes(trade_alert_router)
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token='secret',
    )
    webhook_requests_handler.register(app, path='/telegram')
    setup_application(app, dp, bot=bot)
    web.run_app(app, host='127.0.0.1', port=5300)


if __name__ == "__main__":
    main()
