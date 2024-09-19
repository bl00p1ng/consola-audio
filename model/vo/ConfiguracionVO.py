from datetime import datetime
from typing import Optional
from model.vo.UsuarioVO import UsuarioVO
from model.vo.InterfazAudioVO import InterfazAudioVO

class ConfiguracionVO:
    def __init__(self, ID: int = -1, Fecha: datetime = datetime.now(), 
                 Usuario: Optional[UsuarioVO] = None, 
                 Interfaz: Optional[InterfazAudioVO] = None):
        """
        Inicializa una nueva instancia de ConfiguracionVO.

        Args:
            ID (int): Identificador único de la configuración. Por defecto es -1.
            Fecha (datetime): Fecha de la configuración. Por defecto es la fecha actual.
            Usuario (Optional[UsuarioVO]): Usuario asociado a la configuración. Por defecto es None.
            Interfaz (Optional[InterfazAudioVO]): Interfaz de audio asociada a la configuración. Por defecto es None.
        """
        self.__ID = ID
        self.__Fecha = Fecha
        self.__Usuario = Usuario
        self.__Interfaz = Interfaz

    @property
    def ID(self) -> int:
        """
        Obtiene el ID de la configuración.

        Returns:
            int: El ID de la configuración.
        """
        return self.__ID

    @property
    def Fecha(self) -> datetime:
        """
        Obtiene la fecha de la configuración.

        Returns:
            datetime: La fecha de la configuración.
        """
        return self.__Fecha

    @Fecha.setter
    def Fecha(self, Fecha: datetime) -> None:
        """
        Establece la fecha de la configuración.

        Args:
            Fecha (datetime): La nueva fecha de la configuración.
        """
        self.__Fecha = Fecha

    @property
    def Usuario(self) -> Optional[UsuarioVO]:
        """
        Obtiene el usuario asociado a la configuración.

        Returns:
            Optional[UsuarioVO]: El usuario asociado a la configuración, o None si no hay ninguno.
        """
        return self.__Usuario

    @Usuario.setter
    def Usuario(self, Usuario: UsuarioVO) -> None:
        """
        Establece el usuario asociado a la configuración.

        Args:
            Usuario (UsuarioVO): El nuevo usuario a asociar con la configuración.
        """
        self.__Usuario = Usuario

    @property
    def Interfaz(self) -> Optional[InterfazAudioVO]:
        """
        Obtiene la interfaz de audio asociada a la configuración.

        Returns:
            Optional[InterfazAudioVO]: La interfaz de audio asociada a la configuración, o None si no hay ninguna.
        """
        return self.__Interfaz

    @Interfaz.setter
    def Interfaz(self, Interfaz: InterfazAudioVO) -> None:
        """
        Establece la interfaz de audio asociada a la configuración.

        Args:
            Interfaz (InterfazAudioVO): La nueva interfaz de audio a asociar con la configuración.
        """
        self.__Interfaz = Interfaz

    def __str__(self) -> str:
        """
        Retorna una representación en cadena de la configuración.

        Returns:
            str: Una cadena que representa la configuración.
        """
        return (f"Configuración ID: {self.__ID}, "
                f"Fecha: {self.__Fecha}, "
                f"Usuario: {self.__Usuario.getEmail() if self.__Usuario else 'No asignado'}, "
                f"Interfaz: {self.__Interfaz.nombreCorto if self.__Interfaz else 'No asignada'}")

    def to_dict(self) -> dict:
        """
        Convierte la configuración a un diccionario.

        Returns:
            dict: Un diccionario que representa la configuración.
        """
        return {
            "ID": self.__ID,
            "Fecha": self.__Fecha.isoformat(),
            "Usuario": self.__Usuario.to_dict() if self.__Usuario else None,
            "Interfaz": self.__Interfaz.to_dict() if self.__Interfaz else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ConfiguracionVO':
        """
        Crea una instancia de ConfiguracionVO a partir de un diccionario.

        Args:
            data (dict): Un diccionario que contiene los datos de la configuración.

        Returns:
            ConfiguracionVO: Una nueva instancia de ConfiguracionVO.
        """
        return cls(
            ID=data.get('ID', -1),
            Fecha=datetime.fromisoformat(data['Fecha']) if 'Fecha' in data else datetime.now(),
            Usuario=UsuarioVO.from_dict(data['Usuario']) if data.get('Usuario') else None,
            Interfaz=InterfazAudioVO.from_dict(data['Interfaz']) if data.get('Interfaz') else None
        )