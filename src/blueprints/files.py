import requests
from vkbottle import BaseStateGroup, CtxStorage, DocMessagesUploader
from vkbottle.bot import Blueprint, Message

bp = Blueprint("Files")
ctx_storage = CtxStorage()
load_json = ctx_storage.get('load_json')
doc_uploader: DocMessagesUploader = ctx_storage.get('doc_uploader')


class States(BaseStateGroup):
    SELECT_FILES_SUBJECT_STATE = "select_subject_files"
    UPLOAD_FILES_SUBJECT_STATE = "upload_subject_files"
    UPLOAD_FILES_FILE_STATE = "upload_file_files"


class Routes(object):
    get_files = ['Файлы']
    add_files = ['Добавить файл']


@bp.on.message(text=Routes.get_files)
async def get_files(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.SELECT_FILES_SUBJECT_STATE)
    return await message.answer(
        'Выбери предмет, по которому хочешь увидеть прикрепленные файлы',
        keyboard=ctx_storage.get('select_files_keyboard').get_keyboard()
    )


@bp.on.message(state=States.SELECT_FILES_SUBJECT_STATE)
async def select_file(message: Message):
    if message.text == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer(
            'Возвращаюсь назад',
            keyboard=ctx_storage.get('default_keyboard').get_keyboard()
        )
    files = ctx_storage.get('files')
    doc_files = []
    if message.text in files.keys():
        for file in files[message.text]:
            doc_files.append(await doc_uploader.upload(file['name'], file['source'], peer_id=message.peer_id))
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer(
            'Вот твои файлы',
            attachment=doc_files,
            keyboard=ctx_storage.get('default_keyboard').get_keyboard()
        )
    else:
        return await message.answer(
            'Такого предмета не существует',
            keyboard=ctx_storage.get('select_files_keyboard').get_keyboard()
        )


@bp.on.message(text=Routes.add_files)
async def add_files(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.UPLOAD_FILES_SUBJECT_STATE)
    return await message.answer(
        'Выбери предмет, по которому хочешь добавить файл',
        keyboard=ctx_storage.get('select_files_keyboard').get_keyboard()
    )


@bp.on.message(state=States.UPLOAD_FILES_SUBJECT_STATE)
async def select_subject_file(message: Message):
    subject = message.text
    if subject == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer(
            'Возвращаюсь назад',
            keyboard=ctx_storage.get('default_keyboard').get_keyboard()
        )
    if len(subject) > 30:
        return await message.answer(
            'Брат, братишка, я столько символов не запомню(',
            keyboard=ctx_storage.get('back_keyboard').get_keyboard()
        )
    await bp.state_dispenser.set(message.peer_id, States.UPLOAD_FILES_FILE_STATE, subject=subject)
    return await message.answer(
        'Отлично. Теперь напиши название и файла. И добавь файл',
        keyboard=ctx_storage.get('back_keyboard').get_keyboard()
    )


@bp.on.message(state=States.UPLOAD_FILES_FILE_STATE)
async def select_name_file(message: Message):
    subject = message.state_peer.payload['subject']
    name = message.text
    if name == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer(
            'Возвращаюсь назад',
            keyboard=ctx_storage.get('default_keyboard').get_keyboard()
        )
    if len(name) > 30:
        return await message.answer(
            'Брат, братишка, я столько символов не запомню(',
            keyboard=ctx_storage.get('back_keyboard').get_keyboard()
        )
    files: dict = ctx_storage.get('files')

    for file in message.attachments:
        if subject not in files.keys():
            files[subject] = []
        source = f'{ctx_storage.get("PROJECT_DIR")}/data/files/{name}.pdf'
        files[subject].append({'name': f'{name}.pdf', 'source': source})

        url = file.doc.url
        doc_data = requests.get(url).content
        with open(source, 'wb') as file:
            file.write(doc_data)

    ctx_storage.set('files', files)
    save_json = ctx_storage.get('save_json')
    save_json('data/files/files.json', files)
    await bp.state_dispenser.delete(message.peer_id)
    return await message.answer(
        'Файл успешно загружен',
        keyboard=ctx_storage.get('default_keyboard').get_keyboard()
    )
