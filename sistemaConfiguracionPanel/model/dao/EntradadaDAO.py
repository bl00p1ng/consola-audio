from typing import List, Optional
from db import conexion as cbd
from model.vo.EntradaVO import EntradaVO
from model.vo.DispositivoVO import DispositivoVO
from model.dao.DispositivoDAO import DispositivoDAO

class EntradaDAO:
    def __init__(self):
        self.resultadoUnaEntrada: Optional[EntradaVO] = None
        self.resultadoVariasEntradas: List[EntradaVO] = []
        self.todasLasEntradas: List[EntradaVO] = []
        self.dispositivoDAO = DispositivoDAO()

    def getAll(self) -> List[EntradaVO]:
        """
        Obtiene todas las entradas de la base de datos.
        
        Returns:
            List[EntradaVO]: Lista con todas las entradas disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT e.ID_Entrada, e.ID_Dispositivo, e.Etiqueta, e.Descripcion 
                FROM Entrada e
                JOIN Dispositivo d ON e.ID_Dispositivo = d.ID_Dispositivo;
            """
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todasLasEntradas.clear()
            for registro in registros:
                dispositivo = self.dispositivoDAO.getDispositivo(DispositivoVO(pID_Dispo=registro[1]))
                self.todasLasEntradas.append(
                    EntradaVO(
                        pId=registro[0],
                        pDispositivo=dispositivo,
                        pEtiqueta=registro[2],
                        pDescripcion=registro[3]
                    )
                )
        return self.todasLasEntradas

    def getEntrada(self, entradaVO: EntradaVO) -> Optional[EntradaVO]:
        """
        Obtiene una entrada específica de la base de datos.
        
        Args:
            entradaVO (EntradaVO): Value Object de la entrada a buscar.
        
        Returns:
            Optional[EntradaVO]: La entrada encontrada o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT e.ID_Entrada, e.ID_Dispositivo, e.Etiqueta, e.Descripcion 
                FROM Entrada e
                JOIN Dispositivo d ON e.ID_Dispositivo = d.ID_Dispositivo
                WHERE e.ID_Entrada = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(entradaVO.id),))
            registro = cur.fetchone()

            if registro:
                dispositivo = self.dispositivoDAO.getDispositivo(DispositivoVO(pID_Dispo=registro[1]))
                self.resultadoUnaEntrada = EntradaVO(
                    pId=registro[0],
                    pDispositivo=dispositivo,
                    pEtiqueta=registro[2],
                    pDescripcion=registro[3]
                )
            else:
                self.resultadoUnaEntrada = None

        return self.resultadoUnaEntrada

    def insertEntrada(self, entradaVO: EntradaVO) -> bool:
        """
        Inserta una nueva entrada en la base de datos.
        
        Args:
            entradaVO (EntradaVO): Value Object de la entrada a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "INSERT INTO Entrada (ID_Dispositivo, Etiqueta, Descripcion) VALUES (?, ?, ?);"
                cur = conn.cursor()
                cur.execute(sql, (entradaVO.dispositivo.Id, entradaVO.etiqueta, entradaVO.descripcion))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar entrada: {e}")
            return False

    def updateEntrada(self, entradaVO: EntradaVO) -> bool:
        """
        Actualiza una entrada existente en la base de datos.
        
        Args:
            entradaVO (EntradaVO): Value Object de la entrada a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "UPDATE Entrada SET ID_Dispositivo = ?, Etiqueta = ?, Descripcion = ? WHERE ID_Entrada = ?;"
                cur = conn.cursor()
                cur.execute(sql, (entradaVO.dispositivo.Id, entradaVO.etiqueta, entradaVO.descripcion, str(entradaVO.id)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar entrada: {e}")
            return False

    def deleteEntrada(self, entradaVO: EntradaVO) -> bool:
        """
        Elimina una entrada de la base de datos.
        
        Args:
            entradaVO (EntradaVO): Value Object de la entrada a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "DELETE FROM Entrada WHERE ID_Entrada = ?;"
                cur = conn.cursor()
                cur.execute(sql, (str(entradaVO.id),))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar entrada: {e}")
            return False

    def getEntradasPorDispositivo(self, dispositivoVO: DispositivoVO) -> List[EntradaVO]:
        """
        Obtiene todas las entradas asociadas a un dispositivo específico.
        
        Args:
            dispositivoVO (DispositivoVO): Value Object del dispositivo.
        
        Returns:
            List[EntradaVO]: Lista de entradas asociadas al dispositivo.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT e.ID_Entrada, e.ID_Dispositivo, e.Etiqueta, e.Descripcion 
                FROM Entrada e
                WHERE e.ID_Dispositivo = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(dispositivoVO.Id),))
            registros = cur.fetchall()

            entradas = []
            for registro in registros:
                entradas.append(
                    EntradaVO(
                        pId=registro[0],
                        pDispositivo=dispositivoVO,
                        pEtiqueta=registro[2],
                        pDescripcion=registro[3]
                    )
                )
        return entradas