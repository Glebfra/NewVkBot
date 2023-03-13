from datetime import datetime

from vkbottle import BaseStateGroup, CtxStorage
from vkbottle.bot import Blueprint, Message

bp = Blueprint("User")
ctx_storage = CtxStorage()


@bp.on.message(text=['Начать'])
async def start(message: Message):
    await message.answer(
        'Привет. Я бот. Еще маленький, но я развиваюсь',
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )


@bp.on.message(text=['Расписание'])
async def schedule(message: Message):
    await message.answer(
        'Держи расписание',
        attachment=ctx_storage.get('schedule'),
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )


@bp.on.message(text=['Неделя'])
async def get_week(message: Message):
    start_time = datetime(*list(map(int, ctx_storage.get('START_DATE').split('.'))))
    now = datetime.now()
    week = now.isocalendar()[1] - start_time.isocalendar()[1] + 1
    await message.answer(
        f'Сейчас идет {week} неделя',
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )
