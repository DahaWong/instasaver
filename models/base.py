from peewee import SqliteDatabase,Model

db = SqliteDatabase('instasaver.db')

class BaseModel(Model):
    class Meta:
        database = db