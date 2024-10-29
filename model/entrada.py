from typing import List, Optional
from datetime import datetime

from peewee import (
    CharField,
    ForeignKeyField,
    DeferredForeignKey,
    IntegerField,
    DatabaseError,
    JOIN
)

from model.base import BaseModel
# from model.configuracion import Conectado, Configuracion
# from model.dispositivo import Dispositivo
from model.interfaz_audio import InterfazAudio

class Entrada(BaseModel):
    """
    Modelo que representa una entrada de audio en el sistema.
    
    Una entrada es un punto de conexión para dispositivos de audio que puede
    ser utilizado en diferentes configuraciones y asociado a diferentes
    interfaces de audio.
    
    Attributes:
        id_entrada (IntegerField): Identificador único de la entrada
        etiqueta (CharField): Etiqueta identificativa de la entrada
        descripcion (CharField): Descripción detallada de la entrada
        created_at (DateTimeField): Fecha y hora de creación
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    
    id_entrada = IntegerField(
        primary_key=True,
        column_name='ID_Entrada',
        help_text="Identificador único de la entrada"
    )
    etiqueta = CharField(
        max_length=100,
        null=False,
        help_text="Etiqueta identificativa de la entrada"
    )
    descripcion = CharField(
        max_length=255,
        null=True,
        help_text="Descripción detallada de la entrada"
    )

    class Meta:
        table_name = 'Entrada'
        indexes = (
            (('etiqueta',), False),  # Índice en etiqueta para búsquedas
        )

    @classmethod
    def crear_entrada(cls, etiqueta: str, descripcion: Optional[str] = None) -> 'Entrada':
        """
        Crea una nueva entrada con los parámetros especificados.
        
        Args:
            etiqueta (str): Etiqueta identificativa de la entrada
            descripcion (Optional[str]): Descripción detallada de la entrada
            
        Returns:
            Entrada: Nueva instancia de Entrada creada
            
        Raises:
            ValueError: Si la etiqueta está vacía
            DatabaseError: Si hay un error en la creación de la entrada
        """
        if not etiqueta:
            raise ValueError("La etiqueta de la entrada no puede estar vacía")
        
        try:
            return cls.create(
                etiqueta=etiqueta,
                descripcion=descripcion
            )
        except DatabaseError as e:
            raise DatabaseError(f"Error al crear la entrada: {str(e)}")

    def get_dispositivo_configuracion(self, configuracion_id: int) -> Optional['Dispositivo']:
        """
        Obtiene el dispositivo conectado a esta entrada en una configuración específica.
        
        Args:
            configuracion_id (int): ID de la configuración
            
        Returns:
            Optional[Dispositivo]: Dispositivo conectado o None si no hay ninguno
        """
        from model.configuracion import Conectado
        try:
            conectado = (Conectado
                        .select()
                        .where(
                            (Conectado.entrada == self) & 
                            (Conectado.configuracion == configuracion_id)
                        )
                        .get())
            return conectado.dispositivo
        except Conectado.DoesNotExist:
            return None

    def set_dispositivo_configuracion(
        self,
        configuracion_id: int,
        dispositivo_id: Optional[int]
    ) -> bool:
        """
        Establece o actualiza el dispositivo conectado a esta entrada
        en una configuración específica.
        
        Args:
            configuracion_id (int): ID de la configuración
            dispositivo_id (Optional[int]): ID del dispositivo a conectar
            
        Returns:
            bool: True si la operación fue exitosa
            
        Raises:
            DatabaseError: Si hay un error al establecer la conexión
        """
        try:
            from model.dispositivo import Dispositivo
            
            # Eliminar conexión existente si la hay
            Conectado.delete().where(
                (Conectado.entrada == self) &
                (Conectado.configuracion == configuracion_id)
            ).execute()
            
            # Si se proporciona un dispositivo, crear nueva conexión
            if dispositivo_id:
                dispositivo = Dispositivo.get_by_id(dispositivo_id)
                Conectado.create(
                    entrada=self,
                    configuracion=configuracion_id,
                    dispositivo=dispositivo
                )
            
            return True
            
        except DatabaseError as e:
            raise DatabaseError(f"Error al establecer dispositivo: {str(e)}")

    def get_interfaces_compatibles(self) -> List['InterfazAudio']:
        """
        Obtiene todas las interfaces de audio compatibles con esta entrada.
        
        Returns:
            List[InterfazAudio]: Lista de interfaces de audio compatibles
        """
        from model.interfaz_audio import InterfazAudio, Permite
        return (InterfazAudio
                .select()
                .join(Permite)
                .where(Permite.entrada == self))

    def get_configuraciones(self) -> List['Configuracion']:
        """
        Obtiene todas las configuraciones que utilizan esta entrada.
        
        Returns:
            List[Configuracion]: Lista de configuraciones que usan esta entrada
        """
        from model.configuracion import Configuracion, Conectado
        return (Configuracion
                .select()
                .join(Conectado)
                .where(Conectado.entrada == self))

    def is_compatible_con_interfaz(self, interfaz_id: int) -> bool:
        """
        Verifica si la entrada es compatible con una interfaz de audio específica.
        
        Args:
            interfaz_id (int): ID de la interfaz de audio
            
        Returns:
            bool: True si la entrada es compatible con la interfaz
        """
        from model.interfaz_audio import Permite
        return (Permite
                .select()
                .where(
                    (Permite.entrada == self) &
                    (Permite.interfaz == interfaz_id)
                )
                .exists())

    def to_dict(self) -> dict:
        """
        Convierte la entrada a un diccionario para serialización.
        
        Returns:
            dict: Representación en diccionario de la entrada
        """
        return {
            'id': self.id_entrada,
            'etiqueta': self.etiqueta,
            'descripcion': self.descripcion,
            'interfaces_compatibles': [
                {'id': i.id, 'nombre': i.nombre_comercial}
                for i in self.get_interfaces_compatibles()
            ]
        }

    @classmethod
    def buscar_por_etiqueta(cls, etiqueta: str) -> List['Entrada']:
        """
        Busca entradas por coincidencia parcial de etiqueta.
        
        Args:
            etiqueta (str): Texto a buscar en las etiquetas
            
        Returns:
            List[Entrada]: Lista de entradas que coinciden con la búsqueda
        """
        return cls.select().where(cls.etiqueta.contains(etiqueta))

    @classmethod
    def get_entradas_por_dispositivo(cls, dispositivo_id: int) -> List['Entrada']:
        """
        Obtiene todas las entradas que han sido utilizadas por un dispositivo específico.
        
        Args:
            dispositivo_id (int): ID del dispositivo
            
        Returns:
            List[Entrada]: Lista de entradas asociadas al dispositivo
        """
        return (cls
                .select()
                .join(Conectado)
                .where(Conectado.dispositivo == dispositivo_id)
                .distinct())

    def __str__(self) -> str:
        """
        Representación en string de la entrada.
        """
        return f"Entrada(id={self.id_entrada}, etiqueta={self.etiqueta})"

class Permite(BaseModel):
    """
    Modelo que representa la relación entre Entrada e InterfazAudio.
    Define qué entradas están disponibles para cada interfaz de audio.
    
    Attributes:
        entrada (ForeignKeyField): Referencia a la entrada
        interfaz (ForeignKeyField): Referencia a la interfaz de audio
    """
    
    entrada = ForeignKeyField(
        Entrada,
        backref='permite_set',
        column_name='ID_Entrada',
        on_delete='CASCADE'
    )
    interfaz = DeferredForeignKey(
        'InterfazAudio',
        backref='permite_set',
        column_name='ID_Interfaz',
        on_delete='CASCADE',
        deferred_class='model.interfaz_audio.InterfazAudio'
    )

    class Meta:
        table_name = 'Permite'
        indexes = (
            (('entrada', 'interfaz'), True),  # Índice único
        )