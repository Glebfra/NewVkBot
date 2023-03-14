from vkbottle import BaseStateGroup
from vkbottle.bot import Blueprint, Message

bp = Blueprint("Files")


class States(BaseStateGroup):
    SELECT_FILES_SUBJECT_STATE = "select_subject_files"


@bp.on.message(text=["Файлы"])
async def files(message: Message):
    pass
