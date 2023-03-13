import json
from datetime import datetime

from vkbottle import BaseStateGroup, CtxStorage
from vkbottle.bot import Blueprint, Message

bp = Blueprint("Homework")
ctx_storage = CtxStorage()


class States(BaseStateGroup):
    ADD_HOMEWORK_SUBJECT_STATE = "add_homework_subject"
    ADD_HOMEWORK_VALUE_STATE = "add_homework_value"
    ADD_HOMEWORK_FILE_STATE = "add_homework_file"
    SELECT_HOMEWORK_STATE = "select_homework_subject"


@bp.on.message(text=['Домашка'])
async def homework(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.SELECT_HOMEWORK_STATE)
    await message.answer(
        'По какому предмету интересует домашка?',
        keyboard=ctx_storage.get('select_homework_keyboard').get_keyboard()
    )


@bp.on.message(state=States.SELECT_HOMEWORK_STATE)
async def select_homework(message: Message):
    if message.text == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer(
            'Возвращаюсь назад',
            keyboard=ctx_storage.get('default_keyboard').get_keyboard()
        )
    subject = message.text
    homework = ctx_storage.get('homework')
    if subject not in homework.keys():
        await message.answer(
            'Такого предмета не существует',
            keyboard=ctx_storage.get('select_homework_keyboard').get_keyboard()
        )
    subject_homework = homework[subject]

    response = f'-- {subject} -- \n'
    for homework in subject_homework:
        response += f'[{homework["date"]}] {homework["value"]} \n'
    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(
        response,
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )


@bp.on.message(state=States.ADD_HOMEWORK_SUBJECT_STATE)
async def add_homework_subject(message: Message):
    if message.text == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer('Возвращаюсь назад', keyboard=ctx_storage.get('default_keyboard').get_keyboard())
    subject = message.text
    ctx_storage.set('subject', subject)
    await bp.state_dispenser.set(message.peer_id, States.ADD_HOMEWORK_VALUE_STATE, subject=subject)
    await message.answer(
        "Введите домашку, или выберите добавить файл (фото или документы)"
    )


@bp.on.message(state=States.ADD_HOMEWORK_VALUE_STATE)
async def add_homework_value(message: Message):
    if message.text == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer('Возвращаюсь назад', keyboard=ctx_storage.get('default_keyboard').get_keyboard())
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
    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(
        'Домашка успешно записана',
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )


def save_json(filename, data):
    with open(f'{ctx_storage.get("PROJECT_DIR")}/data/{filename}', 'w') as file:
        json.dump(data, file)
