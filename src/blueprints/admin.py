import json
import os

import dotenv
from vkbottle import BaseStateGroup, CtxStorage
from vkbottle.bot import Blueprint, Message, rules

bp = Blueprint("Admin")
bp.labeler.auto_rules = [rules.FromPeerRule(list(map(int, os.getenv('ADMINS').split(','))))]
ctx_storage = CtxStorage()
save_json = ctx_storage.get('save_json')


class States(BaseStateGroup):
    ADD_ADMIN_STATE = 'add_admin'
    DELETE_ADMIN_STATE = 'delete_admin'
    SEND_ALL_STATE = 'send_all'
    ADD_FILE_STATE = 'add_file'
    DELETE_SUBJECT_STATE = 'delete_subject'


@bp.on.message(text=['Админ'])
async def start(message: Message):
    await message.answer(
        'Вам доступны админ функции',
        keyboard=ctx_storage.get('admin_default_keyboard').get_keyboard()
    )


@bp.on.message(text=['Добавить админа'])
async def add_admin(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.ADD_ADMIN_STATE)
    await message.answer('Введите id юзера')


@bp.on.message(text=['Удалить предмет'])
async def delete_subject(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.DELETE_SUBJECT_STATE)
    return await message.answer(
        'Введите предмет, который хотите удалить',
        keyboard=ctx_storage.get('select_homework_keyboard').get_keyboard()
    )


@bp.on.message(state=States.DELETE_SUBJECT_STATE)
async def delete_subject_state(message: Message):
    subject = message.text
    try:
        homework = ctx_storage.get('homework')
        homework.pop(subject)
        ctx_storage.set('homework', homework)
        save_json('data/homework.json', homework)

        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer(
            'Предмет успешно удален',
            keyboard=ctx_storage.get('admin_default_keyboard').get_keyboard()
        )
    except KeyError:
        return await message.answer(
            'Такого предмета не существует',
            keyboard=ctx_storage.get('select_homework_keyboard').get_keyboard()
        )


@bp.on.message(state=States.ADD_ADMIN_STATE)
async def add_admin_state(message: Message):
    user_id = message.text
    try:
        user_id = int(user_id)
        admins = os.getenv('ADMINS')
        admins += f',{user_id}'
        dotenv.set_key(f'{ctx_storage.get("PROJECT_DIR")}/.env', 'ADMINS', admins)
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(f'Пользователь с id {user_id} успешно добавлен')
    except ValueError:
        await message.answer('Id пользователя может быть только численным!')


@bp.on.message(text=['Удалить админа'])
async def delete_admin(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.DELETE_ADMIN_STATE)
    await message.answer('Введите id юзера')


@bp.on.message(state=States.DELETE_ADMIN_STATE)
async def delete_admin_state(message: Message):
    user_id = message.text
    try:
        user_id = int(user_id)
        admins = os.getenv('ADMINS')
        admins.replace(f',{user_id}', '')
        dotenv.set_key(f'{ctx_storage.get("PROJECT_DIR")}/.env', 'ADMINS', admins)
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(f'Пользователь с id {user_id} успешно удален')
    except ValueError:
        await message.answer('Id пользователя может быть только численным!')
