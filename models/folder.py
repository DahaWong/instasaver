from peewee import TextField, IntegerField, ForeignKeyField
from .base import BaseModel
from .user import User


class Folder(BaseModel):
    id = IntegerField(primary_key=True)
    title = TextField()
    user = ForeignKeyField(User, backref='folders')
