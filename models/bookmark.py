from peewee import IntegerField, TextField, DateTimeField, ForeignKeyField
from .base import BaseModel
from .user import User
from .folder import Folder
from datetime import datetime

class Bookmark(BaseModel):
    id = IntegerField(primary_key=True)
    url = TextField()
    title = TextField()
    user = ForeignKeyField(User, backref='bookmarks')
    folder = ForeignKeyField(Folder, backref='bookmarks')
    created_at = DateTimeField(default=datetime.datetime.now)