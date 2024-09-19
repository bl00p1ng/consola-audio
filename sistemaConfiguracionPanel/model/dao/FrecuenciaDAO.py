from typing import List, Optional
from db import conexion as cbd
from model.vo.FrecuenciaVO import FrecuenciaVO

class FrecuenciaDAO:
    def __init__(self):
        self.resultadoUnaFrecuencia: Optional[FrecuenciaVO] = None
        self.resultadoVariasFrecuencias: List[FrecuenciaVO] = []
        self.todasLasFrecuencias: List[FrecuenciaVO] = []

    def getAll(self) -> List[FrecuenciaVO]:
        """
        Obtiene todas las frecuencias de la base de datos.
        
        Returns:
            List[FrecuenciaVO]: Lista con todas las frecuencias disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Frecuencia, Valor FROM Frecuencia;"
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todasLasFrecuencias.clear()
            for registro in registros:
                self.todasLasFrecuencias.append(
                    FrecuenciaVO(
                        pId=registro[0],
                        pValor=registro[1]
                    )
                )
        return self.todasLasFrecuencias

    def getFrecuencia(self, frecuenciaVO: FrecuenciaVO) -> Optional[FrecuenciaVO]:
        """
        Obtiene una frecuencia específica de la base de datos.
        
        Args:
            frecuenciaVO (FrecuenciaVO): Value Object de la frecuencia a buscar.
        
        Returns:
            Optional[FrecuenciaVO]: La frecuencia encontrada o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Frecuencia, Valor FROM Frecuencia WHERE ID_Frecuencia = ? OR Valor = ?;"
            cur = conn.cursor()
            cur.execute(sql, (str(frecuenciaVO.id), frecuenciaVO.valor))
            registro = cur.fetchone()

            if registro:
                self.resultadoUnaFrecuencia = FrecuenciaVO(
                    pId=registro[0],
                    pValor=registro[1]
                )
            else:
                self.resultadoUnaFrecuencia = None

        return self.resultadoUnaFrecuencia

    def insertFrecuencia(self, frecuenciaVO: FrecuenciaVO) -> bool:
        """
        Inserta una nueva frecuencia en la base de datos.
        
        Args:
            frecuenciaVO (FrecuenciaVO): Value Object de la frecuencia a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "INSERT INTO Frecuencia (Valor) VALUES (?);"
                cur = conn.cursor()
                cur.execute(sql, (frecuenciaVO.valor,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar frecuencia: {e}")
            return False

    def updateFrecuencia(self, frecuenciaVO: FrecuenciaVO) -> bool:
        """
        Actualiza una frecuencia existente en la base de datos.
        
        Args:
            frecuenciaVO (FrecuenciaVO): Value Object de la frecuencia a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "UPDATE Frecuencia SET Valor = ? WHERE ID_Frecuencia = ?;"
                cur = conn.cursor()
                cur.execute(sql, (frecuenciaVO.valor, str(frecuenciaVO.id)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar frecuencia: {e}")
            return False

    def deleteFrecuencia(self, frecuenciaVO: FrecuenciaVO) -> bool:
        """
        Elimina una frecuencia de la base de datos.
        
        Args:
            frecuenciaVO (FrecuenciaVO): Value Object de la frecuencia a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "DELETE FROM Frecuencia WHERE ID_Frecuencia = ?;"
                cur = conn.cursor()
                cur.execute(sql, (str(frecuenciaVO.id),))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar frecuencia: {e}")
            return False

    def getFrecuenciaPorValor(self, valor: float) -> Optional[FrecuenciaVO]:
        """
        Busca una frecuencia por su valor en la base de datos.
        
        Args:
            valor (float): Valor de la frecuencia a buscar.
        
        Returns:
            Optional[FrecuenciaVO]: La frecuencia encontrada o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Frecuencia, Valor FROM Frecuencia WHERE Valor = ?;"
            cur = conn.cursor()
            cur.execute(sql, (valor,))
            registro = cur.fetchone()

            if registro:
                return FrecuenciaVO(
                    pId=registro[0],
                    pValor=registro[1]
                )
            else:
                return None

    def getFrecuenciasEnRango(self, valor_minimo: float, valor_maximo: float) -> List[FrecuenciaVO]:
        """
        Obtiene todas las frecuencias dentro de un rango especificado.
        
        Args:
            valor_minimo (float): Valor mínimo del rango.
            valor_maximo (float): Valor máximo del rango.
        
        Returns:
            List[FrecuenciaVO]: Lista de frecuencias dentro del rango especificado.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Frecuencia, Valor FROM Frecuencia WHERE Valor BETWEEN ? AND ?;"
            cur = conn.cursor()
            cur.execute(sql, (valor_minimo, valor_maximo))
            registros = cur.fetchall()

            frecuencias = []
            for registro in registros:
                frecuencias.append(
                    FrecuenciaVO(
                        pId=registro[0],
                        pValor=registro[1]
                    )
                )
            return frecuencias