from peewee import *
import datetime

db = SqliteDatabase('instasaver.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    first_name = TextField()


class Bookmark(BaseModel):
    id = IntegerField(primary_key=True)
    url = TextField()
    title = TextField()
    user = ForeignKeyField(User, backref='bookmarks')
    created_at = DateTimeField(default=datetime.datetime.now)


class Tag(BaseModel):
    label = TextField()
    bookmark = ForeignKeyField(Bookmark, backref='tags')


with db:
    db.create_tables([User, Bookmark, Tag])
