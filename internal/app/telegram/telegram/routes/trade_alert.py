from aiohttp import web
from aiogram import types

from bot_init import bot
from src.services.database import db
from handlers.menu import keyboard

from src.services.telegram.generate_reports.convert_html_to_png import convert_html_to_png
from src.services.telegram.generate_reports.templates.get_open_position_html import get_open_position_html
from src.services.telegram.generate_reports.templates.get_close_position_html import get_close_position_html
from src.services.telegram.generate_reports.templates.get_purchased_position_html import get_purchased_position_html
from src.services.telegram.generate_reports.templates.get_set_stop_html import get_set_stop_html
from src.services.telegram.generate_reports.templates.get_trailing_stop_html import get_trailing_stop_html


trade_alert_router = web.RouteTableDef()

@trade_alert_router.post('/telegram/trailing_stop_activated')
async def trailing_stop_activated(request):
    position_data = await request.json()
    html_str = get_trailing_stop_html(position_data)
    await send_alert(html_str, 'Сработал Trailing stop')

@trade_alert_router.post('/telegram/position_opened')
async def position_opened(request):
    position_data = await request.json()
    html_str = get_open_position_html(position_data)
    await send_alert(html_str, 'Открылась позиция')

@trade_alert_router.post('/telegram/position_purchased')
async def position_purchased(request):
    position_data = await request.json()
    html_str = get_purchased_position_html(position_data)
    await send_alert(html_str, 'Добрали позицию')

@trade_alert_router.post('/telegram/set_stop')
async def set_stop(request):
    position_data = await request.json()
    html_str = get_set_stop_html(position_data)
    await send_alert(html_str, 'Выставили Stop')

@trade_alert_router.post('/telegram/position_closed')
async def position_closed(request):
    position_data = await request.json()
    html_str = get_close_position_html(position_data)
    await send_alert(html_str, 'Закрыли позицию')
    

@trade_alert_router.post('/telegram/text_alert')
async def text_alert(request):
    alert_data = await request.json()
    text = alert_data['text']
    
    Telegram = db.get_telegram()
    
    for chat_id in Telegram['chat_id']:
        await bot.send_message(chat_id, text, reply_markup=keyboard.as_markup(resize_keyboard=True))
    return web.Response(text="Hello, world")
    
async def send_alert(html_str, caption):
    png_buffer = convert_html_to_png(html_str)
    png = types.BufferedInputFile(png_buffer, filename="/root/bot/photo.png")

    Telegram = db.get_telegram()
    for chat_id in Telegram['chat_id']:
        await bot.send_photo(chat_id, photo=png, reply_markup=keyboard.as_markup(resize_keyboard=True), caption=caption)