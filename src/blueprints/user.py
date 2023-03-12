import json

from datetime import datetime
from vkbottle import BaseStateGroup, CtxStorage
from vkbottle.bot import Blueprint, Message

bp = Blueprint("For users")
ctx_storage = CtxStorage()


class States(BaseStateGroup):
    ADD_HOMEWORK_SUBJECT_STATE = "add_homework_subject"
    ADD_HOMEWORK_VALUE_STATE = "add_homework_value"
    SELECT_HOMEWORK_STATE = "select_homework_subject"
    TALKING_STATE = "talking_state"


@bp.on.message(text=['Начать'])
async def start(message: Message):
    await message.answer(
        'Привет. Я бот. Еще маленький, но я развиваюсь',
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )


@bp.on.message(text=['Домашка'])
async def homework(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.SELECT_HOMEWORK_STATE)
    await message.answer(
        'По какому предмету интересует домашка?',
        keyboard=ctx_storage.get('select_homework_keyboard').get_keyboard()
    )


@bp.on.message(text=['Давай поболтаем'])
async def start_talking(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.TALKING_STATE)
    await message.answer(
        'Привет. Сейчас запущу всеми любимый chat GPT. Напиши что нибудь, чтобы начать',
        keyboard=ctx_storage.get('talking_keyboard').get_keyboard()
    )


@bp.on.message(state=States.TALKING_STATE)
async def talking(message: Message):
    if message.text == 'Хватит':
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(
            'Надеюсь мы с тобой еще поговорим. Пока',
            keyboard=ctx_storage.get('default_keyboard')
        )


@bp.on.message(state=States.SELECT_HOMEWORK_STATE)
async def select_homework(message: Message):
    if message.text == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return message.answer('Возвращаюсь назад', keyboard=ctx_storage.get('default_keyboard').get_keyboard())
    subject = message.text
    homework = ctx_storage.get('homework')
    if subject not in homework.keys():
        await message.answer('Такого предмета не существует')
    subject_homework = homework[subject]

    response = f'-- {subject} -- \n'
    for homework in subject_homework:
        response += f'[{homework["date"]}] {homework["value"]} \n'
    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(
        response,
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )


@bp.on.message(text=['Добавить домашку'])
async def add_homework(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.ADD_HOMEWORK_SUBJECT_STATE)
    await message.answer(
        'Введите предмет, по которому хотите добавить домашку',
        keyboard=ctx_storage.get('select_homework_keyboard').get_keyboard()
    )


@bp.on.message(state=States.ADD_HOMEWORK_SUBJECT_STATE)
async def add_homework_subject(message: Message):
    subject = message.text
    ctx_storage.set('subject', subject)
    await bp.state_dispenser.set(message.peer_id, States.ADD_HOMEWORK_VALUE_STATE, subject=subject)
    await message.answer(
        "Введите домашку"
    )


@bp.on.message(state=States.ADD_HOMEWORK_VALUE_STATE)
async def add_homework_value(message: Message):
    value = message.text
    subject = message.state_peer.payload['subject']
    homework = ctx_storage.get('homework')
    if subject not in homework:
        homework[subject] = []
    homework[subject].append({
        'date': str(datetime.now().date()),
        'value': value
    })
    ctx_storage.set('homework', homework)
    save_json('homework.json', homework)
    await message.answer(
        'Домашка успешно записана'
    )


@bp.on.message(text=['Неделя'])
async def get_week(message: Message):
    start_time = datetime(*list(map(int, ctx_storage.get('START_DATE').split('.'))))
    now = datetime.now()
    week = now.isocalendar()[1] - start_time.isocalendar()[1] + 1
    await message.answer(
        f'Сейчас идет {week} неделя'
    )


def save_json(filename, data):
    with open(f'{ctx_storage.get("PROJECT_DIR")}/data/{filename}', 'w') as file:
        json.dump(data, file)
