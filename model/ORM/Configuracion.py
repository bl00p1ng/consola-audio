from peewee import SqliteDatabase, Model, AutoField, DateField, ForeignKeyField, FloatField, BooleanField
from typing import List, Optional
from datetime import datetime

db = SqliteDatabase('db/Base_De_Datos.db')

class Usuario(Model):
    id = AutoField()
    # Agregar otros campos necesarios para Usuario

    class Meta:
        database = db

class InterfazAudio(Model):
    id = AutoField()
    # Agregar otros campos necesarios para InterfazAudio

    class Meta:
        database = db

class Canal(Model):
    id = AutoField()
    etiqueta = CharField()
    # Otros campos de Canal...

    class Meta:
        database = db

class Dispositivo(Model):
    id = AutoField()
    # Agregar campos necesarios para Dispositivo

    class Meta:
        database = db

class Entrada(Model):
    id = AutoField()
    dispositivo = ForeignKeyField(Dispositivo, backref='entradas')
    # Otros campos de Entrada...

    class Meta:
        database = db

class Configuracion(Model):
    id = AutoField()
    fecha = DateField()
    usuario = ForeignKeyField(Usuario, backref='configuraciones')
    interfaz = ForeignKeyField(InterfazAudio, backref='configuraciones')

    class Meta:
        database = db

class ConfiguracionCanal(Model):
    configuracion = ForeignKeyField(Configuracion, backref='canales')
    canal = ForeignKeyField(Canal, backref='configuraciones')
    volumen = FloatField()
    solo = BooleanField()
    mute = BooleanField()
    link = BooleanField()

    class Meta:
        database = db
        primary_key = CompositeKey('configuracion', 'canal')

class ConfiguracionEntrada(Model):
    configuracion = ForeignKeyField(Configuracion, backref='entradas')
    entrada = ForeignKeyField(Entrada, backref='configuraciones')

    class Meta:
        database = db
        primary_key = CompositeKey('configuracion', 'entrada')

class ConfiguracionDAO:
    @staticmethod
    def get_all() -> List[Configuracion]:
        """
        Obtiene todas las configuraciones de la base de datos.
        
        Returns:
            List[Configuracion]: Lista con todas las configuraciones disponibles.
        """
        return list(Configuracion.select().prefetch(Usuario, InterfazAudio))

    @staticmethod
    def get_configuracion(config_id: int) -> Optional[Configuracion]:
        """
        Obtiene una configuración específica de la base de datos.
        
        Args:
            config_id (int): ID de la configuración a buscar.
        
        Returns:
            Optional[Configuracion]: La configuración encontrada o None si no existe.
        """
        try:
            return Configuracion.get_by_id(config_id)
        except Configuracion.DoesNotExist:
            return None

    @staticmethod
    def insert_configuracion(configuracion: Configuracion) -> bool:
        """
        Inserta una nueva configuración en la base de datos.
        
        Args:
            configuracion (Configuracion): Instancia de la configuración a insertar.
        
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            with db.atomic():
                configuracion.save()
                return True
        except Exception as e:
            print(f"Error al insertar configuración: {e}")
            return False

    @staticmethod
    def update_configuracion(configuracion: Configuracion) -> bool:
        """
        Actualiza una configuración existente en la base de datos.
        
        Args:
            configuracion (Configuracion): Instancia de la configuración a actualizar.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            with db.atomic():
                configuracion.save()
                return True
        except Exception as e:
            print(f"Error al actualizar configuración: {e}")
            return False

    @staticmethod
    def delete_configuracion(configuracion: Configuracion) -> bool:
        """
        Elimina una configuración de la base de datos.
        
        Args:
            configuracion (Configuracion): Instancia de la configuración a eliminar.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            with db.atomic():
                configuracion.delete_instance(recursive=True)
                return True
        except Exception as e:
            print(f"Error al eliminar configuración: {e}")
            return False

    @staticmethod
    def get_configuraciones_por_usuario(usuario: Usuario) -> List[Configuracion]:
        """
        Obtiene todas las configuraciones asociadas a un usuario específico.
        
        Args:
            usuario (Usuario): Instancia del usuario.
        
        Returns:
            List[Configuracion]: Lista de configuraciones asociadas al usuario.
        """
        return list(Configuracion.select().where(Configuracion.usuario == usuario))

    @staticmethod
    def ajustar_volumen(configuracion: Configuracion, canal: Canal, nuevo_volumen: float) -> bool:
        """
        Ajusta el volumen de un canal específico en una configuración.
        
        Args:
            configuracion (Configuracion): Instancia de la configuración.
            canal (Canal): Instancia del canal a ajustar.
            nuevo_volumen (float): Nuevo valor de volumen.
        
        Returns:
            bool: True si el ajuste fue exitoso, False en caso contrario.
        """
        try:
            with db.atomic():
                config_canal = ConfiguracionCanal.get(
                    (ConfiguracionCanal.configuracion == configuracion) &
                    (ConfiguracionCanal.canal == canal)
                )
                config_canal.volumen = nuevo_volumen
                config_canal.save()
                return True
        except Exception as e:
            print(f"Error al ajustar volumen: {e}")
            return False

    @staticmethod
    def cargar_configuracion(configuracion: Configuracion) -> bool:
        """
        Carga una configuración específica, actualizando el estado actual del sistema.
        
        Args:
            configuracion (Configuracion): Instancia de la configuración a cargar.
        
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario.
        """
        try:
            with db.atomic():
                # Actualizar la interfaz de audio
                InterfazAudio.update(**configuracion.interfaz.__data__).where(
                    InterfazAudio.id == configuracion.interfaz.id
                ).execute()

                # Actualizar los canales
                for config_canal in configuracion.canales:
                    Canal.update(**config_canal.canal.__data__).where(
                        Canal.id == config_canal.canal.id
                    ).execute()

                # Actualizar las entradas
                for config_entrada in configuracion.entradas:
                    Entrada.update(**config_entrada.entrada.__data__).where(
                        Entrada.id == config_entrada.entrada.id
                    ).execute()

                print(f"Configuración cargada exitosamente: ID {configuracion.id}")
                return True
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            return False

    @staticmethod
    def get_canales_configuracion(configuracion: Configuracion) -> List[ConfiguracionCanal]:
        """
        Obtiene los canales asociados a una configuración específica.
        
        Args:
            configuracion (Configuracion): Instancia de la configuración.
        
        Returns:
            List[ConfiguracionCanal]: Lista de canales asociados a la configuración.
        """
        return list(ConfiguracionCanal.select().where(ConfiguracionCanal.configuracion == configuracion))

    @staticmethod
    def get_entradas_configuracion(configuracion: Configuracion) -> List[ConfiguracionEntrada]:
        """
        Obtiene las entradas asociadas a una configuración específica.
        
        Args:
            configuracion (Configuracion): Instancia de la configuración.
        
        Returns:
            List[ConfiguracionEntrada]: Lista de entradas asociadas a la configuración.
        """
        return list(ConfiguracionEntrada.select().where(ConfiguracionEntrada.configuracion == configuracion))

    @staticmethod
    def get_configuraciones_por_interfaz(interfaz: InterfazAudio) -> List[Configuracion]:
        """
        Obtiene todas las configuraciones asociadas a una interfaz de audio específica.
        
        Args:
            interfaz (InterfazAudio): Instancia de la interfaz de audio.
        
        Returns:
            List[Configuracion]: Lista de configuraciones asociadas a la interfaz de audio.
        """
        return list(Configuracion.select().where(Configuracion.interfaz == interfaz))