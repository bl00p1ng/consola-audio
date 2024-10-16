from peewee import SqliteDatabase, AutoField, CharField, DateField, FloatField, ForeignKeyField, Model, IntegerField, BooleanField

db = SqliteDatabase('db/Base_De_Datos.db')

class Frecuencia:
    id = AutoField()
    valor = FloatField()
    
    class Meta:
        database = db