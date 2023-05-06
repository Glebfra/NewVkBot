from datetime import datetime

from vkbottle import CtxStorage
from vkbottle.bot import Blueprint, Message

bp = Blueprint("User")
ctx_storage = CtxStorage()

User = ctx_storage.get('User')
db = ctx_storage.get('db')


class Routes:
    start = ['Начать']
    schedule = ['Расписание']
    week = ['Неделя']


@bp.on.message(text=Routes.start)
async def start(message: Message):
    try:
        await bp.state_dispenser.delete(message.peer_id)
    except Exception:
        pass

    db.connect()
    User.get_or_create(vk_id=message.peer_id)
    db.close()

    await message.answer(
        'Привет. Я бот. Еще маленький, но я развиваюсь',
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )


@bp.on.message(text=Routes.schedule)
async def schedule(message: Message):
    await message.answer(
        'Держи расписание',
        attachment=ctx_storage.get('schedule'),
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )


@bp.on.message(text=Routes.week)
async def get_week(message: Message):
    start_time = datetime(*list(map(int, ctx_storage.get('START_DATE').split('.'))))
    now = datetime.now()
    week = now.isocalendar()[1] - start_time.isocalendar()[1] + 1
    await message.answer(
        f'Сейчас идет {week} неделя',
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )
