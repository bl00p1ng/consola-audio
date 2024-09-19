# InterfazAudioDAO.py

from typing import List, Optional
from db import conexion as cbd
from model.vo.FrecuenciaVO import FrecuenciaVO
from model.dao.FrecuenciaDAO import FrecuenciaDAO

class InterfazAudioVO:
    def __init__(self, pId: int = -1, pNombreCorto: str = "", pModelo: str = "", 
                 pNombreComercial: str = "", pPrecio: float = 0.0, pFrecuencia: FrecuenciaVO = None):
        self.__id = pId
        self.__nombreCorto = pNombreCorto
        self.__modelo = pModelo
        self.__nombreComercial = pNombreComercial
        self.__precio = pPrecio
        self.__frecuencia = pFrecuencia

    @property
    def id(self):
        return self.__id

    @property
    def nombreCorto(self):
        return self.__nombreCorto

    @property
    def modelo(self):
        return self.__modelo

    @property
    def nombreComercial(self):
        return self.__nombreComercial

    @property
    def precio(self):
        return self.__precio

    @property
    def frecuencia(self):
        return self.__frecuencia

    def setNombreCorto(self, pNombreCorto: str):
        self.__nombreCorto = pNombreCorto

    def setModelo(self, pModelo: str):
        self.__modelo = pModelo

    def setNombreComercial(self, pNombreComercial: str):
        self.__nombreComercial = pNombreComercial

    def setPrecio(self, pPrecio: float):
        self.__precio = pPrecio

    def setFrecuencia(self, pFrecuencia: FrecuenciaVO):
        self.__frecuencia = pFrecuencia

    def __str__(self) -> str:
        return f'ID: {self.__id}, Nombre Corto: {self.__nombreCorto}, Modelo: {self.__modelo}, ' \
               f'Nombre Comercial: {self.__nombreComercial}, Precio: {self.__precio}, Frecuencia: {self.__frecuencia}'

