from datetime import datetime
import re
from typing import List

from peewee import CharField, DateTimeField, ForeignKeyField, DeferredForeignKey
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from model.base import BaseModel

class Usuario(BaseModel):
    """
    Modelo que representa un usuario en el sistema de la consola de audio.
    
    Este modelo implementa las funcionalidades básicas de usuario incluyendo
    autenticación y validación de email, así como la gestión segura de contraseñas
    usando el algoritmo Argon2.
    
    Attributes:
        email (CharField): Email del usuario, único en el sistema
        password (CharField): Contraseña hasheada del usuario
        created_at (DateTimeField): Fecha y hora de creación del usuario
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    
    email = CharField(
        unique=True,
        index=True,
        max_length=255,
        help_text="Email del usuario"
    )
    password = CharField(
        max_length=255,
        help_text="Contraseña hasheada del usuario"
    )
    created_at = DateTimeField(
        default=datetime.now,
        help_text="Fecha y hora de creación del usuario"
    )
    updated_at = DateTimeField(
        default=datetime.now,
        help_text="Fecha y hora de última actualización"
    )
    
    # Configuración de la tabla
    class Meta:
        table_name = 'Usuario'
        indexes = (
            (('email',), True),  # Índice único en email
        )
    
    @classmethod
    def create_user(cls, email: str, password: str) -> 'Usuario':
        """
        Crea un nuevo usuario con el email y contraseña proporcionados.
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña sin procesar
            
        Returns:
            Usuario: Nueva instancia de Usuario creada
            
        Raises:
            ValueError: Si el email no es válido o la contraseña es muy débil
            peewee.IntegrityError: Si el email ya existe
        """
        if not cls.is_valid_email(email):
            raise ValueError("Email inválido")
        
        if not cls.is_valid_password(password):
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres, "
                "incluir mayúsculas, minúsculas y números"
            )
        
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        
        return cls.create(
            email=email.lower(),
            password=hashed_password
        )
    
    def verify_password(self, password: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con la almacenada.
        
        Args:
            password (str): Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta, False en caso contrario
        """
        ph = PasswordHasher()
        try:
            ph.verify(self.password, password)
            return True
        except VerifyMismatchError:
            return False
    
    def update_password(self, new_password: str) -> bool:
        """
        Actualiza la contraseña del usuario.
        
        Args:
            new_password (str): Nueva contraseña
            
        Returns:
            bool: True si la actualización fue exitosa
            
        Raises:
            ValueError: Si la nueva contraseña es muy débil
        """
        if not self.is_valid_password(new_password):
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres, "
                "incluir mayúsculas, minúsculas y números"
            )
        
        ph = PasswordHasher()
        self.password = ph.hash(new_password)
        self.updated_at = datetime.now()
        self.save()
        return True
    
    def get_configuraciones(self) -> List['Configuracion']:
        """
        Obtiene todas las configuraciones asociadas al usuario.
        
        Returns:
            List[Configuracion]: Lista de configuraciones del usuario
        """
        from model.configuracion import Configuracion
        from model.usuario import Personaliza

        return (Configuracion
                .select()
                .join(Personaliza)
                .where(Personaliza.usuario == self))
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Valida si el email tiene un formato correcto.
        
        Args:
            email (str): Email a validar
            
        Returns:
            bool: True si el email es válido, False en caso contrario
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Valida si la contraseña cumple con los requisitos mínimos de seguridad.
        
        Args:
            password (str): Contraseña a validar
            
        Returns:
            bool: True si la contraseña es válida, False en caso contrario
        """
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True
    
    def save(self, *args, **kwargs):
        """
        Guarda el usuario actualizando el timestamp de modificación.
        """
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        """
        Representación en string del usuario.
        """
        return f"Usuario(email={self.email})"

# Definición de la tabla de relación Personaliza
class Personaliza(BaseModel):
    """
    Modelo que representa la relación entre Usuario, Configuracion e InterfazAudio.
    """
    
    usuario = ForeignKeyField(
        Usuario, 
        backref='personalizaciones',
        column_name='ID_Usuario',
        on_delete='CASCADE'
    )
    configuracion = DeferredForeignKey(
        'Configuracion',
        backref='personalizaciones',
        column_name='ID_Configuracion',
        on_delete='CASCADE'
    )
    interfaz = DeferredForeignKey(
        'InterfazAudio',
        backref='personalizaciones',
        column_name='ID_Interfaz',
        on_delete='CASCADE'
    )
    
    class Meta:
        table_name = 'Personaliza'
        indexes = (
            (('usuario', 'configuracion', 'interfaz'), True),
        )