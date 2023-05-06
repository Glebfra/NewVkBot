import datetime

from .BaseModel import BaseModel
from .Subject import Subject
from peewee import *

from .User import User


class Homework(BaseModel):
    id = AutoField()
    subject = ForeignKeyField(Subject, id, on_delete='CASCADE')
    text = CharField(max_length=200)
    created_at = DateTimeField(default=datetime.datetime.now())
    created_by = ForeignKeyField(User, id)
