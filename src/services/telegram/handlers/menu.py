from aiogram import Router, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder

from src.services import utils
from src.services.database import db
from src.services.telegram.generate_reports.templates.get_account_info_html import get_account_info_html
from src.services.telegram.generate_reports.templates.get_active_position_html import get_active_position_html
from src.services.telegram.generate_reports.convert_html_to_png import convert_html_to_png

menu_router = Router()
keyboard = ReplyKeyboardBuilder()
keyboard.row(
    types.KeyboardButton(text="Информация об аккаунте"),
    types.KeyboardButton(text="Сбросить статистику")
)

keyboard.row(
    types.KeyboardButton(text="Активные позиции"),
    types.KeyboardButton(text="Закрытые позиции")
)


@menu_router.message(F.text.lower() == "сбросить статистику")
async def reset_db(message: types.Message):
    db.create_db()
    await message.answer('Статистика сброшена')


@menu_router.message(F.text.lower() == "активные позиции")
async def get_active_position(message: types.Message):
    active_positions = db.get_positions(state='active')
    client = utils.client_init()

    if len(active_positions) == 0:
        await message.answer('Активных позиций нет')
    elif len(active_positions) < 4:
        album_builder = MediaGroupBuilder(
            caption="Активные позиции"
        )
        for _id in range(len(active_positions)):
            position = active_positions.iloc[_id]
            html_str = get_active_position_html(position, client, _id)
            png_buffer = convert_html_to_png(html_str)
            png = types.BufferedInputFile(png_buffer, filename="close_position.png")
            album_builder.add_photo(media=png)
        await message.answer_media_group(media=album_builder.build())


@menu_router.message(F.text.lower() == "закрытые позиции")
async def get_closed_position(message: types.Message):
    closed_positions = db.get_positions(state='close', remote=True)

    letter = f'Закрытые позиции\n'

    for id in range(len(closed_positions)):
        position = closed_positions.iloc[id]
        open_price = position['open_price']
        close_price = position['close_price']
        symbol = position['symbol']
        take_price = position['take_price']
        stop_price = position['stop_price']
        profit_in_dollars = round(position['profit_in_dollars'], 3)
        profit_in_percent = round(position['profit_in_percent'], 3)
        size = position['size']
        position_side = position['position_side']
        open_time = str(position['open_time'])[:-7]
        close_time = str(position['close_time'])[:-7]
        count_trail_take = position['count_trail_take']
        count_trail_stop = position['count_trail_stop']

        letter += (
            f'\n\nПозиция {position_side} {symbol}\n\n'
            f'Цена открытия: {open_price}$\n'
            f'Цена закрытия: {close_price}$\n'
            f'Take: {take_price}\n'
            f'Stop: {stop_price}\n'
            f'Количество переносов Stop {count_trail_stop}\n'
            f'Количество переносов Take {count_trail_take}\n'
            f'Количество: {size}\n'
            f'Профит: {profit_in_dollars}$ / {profit_in_percent}%\n'
            f'Время открытия: {open_time}\n'
            f'Время закрытия: {close_time}'
        )
    await message.answer(letter)


@menu_router.message(F.text.lower() == "информация об аккаунте")
async def get_account_info(message: types.Message):
    html_str = get_account_info_html()
    png_buffer = convert_html_to_png(html_str)
    png = types.BufferedInputFile(png_buffer, filename="close_position.png")
    await message.answer_photo(photo=png)
