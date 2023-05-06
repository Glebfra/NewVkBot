from .BaseModel import BaseModel
from peewee import *


class User(BaseModel):
    id = AutoField()
    vk_id = IntegerField()
    role = CharField(default='USER')
