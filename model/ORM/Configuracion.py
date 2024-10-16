from peewee import SqliteDatabase, AutoField, CharField, DateField, FloatField, ForeignKeyField, Model, IntegerField

db = SqliteDatabase('db/Base_De_Datos.db')

class Configuracion:
    id = AutoField()
    fecha = DateField()
    
    class Meta:
        database = db