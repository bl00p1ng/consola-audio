from peewee import SqliteDatabase, AutoField, CharField, DateField, FloatField, ForeignKeyField, Model, IntegerField, BooleanField

db = SqliteDatabase('db/Base_De_Datos.db')
class Canal(Model):
    id = AutoField()
    etiqueta = CharField()
    volumen = FloatField()
    link = BooleanField()
    mute = BooleanField()
    solo = BooleanField()
    
    class Meta:
        database = db