from typing import List, Optional
from db import conexion as cbd

class TipoVO:
    def __init__(self, pId: int = -1, pNombre: str = "", pDescripcion: str = ""):
        self.__id = pId
        self.__nombre = pNombre
        self.__descripcion = pDescripcion

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def descripcion(self):
        return self.__descripcion

    def setNombre(self, pNombre: str):
        self.__nombre = pNombre

    def setDescripcion(self, pDescripcion: str):
        self.__descripcion = pDescripcion

    def __str__(self) -> str:
        return f'ID: {self.__id}, Nombre: {self.__nombre}, Descripción: {self.__descripcion}'

class TipoDAO:
    def __init__(self):
        self.resultadoUnTipo: Optional[TipoVO] = None
        self.resultadoVariosTipos: List[TipoVO] = []
        self.todosLosTipos: List[TipoVO] = []

    def getAll(self) -> List[TipoVO]:
        """
        Obtiene todos los tipos de la base de datos.
        
        Returns:
            List[TipoVO]: Lista con todos los tipos disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Tipo, Nombre, Descripcion FROM Tipo;"
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todosLosTipos.clear()
            for registro in registros:
                self.todosLosTipos.append(
                    TipoVO(
                        pId=registro[0],
                        pNombre=registro[1],
                        pDescripcion=registro[2]
                    )
                )
        return self.todosLosTipos

    def getTipo(self, tipoVO: TipoVO) -> Optional[TipoVO]:
        """
        Obtiene un tipo específico de la base de datos.
        
        Args:
            tipoVO (TipoVO): Value Object del tipo a buscar.
        
        Returns:
            Optional[TipoVO]: El tipo encontrado o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Tipo, Nombre, Descripcion FROM Tipo WHERE ID_Tipo = ?;"
            cur = conn.cursor()
            cur.execute(sql, (str(tipoVO.id),))
            registro = cur.fetchone()

            if registro:
                self.resultadoUnTipo = TipoVO(
                    pId=registro[0],
                    pNombre=registro[1],
                    pDescripcion=registro[2]
                )
            else:
                self.resultadoUnTipo = None

        return self.resultadoUnTipo

    def insertTipo(self, tipoVO: TipoVO) -> bool:
        """
        Inserta un nuevo tipo en la base de datos.
        
        Args:
            tipoVO (TipoVO): Value Object del tipo a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "INSERT INTO Tipo (Nombre, Descripcion) VALUES (?, ?);"
                cur = conn.cursor()
                cur.execute(sql, (tipoVO.nombre, tipoVO.descripcion))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar tipo: {e}")
            return False

    def updateTipo(self, tipoVO: TipoVO) -> bool:
        """
        Actualiza un tipo existente en la base de datos.
        
        Args:
            tipoVO (TipoVO): Value Object del tipo a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "UPDATE Tipo SET Nombre = ?, Descripcion = ? WHERE ID_Tipo = ?;"
                cur = conn.cursor()
                cur.execute(sql, (tipoVO.nombre, tipoVO.descripcion, str(tipoVO.id)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar tipo: {e}")
            return False

    def deleteTipo(self, tipoVO: TipoVO) -> bool:
        """
        Elimina un tipo de la base de datos.
        
        Args:
            tipoVO (TipoVO): Value Object del tipo a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "DELETE FROM Tipo WHERE ID_Tipo = ?;"
                cur = conn.cursor()
                cur.execute(sql, (str(tipoVO.id),))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar tipo: {e}")
            return False

    def getTipoPorNombre(self, nombre: str) -> Optional[TipoVO]:
        """
        Busca un tipo por su nombre en la base de datos.
        
        Args:
            nombre (str): Nombre del tipo a buscar.
        
        Returns:
            Optional[TipoVO]: El tipo encontrado o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Tipo, Nombre, Descripcion FROM Tipo WHERE Nombre = ?;"
            cur = conn.cursor()
            cur.execute(sql, (nombre,))
            registro = cur.fetchone()

            if registro:
                return TipoVO(
                    pId=registro[0],
                    pNombre=registro[1],
                    pDescripcion=registro[2]
                )
            else:
                return None