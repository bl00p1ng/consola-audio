from peewee import SqliteDatabase, Model, AutoField, CharField
from typing import List, Optional

db = SqliteDatabase('db/Base_De_Datos.db')

class Tipo(Model):
    id = AutoField()
    nombre = CharField(unique=True)
    descripcion = CharField(null=True)

    class Meta:
        database = db

class TipoDAO:
    @staticmethod
    def get_all() -> List[Tipo]:
        """
        Obtiene todos los tipos de la base de datos.
        
        Returns:
            List[Tipo]: Lista con todos los tipos disponibles.
        """
        return list(Tipo.select())

    @staticmethod
    def get_tipo(tipo_id: int) -> Optional[Tipo]:
        """
        Obtiene un tipo específico de la base de datos.
        
        Args:
            tipo_id (int): ID del tipo a buscar.
        
        Returns:
            Optional[Tipo]: El tipo encontrado o None si no existe.
        """
        try:
            return Tipo.get_by_id(tipo_id)
        except Tipo.DoesNotExist:
            return None

    @staticmethod
    def insert_tipo(tipo: Tipo) -> bool:
        """
        Inserta un nuevo tipo en la base de datos.
        
        Args:
            tipo (Tipo): Instancia del tipo a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            tipo.save()
            return True
        except Exception as e:
            print(f"Error al insertar tipo: {e}")
            return False

    @staticmethod
    def update_tipo(tipo: Tipo) -> bool:
        """
        Actualiza un tipo existente en la base de datos.
        
        Args:
            tipo (Tipo): Instancia del tipo a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            tipo.save()
            return True
        except Exception as e:
            print(f"Error al actualizar tipo: {e}")
            return False

    @staticmethod
    def delete_tipo(tipo: Tipo) -> bool:
        """
        Elimina un tipo de la base de datos.
        
        Args:
            tipo (Tipo): Instancia del tipo a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            tipo.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar tipo: {e}")
            return False

    @staticmethod
    def get_tipo_por_nombre(nombre: str) -> Optional[Tipo]:
        """
        Busca un tipo por su nombre en la base de datos.
        
        Args:
            nombre (str): Nombre del tipo a buscar.
        
        Returns:
            Optional[Tipo]: El tipo encontrado o None si no existe.
        """
        try:
            return Tipo.get(Tipo.nombre == nombre)
        except Tipo.DoesNotExist:
            return None

    @staticmethod
    def buscar_tipos(criterio: str) -> List[Tipo]:
        """
        Busca tipos que coincidan con un criterio en nombre o descripción.
        
        Args:
            criterio (str): Criterio de búsqueda.
        
        Returns:
            List[Tipo]: Lista de tipos que coinciden con el criterio.
        """
        return list(Tipo.select().where(
            (Tipo.nombre.contains(criterio)) |
            (Tipo.descripcion.contains(criterio))
        ))

    @staticmethod
    def get_tipos_por_pagina(pagina: int, elementos_por_pagina: int) -> List[Tipo]:
        """
        Obtiene una página de tipos para implementar paginación.
        
        Args:
            pagina (int): Número de página (comenzando desde 1).
            elementos_por_pagina (int): Cantidad de elementos por página.
        
        Returns:
            List[Tipo]: Lista de tipos para la página especificada.
        """
        return list(Tipo.select().order_by(Tipo.nombre).paginate(pagina, elementos_por_pagina))