class InterfazAudioDAO:
    def __init__(self):
        self.resultadoUnaInterfaz: Optional[InterfazAudioVO] = None
        self.resultadoVariasInterfaces: List[InterfazAudioVO] = []
        self.todasLasInterfaces: List[InterfazAudioVO] = []
        self.frecuenciaDAO = FrecuenciaDAO()

    def getAll(self) -> List[InterfazAudioVO]:
        """
        Obtiene todas las interfaces de audio de la base de datos.
        
        Returns:
            List[InterfazAudioVO]: Lista con todas las interfaces de audio disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT i.ID_InterfazAudio, i.NombreCorto, i.Modelo, i.NombreComercial, i.Precio, i.ID_Frecuencia 
                FROM InterfazAudio i
                JOIN Frecuencia f ON i.ID_Frecuencia = f.ID_Frecuencia;
            """
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todasLasInterfaces.clear()
            for registro in registros:
                frecuencia = self.frecuenciaDAO.getFrecuencia(FrecuenciaVO(pId=registro[5]))
                self.todasLasInterfaces.append(
                    InterfazAudioVO(
                        pId=registro[0],
                        pNombreCorto=registro[1],
                        pModelo=registro[2],
                        pNombreComercial=registro[3],
                        pPrecio=registro[4],
                        pFrecuencia=frecuencia
                    )
                )
        return self.todasLasInterfaces

    def getInterfazAudio(self, interfazAudioVO: InterfazAudioVO) -> Optional[InterfazAudioVO]:
        """
        Obtiene una interfaz de audio específica de la base de datos.
        
        Args:
            interfazAudioVO (InterfazAudioVO): Value Object de la interfaz de audio a buscar.
        
        Returns:
            Optional[InterfazAudioVO]: La interfaz de audio encontrada o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT ID_Interfaz, Nombre_Corto, Modelo, Nombre_Comercial, Precio, ID_Frecuencia 
                FROM Interfaz_de_Audio 
                JOIN Frecuencia  ON ID_Frecuencia = ID_Frecuencia
                WHERE ID_Interfaz = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(interfazAudioVO.id),))
            registro = cur.fetchone()

            if registro:
                frecuencia = self.frecuenciaDAO.getFrecuencia(FrecuenciaVO(pId=registro[5]))
                self.resultadoUnaInterfaz = InterfazAudioVO(
                    pId=registro[0],
                    pNombreCorto=registro[1],
                    pModelo=registro[2],
                    pNombreComercial=registro[3],
                    pPrecio=registro[4],
                    pFrecuencia=frecuencia
                )
            else:
                self.resultadoUnaInterfaz = None

        return self.resultadoUnaInterfaz

    def insertInterfazAudio(self, interfazAudioVO: InterfazAudioVO) -> bool:
        """
        Inserta una nueva interfaz de audio en la base de datos.
        
        Args:
            interfazAudioVO (InterfazAudioVO): Value Object de la interfaz de audio a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = """
                    INSERT INTO Interfaz_de_Audio (NombreCorto, Modelo, NombreComercial, Precio, ID_Frecuencia) 
                    VALUES (?, ?, ?, ?, ?);
                """
                cur = conn.cursor()
                cur.execute(sql, (interfazAudioVO.nombreCorto, interfazAudioVO.modelo, 
                                  interfazAudioVO.nombreComercial, interfazAudioVO.precio, 
                                  interfazAudioVO.frecuencia.id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar interfaz de audio: {e}")
            return False

    def updateInterfazAudio(self, interfazAudioVO: InterfazAudioVO) -> bool:
        """
        Actualiza una interfaz de audio existente en la base de datos.
        
        Args:
            interfazAudioVO (InterfazAudioVO): Value Object de la interfaz de audio a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = """
                    UPDATE Interfaz_de_Audio 
                    SET NombreCorto = ?, Modelo = ?, NombreComercial = ?, Precio = ?, ID_Frecuencia = ? 
                    WHERE ID_InterfazAudio = ?;
                """
                cur = conn.cursor()
                cur.execute(sql, (interfazAudioVO.nombreCorto, interfazAudioVO.modelo, 
                                  interfazAudioVO.nombreComercial, interfazAudioVO.precio, 
                                  interfazAudioVO.frecuencia.id, str(interfazAudioVO.id)))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar interfaz de audio: {e}")
            return False

    def deleteInterfazAudio(self, interfazAudioVO: InterfazAudioVO) -> bool:
        """
        Elimina una interfaz de audio de la base de datos.
        
        Args:
            interfazAudioVO (InterfazAudioVO): Value Object de la interfaz de audio a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = "DELETE FROM InterfazAudio WHERE ID_InterfazAudio = ?;"
                cur = conn.cursor()
                cur.execute(sql, (str(interfazAudioVO.id),))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar interfaz de audio: {e}")
            return False

    def getInterfacesPorFrecuencia(self, frecuenciaVO: FrecuenciaVO) -> List[InterfazAudioVO]:
        """
        Obtiene todas las interfaces de audio asociadas a una frecuencia específica.
        
        Args:
            frecuenciaVO (FrecuenciaVO): Value Object de la frecuencia.
        
        Returns:
            List[InterfazAudioVO]: Lista de interfaces de audio asociadas a la frecuencia.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT ID_Interfaz, NombreCorto, Modelo, NombreComercial, i.Precio, i.ID_Frecuencia 
                FROM Interfaz_de_Audio
                WHERE i.ID_Frecuencia = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(frecuenciaVO.id),))
            registros = cur.fetchall()

            interfaces = []
            for registro in registros:
                interfaces.append(
                    InterfazAudioVO(
                        pId=registro[0],
                        pNombreCorto=registro[1],
                        pModelo=registro[2],
                        pNombreComercial=registro[3],
                        pPrecio=registro[4],
                        pFrecuencia=frecuenciaVO
                    )
                )
        return interfaces