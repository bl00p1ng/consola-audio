from peewee import SqliteDatabase, Model, AutoField, CharField, FloatField, ForeignKeyField
from typing import List, Optional

db = SqliteDatabase('db/Base_De_Datos.db')

class Frecuencia(Model):
    id = AutoField()
    valor = FloatField(unique=True)

    class Meta:
        database = db

class InterfazAudio(Model):
    id = AutoField()
    nombrecorto = CharField()
    modelo = CharField()
    nombrecomercial = CharField()
    precio = FloatField()
    frecuencia = ForeignKeyField(Frecuencia, backref='interfaces')

    class Meta:
        database = db

class InterfazAudioDAO:
    @staticmethod
    def get_all() -> List[InterfazAudio]:
        """
        Obtiene todas las interfaces de audio de la base de datos.
        
        Returns:
            List[InterfazAudio]: Lista con todas las interfaces de audio disponibles.
        """
        return list(InterfazAudio.select(InterfazAudio, Frecuencia).join(Frecuencia))

    @staticmethod
    def get_interfaz_audio(interfaz_id: int) -> Optional[InterfazAudio]:
        """
        Obtiene una interfaz de audio específica de la base de datos.
        
        Args:
            interfaz_id (int): ID de la interfaz de audio a buscar.
        
        Returns:
            Optional[InterfazAudio]: La interfaz de audio encontrada o None si no existe.
        """
        try:
            return InterfazAudio.select(InterfazAudio, Frecuencia).join(Frecuencia).where(InterfazAudio.id == interfaz_id).get()
        except InterfazAudio.DoesNotExist:
            return None

    @staticmethod
    def insert_interfaz_audio(interfaz: InterfazAudio) -> bool:
        """
        Inserta una nueva interfaz de audio en la base de datos.
        
        Args:
            interfaz (InterfazAudio): Instancia de la interfaz de audio a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            interfaz.save()
            return True
        except Exception as e:
            print(f"Error al insertar interfaz de audio: {e}")
            return False

    @staticmethod
    def update_interfaz_audio(interfaz: InterfazAudio) -> bool:
        """
        Actualiza una interfaz de audio existente en la base de datos.
        
        Args:
            interfaz (InterfazAudio): Instancia de la interfaz de audio a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            interfaz.save()
            return True
        except Exception as e:
            print(f"Error al actualizar interfaz de audio: {e}")
            return False

    @staticmethod
    def delete_interfaz_audio(interfaz: InterfazAudio) -> bool:
        """
        Elimina una interfaz de audio de la base de datos.
        
        Args:
            interfaz (InterfazAudio): Instancia de la interfaz de audio a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            interfaz.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar interfaz de audio: {e}")
            return False

    @staticmethod
    def get_interfaces_por_frecuencia(frecuencia: Frecuencia) -> List[InterfazAudio]:
        """
        Obtiene todas las interfaces de audio asociadas a una frecuencia específica.
        
        Args:
            frecuencia (Frecuencia): Instancia de la frecuencia.
        
        Returns:
            List[InterfazAudio]: Lista de interfaces de audio asociadas a la frecuencia.
        """
        return list(InterfazAudio.select().where(InterfazAudio.frecuencia == frecuencia))

    @staticmethod
    def get_interfaces_por_rango_precio(precio_min: float, precio_max: float) -> List[InterfazAudio]:
        """
        Obtiene todas las interfaces de audio dentro de un rango de precios específico.
        
        Args:
            precio_min (float): Precio mínimo del rango.
            precio_max (float): Precio máximo del rango.
        
        Returns:
            List[InterfazAudio]: Lista de interfaces de audio dentro del rango de precios.
        """
        return list(InterfazAudio.select().where((InterfazAudio.precio >= precio_min) & (InterfazAudio.precio <= precio_max)))

    @staticmethod
    def buscar_interfaces(criterio: str) -> List[InterfazAudio]:
        """
        Busca interfaces de audio que coincidan con un criterio en nombre corto, modelo o nombre comercial.
        
        Args:
            criterio (str): Criterio de búsqueda.
        
        Returns:
            List[InterfazAudio]: Lista de interfaces de audio que coinciden con el criterio.
        """
        return list(InterfazAudio.select().where(
            (InterfazAudio.nombrecorto.contains(criterio)) |
            (InterfazAudio.modelo.contains(criterio)) |
            (InterfazAudio.nombrecomercial.contains(criterio))
        ))

    @staticmethod
    def get_interfaces_por_pagina(pagina: int, elementos_por_pagina: int) -> List[InterfazAudio]:
        """
        Obtiene una página de interfaces de audio para implementar paginación.
        
        Args:
            pagina (int): Número de página (comenzando desde 1).
            elementos_por_pagina (int): Cantidad de elementos por página.
        
        Returns:
            List[InterfazAudio]: Lista de interfaces de audio para la página especificada.
        """
        return list(InterfazAudio.select().order_by(InterfazAudio.id).paginate(pagina, elementos_por_pagina))