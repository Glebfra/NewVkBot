import json
import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from peewee import *
from vkbottle import API, Bot, CtxStorage, DocMessagesUploader, load_blueprints_from_package

ctx_storage = CtxStorage()


def main():
    api = API(token=os.getenv('TOKEN'))
    bot = Bot(api=api)

    doc_uploader = DocMessagesUploader(bot.api)
    ctx_storage.set('doc_uploader', doc_uploader)

    for bp in load_blueprints_from_package("blueprints"):
        bp.load(bot)

    bot.run_forever()


def load_json(filepath):
    with open(f'{ctx_storage.get("PROJECT_DIR")}/{filepath}', 'r') as file:
        response = json.load(file)
    return response


def save_json(filepath, data):
    with open(f'{ctx_storage.get("PROJECT_DIR")}/{filepath}', 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    load_dotenv('../.env')

    ctx_storage = CtxStorage()

    ctx_storage.set(
        'db', MySQLDatabase(
            'db_name', user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'), host='database', port=3306
        )
    )

    # Prepare models
    from models.Homework import Homework
    from models.Subject import Subject
    from models.User import User

    ctx_storage.set('Homework', Homework)
    ctx_storage.set('Subject', Subject)
    ctx_storage.set('User', User)

    # Prepare env variables
    ctx_storage.set('save_json', save_json)
    ctx_storage.set('load_json', load_json)

    ctx_storage.set('PROJECT_DIR', str(Path(__file__).resolve().parent.parent))
    ctx_storage.set('START_DATE', os.getenv('START_TIME'))
    ctx_storage.set('files', load_json('data/files/files.json'))
    ctx_storage.set('schedule', os.getenv('SCHEDULE_URL'))
    ctx_storage.set('open_ai_token', os.getenv('OPEN_AI_TOKEN'))

    # Prepare keyboard module
    from keyboard.keyboards import *

    ctx_storage.set('default_keyboard', DefaultKeyboard())
    ctx_storage.set('select_homework_keyboard', SelectHomeworkKeyboard())
    ctx_storage.set('admin_default_keyboard', AdminDefaultKeyboard())
    ctx_storage.set('back_keyboard', BackKeyboard())

    logger.enable('vkbottle')
    logger.add(f'{ctx_storage.get("PROJECT_DIR")}/logs/vkbot.log', rotation=os.getenv('LOGS_AUTO_DELETE_SIZE'))

    main()
