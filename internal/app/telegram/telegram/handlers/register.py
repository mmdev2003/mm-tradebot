from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router

from src.services.database import db
from handlers.menu import keyboard

register_router = Router()

@register_router.message(CommandStart())
async def register(message: Message):
    await message.answer(f'Для подписки на уведомления необходимо ввести пароль')
    
@register_router.message(lambda msg: msg.text.lower() == '89172451')
async def answer(message: Message):
    Telegram = db.get_telegram()
    
    telegram_data = {
        "chat_id": message.chat.id
    }
    db.set_telegram_chat(Telegram, telegram_data)
    await message.answer('Вы зарегистрировались', reply_markup=keyboard.as_markup(resize_keyboard=True))

