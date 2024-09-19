from typing import List, Optional
from datetime import datetime
from db import conexion as cbd
from model.vo.ConfiguracionVO import ConfiguracionVO
from model.vo.UsuarioVO import UsuarioVO
from model.vo.canalVO import CanalVO
from model.dao.UsuarioDAO import UsuarioDAO
from model.dao.CanalDAO import CanalDAO
from model.dao.EntradadaDAO import EntradaDAO
from model.vo.EntradaVO import EntradaVO

class ConfiguracionUsuarioDAO:
    def __init__(self):
        self.usuarioDAO = UsuarioDAO()
        self.canalDAO = CanalDAO()
        self.entradaDAO = EntradaDAO()

    def getConfiguracionUsuario(self, configuracionVO: ConfiguracionVO) -> Optional[ConfiguracionVO]:
        """
        Obtiene una configuración específica de usuario con todos sus detalles.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a buscar.
        
        Returns:
            Optional[ConfiguracionVO]: La configuración encontrada con todos sus detalles o None si no existe.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT c.ID, c.Fecha, c.ID_Usuario, c.ID_Interfaz
                FROM Configuracion c
                WHERE c.ID = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.ID),))
            registro = cur.fetchone()

            if registro:
                usuario = self.usuarioDAO.getUsuario(UsuarioVO(uId=registro[2]))
                configuracion = ConfiguracionVO(ID=registro[0], Fecha=registro[1])
                configuracion.setUsuario(usuario)
                
                # Obtener canales asociados a esta configuración
                configuracion.setCanales(self.getCanalesConfiguracion(configuracion))
                
                # Obtener entradas asociadas a esta configuración
                configuracion.setEntradas(self.getEntradasConfiguracion(configuracion))

                return configuracion
            else:
                return None

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
                SELECT c.Codigo_Canal
                FROM Canal c
                JOIN ConfiguracionCanal cc ON c.Codigo_Canal = cc.ID_Canal
                WHERE cc.ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.ID),))
            registros = cur.fetchall()

            canales = []
            for registro in registros:
                canal = self.canalDAO.getCanal(CanalVO(pId=registro[0]))
                if canal:
                    canales.append(canal)

            return canales

    def getEntradasConfiguracion(self, configuracionVO: ConfiguracionVO) -> List:
        """
        Obtiene las entradas asociadas a una configuración específica.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración.
        
        Returns:
            List: Lista de entradas asociadas a la configuración.
        """
        with cbd.crearConexion() as conn:
            sql = """
                SELECT e.ID_Entrada
                FROM Entrada e
                JOIN ConfiguracionEntrada ce ON e.ID_Entrada = ce.ID_Entrada
                WHERE ce.ID_Configuracion = ?;
            """
            cur = conn.cursor()
            cur.execute(sql, (str(configuracionVO.ID),))
            registros = cur.fetchall()

            entradas = []
            for registro in registros:
                entrada = self.entradaDAO.getEntrada(EntradaVO(pId=registro[0]))
                if entrada:
                    entradas.append(entrada)

            return entradas

    def insertConfiguracionUsuario(self, configuracionVO: ConfiguracionVO) -> bool:
        """
        Inserta una nueva configuración de usuario en la base de datos.
        
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
                sql_canal = "INSERT INTO ConfiguracionCanal (ID_Configuracion, ID_Canal) VALUES (?, ?);"
                for canal in configuracionVO.getCanales():
                    cur.execute(sql_canal, (id_configuracion, canal.id))

                # Insertar relaciones con entradas
                sql_entrada = "INSERT INTO ConfiguracionEntrada (ID_Configuracion, ID_Entrada) VALUES (?, ?);"
                for entrada in configuracionVO.getEntradas():
                    cur.execute(sql_entrada, (id_configuracion, entrada.id))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error al insertar configuración de usuario: {e}")
            return False

    def updateConfiguracionUsuario(self, configuracionVO: ConfiguracionVO) -> bool:
        """
        Actualiza una configuración de usuario existente en la base de datos.
        
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

                # Eliminar relaciones existentes
                cur.execute("DELETE FROM ConfiguracionCanal WHERE ID_Configuracion = ?;", (configuracionVO.ID,))
                cur.execute("DELETE FROM ConfiguracionEntrada WHERE ID_Configuracion = ?;", (configuracionVO.ID,))

                # Insertar nuevas relaciones con canales
                sql_canal = "INSERT INTO ConfiguracionCanal (ID_Configuracion, ID_Canal) VALUES (?, ?);"
                for canal in configuracionVO.getCanales():
                    cur.execute(sql_canal, (configuracionVO.ID, canal.id))

                # Insertar nuevas relaciones con entradas
                sql_entrada = "INSERT INTO ConfiguracionEntrada (ID_Configuracion, ID_Entrada) VALUES (?, ?);"
                for entrada in configuracionVO.getEntradas():
                    cur.execute(sql_entrada, (configuracionVO.ID, entrada.id))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar configuración de usuario: {e}")
            return False

    def deleteConfiguracionUsuario(self, configuracionVO: ConfiguracionVO) -> bool:
        """
        Elimina una configuración de usuario de la base de datos.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                cur = conn.cursor()
                
                # Eliminar relaciones
                cur.execute("DELETE FROM ConfiguracionCanal WHERE ID_Configuracion = ?;", (configuracionVO.ID,))
                cur.execute("DELETE FROM ConfiguracionEntrada WHERE ID_Configuracion = ?;", (configuracionVO.ID,))
                
                # Eliminar la configuración principal
                cur.execute("DELETE FROM Configuracion WHERE ID = ?;", (configuracionVO.ID,))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error al eliminar configuración de usuario: {e}")
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
            sql = "SELECT ID FROM Configuracion WHERE ID_Usuario = ?;"
            cur = conn.cursor()
            cur.execute(sql, (str(usuarioVO.getId()),))
            registros = cur.fetchall()

            for registro in registros:
                configuracion = self.getConfiguracionUsuario(ConfiguracionVO(ID=registro[0]))
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
        Carga una configuración específica, actualizando el estado en la base de datos.
        
        Args:
            configuracionVO (ConfiguracionVO): Value Object de la configuración a cargar.
        
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario.
        """
        try:
            with cbd.crearConexion() as conn:
                cur = conn.cursor()
                
                # 1. Obtener la configuración completa
                configuracion = self.getConfiguracionUsuario(configuracionVO)
                if not configuracion:
                    print("No se pudo encontrar la configuración especificada.")
                    return False

                # 2. Actualizar la configuración principal
                sql_update_config = """
                    UPDATE Configuracion
                    SET Fecha = ?, ID_Usuario = ?, ID_Interfaz = ?
                    WHERE ID = ?;
                """
                cur.execute(sql_update_config, (
                    configuracion.Fecha,
                    configuracion.getUsuario().getId(),
                    configuracion.getInterfaz().id,
                    configuracion.ID
                ))

                # 3. Actualizar los canales asociados
                self.actualizarCanalesConfiguracion(cur, configuracion)

                # 4. Actualizar las entradas asociadas
                self.actualizarEntradasConfiguracion(cur, configuracion)

                conn.commit()
                print(f"Configuración cargada y actualizada exitosamente: {configuracion}")
                return True

        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            return False

def actualizarCanalesConfiguracion(self, cursor, configuracion: ConfiguracionVO):
    """
    Actualiza los canales asociados a la configuración en la base de datos.
    """
    # Primero, eliminar las asociaciones existentes
    cursor.execute("DELETE FROM ConfiguracionCanal WHERE ID_Configuracion = ?", (configuracion.ID,))
    
    # Luego, insertar las nuevas asociaciones
    sql_insert_canal = """
        INSERT INTO ConfiguracionCanal (ID_Configuracion, ID_Canal, Volumen, Solo, Mute, Link)
        VALUES (?, ?, ?, ?, ?, ?);
    """
    for canal in configuracion.getCanales():
        cursor.execute(sql_insert_canal, (
            configuracion.ID,
            canal.id,
            canal.volumen,
            canal.solo,
            canal.mute,
            canal.link
        ))

def actualizarEntradasConfiguracion(self, cursor, configuracion: ConfiguracionVO):
    """
    Actualiza las entradas asociadas a la configuración en la base de datos.
    """
    # Primero, eliminar las asociaciones existentes
    cursor.execute("DELETE FROM ConfiguracionEntrada WHERE ID_Configuracion = ?", (configuracion.ID,))
    
    # Luego, insertar las nuevas asociaciones
    sql_insert_entrada = """
        INSERT INTO ConfiguracionEntrada (ID_Configuracion, ID_Entrada)
        VALUES (?, ?);
    """
    for entrada in configuracion.getEntradas():
        cursor.execute(sql_insert_entrada, (configuracion.ID, entrada.id))

def modificarConfiguracion(self, configuracionVO: ConfiguracionVO) -> bool:
    """
    Modifica una configuración existente en la base de datos.
    
    Args:
        configuracionVO (ConfiguracionVO): Value Object de la configuración modificada.
    
    Returns:
        bool: True si la modificación fue exitosa, False en caso contrario.
    """
    try:
        with cbd.crearConexion() as conn:
            cur = conn.cursor()
            
            # Actualizar la configuración principal
            sql_update_config = """
                UPDATE Configuracion
                SET Fecha = ?, ID_Usuario = ?, ID_Interfaz = ?
                WHERE ID = ?;
            """
            cur.execute(sql_update_config, (
                configuracionVO.Fecha,
                configuracionVO.getUsuario().getId(),
                configuracionVO.getInterfaz().id,
                configuracionVO.ID
            ))

            # Actualizar los canales y entradas asociados
            self.actualizarCanalesConfiguracion(cur, configuracionVO)
            self.actualizarEntradasConfiguracion(cur, configuracionVO)

            conn.commit()
            print(f"Configuración modificada exitosamente: {configuracionVO}")
            return True

    except Exception as e:
        print(f"Error al modificar configuración: {e}")
        return False