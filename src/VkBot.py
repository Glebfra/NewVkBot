import json
import os
from pathlib import Path

from aiohttp import ClientSession
from aiohttp_proxy import ProxyConnector
from dotenv import load_dotenv
from vkbottle import API, Bot, load_blueprints_from_package
from vkbottle.http import AiohttpClient

from keyboard.keyboards import *

ctx_storage = CtxStorage()


def main():
    connector = ProxyConnector.from_url('http://proxy.server:3128')
    session = ClientSession(connector=connector)
    proxy = AiohttpClient(session=session)
    api = API(token=os.getenv('TOKEN'))
    bot = Bot(api=api)

    for bp in load_blueprints_from_package("blueprints"):
        bp.load(bot)

    bot.run_forever()


def load_json(filename):
    with open(f'{ctx_storage.get("PROJECT_DIR")}/data/{filename}', 'r') as file:
        response = json.load(file)
    return response


if __name__ == '__main__':
    load_dotenv('../.env')

    ctx_storage = CtxStorage()
    ctx_storage.set('PROJECT_DIR', str(Path(__file__).resolve().parent.parent))
    ctx_storage.set('START_DATE', os.getenv('START_TIME'))
    ctx_storage.set('homework', load_json('homework.json'))
    ctx_storage.set('schedule', os.getenv('SCHEDULE_URL'))

    ctx_storage.set('default_keyboard', DefaultKeyboard())
    ctx_storage.set('select_homework_keyboard', SelectHomeworkKeyboard())
    ctx_storage.set('admin_default_keyboard', AdminDefaultKeyboard())
    ctx_storage.set('back_keyboard', BackKeyboard())

    main()
