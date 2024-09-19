from typing import List, Optional
from db import conexion as cbd
from model.vo.canalVO import CanalVO
from model.dao.FuenteDAO import FuenteDAO

class CanalDAO:
    def __init__(self):
        self.resultadoUnCanal: Optional[CanalVO] = None
        self.resultadoVariosCanales: List[CanalVO] = []
        self.todosLosCanales: List[CanalVO] = []
        self.fuenteDAO = FuenteDAO()

    def getAll(self) -> List[CanalVO]:
        """
        Obtiene todos los canales de la base de datos.
        
        Returns:
            List[CanalVO]: Lista con todos los canales disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT c.Codigo_Canal, c.Etiqueta, c.Volumen, c.Link, c.Mute, c.Solo, c.ID_Fuente 
                FROM Canal c
                LEFT JOIN Fuente f ON c.ID_Fuente = f.ID_Fuente;
            """
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todosLosCanales.clear()
            for registro in registros:
                fuente = self.fuenteDAO.getFuente(registro[6]) if registro[6] else None
                self.todosLosCanales.append(
                    CanalVO(
                        pId=registro[0],
                        pEtiqueta=registro[1],
                        pVolumen=registro[2],
                        pLink=bool(registro[3]),
                        pMute=bool(registro[4]),
                        pSolo=bool(registro[5]),
                        pFuente=fuente
                    )
                )
        return self.todosLosCanales

    def getCanal(self, canalVO: CanalVO) -> Optional[CanalVO]:
        """
        Obtiene un canal específico de la base de datos.
        
        Args:
            canalVO (CanalVO): Value Object del canal a buscar.
        
        Returns:
            Optional[CanalVO]: El canal encontrado o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT c.Codigo_Canal, c.Etiqueta, c.Volumen, c.Link, c.Mute, c.Solo, c.ID_Fuente 
                FROM Canal c
                LEFT JOIN Fuente f ON c.ID_Fuente = f.ID_Fuente
                WHERE c.Codigo_Canal = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(canalVO.id),))
            registro = cur.fetchone()

            if registro:
                fuente = self.fuenteDAO.getFuente(registro[6]) if registro[6] else None
                self.resultadoUnCanal = CanalVO(
                    pId=registro[0],
                    pEtiqueta=registro[1],
                    pVolumen=registro[2],
                    pLink=bool(registro[3]),
                    pMute=bool(registro[4]),
                    pSolo=bool(registro[5]),
                    pFuente=fuente
                )
            else:
                self.resultadoUnCanal = None

        return self.resultadoUnCanal

    def insertCanal(self, canalVO: CanalVO) -> bool:
        """
        Inserta un nuevo canal en la base de datos.
        
        Args:
            canalVO (CanalVO): Value Object del canal a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = """
                    INSERT INTO Canal (Etiqueta, Volumen, Link, Mute, Solo, ID_Fuente)
                    VALUES (?, ?, ?, ?, ?, ?);
                """
                cur = conn.cursor()
                cur.execute(sql, (
                    canalVO.etiqueta,
                    canalVO.volumen,
                    int(canalVO.link),
                    int(canalVO.mute),
                    int(canalVO.solo),
                    canalVO.fuente.id if canalVO.fuente else None
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar canal: {e}")
            return False

    def updateCanal(self, canalVO: CanalVO) -> bool:
        """
        Actualiza un canal existente en la base de datos.
        
        Args:
            canalVO (CanalVO): Value Object del canal a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = """
                    UPDATE Canal
                    SET Etiqueta = ?, Volumen = ?, Link = ?, Mute = ?, Solo = ?, ID_Fuente = ?
                    WHERE Codigo_Canal = ?;
                """
                cur = conn.cursor()
                cur.execute(sql, (
                    canalVO.etiqueta,
                    canalVO.volumen,
                    int(canalVO.link),
                    int(canalVO.mute),
                    int(canalVO.solo),
                    canalVO.fuente.id if canalVO.fuente else None,
                    str(canalVO.id)
                ))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar canal: {e}")
            return False

    def deleteCanal(self, canalVO: CanalVO) -> bool:
        """
        Elimina un canal de la base de datos.
        
        Args:
            canalVO (CanalVO): Value Object del canal a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "DELETE FROM Canal WHERE Codigo_Canal = ?;"
                cur = conn.cursor()
                cur.execute(sql, (str(canalVO.id),))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar canal: {e}")
            return False

    def getCanalPorEtiqueta(self, etiqueta: str) -> Optional[CanalVO]:
        """
        Busca un canal por su etiqueta en la base de datos.
        
        Args:
            etiqueta (str): Etiqueta del canal a buscar.
        
        Returns:
            Optional[CanalVO]: El canal encontrado o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT c.Codigo_Canal, c.Etiqueta, c.Volumen, c.Link, c.Mute, c.Solo, c.ID_Fuente 
                FROM Canal c
                LEFT JOIN Fuente f ON c.ID_Fuente = f.ID_Fuente
                WHERE c.Etiqueta = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (etiqueta,))
            registro = cur.fetchone()

            if registro:
                fuente = self.fuenteDAO.getFuente(registro[6]) if registro[6] else None
                return CanalVO(
                    pId=registro[0],
                    pEtiqueta=registro[1],
                    pVolumen=registro[2],
                    pLink=bool(registro[3]),
                    pMute=bool(registro[4]),
                    pSolo=bool(registro[5]),
                    pFuente=fuente
                )
            else:
                return None

    def getCanalesPorFuente(self, fuenteId: int) -> List[CanalVO]:
        """
        Obtiene todos los canales asociados a una fuente específica.
        
        Args:
            fuenteId (int): ID de la fuente.
        
        Returns:
            List[CanalVO]: Lista de canales asociados a la fuente.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT c.Codigo_Canal, c.Etiqueta, c.Volumen, c.Link, c.Mute, c.Solo, c.ID_Fuente 
                FROM Canal c
                WHERE c.ID_Fuente = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(fuenteId),))
            registros = cur.fetchall()

            canales = []
            for registro in registros:
                fuente = self.fuenteDAO.getFuente(registro[6])
                canales.append(
                    CanalVO(
                        pId=registro[0],
                        pEtiqueta=registro[1],
                        pVolumen=registro[2],
                        pLink=bool(registro[3]),
                        pMute=bool(registro[4]),
                        pSolo=bool(registro[5]),
                        pFuente=fuente
                    )
                )
            return canales

    def ajustarVolumen(self, canalId: int, nuevoVolumen: float) -> bool:
        """
        Ajusta el volumen de un canal específico.
        
        Args:
            canalId (int): ID del canal a ajustar.
            nuevoVolumen (float): Nuevo valor de volumen.
        
        Returns:
            bool: True si el ajuste fue exitoso, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "UPDATE Canal SET Volumen = ? WHERE Codigo_Canal = ?;"
                cur = conn.cursor()
                cur.execute(sql, (nuevoVolumen, str(canalId)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al ajustar volumen del canal: {e}")
            return False

    def toggleMute(self, canalId: int) -> bool:
        """
        Activa o desactiva el mute de un canal específico.
        
        Args:
            canalId (int): ID del canal a modificar.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                # Primero, obtenemos el estado actual de mute
                cur = conn.cursor()
                cur.execute("SELECT Mute FROM Canal WHERE Codigo_Canal = ?;", (str(canalId),))
                resultado = cur.fetchone()
                if resultado is None:
                    return False
                
                estado_actual = bool(resultado[0])
                nuevo_estado = not estado_actual

                # Luego, actualizamos al nuevo estado
                sql = "UPDATE Canal SET Mute = ? WHERE Codigo_Canal = ?;"
                cur.execute(sql, (int(nuevo_estado), str(canalId)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al cambiar el estado de mute del canal: {e}")
            return False

    def toggleSolo(self, canalId: int) -> bool:
        """
        Activa o desactiva el solo de un canal específico.
        
        Args:
            canalId (int): ID del canal a modificar.
        
        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                # Primero, obtenemos el estado actual de solo
                cur = conn.cursor()
                cur.execute("SELECT Solo FROM Canal WHERE Codigo_Canal = ?;", (str(canalId),))
                resultado = cur.fetchone()
                if resultado is None:
                    return False
                
                estado_actual = bool(resultado[0])
                nuevo_estado = not estado_actual

                # Luego, actualizamos al nuevo estado
                sql = "UPDATE Canal SET Solo = ? WHERE Codigo_Canal = ?;"
                cur.execute(sql, (int(nuevo_estado), str(canalId)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al cambiar el estado de solo del canal: {e}")
            return False