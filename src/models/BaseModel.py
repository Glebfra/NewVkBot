from peewee import *
from vkbottle import CtxStorage

ctx_storage = CtxStorage()
db = ctx_storage.get('db')


class BaseModel(Model):
    class Meta:
        database = db
