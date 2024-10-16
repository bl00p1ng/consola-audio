from peewee import SqliteDatabase, AutoField, CharField, DateField, FloatField, ForeignKeyField, Model, IntegerField, BooleanField

db = SqliteDatabase('db/Base_De_Datos.db')

class Usuario:
    id = AutoField()
    email = CharField()
    password = CharField()
    
    class Meta:
        database = db