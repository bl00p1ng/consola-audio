from typing import List, Optional
from datetime import datetime

from peewee import (
    CharField,
    IntegerField,
    DateTimeField,
    DatabaseError
)

# from model.configuracion import Configuracion
# from model.entrada import Entrada
from model.base import BaseModel
# from model.configuracion import Conectado

class Dispositivo(BaseModel):
    """
    Modelo que representa un dispositivo de audio en el sistema.
    
    Un dispositivo puede ser cualquier equipo físico que se conecte a las
    entradas de la interfaz de audio, como micrófonos, instrumentos, etc.
    
    Attributes:
        id_dispositivo (IntegerField): Identificador único del dispositivo
        nombre (CharField): Nombre del dispositivo
        descripcion (CharField): Descripción detallada del dispositivo
        created_at (DateTimeField): Fecha y hora de creación
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    
    id_dispositivo = IntegerField(
        primary_key=True,
        column_name='ID_Dispositivo',
        help_text="Identificador único del dispositivo"
    )
    nombre = CharField(
        max_length=100,
        null=False,
        index=True,
        help_text="Nombre del dispositivo"
    )
    descripcion = CharField(
        max_length=255,
        null=True,
        help_text="Descripción detallada del dispositivo"
    )

    class Meta:
        table_name = 'Dispositivo'
        indexes = (
            (('nombre',), False),  # Índice en nombre para búsquedas
        )

    @classmethod
    def crear_dispositivo(
        cls,
        nombre: str,
        descripcion: Optional[str] = None
    ) -> 'Dispositivo':
        """
        Crea un nuevo dispositivo con los parámetros especificados.
        
        Args:
            nombre (str): Nombre del dispositivo
            descripcion (Optional[str]): Descripción detallada del dispositivo
            
        Returns:
            Dispositivo: Nueva instancia de Dispositivo creada
            
        Raises:
            ValueError: Si el nombre está vacío
            DatabaseError: Si hay un error en la creación del dispositivo
        """
        if not nombre:
            raise ValueError("El nombre del dispositivo no puede estar vacío")
        
        try:
            return cls.create(
                nombre=nombre,
                descripcion=descripcion
            )
        except DatabaseError as e:
            raise DatabaseError(f"Error al crear el dispositivo: {str(e)}")

    def get_entradas_activas(self, configuracion_id: Optional[int] = None):
        """
        Obtiene las entradas a las que está conectado este dispositivo.
        
        Args:
            configuracion_id (Optional[int]): ID de la configuración específica
                                            o None para obtener todas
            
        Returns:
            List[Entrada]: Lista de entradas conectadas al dispositivo
        """
        from model.entrada import Entrada
        from model.configuracion import Conectado
        
        query = (Entrada
                .select()
                .join(Conectado)
                .where(Conectado.dispositivo == self))
        
        if configuracion_id is not None:
            query = query.where(Conectado.configuracion == configuracion_id)
        
        return list(query.distinct())

    def conectar_a_entrada(
        self,
        entrada_id: int,
        configuracion_id: int
    ) -> bool:
        """
        Conecta el dispositivo a una entrada específica en una configuración.
        
        Args:
            entrada_id (int): ID de la entrada a conectar
            configuracion_id (int): ID de la configuración
            
        Returns:
            bool: True si la conexión fue exitosa
            
        Raises:
            DatabaseError: Si hay un error al establecer la conexión
        """
        try:
            from model.entrada import Entrada
            from model.configuracion import Conectado
            entrada = Entrada.get_by_id(entrada_id)
            
            Conectado.create(
                dispositivo=self,
                entrada=entrada,
                configuracion=configuracion_id
            )
            return True
            
        except DatabaseError as e:
            raise DatabaseError(f"Error al conectar dispositivo: {str(e)}")

    def desconectar_de_entrada(
        self,
        entrada_id: int,
        configuracion_id: int
    ) -> bool:
        """
        Desconecta el dispositivo de una entrada específica en una configuración.
        
        Args:
            entrada_id (int): ID de la entrada a desconectar
            configuracion_id (int): ID de la configuración
            
        Returns:
            bool: True si la desconexión fue exitosa
        """
        from model.configuracion import Conectado
        try:
            return bool(Conectado.delete().where(
                (Conectado.dispositivo == self) &
                (Conectado.entrada == entrada_id) &
                (Conectado.configuracion == configuracion_id)
            ).execute())
        except DatabaseError as e:
            raise DatabaseError(f"Error al desconectar dispositivo: {str(e)}")

    def get_configuraciones(self):
        """
        Obtiene todas las configuraciones en las que se usa este dispositivo.
        
        Returns:
            List[Configuracion]: Lista de configuraciones que usan este dispositivo
        """
        from model.configuracion import Configuracion, Conectado
        return (Configuracion
                .select()
                .join(Conectado)
                .where(Conectado.dispositivo == self)
                .distinct())

    def esta_en_uso(self) -> bool:
        """
        Verifica si el dispositivo está siendo utilizado en alguna configuración.
        
        Returns:
            bool: True si el dispositivo está en uso
        """
        from model.configuracion import Conectado
        return (Conectado
                .select()
                .where(Conectado.dispositivo == self)
                .exists())

    def actualizar(
        self,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None
    ) -> bool:
        """
        Actualiza los datos del dispositivo.
        
        Args:
            nombre (Optional[str]): Nuevo nombre del dispositivo
            descripcion (Optional[str]): Nueva descripción del dispositivo
            
        Returns:
            bool: True si la actualización fue exitosa
            
        Raises:
            ValueError: Si el nuevo nombre está vacío
        """
        if nombre is not None:
            if not nombre:
                raise ValueError("El nombre del dispositivo no puede estar vacío")
            self.nombre = nombre
            
        if descripcion is not None:
            self.descripcion = descripcion
            
        self.updated_at = datetime.now()
        self.save()
        return True

    def to_dict(self) -> dict:
        """
        Convierte el dispositivo a un diccionario para serialización.
        
        Returns:
            dict: Representación en diccionario del dispositivo
        """
        return {
            'id': self.id_dispositivo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'entradas_activas': [
                {'id': e.id, 'etiqueta': e.etiqueta}
                for e in self.get_entradas_activas()
            ]
        }

    @classmethod
    def buscar_por_nombre(cls, nombre: str) -> List['Dispositivo']:
        """
        Busca dispositivos por coincidencia parcial de nombre.
        
        Args:
            nombre (str): Texto a buscar en los nombres
            
        Returns:
            List[Dispositivo]: Lista de dispositivos que coinciden con la búsqueda
        """
        return cls.select().where(cls.nombre.contains(nombre))

    def __str__(self) -> str:
        """
        Representación en string del dispositivo.
        """
        return f"Dispositivo(id={self.id_dispositivo}, nombre={self.nombre})"