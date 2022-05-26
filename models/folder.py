from peewee import TextField, IntegerField, ForeignField
from .base import BaseModel
from .user import User

class Folder(BaseModel):
    id = IntegerField(primary_key=True)
    title = TextField()
    user = ForeignField(User, backref='folders')