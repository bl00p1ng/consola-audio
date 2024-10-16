from peewee import SqliteDatabase, AutoField, CharField, DateField, FloatField, ForeignKeyField, Model, IntegerField, BooleanField

db = SqliteDatabase('db/Base_De_Datos.db')

class InterfazAudio:
    id = AutoField()
    nombrecorto = CharField()
    modelo = CharField()
    nombrecomercial = CharField()
    precio = FloatField()
    
    class Meta:
        database = db