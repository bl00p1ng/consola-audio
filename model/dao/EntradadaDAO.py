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
                SELECT Entrada.ID_Entrada, Conectado.ID_Dispositivo, Entrada.Etiqueta, Entrada.Descripcion 
                FROM Entrada
                LEFT JOIN Conectado ON Entrada.ID_Entrada = Conectado.ID_Entrada;
            """
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todasLasEntradas.clear()
            for registro in registros:
                dispositivo = self.dispositivoDAO.getDispositivo(DispositivoVO(pID_Dispo=registro[1])) if registro[1] else None
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
                SELECT Entrada.ID_Entrada, Conectado.ID_Dispositivo, Entrada.Etiqueta, Entrada.Descripcion 
                FROM Entrada
                LEFT JOIN Conectado ON Entrada.ID_Entrada = Conectado.ID_Entrada
                WHERE Entrada.ID_Entrada = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(entradaVO.id),))
            registro = cur.fetchone()

            if registro:
                dispositivo = self.dispositivoDAO.getDispositivo(DispositivoVO(pID_Dispo=registro[1])) if registro[1] else None
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
                cur = conn.cursor()
                
                # Insertar en la tabla Entrada
                sql_entrada = "INSERT INTO Entrada (Etiqueta, Descripcion) VALUES (?, ?);"
                cur.execute(sql_entrada, (entradaVO.etiqueta, entradaVO.descripcion))
                id_entrada = cur.lastrowid

                # Si hay un dispositivo asociado, insertar en la tabla Conectado
                if entradaVO.dispositivo:
                    sql_conectado = "INSERT INTO Conectado (ID_Entrada, ID_Dispositivo) VALUES (?, ?);"
                    cur.execute(sql_conectado, (id_entrada, entradaVO.dispositivo.Id))

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
                cur = conn.cursor()
                
                # Actualizar la tabla Entrada
                sql_entrada = "UPDATE Entrada SET Etiqueta = ?, Descripcion = ? WHERE ID_Entrada = ?;"
                cur.execute(sql_entrada, (entradaVO.etiqueta, entradaVO.descripcion, str(entradaVO.id)))

                # Actualizar o insertar en la tabla Conectado
                if entradaVO.dispositivo:
                    sql_check = "SELECT 1 FROM Conectado WHERE ID_Entrada = ?;"
                    cur.execute(sql_check, (str(entradaVO.id),))
                    if cur.fetchone():
                        sql_conectado = "UPDATE Conectado SET ID_Dispositivo = ? WHERE ID_Entrada = ?;"
                    else:
                        sql_conectado = "INSERT INTO Conectado (ID_Dispositivo, ID_Entrada) VALUES (?, ?);"
                    cur.execute(sql_conectado, (entradaVO.dispositivo.Id, str(entradaVO.id)))
                else:
                    # Si no hay dispositivo, eliminar la relación si existía
                    sql_delete = "DELETE FROM Conectado WHERE ID_Entrada = ?;"
                    cur.execute(sql_delete, (str(entradaVO.id),))

                conn.commit()
                return True
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
                cur = conn.cursor()
                
                # Eliminar de la tabla Conectado primero (si existe)
                sql_delete_conectado = "DELETE FROM Conectado WHERE ID_Entrada = ?;"
                cur.execute(sql_delete_conectado, (str(entradaVO.id),))
                
                # Luego eliminar de la tabla Entrada
                sql_delete_entrada = "DELETE FROM Entrada WHERE ID_Entrada = ?;"
                cur.execute(sql_delete_entrada, (str(entradaVO.id),))
                
                conn.commit()
                return True
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
                SELECT Entrada.ID_Entrada, Conectado.ID_Dispositivo, Entrada.Etiqueta, Entrada.Descripcion 
                FROM Entrada
                JOIN Conectado ON Entrada.ID_Entrada = Conectado.ID_Entrada
                WHERE Conectado.ID_Dispositivo = ?;
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