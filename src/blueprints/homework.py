import json
from datetime import datetime

from vkbottle import BaseStateGroup, CtxStorage
from vkbottle.bot import Blueprint, Message

bp = Blueprint("Homework")
ctx_storage = CtxStorage()
save_json = ctx_storage.get('save_json')

Homework = ctx_storage.get('Homework')
Subject = ctx_storage.get('Subject')
User = ctx_storage.get('User')
db = ctx_storage.get('db')


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


@bp.on.message(text=['Добавить домашку'])
async def add_homework(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.ADD_HOMEWORK_SUBJECT_STATE)
    await message.answer(
        'Введите предмет, по которому хотите добавить домашку',
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
    if db.is_closed():
        db.connect()
    if not (subject := Subject.select().where(Subject.name==message.text)):
        await message.answer(
            'Такого предмета не существует',
            keyboard=ctx_storage.get('select_homework_keyboard').get_keyboard()
        )
    homeworks = Homework.select().where(Homework.subject==subject)

    response = f'-- {subject[0].name} -- \n'
    for homework in homeworks:
        response += f'[{homework.created_at}] {homework.text} \n'
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
    if db.is_closed():
        db.connect()
    subject, created = Subject.get_or_create(name=message.text)
    ctx_storage.set('subject', subject)
    await bp.state_dispenser.set(message.peer_id, States.ADD_HOMEWORK_VALUE_STATE, subject=subject)
    await message.answer(
        "Введите домашку",
        keyboard=ctx_storage.get('back_keyboard').get_keyboard()
    )


@bp.on.message(state=States.ADD_HOMEWORK_VALUE_STATE)
async def add_homework_value(message: Message):
    if message.text == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer('Возвращаюсь назад', keyboard=ctx_storage.get('default_keyboard').get_keyboard())

    if db.is_closed():
        db.connect()
    subject = message.state_peer.payload['subject']
    user, created = User.get_or_create(vk_id=message.peer_id)
    Homework.create(subject=subject, text=message.text, created_by=user)

    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(
        'Домашка успешно записана',
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )
