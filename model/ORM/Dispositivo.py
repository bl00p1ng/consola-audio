from peewee import SqliteDatabase, Model, AutoField, CharField
from typing import List, Optional

db = SqliteDatabase('db/Base_De_Datos.db')

class Dispositivo(Model):
    id = AutoField()
    nombre = CharField()
    descripcion = CharField()

    class Meta:
        database = db

class DispositivoDAO:
    @staticmethod
    def get_all() -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos de la base de datos.
        
        Returns:
            List[Dispositivo]: Lista con todos los dispositivos disponibles.
        """
        return list(Dispositivo.select())

    @staticmethod
    def get_dispositivo(dispositivo_id: int) -> Optional[Dispositivo]:
        """
        Obtiene un dispositivo específico de la base de datos.
        
        Args:
            dispositivo_id (int): ID del dispositivo a buscar.
        
        Returns:
            Optional[Dispositivo]: El dispositivo encontrado o None si no existe.
        """
        try:
            return Dispositivo.get_by_id(dispositivo_id)
        except Dispositivo.DoesNotExist:
            return None

    @staticmethod
    def insert_dispositivo(dispositivo: Dispositivo) -> bool:
        """
        Inserta un nuevo dispositivo en la base de datos.
        
        Args:
            dispositivo (Dispositivo): Instancia del dispositivo a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            dispositivo.save()
            return True
        except Exception as e:
            print(f"Error al insertar dispositivo: {e}")
            return False

    @staticmethod
    def update_dispositivo(dispositivo: Dispositivo) -> bool:
        """
        Actualiza un dispositivo existente en la base de datos.
        
        Args:
            dispositivo (Dispositivo): Instancia del dispositivo a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            dispositivo.save()
            return True
        except Exception as e:
            print(f"Error al actualizar dispositivo: {e}")
            return False

    @staticmethod
    def delete_dispositivo(dispositivo: Dispositivo) -> bool:
        """
        Elimina un dispositivo de la base de datos.
        
        Args:
            dispositivo (Dispositivo): Instancia del dispositivo a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            dispositivo.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar dispositivo: {e}")
            return False

    @staticmethod
    def get_dispositivo_por_nombre(nombre: str) -> Optional[Dispositivo]:
        """
        Busca un dispositivo por su nombre en la base de datos.
        
        Args:
            nombre (str): Nombre del dispositivo a buscar.
        
        Returns:
            Optional[Dispositivo]: El dispositivo encontrado o None si no existe.
        """
        try:
            return Dispositivo.get(Dispositivo.nombre == nombre)
        except Dispositivo.DoesNotExist:
            return None

    @staticmethod
    def buscar_dispositivos(criterio: str) -> List[Dispositivo]:
        """
        Busca dispositivos que coincidan con un criterio en nombre o descripción.
        
        Args:
            criterio (str): Criterio de búsqueda.
        
        Returns:
            List[Dispositivo]: Lista de dispositivos que coinciden con el criterio.
        """
        return list(Dispositivo.select().where(
            (Dispositivo.nombre.contains(criterio)) |
            (Dispositivo.descripcion.contains(criterio))
        ))