from peewee import SqliteDatabase, AutoField, CharField, DateField, FloatField, ForeignKeyField, Model, IntegerField, BooleanField

db = SqliteDatabase('db/Base_De_Datos.db')

class Tipo:
    id = AutoField()
    nombre = CharField()
    descripcion = CharField()
    
    class Meta:
        database = db