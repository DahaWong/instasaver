from peewee import SqliteDatabase
from models import *

db = SqliteDatabase('instasaver.db')

def create_tables():
   with db: 
    db.create_tables([User, Bookmark, Tag, Folder, UserSetting])
