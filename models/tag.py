from peewee import TextField, ForeignKeyField
from .base import BaseModel
from .bookmark import Bookmark

class Tag(BaseModel):
    label = TextField()
    bookmark = ForeignKeyField(Bookmark, backref='tags')