from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from peewee import (
    CharField,
    DecimalField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
    DatabaseError
)

from model.configuracion import Configuracion
from model.entrada import Entrada
from model.base import BaseModel
from model.entrada import Permite
from model.frecuencia import Frecuencia

class InterfazAudio(BaseModel):
    """
    Modelo que representa una interfaz de audio en el sistema.
    
    Una interfaz de audio es el dispositivo principal que gestiona las entradas,
    salidas y el procesamiento de audio. Puede tener múltiples configuraciones,
    frecuencias de muestreo soportadas y entradas disponibles.
    
    Attributes:
        id_interfaz (IntegerField): Identificador único de la interfaz
        nombre_corto (CharField): Nombre corto o identificador de la interfaz
        modelo (CharField): Modelo específico de la interfaz
        nombre_comercial (CharField): Nombre comercial completo
        precio (DecimalField): Precio de la interfaz
        created_at (DateTimeField): Fecha y hora de creación
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    
    id_interfaz = IntegerField(
        primary_key=True,
        column_name='ID_Interfaz',
        help_text="Identificador único de la interfaz"
    )
    nombre_corto = CharField(
        max_length=50,
        column_name='Nombre_Corto',
        help_text="Nombre corto o identificador de la interfaz"
    )
    modelo = CharField(
        max_length=100,
        help_text="Modelo específico de la interfaz"
    )
    nombre_comercial = CharField(
        max_length=255,
        column_name='Nombre_Comercial',
        help_text="Nombre comercial completo de la interfaz"
    )
    precio = DecimalField(
        decimal_places=2,
        auto_round=True,
        help_text="Precio de la interfaz"
    )
    created_at = DateTimeField(
        default=datetime.now,
        help_text="Fecha y hora de creación"
    )
    updated_at = DateTimeField(
        default=datetime.now,
        help_text="Fecha y hora de última actualización"
    )

    class Meta:
        table_name = 'Interfaz_de_Audio'
        indexes = (
            (('nombre_corto',), True),  # Índice único en nombre_corto
            (('modelo',), False),       # Índice en modelo para búsquedas
        )

    @classmethod
    def crear_interfaz(
        cls,
        nombre_corto: str,
        modelo: str,
        nombre_comercial: str,
        precio: Decimal,
        frecuencias: List[float] = None
    ) -> 'InterfazAudio':
        """
        Crea una nueva interfaz de audio con los parámetros especificados.
        
        Args:
            nombre_corto (str): Nombre corto de la interfaz
            modelo (str): Modelo de la interfaz
            nombre_comercial (str): Nombre comercial completo
            precio (Decimal): Precio de la interfaz
            frecuencias (List[float], optional): Lista de frecuencias soportadas
            
        Returns:
            InterfazAudio: Nueva instancia de InterfazAudio creada
            
        Raises:
            ValueError: Si algún parámetro requerido está vacío o es inválido
            DatabaseError: Si hay un error en la creación
        """
        if not all([nombre_corto, modelo, nombre_comercial]):
            raise ValueError("Todos los campos de nombre son requeridos")
        
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        
        try:
            interfaz = cls.create(
                nombre_corto=nombre_corto,
                modelo=modelo,
                nombre_comercial=nombre_comercial,
                precio=precio
            )
            
            if frecuencias:
                for freq in frecuencias:
                    frecuencia = Frecuencia.get_or_create(valor=freq)[0]
                    InterfazFrecuencia.create(
                        interfaz=interfaz,
                        frecuencia=frecuencia
                    )
            
            return interfaz
            
        except DatabaseError as e:
            raise DatabaseError(f"Error al crear la interfaz de audio: {str(e)}")

    def agregar_entrada(self, entrada_id: int) -> bool:
        """
        Agrega una entrada disponible para esta interfaz.
        
        Args:
            entrada_id (int): ID de la entrada a agregar
            
        Returns:
            bool: True si la entrada fue agregada exitosamente
            
        Raises:
            DatabaseError: Si hay un error al agregar la entrada
        """
        from model.entrada import Entrada
        try:
            Permite.create(
                interfaz=self,
                entrada=entrada_id
            )
            return True
        except DatabaseError as e:
            raise DatabaseError(f"Error al agregar entrada: {str(e)}")

    def get_frecuencias_soportadas(self) -> List[float]:
        """
        Obtiene todas las frecuencias de muestreo soportadas por la interfaz.
        
        Returns:
            List[float]: Lista de frecuencias soportadas en Hz
        """
        return [
            if_freq.frecuencia.valor
            for if_freq in self.interfaz_frecuencia_set
        ]

    def get_entradas_disponibles(self) -> List['Entrada']:
        """
        Obtiene todas las entradas disponibles para esta interfaz.
        
        Returns:
            List[Entrada]: Lista de entradas disponibles
        """
        from model.entrada import Entrada
        return (Entrada
                .select()
                .join(Permite)
                .where(Permite.interfaz == self))

    def get_fuentes_soportadas(self) -> List['Fuente']:
        """
        Obtiene todas las fuentes de audio soportadas por esta interfaz.
        
        Returns:
            List[Fuente]: Lista de fuentes soportadas
        """
        from model.fuente import Fuente, Maneja
        return (Fuente
                .select()
                .join(Maneja)
                .where(Maneja.interfaz == self))

    def get_configuraciones(self) -> List['Configuracion']:
        """
        Obtiene todas las configuraciones que utilizan esta interfaz.
        
        Returns:
            List[Configuracion]: Lista de configuraciones asociadas
        """
        from model.configuracion import Configuracion
        from model.usuario import Personaliza
        return (Configuracion
                .select()
                .join(Personaliza)
                .where(Personaliza.interfaz == self))

    def actualizar(
        self,
        nombre_corto: Optional[str] = None,
        modelo: Optional[str] = None,
        nombre_comercial: Optional[str] = None,
        precio: Optional[Decimal] = None
    ) -> bool:
        """
        Actualiza los datos de la interfaz de audio.
        
        Args:
            nombre_corto (Optional[str]): Nuevo nombre corto
            modelo (Optional[str]): Nuevo modelo
            nombre_comercial (Optional[str]): Nuevo nombre comercial
            precio (Optional[Decimal]): Nuevo precio
            
        Returns:
            bool: True si la actualización fue exitosa
            
        Raises:
            ValueError: Si algún parámetro es inválido
        """
        if nombre_corto is not None:
            if not nombre_corto:
                raise ValueError("El nombre corto no puede estar vacío")
            self.nombre_corto = nombre_corto
            
        if modelo is not None:
            if not modelo:
                raise ValueError("El modelo no puede estar vacío")
            self.modelo = modelo
            
        if nombre_comercial is not None:
            if not nombre_comercial:
                raise ValueError("El nombre comercial no puede estar vacío")
            self.nombre_comercial = nombre_comercial
            
        if precio is not None:
            if precio <= 0:
                raise ValueError("El precio debe ser mayor que 0")
            self.precio = precio
            
        self.updated_at = datetime.now()
        self.save()
        return True

    def to_dict(self) -> dict:
        """
        Convierte la interfaz a un diccionario para serialización.
        
        Returns:
            dict: Representación en diccionario de la interfaz
        """
        return {
            'id': self.id_interfaz,
            'nombre_corto': self.nombre_corto,
            'modelo': self.modelo,
            'nombre_comercial': self.nombre_comercial,
            'precio': float(self.precio),
            'frecuencias_soportadas': self.get_frecuencias_soportadas(),
            'entradas_disponibles': [
                {'id': e.id, 'etiqueta': e.etiqueta}
                for e in self.get_entradas_disponibles()
            ],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __str__(self) -> str:
        """
        Representación en string de la interfaz.
        """
        return (f"InterfazAudio(id={self.id_interfaz}, "
                f"modelo={self.modelo}, "
                f"nombre_comercial={self.nombre_comercial})")

class InterfazFrecuencia(BaseModel):
    """
    Modelo que representa la relación entre InterfazAudio y Frecuencia.
    Define las frecuencias de muestreo soportadas por cada interfaz.
    
    Attributes:
        interfaz (ForeignKeyField): Referencia a la interfaz de audio
        frecuencia (ForeignKeyField): Referencia a la frecuencia soportada
    """
    
    interfaz = ForeignKeyField(
        InterfazAudio,
        backref='interfaz_frecuencia_set',
        column_name='ID_Interfaz',
        on_delete='CASCADE'
    )
    frecuencia = ForeignKeyField(
        Frecuencia,
        backref='interfaz_frecuencia_set',
        column_name='ID_Frecuencia',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'Interfaz_Frecuencia'
        indexes = (
            (('interfaz', 'frecuencia'), True),  # Índice único
        )