from typing import List, Optional
from db import conexion as cbd
from model.vo.FrecuenciaVO import FrecuenciaVO
from model.vo.TipoVO import TipoVO
from model.vo.FuenteVO import FuenteVO

class FuenteDAO:
    def __init__(self):
        self.resultadoUnaFuente: Optional[FuenteVO] = None
        self.resultadoVariasFuentes: List[FuenteVO] = []
        self.todasLasFuentes: List[FuenteVO] = []

    def getAll(self) -> List[FuenteVO]:
        """
        Obtiene todas las fuentes de la base de datos.
        
        Returns:
            List[FuenteVO]: Lista con todas las fuentes disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT f.ID_Fuente, f.ID_Tipo, t.Nombre, t.Descripcion 
                FROM Fuente f
                JOIN Tipo t ON f.ID_Tipo = t.ID_Tipo;
            """
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todasLasFuentes.clear()
            for registro in registros:
                tipo = TipoVO(pId=registro[1], pNombre=registro[2], pDescripcion=registro[3])
                self.todasLasFuentes.append(
                    FuenteVO(
                        pId=registro[0],
                        pTipo=tipo
                    )
                )
        return self.todasLasFuentes

    def getFuente(self, fuenteVO: FuenteVO) -> Optional[FuenteVO]:
        """
        Obtiene una fuente específica de la base de datos.
        
        Args:
            fuenteVO (FuenteVO): Value Object de la fuente a buscar.
        
        Returns:
            Optional[FuenteVO]: La fuente encontrada o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT f.ID_Fuente, f.ID_Tipo, t.Nombre, t.Descripcion 
                FROM Fuente f
                JOIN Tipo t ON f.ID_Tipo = t.ID_Tipo
                WHERE f.ID_Fuente = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(fuenteVO.id),))
            registro = cur.fetchone()

            if registro:
                tipo = TipoVO(pId=registro[1], pNombre=registro[2], pDescripcion=registro[3])
                self.resultadoUnaFuente = FuenteVO(
                    pId=registro[0],
                    pTipo=tipo
                )
            else:
                self.resultadoUnaFuente = None

        return self.resultadoUnaFuente

    def insertFuente(self, fuenteVO: FuenteVO) -> bool:
        """
        Inserta una nueva fuente en la base de datos.
        
        Args:
            fuenteVO (FuenteVO): Value Object de la fuente a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "INSERT INTO Fuente (ID_Tipo) VALUES (?);"
                cur = conn.cursor()
                cur.execute(sql, (fuenteVO.tipo.id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar fuente: {e}")
            return False

    def updateFuente(self, fuenteVO: FuenteVO) -> bool:
        """
        Actualiza una fuente existente en la base de datos.
        
        Args:
            fuenteVO (FuenteVO): Value Object de la fuente a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "UPDATE Fuente SET ID_Tipo = ? WHERE ID_Fuente = ?;"
                cur = conn.cursor()
                cur.execute(sql, (fuenteVO.tipo.id, str(fuenteVO.id)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar fuente: {e}")
            return False

    def deleteFuente(self, fuenteVO: FuenteVO) -> bool:
        """
        Elimina una fuente de la base de datos.
        
        Args:
            fuenteVO (FuenteVO): Value Object de la fuente a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "DELETE FROM Fuente WHERE ID_Fuente = ?;"
                cur = conn.cursor()
                cur.execute(sql, (str(fuenteVO.id),))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar fuente: {e}")
            return False

    def getFuentesPorTipo(self, tipoVO: TipoVO) -> List[FuenteVO]:
        """
        Obtiene todas las fuentes asociadas a un tipo específico.
        
        Args:
            tipoVO (TipoVO): Value Object del tipo.
        
        Returns:
            List[FuenteVO]: Lista de fuentes asociadas al tipo.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT f.ID_Fuente, f.ID_Tipo 
                FROM Fuente f
                WHERE f.ID_Tipo = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(tipoVO.id),))
            registros = cur.fetchall()

            fuentes = []
            for registro in registros:
                fuentes.append(
                    FuenteVO(
                        pId=registro[0],
                        pTipo=tipoVO
                    )
                )
        return fuentes