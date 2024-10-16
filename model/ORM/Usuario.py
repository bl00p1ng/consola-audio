from peewee import SqliteDatabase, Model, AutoField, CharField
from typing import List, Optional
import bcrypt

db = SqliteDatabase('db/Base_De_Datos.db')

class Usuario(Model):
    id = AutoField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

class UsuarioDAO:
    @staticmethod
    def get_all(limit: int = 100) -> List[Usuario]:
        """
        Obtiene todos los usuarios de la base de datos.
        
        Args:
            limit (int): Número máximo de usuarios a recuperar.
        
        Returns:
            List[Usuario]: Lista con todos los usuarios disponibles.
        """
        return list(Usuario.select().limit(limit))

    @staticmethod
    def get_usuario(usuario_id: int) -> Optional[Usuario]:
        """
        Obtiene un usuario específico de la base de datos.
        
        Args:
            usuario_id (int): ID del usuario a buscar.
        
        Returns:
            Optional[Usuario]: El usuario encontrado o None si no existe.
        """
        try:
            return Usuario.get_by_id(usuario_id)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def insert_usuario(usuario: Usuario) -> bool:
        """
        Inserta un nuevo usuario en la base de datos.
        
        Args:
            usuario (Usuario): Instancia del usuario a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            usuario.password = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt())
            usuario.save()
            return True
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            return False

    @staticmethod
    def update_usuario(usuario: Usuario) -> bool:
        """
        Actualiza un usuario existente en la base de datos.
        
        Args:
            usuario (Usuario): Instancia del usuario a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            if not usuario.password.startswith('$2b$'):  # Verificar si la contraseña ya está hasheada
                usuario.password = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt())
            usuario.save()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False

    @staticmethod
    def delete_usuario(usuario: Usuario) -> bool:
        """
        Elimina un usuario de la base de datos.
        
        Args:
            usuario (Usuario): Instancia del usuario a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            usuario.delete_instance()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False

    @staticmethod
    def get_usuario_por_email(email: str) -> Optional[Usuario]:
        """
        Busca un usuario por su email en la base de datos.
        
        Args:
            email (str): Email del usuario a buscar.
        
        Returns:
            Optional[Usuario]: El usuario encontrado o None si no existe.
        """
        try:
            return Usuario.get(Usuario.email == email)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def autenticar_usuario(email: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario por su email y contraseña.
        
        Args:
            email (str): Email del usuario.
            password (str): Contraseña del usuario.
        
        Returns:
            Optional[Usuario]: El usuario autenticado o None si la autenticación falla.
        """
        try:
            usuario = Usuario.get(Usuario.email == email)
            if bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
                return usuario
            return None
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def buscar_usuarios(criterio: str) -> List[Usuario]:
        """
        Busca usuarios que coincidan con un criterio en el email.
        
        Args:
            criterio (str): Criterio de búsqueda.
        
        Returns:
            List[Usuario]: Lista de usuarios que coinciden con el criterio.
        """
        return list(Usuario.select().where(Usuario.email.contains(criterio)))

    @staticmethod
    def get_usuarios_por_pagina(pagina: int, elementos_por_pagina: int) -> List[Usuario]:
        """
        Obtiene una página de usuarios para implementar paginación.
        
        Args:
            pagina (int): Número de página (comenzando desde 1).
            elementos_por_pagina (int): Cantidad de elementos por página.
        
        Returns:
            List[Usuario]: Lista de usuarios para la página especificada.
        """
        return list(Usuario.select().order_by(Usuario.email).paginate(pagina, elementos_por_pagina))

    @staticmethod
    def cambiar_password(usuario: Usuario, nueva_password: str) -> bool:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            usuario (Usuario): Instancia del usuario.
            nueva_password (str): Nueva contraseña.
        
        Returns:
            bool: True si el cambio fue exitoso, False en caso contrario.
        """
        try:
            usuario.password = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
            usuario.save()
            return True
        except Exception as e:
            print(f"Error al cambiar la contraseña: {e}")
            return False