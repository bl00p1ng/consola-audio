from typing import List, Optional
from db import conexion as cbd
from model.vo.DispositivoVO import DispositivoVO

class DispositivoDAO:
    def __init__(self):
        self.resultadoUnDispositivo: Optional[DispositivoVO] = None
        self.resultadoVariosDispositivos: List[DispositivoVO] = []
        self.todosLosDispositivos: List[DispositivoVO] = []

    def getAll(self) -> List[DispositivoVO]:
        """
        Obtiene todos los dispositivos de la base de datos.
        
        Returns:
            List[DispositivoVO]: Lista con todos los dispositivos disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT * FROM Dispositivo;"
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todosLosDispositivos.clear()
            for registro in registros:
                self.todosLosDispositivos.append(
                    DispositivoVO(
                        pID_Dispo=registro[0],
                        pNombre=registro[1],
                        pDescripcion=registro[2]
                    )
                )
        return self.todosLosDispositivos

    def getDispositivo(self, dispositivoVO: DispositivoVO) -> Optional[DispositivoVO]:
        """
        Obtiene un dispositivo específico de la base de datos.
        
        Args:
            dispositivoVO (DispositivoVO): Value Object del dispositivo a buscar.
        
        Returns:
            Optional[DispositivoVO]: El dispositivo encontrado o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT * FROM Dispositivo WHERE ID_Dispositivo = ?;"
            cur = conn.cursor()
            cur.execute(sql, (str(dispositivoVO.Id),))
            registro = cur.fetchone()

            if registro:
                self.resultadoUnDispositivo = DispositivoVO(
                    pID_Dispo=registro[0],
                    pNombre=registro[1],
                    pDescripcion=registro[2]
                )
            else:
                self.resultadoUnDispositivo = None

        return self.resultadoUnDispositivo

    def insertDispositivo(self, dispositivoVO: DispositivoVO) -> bool:
        """
        Inserta un nuevo dispositivo en la base de datos.
        
        Args:
            dispositivoVO (DispositivoVO): Value Object del dispositivo a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "INSERT INTO Dispositivo (Nombre, Descripcion) VALUES (?, ?);"
                cur = conn.cursor()
                cur.execute(sql, (dispositivoVO.Nombre, dispositivoVO.Descripcion))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar dispositivo: {e}")
            return False

    def updateDispositivo(self, dispositivoVO: DispositivoVO) -> bool:
        """
        Actualiza un dispositivo existente en la base de datos.
        
        Args:
            dispositivoVO (DispositivoVO): Value Object del dispositivo a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "UPDATE Dispositivo SET Nombre = ?, Descripcion = ? WHERE ID_Dispositivo = ?;"
                cur = conn.cursor()
                cur.execute(sql, (dispositivoVO.Nombre, dispositivoVO.Descripcion, str(dispositivoVO.Id)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar dispositivo: {e}")
            return False

    def deleteDispositivo(self, dispositivoVO: DispositivoVO) -> bool:
        """
        Elimina un dispositivo de la base de datos.
        
        Args:
            dispositivoVO (DispositivoVO): Value Object del dispositivo a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "DELETE FROM Dispositivo WHERE ID_Dispositivo = ?;"
                cur = conn.cursor()
                cur.execute(sql, (str(dispositivoVO.Id),))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar dispositivo: {e}")
            return False