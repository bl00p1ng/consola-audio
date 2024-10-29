from typing import List, Optional
from datetime import datetime

from peewee import (
    IntegerField,
    ForeignKeyField,
    DeferredForeignKey,
    DateTimeField,
    DatabaseError
)

# from model.canal import Canal
# from model.interfaz_audio import InterfazAudio
from model.base import BaseModel
# from model.tipo import Tipo

class Fuente(BaseModel):
    """
    Modelo que representa una fuente de audio en el sistema.
    
    Una fuente es el origen de una señal de audio que puede ser asignada a
    diferentes canales y es compatible con ciertas interfaces de audio.
    Cada fuente tiene un tipo específico que define sus características.
    
    Attributes:
        id_fuente (IntegerField): Identificador único de la fuente
        created_at (DateTimeField): Fecha y hora de creación
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    
    id_fuente = IntegerField(
        primary_key=True,
        column_name='ID_Fuente',
        help_text="Identificador único de la fuente"
    )

    class Meta:
        table_name = 'Fuente'

    @classmethod
    def crear_fuente(cls, tipo_id: Optional[int] = None) -> 'Fuente':
        """
        Crea una nueva fuente con el tipo especificado.
        
        Args:
            tipo_id (Optional[int]): ID del tipo de fuente
            
        Returns:
            Fuente: Nueva instancia de Fuente creada
            
        Raises:
            DatabaseError: Si hay un error en la creación
        """
        try:
            fuente = cls.create()
            
            if tipo_id:
                from model.tipo import Tipo
                tipo = Tipo.get_by_id(tipo_id)
                Clasifica.create(
                    fuente=fuente,
                    tipo=tipo
                )
            
            return fuente
            
        except DatabaseError as e:
            raise DatabaseError(f"Error al crear la fuente: {str(e)}")

    def get_tipo(self):
        """
        Obtiene el tipo asociado a esta fuente.
        
        Returns:
            Optional[Tipo]: Tipo de la fuente o None si no tiene tipo
        """
        clasifica = (Clasifica
                    .select()
                    .where(Clasifica.fuente == self)
                    .first())
        return clasifica.tipo if clasifica else None

    def set_tipo(self, tipo_id: int) -> bool:
        """
        Establece el tipo de la fuente.
        
        Args:
            tipo_id (int): ID del tipo a asignar
            
        Returns:
            bool: True si la asignación fue exitosa
            
        Raises:
            DatabaseError: Si hay un error al establecer el tipo
        """
        try:
            from model.tipo import Tipo
            tipo = Tipo.get_by_id(tipo_id)
            
            Clasifica.delete().where(Clasifica.fuente == self).execute()
            Clasifica.create(
                fuente=self,
                tipo=tipo
            )
            return True
            
        except DatabaseError as e:
            raise DatabaseError(f"Error al establecer el tipo: {str(e)}")

    def get_canales(self):
        """
        Obtiene todos los canales que utilizan esta fuente.
        
        Returns:
            List[Canal]: Lista de canales asociados
        """
        from model.canal import Canal
        return (Canal
                .select()
                .where(Canal.fuente == self))

    def get_interfaces_compatibles(self):
        """
        Obtiene todas las interfaces de audio compatibles con esta fuente.
        
        Returns:
            List[InterfazAudio]: Lista de interfaces compatibles
        """
        from model.interfaz_audio import InterfazAudio
        return (InterfazAudio
                .select()
                .join(Maneja)
                .where(Maneja.fuente == self))

    def agregar_interfaz_compatible(self, interfaz_id: int) -> bool:
        """
        Agrega una interfaz de audio como compatible con esta fuente.
        
        Args:
            interfaz_id (int): ID de la interfaz a agregar
            
        Returns:
            bool: True si la interfaz fue agregada exitosamente
        """
        try:
            from model.interfaz_audio import InterfazAudio, Maneja
            interfaz = InterfazAudio.get_by_id(interfaz_id)
            
            Maneja.create(
                fuente=self,
                interfaz=interfaz
            )
            return True
            
        except DatabaseError as e:
            raise DatabaseError(f"Error al agregar interfaz compatible: {str(e)}")

    def is_compatible_con_interfaz(self, interfaz_id: int) -> bool:
        """
        Verifica si la fuente es compatible con una interfaz específica.
        
        Args:
            interfaz_id (int): ID de la interfaz a verificar
            
        Returns:
            bool: True si la fuente es compatible con la interfaz
        """
        from model.interfaz_audio import Maneja
        return (Maneja
                .select()
                .where(
                    (Maneja.fuente == self) &
                    (Maneja.interfaz == interfaz_id)
                )
                .exists())

    def to_dict(self) -> dict:
        """
        Convierte la fuente a un diccionario para serialización.
        
        Returns:
            dict: Representación en diccionario de la fuente
        """
        tipo = self.get_tipo()
        return {
            'id': self.id_fuente,
            'tipo': {
                'id': tipo.id,
                'nombre': tipo.nombre,
                'descripcion': tipo.descripcion
            } if tipo else None,
            'interfaces_compatibles': [
                {'id': i.id_interfaz, 'nombre': i.nombre_comercial}
                for i in self.get_interfaces_compatibles()
            ],
            'canales': [
                {'id': c.codigo_canal, 'etiqueta': c.etiqueta}
                for c in self.get_canales()
            ],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __str__(self) -> str:
        """
        Representación en string de la fuente.
        """
        tipo = self.get_tipo()
        return f"Fuente(id={self.id_fuente}, tipo={tipo.nombre if tipo else 'Sin tipo'})"


class Clasifica(BaseModel):
    """
    Modelo que representa la relación entre Fuente y Tipo.
    Define el tipo específico de cada fuente de audio.
    
    Attributes:
        fuente (ForeignKeyField): Referencia a la fuente
        tipo (ForeignKeyField): Referencia al tipo de fuente
    """
    
    fuente = ForeignKeyField(
        Fuente,
        backref='clasifica_set',
        column_name='ID_Fuente',
        on_delete='CASCADE'
    )
    tipo = DeferredForeignKey(
        'Tipo',
        backref='clasifica_set',
        column_name='ID_Tipo',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'Clasifica'
        indexes = (
            (('fuente', 'tipo'), True),  # Índice único
        )


class Maneja(BaseModel):
    """
    Modelo que representa la relación entre Fuente e InterfazAudio.
    Define qué interfaces de audio son compatibles con cada fuente.
    
    Attributes:
        fuente (ForeignKeyField): Referencia a la fuente
        interfaz (ForeignKeyField): Referencia a la interfaz compatible
    """
    
    fuente = ForeignKeyField(
        Fuente,
        backref='maneja_set',
        column_name='ID_Fuente',
        on_delete='CASCADE'
    )
    interfaz = DeferredForeignKey(
        'InterfazAudio',
        backref='maneja_set',
        column_name='ID_Interfaz',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'Maneja'
        indexes = (
            (('fuente', 'interfaz'), True),  # Índice único
        )