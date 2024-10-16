from peewee import SqliteDatabase, Model, AutoField, FloatField
from typing import List, Optional

db = SqliteDatabase('db/Base_De_Datos.db')

class Frecuencia(Model):
    id = AutoField()
    valor = FloatField(unique=True)

    class Meta:
        database = db

class FrecuenciaDAO:
    @staticmethod
    def get_all() -> List[Frecuencia]:
        """
        Obtiene todas las frecuencias de la base de datos.
        
        Returns:
            List[Frecuencia]: Lista con todas las frecuencias disponibles.
        """
        return list(Frecuencia.select())

    @staticmethod
    def get_frecuencia(frecuencia_id: int) -> Optional[Frecuencia]:
        """
        Obtiene una frecuencia específica de la base de datos.
        
        Args:
            frecuencia_id (int): ID de la frecuencia a buscar.
        
        Returns:
            Optional[Frecuencia]: La frecuencia encontrada o None si no existe.
        """
        try:
            return Frecuencia.get_by_id(frecuencia_id)
        except Frecuencia.DoesNotExist:
            return None

    @staticmethod
    def insert_frecuencia(frecuencia: Frecuencia) -> bool:
        """
        Inserta una nueva frecuencia en la base de datos.
        
        Args:
            frecuencia (Frecuencia): Instancia de la frecuencia a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            frecuencia.save()
            return True
        except Exception as e:
            print(f"Error al insertar frecuencia: {e}")
            return False

    @staticmethod
    def update_frecuencia(frecuencia: Frecuencia) -> bool:
        """
        Actualiza una frecuencia existente en la base de datos.
        
        Args:
            frecuencia (Frecuencia): Instancia de la frecuencia a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            frecuencia.save()
            return True
        except Exception as e:
            print(f"Error al actualizar frecuencia: {e}")
            return False

    @staticmethod
    def delete_frecuencia(frecuencia: Frecuencia) -> bool:
        """
        Elimina una frecuencia de la base de datos.
        
        Args:
            frecuencia (Frecuencia): Instancia de la frecuencia a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            frecuencia.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar frecuencia: {e}")
            return False

    @staticmethod
    def get_frecuencia_por_valor(valor: float) -> Optional[Frecuencia]:
        """
        Busca una frecuencia por su valor en la base de datos.
        
        Args:
            valor (float): Valor de la frecuencia a buscar.
        
        Returns:
            Optional[Frecuencia]: La frecuencia encontrada o None si no existe.
        """
        try:
            return Frecuencia.get(Frecuencia.valor == valor)
        except Frecuencia.DoesNotExist:
            return None

    @staticmethod
    def get_frecuencias_en_rango(valor_minimo: float, valor_maximo: float) -> List[Frecuencia]:
        """
        Obtiene todas las frecuencias dentro de un rango especificado.
        
        Args:
            valor_minimo (float): Valor mínimo del rango.
            valor_maximo (float): Valor máximo del rango.
        
        Returns:
            List[Frecuencia]: Lista de frecuencias dentro del rango especificado.
        """
        return list(Frecuencia.select().where(
            (Frecuencia.valor >= valor_minimo) & 
            (Frecuencia.valor <= valor_maximo)
        ))

    @staticmethod
    def get_frecuencia_mas_cercana(valor: float) -> Optional[Frecuencia]:
        """
        Obtiene la frecuencia más cercana al valor proporcionado.
        
        Args:
            valor (float): Valor de referencia.
        
        Returns:
            Optional[Frecuencia]: La frecuencia más cercana o None si no hay frecuencias.
        """
        return Frecuencia.select().order_by(
            (Frecuencia.valor - valor).abs()
        ).first()

    @staticmethod
    def get_frecuencias_por_pagina(pagina: int, elementos_por_pagina: int) -> List[Frecuencia]:
        """
        Obtiene una página de frecuencias para implementar paginación.
        
        Args:
            pagina (int): Número de página (comenzando desde 1).
            elementos_por_pagina (int): Cantidad de elementos por página.
        
        Returns:
            List[Frecuencia]: Lista de frecuencias para la página especificada.
        """
        return list(Frecuencia.select().order_by(Frecuencia.valor).paginate(pagina, elementos_por_pagina))