from datetime import datetime

from peewee import SqliteDatabase, Model, AutoField, CharField, IntegerField, DateTimeField
from pydantic import BaseModel

db = SqliteDatabase("database.db")


class DefaultModel(Model):
    class Meta:
        database = db


class Tickets(DefaultModel):
    """ Модель описывающая таблицу tickets в БД """
    request_id = AutoField()
    ne_name = CharField()
    status = IntegerField()
    eventtime = DateTimeField(default=datetime.now())


class Alarms(DefaultModel):
    """ Модель описывающая таблицу alarms в БД """
    notification_id = AutoField()
    ne_name = CharField()
    eventtime = DateTimeField(default=datetime.now())


def create_models():
    """ Метод для создания таблиц в БД """
    db.create_tables(DefaultModel.__subclasses__())


class TicketCreate(BaseModel):
    """ Pydantic модель для валидации данных при создании записи в таблице tickets """
    ne_name: str
    status: int


class TicketUpdate(BaseModel):
    """ Pydantic модель для валидации данных при обновлении статуса записи в таблице tickets """
    request_id: int
    status: int


class AlarmCreate(BaseModel):
    """ Pydantic модель для валидации данных при создании записи в таблице alarms """
    ne_name: str
