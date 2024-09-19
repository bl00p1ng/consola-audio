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
        Obtiene todas las fuentes de la base de datos, incluyendo su tipo asociado.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT f.ID_Fuente, t.ID_Tipo, t.Nombre, t.Descripcion 
                FROM Fuente f
                LEFT JOIN Clasifica c ON f.ID_Fuente = c.ID_Fuente
                LEFT JOIN Tipo t ON c.ID_Tipo = t.ID_Tipo;
            """
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todasLasFuentes.clear()
            for registro in registros:
                tipo = TipoVO(pId=registro[1], pNombre=registro[2], pDescripcion=registro[3]) if registro[1] else None
                self.todasLasFuentes.append(
                    FuenteVO(
                        pId=registro[0],
                        pTipo=tipo
                    )
                )
        return self.todasLasFuentes

    def getFuente(self, fuenteVO: FuenteVO) -> Optional[FuenteVO]:
        """
        Obtiene una fuente específica de la base de datos, incluyendo su tipo.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT f.ID_Fuente, t.ID_Tipo, t.Nombre, t.Descripcion 
                FROM Fuente f
                LEFT JOIN Clasifica c ON f.ID_Fuente = c.ID_Fuente
                LEFT JOIN Tipo t ON c.ID_Tipo = t.ID_Tipo
                WHERE f.ID_Fuente = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(fuenteVO.id),))
            registro = cur.fetchone()

            if registro:
                tipo = TipoVO(pId=registro[1], pNombre=registro[2], pDescripcion=registro[3]) if registro[1] else None
                self.resultadoUnaFuente = FuenteVO(
                    pId=registro[0],
                    pTipo=tipo
                )
            else:
                self.resultadoUnaFuente = None

        return self.resultadoUnaFuente

    def insertFuente(self, fuenteVO: FuenteVO) -> bool:
        """
        Inserta una nueva fuente en la base de datos y establece su relación con un tipo.
        """
        try:
            with cbd.crearConexion() as conn:
                cur = conn.cursor()
                
                # Insertar la fuente
                sql_fuente = "INSERT INTO Fuente (ID_Fuente) VALUES (NULL);"
                cur.execute(sql_fuente)
                id_fuente = cur.lastrowid

                # Si hay un tipo asociado, insertar la relación en Clasifica
                if fuenteVO.tipo:
                    sql_clasifica = "INSERT INTO Clasifica (ID_Fuente, ID_Tipo) VALUES (?, ?);"
                    cur.execute(sql_clasifica, (id_fuente, fuenteVO.tipo.id))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar fuente: {e}")
            return False


    def updateFuente(self, fuenteVO: FuenteVO) -> bool:
        """
        Actualiza una fuente existente en la base de datos y su relación con un tipo.
        """
        try:
            with cbd.crearConexion() as conn:
                cur = conn.cursor()
                
                # Actualizar la relación en Clasifica
                if fuenteVO.tipo:
                    sql_clasifica = """
                        INSERT OR REPLACE INTO Clasifica (ID_Fuente, ID_Tipo) 
                        VALUES (?, ?);
                    """
                    cur.execute(sql_clasifica, (fuenteVO.id, fuenteVO.tipo.id))
                else:
                    # Si no hay tipo, eliminar la relación si existía
                    sql_delete_clasifica = "DELETE FROM Clasifica WHERE ID_Fuente = ?;"
                    cur.execute(sql_delete_clasifica, (fuenteVO.id,))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar fuente: {e}")
            return False


    def deleteFuente(self, fuenteVO: FuenteVO) -> bool:
        """
        Elimina una fuente de la base de datos y sus relaciones asociadas.
        """
        try:
            with cbd.crearConexion() as conn:
                cur = conn.cursor()
                
                # Eliminar relaciones en Clasifica
                sql_delete_clasifica = "DELETE FROM Clasifica WHERE ID_Fuente = ?;"
                cur.execute(sql_delete_clasifica, (fuenteVO.id,))
                
                # Eliminar la fuente
                sql_delete_fuente = "DELETE FROM Fuente WHERE ID_Fuente = ?;"
                cur.execute(sql_delete_fuente, (fuenteVO.id,))
                
                conn.commit()
                return True
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
        fuentes = []
        with cbd.crearConexion() as conn:
            sql = """
                SELECT f.ID_Fuente, t.ID_Tipo, t.Nombre, t.Descripcion 
                FROM Fuente f
                JOIN Clasifica c ON f.ID_Fuente = c.ID_Fuente
                JOIN Tipo t ON c.ID_Tipo = t.ID_Tipo
                WHERE t.ID_Tipo = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(tipoVO.id),))
            registros = cur.fetchall()

            for registro in registros:
                tipo = TipoVO(pId=registro[1], pNombre=registro[2], pDescripcion=registro[3])
                fuente = FuenteVO(
                    pId=registro[0],
                    pTipo=tipo
                )
                fuentes.append(fuente)

        return fuentes