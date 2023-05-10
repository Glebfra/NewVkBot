import os

from dotenv import load_dotenv
from peewee import *
from vkbottle import CtxStorage

ctx_storage = CtxStorage()
load_dotenv('../.env')
db = MySQLDatabase(
    'db_name', user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'), host='localhost', port=3306
    )
ctx_storage.set('db', db)

from models.Subject import Subject
from models.User import User
from models.Homework import Homework

db.connect()
db.create_tables([Subject, User, Homework])
db.close()
