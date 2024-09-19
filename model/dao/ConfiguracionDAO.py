from typing import List, Optional
from datetime import datetime
from db import conexion as cbd
from model.vo.ConfiguracionVO import ConfiguracionVO
from model.vo.UsuarioVO import UsuarioVO
from model.vo.InterfazAudioVO import InterfazAudioVO
from model.vo.canalVO import CanalVO
from model.vo.DispositivoVO import DispositivoVO
from model.vo.EntradaVO import EntradaVO
from model.dao.UsuarioDAO import UsuarioDAO
from model.dao.InterfazAudioDAO import InterfazAudioDAO
from model.dao.CanalDAO import CanalDAO
from model.dao.DispositivoDAO import DispositivoDAO
from model.dao.EntradadaDAO import EntradaDAO

class ConfiguracionDAO:
    def __init__(self):
        self.resultadoUnaConfiguracion: Optional[ConfiguracionVO] = None
        self.resultadoVariasConfiguraciones: List[ConfiguracionVO] = []
        self.todasLasConfiguraciones: List[ConfiguracionVO] = []
        self.usuarioDAO = UsuarioDAO()
        self.interfazAudioDAO = InterfazAudioDAO()
        self.canalDAO = CanalDAO()
        self.dispositivoDAO = DispositivoDAO()
        self.entradaDAO = EntradaDAO()

    def getAll(self) -> List[ConfiguracionVO]:
        """
        Obtiene todas las configuraciones de la base de datos.
        
        Returns:
            List[ConfiguracionVO]: Lista con todas las configuraciones disponibles.
        """
        with cbd.crearConexion() as conn:
            sql = "SELECT ID_Configuracion, Fecha FROM Configuracion;"
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            self.todasLasConfiguraciones.clear()
            for registro in registros:
                configuracion = ConfiguracionVO(ID=registro[0], Fecha=registro[1])
                self.cargarRelacionesConfiguracion(configuracion)
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
            sql = "SELECT ID_Configuracion, Fecha FROM Configuracion WHERE ID_Configuracion = ?;"
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.ID),))
            registro = cur.fetchone()

            if registro:
                self.resultadoUnaConfiguracion = ConfiguracionVO(ID=registro[0], Fecha=registro[1])
                self.cargarRelacionesConfiguracion(self.resultadoUnaConfiguracion)
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
                sql_config = "INSERT INTO Configuracion (Fecha) VALUES (?);"
                cur.execute(sql_config, (configuracionVO.Fecha,))
                id_configuracion = cur.lastrowid

                # Insertar relación en Personaliza
                self.insertPersonaliza(cur, id_configuracion, configuracionVO)

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
                sql_config = "UPDATE Configuracion SET Fecha = ? WHERE ID_Configuracion = ?;"
                cur.execute(sql_config, (configuracionVO.Fecha, configuracionVO.ID))

                # Actualizar relación en Personaliza
                self.updatePersonaliza(cur, configuracionVO)

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
                self.deletePersonaliza(cur, configuracionVO.ID)
                self.deleteCanalesConfiguracion(cur, configuracionVO.ID)
                self.deleteEntradasConfiguracion(cur, configuracionVO.ID)
                
                # Eliminar la configuración principal
                sql = "DELETE FROM Configuracion WHERE ID_Configuracion = ?;"
                cur.execute(sql, (str(configuracionVO.ID),))
                
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar configuración: {e}")
            return False

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
            sql = """
                SELECT c.ID_Configuracion, c.Fecha
                FROM Configuracion c
                JOIN Personaliza p ON c.ID_Configuracion = p.ID_Configuracion
                WHERE p.ID_Usuario = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(usuarioVO.getId()),))
            registros = cur.fetchall()

            for registro in registros:
                configuracion = ConfiguracionVO(ID=registro[0], Fecha=registro[1])
                self.cargarRelacionesConfiguracion(configuracion)
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
                    UPDATE Establece
                    SET Volumen = ?
                    WHERE ID_Configuracion = ? AND Codigo_Canal = ?;
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
                # Actualizar la interfaz de audio
                self.interfazAudioDAO.updateInterfazAudio(configuracion.getInterfaz())

                # Actualizar los canales
                for canal in configuracion.getCanales():
                    self.canalDAO.updateCanal(canal)

                # Actualizar las entradas (dispositivos)
                for entrada in configuracion.getEntradas():
                    self.entradaDAO.updateEntrada(entrada)

                print(f"Configuración cargada exitosamente: ID {configuracion.ID}")
                return True
            else:
                print(f"No se encontró la configuración con ID {configuracionVO.ID}")
                return False
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            return False

    def cargarRelacionesConfiguracion(self, configuracionVO: ConfiguracionVO):
        """
        Carga todas las relaciones de una configuración.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a cargar.
        """
        with cbd.crearConexion() as conn:
            # Cargar relación Personaliza
            sql_personaliza = """
                SELECT ID_Usuario, ID_Interfaz
                FROM Personaliza
                WHERE ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql_personaliza, (configuracionVO.getID(),))
            personaliza = cur.fetchone()
            if personaliza:
                usuario = self.usuarioDAO.getUsuario(UsuarioVO(uId=personaliza[0]))
                interfaz = self.interfazAudioDAO.getInterfazAudio(InterfazAudioVO(pId=personaliza[1]))
                configuracionVO.setUsuario(usuario)
                configuracionVO.setInterfaz(interfaz)

            # Cargar canales
            canales = self.getCanalesConfiguracion(configuracionVO)
            for canal in canales:
                configuracionVO.setCanal(canal)

            # Cargar entradas
            entradas = self.getEntradasConfiguracion(configuracionVO)
            for entrada in entradas:
                configuracionVO.setEntrada(entrada)

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
                SELECT c.Codigo_Canal, e.Volumen, e.Solo, e.Mute, e.Link
                FROM Canal c
                JOIN Establece e ON c.Codigo_Canal = e.Codigo_Canal
                WHERE e.ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.getID()),))
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

    def getEntradasConfiguracion(self, configuracionVO: ConfiguracionVO) -> List[EntradaVO]:
        """
        Obtiene las entradas asociadas a una configuración específica.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración.
        
        Returns:
            List[EntradaVO]: Lista de entradas asociadas a la configuración.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT e.ID_Entrada
                FROM Entrada e
                JOIN Conectado c ON e.ID_Entrada = c.ID_Entrada
                WHERE c.ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.getID()),))
            registros = cur.fetchall()

            entradas = []
            for registro in registros:
                entrada = self.entradaDAO.getEntrada(EntradaVO(pId=registro[0]))
                if entrada:
                    entradas.append(entrada)

            return entradas

    def updatePersonaliza(self, cursor, configuracionVO: ConfiguracionVO):
        """
        Actualiza la relación en la tabla Personaliza.
        """
        sql = """
            UPDATE Personaliza
            SET ID_Usuario = ?, ID_Interfaz = ?
            WHERE ID_Configuracion = ?;
        """
        cursor.execute(sql, (
            configuracionVO.getUsuario().getId(),
            configuracionVO.getInterfaz().id,
            configuracionVO.ID
        ))

    def deletePersonaliza(self, cursor, id_configuracion: int):
        """
        Elimina la relación en la tabla Personaliza.
        """
        sql = "DELETE FROM Personaliza WHERE ID_Configuracion = ?;"
        cursor.execute(sql, (id_configuracion,))

    def insertCanalesConfiguracion(self, cursor, id_configuracion: int, canales: List[CanalVO]):
        """
        Inserta las relaciones entre una configuración y sus canales en la tabla Establece.
        """
        sql = """
            INSERT INTO Establece (ID_Configuracion, Codigo_Canal, Volumen, Solo, Mute, Link)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        for canal in canales:
            cursor.execute(sql, (
                id_configuracion,
                canal.id,
                canal.volumen,
                int(canal.solo),
                int(canal.mute),
                int(canal.link)
            ))

    def deleteCanalesConfiguracion(self, cursor, id_configuracion: int):
        """
        Elimina todas las relaciones de canales para una configuración específica en la tabla Establece.
        """
        sql = "DELETE FROM Establece WHERE ID_Configuracion = ?;"
        cursor.execute(sql, (id_configuracion,))

    def insertEntradasConfiguracion(self, cursor, id_configuracion: int, entradas: List[EntradaVO]):
        """
        Inserta las relaciones entre una configuración y sus entradas en la tabla Conectado.
        """
        sql = "INSERT INTO Conectado (ID_Configuracion, ID_Entrada) VALUES (?, ?);"
        for entrada in entradas:
            cursor.execute(sql, (id_configuracion, entrada.id))

    def deleteEntradasConfiguracion(self, cursor, id_configuracion: int):
        """
        Elimina todas las relaciones de entradas para una configuración específica en la tabla Conectado.
        """
        sql = "DELETE FROM Conectado WHERE ID_Configuracion = ?;"
        cursor.execute(sql, (id_configuracion,))

    def getConfiguracionesPorInterfaz(self, interfazVO: InterfazAudioVO) -> List[ConfiguracionVO]:
        """
        Obtiene todas las configuraciones asociadas a una interfaz de audio específica.
        
        Args:
            interfazVO (InterfazAudioVO): Value Object de la interfaz de audio.
        
        Returns:
            List[ConfiguracionVO]: Lista de configuraciones asociadas a la interfaz de audio.
        """
        configuraciones = []
        with cbd.crearConexion() as conn:
            sql = """
                SELECT c.ID_Configuracion, c.Fecha
                FROM Configuracion c
                JOIN Personaliza p ON c.ID_Configuracion = p.ID_Configuracion
                WHERE p.ID_Interfaz = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(interfazVO.id),))
            registros = cur.fetchall()

            for registro in registros:
                configuracion = ConfiguracionVO(ID=registro[0], Fecha=registro[1])
                self.cargarRelacionesConfiguracion(configuracion)
                configuraciones.append(configuracion)

        return configuraciones
