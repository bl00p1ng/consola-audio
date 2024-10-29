from typing import Optional, List
from datetime import datetime

from peewee import (
    CharField,
    ForeignKeyField,
    FloatField,
    IntegerField,
    BooleanField,
    DatabaseError
)

from model.base import BaseModel
from model.configuracion import Configuracion, Establece

class Canal(BaseModel):
    """
    Modelo que representa un canal de audio en el sistema.
    
    Un canal es una vía de procesamiento de audio que puede tener diferentes
    parámetros según la configuración activa. Cada canal está asociado a una
    fuente de audio y puede ser controlado mediante diversos parámetros.
    
    Attributes:
        codigo_canal (IntegerField): Identificador único del canal
        etiqueta (CharField): Nombre o etiqueta identificativa del canal
        fuente (ForeignKeyField): Fuente de audio asociada al canal
        created_at (DateTimeField): Fecha y hora de creación
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    
    codigo_canal = IntegerField(
        primary_key=True,
        column_name='Codigo_Canal',
        help_text="Identificador único del canal"
    )
    etiqueta = CharField(
        max_length=100,
        null=False,
        help_text="Etiqueta identificativa del canal"
    )
    fuente = ForeignKeyField(
        'Fuente',
        backref='canales',
        column_name='ID_Fuente',
        null=True,
        on_delete='SET NULL',
        help_text="Fuente de audio asociada al canal"
    )

    class Meta:
        table_name = 'Canal'
        indexes = (
            (('etiqueta',), False),  # Índice en etiqueta para búsquedas
        )

    @classmethod
    def crear_canal(cls, etiqueta: str, fuente_id: Optional[int] = None) -> 'Canal':
        """
        Crea un nuevo canal con los parámetros especificados.
        
        Args:
            etiqueta (str): Etiqueta identificativa del canal
            fuente_id (Optional[int]): ID de la fuente asociada
            
        Returns:
            Canal: Nueva instancia de Canal creada
            
        Raises:
            ValueError: Si la etiqueta está vacía
            DatabaseError: Si hay un error en la creación del canal
        """
        if not etiqueta:
            raise ValueError("La etiqueta del canal no puede estar vacía")
        
        try:
            from model.fuente import Fuente
            fuente = Fuente.get_by_id(fuente_id) if fuente_id else None
            
            return cls.create(
                etiqueta=etiqueta,
                fuente=fuente
            )
        except DatabaseError as e:
            raise DatabaseError(f"Error al crear el canal: {str(e)}")

    def get_parametros_configuracion(self, configuracion_id: int) -> dict:
        """
        Obtiene los parámetros del canal para una configuración específica.
        
        Args:
            configuracion_id (int): ID de la configuración
            
        Returns:
            dict: Diccionario con los parámetros del canal
        """
        try:
            establece = (Establece
                        .select()
                        .where(
                            (Establece.canal == self) & 
                            (Establece.configuracion == configuracion_id)
                        )
                        .get())
            
            return {
                'volumen': establece.volumen,
                'solo': establece.solo,
                'mute': establece.mute,
                'link': establece.link
            }
        except Establece.DoesNotExist:
            return {
                'volumen': 0.0,
                'solo': False,
                'mute': False,
                'link': False
            }

    def set_parametros_configuracion(
        self,
        configuracion_id: int,
        volumen: Optional[float] = None,
        solo: Optional[bool] = None,
        mute: Optional[bool] = None,
        link: Optional[bool] = None
    ) -> bool:
        """
        Establece los parámetros del canal para una configuración específica.
        
        Args:
            configuracion_id (int): ID de la configuración
            volumen (Optional[float]): Nivel de volumen (0.0 a 1.0)
            solo (Optional[bool]): Estado de solo
            mute (Optional[bool]): Estado de mute
            link (Optional[bool]): Estado de link
            
        Returns:
            bool: True si la operación fue exitosa
            
        Raises:
            ValueError: Si el volumen está fuera del rango válido
        """
        if volumen is not None and not (0.0 <= volumen <= 1.0):
            raise ValueError("El volumen debe estar entre 0.0 y 1.0")

        try:
            establece, created = Establece.get_or_create(
                canal=self,
                configuracion=configuracion_id,
                defaults={
                    'volumen': 0.0,
                    'solo': False,
                    'mute': False,
                    'link': False
                }
            )
            
            if volumen is not None:
                establece.volumen = volumen
            if solo is not None:
                establece.solo = solo
            if mute is not None:
                establece.mute = mute
            if link is not None:
                establece.link = link
                
            establece.save()
            return True
            
        except DatabaseError as e:
            raise DatabaseError(f"Error al establecer parámetros: {str(e)}")

    def get_configuraciones(self) -> List['Configuracion']:
        """
        Obtiene todas las configuraciones que utilizan este canal.
        
        Returns:
            List[Configuracion]: Lista de configuraciones asociadas
        """
        from model.configuracion import Configuracion
        return (Configuracion
                .select()
                .join(Establece)
                .where(Establece.canal == self))

    def get_tipo_fuente(self) -> Optional[str]:
        """
        Obtiene el tipo de fuente asociada al canal.
        
        Returns:
            Optional[str]: Nombre del tipo de fuente o None si no tiene
        """
        if self.fuente and self.fuente.tipo:
            return self.fuente.tipo.nombre
        return None

    def to_dict(self) -> dict:
        """
        Convierte el canal a un diccionario para serialización.
        
        Returns:
            dict: Representación en diccionario del canal
        """
        return {
            'codigo_canal': self.codigo_canal,
            'etiqueta': self.etiqueta,
            'fuente_id': self.fuente.id if self.fuente else None,
            'tipo_fuente': self.get_tipo_fuente()
        }

    def __str__(self) -> str:
        """
        Representación en string del canal.
        """
        return f"Canal(codigo={self.codigo_canal}, etiqueta={self.etiqueta})"

    @classmethod
    def get_canales_por_tipo_fuente(cls, tipo_id: int) -> List['Canal']:
        """
        Obtiene todos los canales asociados a un tipo de fuente específico.
        
        Args:
            tipo_id (int): ID del tipo de fuente
            
        Returns:
            List[Canal]: Lista de canales que usan ese tipo de fuente
        """
        from model.fuente import Fuente
        from model.tipo import Tipo
        
        return (cls
                .select()
                .join(Fuente)
                .join(Tipo)
                .where(Tipo.id == tipo_id))

    @classmethod
    def buscar_por_etiqueta(cls, etiqueta: str) -> List['Canal']:
        """
        Busca canales por coincidencia parcial de etiqueta.
        
        Args:
            etiqueta (str): Texto a buscar en las etiquetas
            
        Returns:
            List[Canal]: Lista de canales que coinciden con la búsqueda
        """
        return cls.select().where(cls.etiqueta.contains(etiqueta))