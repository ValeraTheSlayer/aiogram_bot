from peewee import Model, CharField, TextField, DateTimeField, ForeignKeyField
from config import DATABASE
from peewee import PostgresqlDatabase

db = PostgresqlDatabase(**DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = CharField(unique=True)


class MessageTemplate(BaseModel):
    content = TextField()
    image = CharField(null=True)
    video = CharField(null=True)


class ScheduledMessage(BaseModel):
    template = ForeignKeyField(MessageTemplate, backref='schedules')
    user = ForeignKeyField(User, backref='schedules')
    send_at = DateTimeField()
