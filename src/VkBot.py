import json

import os
from dotenv import load_dotenv
from pathlib import Path
from vkbottle import Bot, CtxStorage, load_blueprints_from_package
from keyboard.keyboards import *

ctx_storage = CtxStorage()


def main():
    bot = Bot(token=os.getenv('TOKEN'))

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

    ctx_storage.set('default_keyboard', DefaultKeyboard())
    ctx_storage.set('select_homework_keyboard', SelectHomeworkKeyboard())
    ctx_storage.set('admin_default_keyboard', AdminDefaultKeyboard())
    ctx_storage.set('talking_keyboard', TalkingKeyboard())

    main()
