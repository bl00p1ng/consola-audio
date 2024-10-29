from typing import List, Optional
from datetime import datetime

from peewee import (
    FloatField,
    IntegerField,
    DateTimeField,
    DatabaseError
)

# from model.interfaz_audio import InterfazAudio
from model.base import BaseModel

class Frecuencia(BaseModel):
    """
    Modelo que representa una frecuencia de muestreo en el sistema.
    
    Las frecuencias de muestreo son valores fundamentales que determinan
    la calidad y capacidad de procesamiento del audio digital en las
    interfaces de audio.
    
    Attributes:
        id_frecuencia (IntegerField): Identificador único de la frecuencia
        valor (FloatField): Valor de la frecuencia en kHz
        created_at (DateTimeField): Fecha y hora de creación
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    
    id_frecuencia = IntegerField(
        primary_key=True,
        column_name='ID_Frecuencia',
        help_text="Identificador único de la frecuencia"
    )
    valor = FloatField(
        unique=True,
        index=True,
        help_text="Valor de la frecuencia en kHz"
    )

    class Meta:
        table_name = 'Frecuencia'
        indexes = (
            (('valor',), True),  # Índice único en valor
        )

    @classmethod
    def crear_frecuencia(cls, valor: float) -> 'Frecuencia':
        """
        Crea una nueva frecuencia con el valor especificado.
        
        Args:
            valor (float): Valor de la frecuencia en kHz
            
        Returns:
            Frecuencia: Nueva instancia de Frecuencia creada
            
        Raises:
            ValueError: Si el valor es inválido
            DatabaseError: Si hay un error en la creación
        """
        if not cls.es_valor_valido(valor):
            raise ValueError(
                "El valor de frecuencia debe ser positivo y estar en un rango válido (8-192 kHz)"
            )
        
        try:
            return cls.create(valor=valor)
        except DatabaseError as e:
            raise DatabaseError(f"Error al crear la frecuencia: {str(e)}")

    @staticmethod
    def es_valor_valido(valor: float) -> bool:
        """
        Verifica si un valor de frecuencia es válido.
        
        Args:
            valor (float): Valor a verificar
            
        Returns:
            bool: True si el valor es válido
        """
        # Rango típico de frecuencias de muestreo en audio digital (8-192 kHz)
        return 8.0 <= valor <= 192.0

    def get_interfaces(self):
        """
        Obtiene todas las interfaces de audio que soportan esta frecuencia.
        
        Returns:
            List[InterfazAudio]: Lista de interfaces que soportan esta frecuencia
        """
        from model.interfaz_audio import InterfazAudio, InterfazFrecuencia
        return (InterfazAudio
                .select()
                .join(InterfazFrecuencia)
                .where(InterfazFrecuencia.frecuencia == self))

    @classmethod
    def get_frecuencias_comunes(cls) -> List['Frecuencia']:
        """
        Obtiene una lista de frecuencias de muestreo comunes.
        
        Returns:
            List[Frecuencia]: Lista de frecuencias comunes
        """
        frecuencias_comunes = [44.1, 48.0, 88.2, 96.0, 176.4, 192.0]
        resultado = []
        
        for valor in frecuencias_comunes:
            frecuencia, _ = cls.get_or_create(
                valor=valor,
                defaults={'valor': valor}
            )
            resultado.append(frecuencia)
        
        return resultado

    @classmethod
    def get_por_valor(cls, valor: float) -> Optional['Frecuencia']:
        """
        Obtiene una frecuencia por su valor exacto.
        
        Args:
            valor (float): Valor de la frecuencia a buscar
            
        Returns:
            Optional[Frecuencia]: Frecuencia encontrada o None
        """
        try:
            return cls.get(cls.valor == valor)
        except cls.DoesNotExist:
            return None

    def get_frecuencias_relacionadas(self) -> List['Frecuencia']:
        """
        Obtiene frecuencias relacionadas (múltiplos o submúltiplos).
        
        Returns:
            List[Frecuencia]: Lista de frecuencias relacionadas
        """
        # Busca múltiplos y submúltiplos comunes (2x, 4x, 1/2x)
        valores_relacionados = [
            self.valor * 2,
            self.valor * 4,
            self.valor / 2
        ]
        
        return [
            freq for freq in Frecuencia.select()
            .where(Frecuencia.valor.in_(valores_relacionados))
        ]

    def to_dict(self) -> dict:
        """
        Convierte la frecuencia a un diccionario para serialización.
        
        Returns:
            dict: Representación en diccionario de la frecuencia
        """
        return {
            'id': self.id_frecuencia,
            'valor': self.valor,
            'valor_formateado': f"{self.valor} kHz",
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'interfaces_compatibles': [
                {'id': i.id_interfaz, 'nombre': i.nombre_comercial}
                for i in self.get_interfaces()
            ]
        }

    @classmethod
    def get_rango_frecuencias(
        cls,
        valor_min: float,
        valor_max: float
    ) -> List['Frecuencia']:
        """
        Obtiene frecuencias dentro de un rango específico.
        
        Args:
            valor_min (float): Valor mínimo del rango
            valor_max (float): Valor máximo del rango
            
        Returns:
            List[Frecuencia]: Lista de frecuencias en el rango
        """
        return cls.select().where(
            (cls.valor >= valor_min) &
            (cls.valor <= valor_max)
        ).order_by(cls.valor)

    def save(self, *args, **kwargs):
        """
        Guarda la frecuencia actualizando el timestamp de modificación.
        
        Raises:
            ValueError: Si el valor no es válido
        """
        if not self.es_valor_valido(self.valor):
            raise ValueError(
                "El valor de frecuencia debe ser positivo y estar en un rango válido (8-192 kHz)"
            )
            
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Representación en string de la frecuencia.
        """
        return f"{self.valor} kHz"

    def __repr__(self) -> str:
        """
        Representación detallada de la frecuencia.
        """
        return f"Frecuencia(id={self.id_frecuencia}, valor={self.valor} kHz)"