# ConfiguracionDAO.py

from typing import List, Optional
from datetime import datetime
from db import conexion as cbd
from model.vo.ConfiguracionVO import ConfiguracionVO
from model.vo.UsuarioVO import UsuarioVO
from model.vo.InterfazAudioVO import InterfazAudioVO
from model.vo.canalVO import CanalVO
from model.vo.DispositivoVO import DispositivoVO
from model.dao.UsuarioDAO import UsuarioDAO
from model.dao.InterfazAudioDAO import InterfazAudioDAO
from model.dao.CanalDAO import CanalDAO
from model.dao.DispositivoDAO import DispositivoDAO

class ConfiguracionDAO:
    def __init__(self):
        self.resultadoUnaConfiguracion: Optional[ConfiguracionVO] = None
        self.resultadoVariasConfiguraciones: List[ConfiguracionVO] = []
        self.todasLasConfiguraciones: List[ConfiguracionVO] = []
        self.usuarioDAO = UsuarioDAO()
        self.interfazAudioDAO = InterfazAudioDAO()
        self.canalDAO = CanalDAO()
        self.dispositivoDAO = DispositivoDAO()

    def getAll(self) -> List[ConfiguracionVO]:
        """
        Obtiene todas las configuraciones de la base de datos.
        
        Returns:
            List[ConfiguracionVO]: Lista con todas las configuraciones disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT c.ID, c.Fecha, c.ID_Usuario, c.ID_Interfaz
                FROM Configuracion c;
            """
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todasLasConfiguraciones.clear()
            for registro in registros:
                usuario = self.usuarioDAO.getUsuario(UsuarioVO(uId=registro[2]))
                interfaz = self.interfazAudioDAO.getInterfazAudio(InterfazAudioVO(pId=registro[3]))
                configuracion = ConfiguracionVO(ID=registro[0], Fecha=registro[1])
                configuracion.setUsuario(usuario)
                configuracion.setInterfaz(interfaz)
                
                # Obtener canales y entradas asociados
                configuracion.setCanales(self.getCanalesConfiguracion(configuracion))
                configuracion.setEntradas(self.getEntradasConfiguracion(configuracion))
                
                self.todasLasConfiguraciones.append(configuracion)
        
        return self.todasLasConfiguraciones

    def getConfiguracion(self, configuracionVO: ConfiguracionVO) -> Optional[ConfiguracionVO]:
        """
        Obtiene una configuración específica de la base de datos.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a buscar.
        
        Returns:
            Optional[ConfiguracionVO]: La configuración encontrada o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT ID_Configuracion, Fecha
                FROM Configuracion 
                WHERE ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.ID),))
            registro = cur.fetchone()

            if registro:
                usuario = self.usuarioDAO.getUsuario(UsuarioVO(uId=registro[1]))
                interfaz = self.interfazAudioDAO.getInterfazAudio(InterfazAudioVO(pId=registro[1]))
                self.resultadoUnaConfiguracion = ConfiguracionVO(ID=registro[0], Fecha=registro[1])
                self.resultadoUnaConfiguracion.setUsuario(usuario)
                self.resultadoUnaConfiguracion.setInterfaz(interfaz)
                
                # Obtener canales y entradas asociados
                self.resultadoUnaConfiguracion.setCanales(self.getCanalesConfiguracion(self.resultadoUnaConfiguracion))
                self.resultadoUnaConfiguracion.setEntradas(self.getEntradasConfiguracion(self.resultadoUnaConfiguracion))
            else:
                self.resultadoUnaConfiguracion = None

        return self.resultadoUnaConfiguracion

    def insertConfiguracion(self, configuracionVO: ConfiguracionVO) -> bool:
        """
        Inserta una nueva configuración en la base de datos.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                cur = conn.cursor()
                
                # Insertar la configuración principal
                sql_config = """
                    INSERT INTO Configuracion (Fecha, ID_Usuario, ID_Interfaz)
                    VALUES (?, ?, ?);
                """
                cur.execute(sql_config, (configuracionVO.Fecha, configuracionVO.getUsuario().getId(), configuracionVO.getInterfaz().id))
                id_configuracion = cur.lastrowid

                # Insertar relaciones con canales
                self.insertCanalesConfiguracion(cur, id_configuracion, configuracionVO.getCanales())

                # Insertar relaciones con entradas
                self.insertEntradasConfiguracion(cur, id_configuracion, configuracionVO.getEntradas())

                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar configuración: {e}")
            return False

    def updateConfiguracion(self, configuracionVO: ConfiguracionVO) -> bool:
        """
        Actualiza una configuración existente en la base de datos.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                cur = conn.cursor()
                
                # Actualizar la configuración principal
                sql_config = """
                    UPDATE Configuracion
                    SET Fecha = ?, ID_Usuario = ?, ID_Interfaz = ?
                    WHERE ID = ?;
                """
                cur.execute(sql_config, (configuracionVO.Fecha, configuracionVO.getUsuario().getId(), 
                                         configuracionVO.getInterfaz().id, configuracionVO.ID))

                # Actualizar relaciones con canales
                self.deleteCanalesConfiguracion(cur, configuracionVO.ID)
                self.insertCanalesConfiguracion(cur, configuracionVO.ID, configuracionVO.getCanales())

                # Actualizar relaciones con entradas
                self.deleteEntradasConfiguracion(cur, configuracionVO.ID)
                self.insertEntradasConfiguracion(cur, configuracionVO.ID, configuracionVO.getEntradas())

                conn.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar configuración: {e}")
            return False

    def deleteConfiguracion(self, configuracionVO: ConfiguracionVO) -> bool:
        """
        Elimina una configuración de la base de datos.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                cur = conn.cursor()
                
                # Eliminar relaciones
                self.deleteCanalesConfiguracion(cur, configuracionVO.ID)
                self.deleteEntradasConfiguracion(cur, configuracionVO.ID)
                
                # Eliminar la configuración principal
                sql = "DELETE FROM Configuracion WHERE ID = ?;"
                cur.execute(sql, (str(configuracionVO.ID),))
                
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar configuración: {e}")
            return False

    def getCanalesConfiguracion(self, configuracionVO: ConfiguracionVO) -> List[CanalVO]:
        """
        Obtiene los canales asociados a una configuración específica.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración.
        
        Returns:
            List[CanalVO]: Lista de canales asociados a la configuración.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT Codigo_Canal, Volumen, Solo, Mute, Link
                FROM Establece
                JOIN ConfiguracionCanal ON Codigo_Canal = ID_Canal
                WHERE ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.ID),))
            registros = cur.fetchall()

            canales = []
            for registro in registros:
                canal_base = self.canalDAO.getCanal(CanalVO(pId=registro[0]))
                if canal_base:
                    canal = CanalVO(
                        pId=canal_base.id,
                        pEtiqueta=canal_base.etiqueta,
                        pVolumen=registro[1],
                        pSolo=bool(registro[2]),
                        pMute=bool(registro[3]),
                        pLink=bool(registro[4]),
                        pFuente=canal_base.fuente
                    )
                    canales.append(canal)

            return canales

    def getEntradasConfiguracion(self, configuracionVO: ConfiguracionVO) -> List[DispositivoVO]:
        """
        Obtiene las entradas asociadas a una configuración específica.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración.
        
        Returns:
            List[DispositivoVO]: Lista de entradas (dispositivos) asociadas a la configuración.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT d.ID_Dispositivo
                FROM Dispositivo d
                JOIN ConfiguracionEntrada ce ON d.ID_Dispositivo = ce.ID_Entrada
                WHERE ce.ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.ID),))
            registros = cur.fetchall()

            entradas = []
            for registro in registros:
                dispositivo = self.dispositivoDAO.getDispositivo(DispositivoVO(pID_Dispo=registro[0]))
                if dispositivo:
                    entradas.append(dispositivo)

            return entradas

    def insertCanalesConfiguracion(self, cursor, id_configuracion: int, canales: List[CanalVO]):
        """
        Inserta las relaciones entre una configuración y sus canales.
        """
        sql = """
            INSERT INTO ConfiguracionCanal (ID_Configuracion, ID_Canal, Volumen, Solo, Mute, Link)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        for canal in canales:
            cursor.execute(sql, (id_configuracion, canal.id, canal.volumen, int(canal.solo), int(canal.mute), int(canal.link)))

    def insertEntradasConfiguracion(self, cursor, id_configuracion: int, entradas: List[DispositivoVO]):
        """
        Inserta las relaciones entre una configuración y sus entradas (dispositivos).
        """
        sql = "INSERT INTO ConfiguracionEntrada (ID_Configuracion, ID_Entrada) VALUES (?, ?);"
        for entrada in entradas:
            cursor.execute(sql, (id_configuracion, entrada.Id))

    def deleteCanalesConfiguracion(self, cursor, id_configuracion: int):
        """
        Elimina todas las relaciones de canales para una configuración específica.
        """
        cursor.execute("DELETE FROM ConfiguracionCanal WHERE ID_Configuracion = ?;", (id_configuracion,))

    def deleteEntradasConfiguracion(self, cursor, id_configuracion: int):
        """
        Elimina todas las relaciones de entradas para una configuración específica.
        """
        cursor.execute("DELETE FROM ConfiguracionEntrada WHERE ID_Configuracion = ?;", (id_configuracion,))

    def getConfiguracionesPorUsuario(self, usuarioVO: UsuarioVO) -> List[ConfiguracionVO]:
        """
        Obtiene todas las configuraciones asociadas a un usuario específico.
        
        Args:
            usuarioVO (UsuarioVO): Value Object del usuario.
        
        Returns:
            List[ConfiguracionVO]: Lista de configuraciones asociadas al usuario.
        """
        configuraciones = []
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Usuario FROM Personaliza WHERE ID_Usuario = ?;"
            cur = conn.cursor()
            cur.execute(sql, (str(usuarioVO.getId()),))
            registros = cur.fetchall()

            for registro in registros:
                configuracion = self.getConfiguracion(ConfiguracionVO(ID=registro[0]))
                if configuracion:
                    configuraciones.append(configuracion)

        return configuraciones

    def ajustarVolumen(self, configuracionVO: ConfiguracionVO, canalVO: CanalVO, nuevoVolumen: float) -> bool:
        """
        Ajusta el volumen de un canal específico en una configuración.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración.
            canalVO (CanalVO): Value Object del canal a ajustar.
            nuevoVolumen (float): Nuevo valor de volumen.
        
        Returns:
            bool: True si el ajuste fue exitoso, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                sql = """
                    UPDATE ConfiguracionCanal
                    SET Volumen = ?
                    WHERE ID_Configuracion = ? AND ID_Canal = ?;
                """
                cur = conn.cursor()
                cur.execute(sql, (nuevoVolumen, configuracionVO.ID, canalVO.id))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al ajustar volumen: {e}")
            return False

    def cargarConfiguracion(self, configuracionVO: ConfiguracionVO) -> bool:
        """
        Carga una configuración específica, actualizando el estado actual del sistema.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a cargar.
        
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario.
        """
        try:
            configuracion = self.getConfiguracion(configuracionVO)
            if configuracion:
                # 1. Actualizar la interfaz de audio
                interfaz = configuracion.getInterfaz()
                self.interfazAudioDAO.updateInterfazAudio(interfaz)

                # 2. Actualizar los canales
                for canal in configuracion.getCanales():
                    self.canalDAO.updateCanal(canal)

                # 3. Actualizar las entradas (dispositivos)
                for entrada in configuracion.getEntradas():
                    self.dispositivoDAO.updateDispositivo(entrada)

                # 4. Actualizar la configuración en la base de datos
                self.updateConfiguracion(configuracion)

                print(f"Configuración cargada exitosamente: ID {configuracion.ID}")
                return True
            else:
                print(f"No se encontró la configuración con ID {configuracionVO.ID}")
                return False
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            return False