from peewee import *
from vkbottle import CtxStorage
from .BaseModel import BaseModel

ctx_storage = CtxStorage()


class Subject(BaseModel):
    id = AutoField()
    name = CharField(max_length=32)
