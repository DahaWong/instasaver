from peewee import IntegerField, ForeignKeyField
from .base import BaseModel
from .user import User

class UserSetting(BaseModel):
    update_interval = IntegerField() # in minutes
    user = ForeignKeyField(User, backref='settings')