from datetime import datetime
from typing import List, TYPE_CHECKING, Optional

from peewee import (
    DateTimeField, 
    ForeignKeyField, 
    DeferredForeignKey,
    FloatField, 
    IntegerField,
    BooleanField,
    Model
)

from model.base import BaseModel
# from model.canal import Canal
# from model.entrada import Entrada
# from model.usuario import Usuario

if TYPE_CHECKING:
    from model.entrada import Entrada
    from model.canal import Canal
    from model.usuario import Usuario
    from model.dispositivo import Dispositivo
    from model.interfaz_audio import InterfazAudio

class Configuracion(BaseModel):
    """
    Modelo que representa una configuración de la consola de audio.
    
    Este modelo es central en la aplicación y mantiene las relaciones con usuarios,
    canales, entradas y la interfaz de audio, así como los parámetros específicos
    de cada configuración.
    
    Attributes:
        fecha (DateTimeField): Fecha y hora de la configuración
        created_at (DateTimeField): Fecha y hora de creación
        updated_at (DateTimeField): Fecha y hora de última actualización
    """
    id_configuracion = IntegerField(
        primary_key=True,
        column_name='ID_Configuracion',
        help_text="Identificador único de la configuración"
    )
    
    fecha = DateTimeField(
        default=datetime.now,
        index=True,
        help_text="Fecha y hora de la configuración"
    )

    class Meta:
        table_name = 'Configuracion'
        indexes = (
            (('fecha',), False),  # Índice en fecha para búsquedas
        )

    def get_usuario(self):
        """
        Obtiene el usuario asociado a esta configuración.
        
        Returns:
            Usuario: Usuario propietario de la configuración
        """
        from model.usuario import Personaliza
        personaliza = (Personaliza
                      .select()
                      .where(Personaliza.configuracion == self)
                      .first())
        return personaliza.usuario if personaliza else None

    def get_interfaz(self):
        """
        Obtiene la interfaz de audio asociada a esta configuración.
        
        Returns:
            InterfazAudio: Interfaz de audio asociada
        """
        from model.interfaz_audio import InterfazAudio
        from model.usuario import Personaliza
        
        try:
            return (InterfazAudio
                   .select()
                   .join(Personaliza, on=(Personaliza.interfaz == InterfazAudio.id_interfaz))
                   .where(Personaliza.configuracion == self.id_configuracion)
                   .get())
        except Exception as e:
            print(f"Error al obtener interfaz: {e}")
            return None

    def get_canales(self) -> List['Canal']:
        """
        Obtiene todos los canales asociados a esta configuración.
        
        Returns:
            List[Canal]: Lista de canales con sus parámetros
        """
        from model.canal import Canal
        try:
            return (Canal
                   .select()
                   .join(Establece, on=(Establece.canal == Canal.codigo_canal))
                   .where(Establece.configuracion == self.id_configuracion))
        except Exception as e:
            print(f"Error al obtener canales: {e}")
            return []

    def get_entradas(self) -> List['Entrada']:
        """
        Obtiene todas las entradas asociadas a esta configuración.
        
        Returns:
            List[Entrada]: Lista de entradas conectadas
        """
        from model.entrada import Entrada
        try:
            return (Entrada
                   .select()
                   .join(Conectado, on=(Conectado.entrada == Entrada.id_entrada))
                   .where(Conectado.configuracion == self.id_configuracion))
        except Exception as e:
            print(f"Error al obtener entradas: {e}")
            return []

    def actualizar_parametros_canal(self, canal: 'Canal', 
                                  volumen: float = None, 
                                  solo: bool = None, 
                                  mute: bool = None, 
                                  link: bool = None) -> bool:
        """
        Actualiza los parámetros de un canal específico en esta configuración.
        
        Args:
            canal (Canal): Canal a actualizar
            volumen (float, optional): Nuevo valor de volumen
            solo (bool, optional): Nuevo estado de solo
            mute (bool, optional): Nuevo estado de mute
            link (bool, optional): Nuevo estado de link
            
        Returns:
            bool: True si la actualización fue exitosa
        """
        try:
            establece = (Establece
                        .get((Establece.configuracion == self) & 
                             (Establece.canal == canal)))
            
            if volumen is not None:
                establece.volumen = volumen
            if solo is not None:
                establece.solo = solo
            if mute is not None:
                establece.mute = mute
            if link is not None:
                establece.link = link
                
            establece.save()
            return True
        except Establece.DoesNotExist:
            return False

    def save(self, *args, **kwargs):
        """
        Guarda la configuración actualizando el timestamp de modificación.
        """
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Representación en string de la configuración.
        """
        return f"Configuracion(id={self.id}, fecha={self.fecha})"


class Establece(BaseModel):
    """
    Modelo que representa la relación entre Configuracion y Canal,
    incluyendo los parámetros específicos de cada canal en la configuración.
    
    Attributes:
        configuracion (ForeignKeyField): Referencia a la configuración
        canal (ForeignKeyField): Referencia al canal
        volumen (FloatField): Nivel de volumen del canal
        solo (BooleanField): Estado de solo
        mute (BooleanField): Estado de mute
        link (BooleanField): Estado de link
    """
    
    configuracion = ForeignKeyField(
        Configuracion,
        backref='establece_set',
        column_name='ID_Configuracion',
        on_delete='CASCADE'
    )
    canal = DeferredForeignKey(
        'Canal',
        backref='establece_set',
        column_name='Codigo_Canal',
        on_delete='CASCADE'
    )
    volumen = FloatField(
        default=0.0,
        help_text="Nivel de volumen del canal"
    )
    solo = BooleanField(
        default=False,
        help_text="Estado de solo del canal"
    )
    mute = BooleanField(
        default=False,
        help_text="Estado de mute del canal"
    )
    link = BooleanField(
        default=False,
        help_text="Estado de link del canal"
    )

    class Meta:
        table_name = 'Establece'
        indexes = (
            (('configuracion', 'canal'), True),  # Índice único
        )


class Conectado(BaseModel):
    """
    Modelo que representa la relación entre Configuracion, Dispositivo y Entrada.
    
    Attributes:
        configuracion (ForeignKeyField): Referencia a la configuración
        dispositivo (ForeignKeyField): Referencia al dispositivo
        entrada (ForeignKeyField): Referencia a la entrada
    """

    id_conectado = IntegerField(
        primary_key=True,
        column_name='ID_Conectado',
        help_text="Identificador único de la conexión"
    )
    
    configuracion = ForeignKeyField(
        Configuracion,
        backref='conectado_set',
        column_name='ID_Configuracion',
        on_delete='CASCADE'
    )
    dispositivo = DeferredForeignKey(
        'Dispositivo',
        backref='conectado_set',
        column_name='ID_Dispositivo',
        on_delete='CASCADE'
    )
    entrada = DeferredForeignKey(
        'Entrada',
        backref='conectado_set',
        column_name='ID_Entrada',
        on_delete='CASCADE'
    )

    class Meta:
        table_name = 'Conectado'
        indexes = (
            (('configuracion', 'dispositivo', 'entrada'), True),  # Índice único
        )