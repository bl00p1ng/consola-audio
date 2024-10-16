from peewee import SqliteDatabase, Model, AutoField, CharField, FloatField, BooleanField, ForeignKeyField
from typing import List, Optional

db = SqliteDatabase('db/Base_De_Datos.db')

class Fuente(Model):
    id = AutoField()
    # Agregar otros campos necesarios para Fuente

    class Meta:
        database = db

class Canal(Model):
    id = AutoField()
    etiqueta = CharField()
    volumen = FloatField(default=0)
    link = BooleanField(default=False)
    mute = BooleanField(default=False)
    solo = BooleanField(default=False)
    fuente = ForeignKeyField(Fuente, backref='canales', null=True)

    class Meta:
        database = db

class CanalDAO:
    """
    Data Access Object para la entidad Canal utilizando Peewee ORM.
    """

    @staticmethod
    def get_all() -> List[Canal]:
        """
        Obtiene todos los canales de la base de datos.
        
        Returns:
            List[Canal]: Lista con todos los canales disponibles.
        """
        return list(Canal.select().join(Fuente, join_type='LEFT OUTER'))

    @staticmethod
    def get_canal(canal_id: int) -> Optional[Canal]:
        """
        Obtiene un canal específico de la base de datos.
        
        Args:
            canal_id (int): ID del canal a buscar.
        
        Returns:
            Optional[Canal]: El canal encontrado o None si no existe.
        """
        try:
            return Canal.get_by_id(canal_id)
        except Canal.DoesNotExist:
            return None

    @staticmethod
    def insert_canal(canal: Canal) -> bool:
        """
        Inserta un nuevo canal en la base de datos.
        
        Args:
            canal (Canal): Instancia del canal a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            canal.save()
            return True
        except Exception as e:
            print(f"Error al insertar canal: {e}")
            return False

    @staticmethod
    def update_canal(canal: Canal) -> bool:
        """
        Actualiza un canal existente en la base de datos.
        
        Args:
            canal (Canal): Instancia del canal a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            canal.save()
            return True
        except Exception as e:
            print(f"Error al actualizar canal: {e}")
            return False

    @staticmethod
    def delete_canal(canal: Canal) -> bool:
        """
        Elimina un canal de la base de datos.
        
        Args:
            canal (Canal): Instancia del canal a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            canal.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar canal: {e}")
            return False

    @staticmethod
    def get_canal_por_etiqueta(etiqueta: str) -> Optional[Canal]:
        """
        Busca un canal por su etiqueta en la base de datos.
        
        Args:
            etiqueta (str): Etiqueta del canal a buscar.
        
        Returns:
            Optional[Canal]: El canal encontrado o None si no existe.
        """
        try:
            return Canal.get(Canal.etiqueta == etiqueta)
        except Canal.DoesNotExist:
            return None

    @staticmethod
    def get_canales_por_fuente(fuente_id: int) -> List[Canal]:
        """
        Obtiene todos los canales asociados a una fuente específica.
        
        Args:
            fuente_id (int): ID de la fuente.
        
        Returns:
            List[Canal]: Lista de canales asociados a la fuente.
        """
        return list(Canal.select().where(Canal.fuente == fuente_id))

    @staticmethod
    def get_parametros_canal(canal_id: int, configuracion_id: int) -> dict:
        """
        Obtiene los parámetros de un canal para una configuración específica.
        
        Args:
            canal_id (int): ID del canal.
            configuracion_id (int): ID de la configuración.
        
        Returns:
            dict: Diccionario con los parámetros del canal (Volumen, Solo, Mute, Link).
        """
        canal = Canal.get_by_id(canal_id)
        return {
            'Volumen': canal.volumen,
            'Solo': canal.solo,
            'Mute': canal.mute,
            'Link': canal.link
        }

    @staticmethod
    def actualizar_parametros_canal(canal_id: int, configuracion_id: int, parametros: dict) -> bool:
        """
        Actualiza los parámetros de un canal para una configuración específica.
        
        Args:
            canal_id (int): ID del canal.
            configuracion_id (int): ID de la configuración.
            parametros (dict): Diccionario con los parámetros a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            canal = Canal.get_by_id(canal_id)
            canal.volumen = parametros.get('Volumen', canal.volumen)
            canal.solo = parametros.get('Solo', canal.solo)
            canal.mute = parametros.get('Mute', canal.mute)
            canal.link = parametros.get('Link', canal.link)
            canal.save()
            return True
        except Exception as e:
            print(f"Error al actualizar parámetros del canal: {e}")
            return False