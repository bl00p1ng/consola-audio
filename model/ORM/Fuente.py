from peewee import SqliteDatabase, Model, AutoField, ForeignKeyField
from typing import List, Optional

db = SqliteDatabase('db/Base_De_Datos.db')

class Tipo(Model):
    id = AutoField()
    nombre = CharField()
    descripcion = CharField(null=True)

    class Meta:
        database = db

class Fuente(Model):
    id = AutoField()
    tipo = ForeignKeyField(Tipo, backref='fuentes', null=True)

    class Meta:
        database = db

class FuenteDAO:
    @staticmethod
    def get_all() -> List[Fuente]:
        """
        Obtiene todas las fuentes de la base de datos, incluyendo su tipo asociado.

        Returns:
            List[Fuente]: Lista con todas las fuentes disponibles.
        """
        return list(Fuente.select(Fuente, Tipo).join(Tipo, join_type='LEFT OUTER'))

    @staticmethod
    def get_fuente(fuente_id: int) -> Optional[Fuente]:
        """
        Obtiene una fuente específica de la base de datos, incluyendo su tipo.

        Args:
            fuente_id (int): ID de la fuente a buscar.

        Returns:
            Optional[Fuente]: La fuente encontrada o None si no existe.
        """
        try:
            return Fuente.select(Fuente, Tipo).join(Tipo, join_type='LEFT OUTER').where(Fuente.id == fuente_id).get()
        except Fuente.DoesNotExist:
            return None

    @staticmethod
    def insert_fuente(fuente: Fuente) -> bool:
        """
        Inserta una nueva fuente en la base de datos y establece su relación con un tipo.

        Args:
            fuente (Fuente): Instancia de la fuente a insertar.

        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            fuente.save()
            return True
        except Exception as e:
            print(f"Error al insertar fuente: {e}")
            return False

    @staticmethod
    def update_fuente(fuente: Fuente) -> bool:
        """
        Actualiza una fuente existente en la base de datos y su relación con un tipo.

        Args:
            fuente (Fuente): Instancia de la fuente a actualizar.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            fuente.save()
            return True
        except Exception as e:
            print(f"Error al actualizar fuente: {e}")
            return False

    @staticmethod
    def delete_fuente(fuente: Fuente) -> bool:
        """
        Elimina una fuente de la base de datos y sus relaciones asociadas.

        Args:
            fuente (Fuente): Instancia de la fuente a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            fuente.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar fuente: {e}")
            return False

    @staticmethod
    def get_fuentes_por_tipo(tipo: Tipo) -> List[Fuente]:
        """
        Obtiene todas las fuentes asociadas a un tipo específico.

        Args:
            tipo (Tipo): Instancia del tipo.

        Returns:
            List[Fuente]: Lista de fuentes asociadas al tipo.
        """
        return list(Fuente.select().where(Fuente.tipo == tipo))

    @staticmethod
    def get_fuentes_sin_tipo() -> List[Fuente]:
        """
        Obtiene todas las fuentes que no tienen un tipo asociado.

        Returns:
            List[Fuente]: Lista de fuentes sin tipo asociado.
        """
        return list(Fuente.select().where(Fuente.tipo.is_null()))

    @staticmethod
    def asignar_tipo_a_fuente(fuente: Fuente, tipo: Tipo) -> bool:
        """
        Asigna un tipo a una fuente existente.

        Args:
            fuente (Fuente): Instancia de la fuente.
            tipo (Tipo): Instancia del tipo a asignar.

        Returns:
            bool: True si la asignación fue exitosa, False en caso contrario.
        """
        try:
            fuente.tipo = tipo
            fuente.save()
            return True
        except Exception as e:
            print(f"Error al asignar tipo a fuente: {e}")
            return False

    @staticmethod
    def get_fuentes_por_pagina(pagina: int, elementos_por_pagina: int) -> List[Fuente]:
        """
        Obtiene una página de fuentes para implementar paginación.

        Args:
            pagina (int): Número de página (comenzando desde 1).
            elementos_por_pagina (int): Cantidad de elementos por página.

        Returns:
            List[Fuente]: Lista de fuentes para la página especificada.
        """
        return list(Fuente.select().order_by(Fuente.id).paginate(pagina, elementos_por_pagina))