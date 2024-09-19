# UsuarioDAO.py

from typing import List, Optional
from db import conexion as cbd
from model.vo.UsuarioVO import UsuarioVO

class UsuarioDAO:
    def __init__(self):
        self.resultadoUnUsuario: Optional[UsuarioVO] = None
        self.resultadoVariosUsuarios: List[UsuarioVO] = []
        self.todosLosUsuarios: List[UsuarioVO] = []

    def getAll(self, limit: int = 100) -> List[UsuarioVO]:
        """
        Obtiene todos los usuarios de la base de datos.
        
        Args:
            limit (int): Número máximo de usuarios a recuperar.
        
        Returns:
            List[UsuarioVO]: Lista con todos los usuarios disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Usuario, Email FROM Usuario LIMIT ?;"
            cur = conn.cursor()
            cur.execute(sql, (limit,))
            registros = cur.fetchall()

            self.todosLosUsuarios.clear()
            for registro in registros:
                self.todosLosUsuarios.append(
                    UsuarioVO(
                        uId=registro[0],
                        email=registro[1]
                    )
                )
        return self.todosLosUsuarios

    def getUsuario(self, usuarioVO: UsuarioVO) -> Optional[UsuarioVO]:
        """
        Obtiene un usuario específico de la base de datos.
        
        Args:
            usuarioVO (UsuarioVO): Value Object del usuario a buscar.
        
        Returns:
            Optional[UsuarioVO]: El usuario encontrado o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Usuario, Email FROM Usuario WHERE ID_Usuario = ?;"
            cur = conn.cursor()
            cur.execute(sql, (str(usuarioVO.getId()),))
            registro = cur.fetchone()

            if registro:
                self.resultadoUnUsuario = UsuarioVO(
                    uId=registro[0],
                    email=registro[1]
                )
            else:
                self.resultadoUnUsuario = None

        return self.resultadoUnUsuario

    def insertUsuario(self, usuarioVO: UsuarioVO) -> bool:
        """
        Inserta un nuevo usuario en la base de datos.
        
        Args:
            usuarioVO (UsuarioVO): Value Object del usuario a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "INSERT INTO Usuario (Email, Password) VALUES (?, ?);"
                cur = conn.cursor()
                cur.execute(sql, (usuarioVO.getEmail(), usuarioVO.getPassword()))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            return False

    def updateUsuario(self, usuarioVO: UsuarioVO) -> bool:
        """
        Actualiza un usuario existente en la base de datos.
        
        Args:
            usuarioVO (UsuarioVO): Value Object del usuario a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "UPDATE Usuario SET Email = ?, Password = ? WHERE ID_Usuario = ?;"
                cur = conn.cursor()
                cur.execute(sql, (usuarioVO.getEmail(), usuarioVO.getPassword(), str(usuarioVO.getId())))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False

    def deleteUsuario(self, usuarioVO: UsuarioVO) -> bool:
        """
        Elimina un usuario de la base de datos.
        
        Args:
            usuarioVO (UsuarioVO): Value Object del usuario a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "DELETE FROM Usuario WHERE ID_Usuario = ?;"
                cur = conn.cursor()
                cur.execute(sql, (str(usuarioVO.getId()),))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False

    def getUsuarioPorEmail(self, email: str) -> Optional[UsuarioVO]:
        """
        Busca un usuario por su email en la base de datos.
        
        Args:
            email (str): Email del usuario a buscar.
        
        Returns:
            Optional[UsuarioVO]: El usuario encontrado o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Usuario, Email FROM Usuario WHERE Email = ?;"
            cur = conn.cursor()
            cur.execute(sql, (email,))
            registro = cur.fetchone()

            if registro:
                return UsuarioVO(
                    uId=registro[0],
                    email=registro[1]
                )
            else:
                return None

    def autenticarUsuario(self, email: str, password: str) -> Optional[UsuarioVO]:
        """
        Autentica un usuario por su email y contraseña.
        
        Args:
            email (str): Email del usuario.
            password (str): Contraseña del usuario.
        
        Returns:
            Optional[UsuarioVO]: El usuario autenticado o None si la autenticación falla.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Usuario, Email FROM Usuario WHERE Email = ? AND Password = ?;"
            cur = conn.cursor()
            cur.execute(sql, (email, password))
            registro = cur.fetchone()

            if registro:
                return UsuarioVO(
                    uId=registro[0],
                    email=registro[1]
                )
            else:
                return None