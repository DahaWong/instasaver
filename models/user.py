from peewee import IntegerField, TextField, DateTimeField
from .base import BaseModel
from datetime import datetime

class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = TextField()
    join_at = DateTimeField(default=datetime.now)