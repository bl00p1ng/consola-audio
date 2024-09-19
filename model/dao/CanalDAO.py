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
                SELECT c.Codigo_Canal, c.Etiqueta, c.ID_Fuente 
                FROM Canal c
                LEFT JOIN Fuente f ON c.ID_Fuente = f.ID_Fuente;
            """
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todosLosCanales.clear()
            for registro in registros:
                fuente = self.fuenteDAO.getFuente(registro[2]) if registro[2] else None
                self.todosLosCanales.append(
                    CanalVO(
                        pId=registro[0],
                        pEtiqueta=registro[1],
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
                SELECT Codigo_Canal, Etiqueta, ID_Fuente 
                FROM Canal
                WHERE Codigo_Canal = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(canalVO.id),))
            registro = cur.fetchone()

            if registro:
                fuente = self.fuenteDAO.getFuente(registro[2]) if registro[2] else None
                self.resultadoUnCanal = CanalVO(
                    pId=registro[0],
                    pEtiqueta=registro[1],
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
                    INSERT INTO Canal (Etiqueta, ID_Fuente)
                    VALUES (?, ?);
                """
                cur = conn.cursor()
                cur.execute(sql, (
                    canalVO.getEtiqueta(),
                    canalVO.getFuente().getId() if canalVO.getFuente() else None
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
                    SET Etiqueta = ?, ID_Fuente = ?
                    WHERE Codigo_Canal = ?;
                """
                cur = conn.cursor()
                cur.execute(sql, (
                    canalVO.getEtiqueta(),
                    canalVO.getFuente().getId() if canalVO.getFuente() else None,
                    str(canalVO.getId())
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
                cur.execute(sql, (str(canalVO.getId()),))
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
                SELECT c.Codigo_Canal, c.Etiqueta, c.ID_Fuente 
                FROM Canal c
                WHERE c.Etiqueta = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (etiqueta,))
            registro = cur.fetchone()

            if registro:
                fuente = self.fuenteDAO.getFuente(registro[2]) if registro[2] else None
                return CanalVO(
                    pId=registro[0],
                    pEtiqueta=registro[1],
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
                SELECT c.Codigo_Canal, c.Etiqueta, c.ID_Fuente 
                FROM Canal c
                WHERE c.ID_Fuente = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(fuenteId),))
            registros = cur.fetchall()

            canales = []
            for registro in registros:
                fuente = self.fuenteDAO.getFuente(registro[2])
                canales.append(
                    CanalVO(
                        pId=registro[0],
                        pEtiqueta=registro[1],
                        pFuente=fuente
                    )
                )
            return canales

    def getParametrosCanal(self, canalId: int, configuracionId: int) -> dict:
        """
        Obtiene los parámetros de un canal para una configuración específica.
        
        Args:
            canalId (int): ID del canal.
            configuracionId (int): ID de la configuración.
        
        Returns:
            dict: Diccionario con los parámetros del canal (Volumen, Solo, Mute, Link).
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT Volumen, Solo, Mute, Link
                FROM Establece
                WHERE Codigo_Canal = ? AND ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(canalId), str(configuracionId)))
            registro = cur.fetchone()

            if registro:
                return {
                    'Volumen': registro[0],
                    'Solo': bool(registro[1]),
                    'Mute': bool(registro[2]),
                    'Link': bool(registro[3])
                }
            else:
                return {}

    def actualizarParametrosCanal(self, canalId: int, configuracionId: int, parametros: dict) -> bool:
        """
        Actualiza los parámetros de un canal para una configuración específica.
        
        Args:
            canalId (int): ID del canal.
            configuracionId (int): ID de la configuración.
            parametros (dict): Diccionario con los parámetros a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = """
                    INSERT INTO Establece (Codigo_Canal, ID_Configuracion, Volumen, Solo, Mute, Link)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(Codigo_Canal, ID_Configuracion) DO UPDATE SET
                    Volumen = ?, Solo = ?, Mute = ?, Link = ?;
                """
                cur = conn.cursor()
                cur.execute(sql, (
                    str(canalId),
                    str(configuracionId),
                    parametros.get('Volumen', 0),
                    int(parametros.get('Solo', False)),
                    int(parametros.get('Mute', False)),
                    int(parametros.get('Link', False)),
                    parametros.get('Volumen', 0),
                    int(parametros.get('Solo', False)),
                    int(parametros.get('Mute', False)),
                    int(parametros.get('Link', False))
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar parámetros del canal: {e}")
            return False
