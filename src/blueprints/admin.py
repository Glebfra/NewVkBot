import dotenv
import os
from vkbottle import BaseStateGroup, CtxStorage
from vkbottle.bot import Blueprint, Message, rules

bp = Blueprint("Admin")
bp.labeler.auto_rules = [rules.FromPeerRule(list(map(int, os.getenv('ADMINS').split(','))))]
ctx_storage = CtxStorage()


class States(BaseStateGroup):
    ADD_ADMIN_STATE = 'add_admin'
    DELETE_ADMIN_STATE = 'delete_admin'
    SEND_ALL_STATE = 'send_all'
    ADD_FILE_STATE = 'add_file'


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
