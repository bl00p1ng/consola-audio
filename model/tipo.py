from typing import List, Optional
from datetime import datetime

from peewee import (
    CharField,
    IntegerField,
    DateTimeField,
    DatabaseError
)

from model.canal import Canal
from model.fuente import Fuente
from model.base import BaseModel
from model.fuente import Clasifica

class Tipo(BaseModel):
    """
    Modelo que representa un tipo de fuente de audio en el sistema.
    
    Los tipos permiten clasificar las fuentes de audio según sus características
    comunes, como pueden ser instrumentos, micrófonos, líneas, etc.
    
    Attributes:
        id_tipo (IntegerField): Identificador único del tipo
        nombre (CharField): Nombre del tipo de fuente
        descripcion (CharField): Descripción detallada del tipo
        created_at (DateTimeField): Fecha y hora de creación
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    
    id_tipo = IntegerField(
        primary_key=True,
        column_name='ID_Tipo',
        help_text="Identificador único del tipo"
    )
    nombre = CharField(
        max_length=100,
        null=False,
        index=True,
        unique=True,
        help_text="Nombre del tipo de fuente"
    )
    descripcion = CharField(
        max_length=255,
        null=True,
        help_text="Descripción detallada del tipo"
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
        table_name = 'Tipo'
        indexes = (
            (('nombre',), True),  # Índice único en nombre
        )

    @classmethod
    def crear_tipo(
        cls,
        nombre: str,
        descripcion: Optional[str] = None
    ) -> 'Tipo':
        """
        Crea un nuevo tipo de fuente con los parámetros especificados.
        
        Args:
            nombre (str): Nombre del tipo de fuente
            descripcion (Optional[str]): Descripción detallada del tipo
            
        Returns:
            Tipo: Nueva instancia de Tipo creada
            
        Raises:
            ValueError: Si el nombre está vacío
            DatabaseError: Si hay un error en la creación
        """
        if not nombre:
            raise ValueError("El nombre del tipo no puede estar vacío")
        
        nombre = nombre.strip()
        if cls.select().where(cls.nombre == nombre).exists():
            raise ValueError(f"Ya existe un tipo con el nombre '{nombre}'")
        
        try:
            return cls.create(
                nombre=nombre,
                descripcion=descripcion
            )
        except DatabaseError as e:
            raise DatabaseError(f"Error al crear el tipo: {str(e)}")

    def get_fuentes(self) -> List['Fuente']:
        """
        Obtiene todas las fuentes clasificadas con este tipo.
        
        Returns:
            List[Fuente]: Lista de fuentes asociadas a este tipo
        """
        from model.fuente import Fuente
        return (Fuente
                .select()
                .join(Clasifica)
                .where(Clasifica.tipo == self))

    def get_canales_asociados(self) -> List['Canal']:
        """
        Obtiene todos los canales que utilizan fuentes de este tipo.
        
        Returns:
            List[Canal]: Lista de canales que usan fuentes de este tipo
        """
        from model.canal import Canal
        from model.fuente import Fuente
        return (Canal
                .select()
                .join(Fuente)
                .join(Clasifica)
                .where(Clasifica.tipo == self)
                .distinct())

    def actualizar(
        self,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None
    ) -> bool:
        """
        Actualiza los datos del tipo.
        
        Args:
            nombre (Optional[str]): Nuevo nombre del tipo
            descripcion (Optional[str]): Nueva descripción del tipo
            
        Returns:
            bool: True si la actualización fue exitosa
            
        Raises:
            ValueError: Si el nuevo nombre está vacío o ya existe
        """
        if nombre is not None:
            nombre = nombre.strip()
            if not nombre:
                raise ValueError("El nombre del tipo no puede estar vacío")
            
            # Verificar si el nuevo nombre ya existe (excepto para este mismo tipo)
            if (Tipo
                .select()
                .where(
                    (Tipo.nombre == nombre) &
                    (Tipo.id_tipo != self.id_tipo)
                )
                .exists()):
                raise ValueError(f"Ya existe un tipo con el nombre '{nombre}'")
            
            self.nombre = nombre
            
        if descripcion is not None:
            self.descripcion = descripcion
            
        self.updated_at = datetime.now()
        self.save()
        return True

    def eliminar_con_validacion(self) -> bool:
        """
        Elimina el tipo verificando que no tenga fuentes asociadas.
        
        Returns:
            bool: True si la eliminación fue exitosa
            
        Raises:
            ValueError: Si el tipo tiene fuentes asociadas
        """
        if self.get_fuentes():
            raise ValueError(
                "No se puede eliminar el tipo porque tiene fuentes asociadas"
            )
        
        return bool(self.delete_instance())

    def to_dict(self) -> dict:
        """
        Convierte el tipo a un diccionario para serialización.
        
        Returns:
            dict: Representación en diccionario del tipo
        """
        return {
            'id': self.id_tipo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'cantidad_fuentes': len(self.get_fuentes()),
            'cantidad_canales': len(self.get_canales_asociados())
        }

    @classmethod
    def buscar_por_nombre(cls, nombre: str) -> List['Tipo']:
        """
        Busca tipos por coincidencia parcial de nombre.
        
        Args:
            nombre (str): Texto a buscar en los nombres
            
        Returns:
            List[Tipo]: Lista de tipos que coinciden con la búsqueda
        """
        return cls.select().where(cls.nombre.contains(nombre))

    @classmethod
    def get_tipos_utilizados(cls) -> List['Tipo']:
        """
        Obtiene todos los tipos que tienen al menos una fuente asociada.
        
        Returns:
            List[Tipo]: Lista de tipos con fuentes asociadas
        """
        return (cls
                .select()
                .join(Clasifica)
                .distinct())

    def __str__(self) -> str:
        """
        Representación en string del tipo.
        """
        return f"Tipo(id={self.id_tipo}, nombre={self.nombre})"

    def __repr__(self) -> str:
        """
        Representación detallada del tipo.
        """
        return (f"Tipo(id={self.id_tipo}, "
                f"nombre={self.nombre}, "
                f"fuentes={len(self.get_fuentes())})")