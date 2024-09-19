from datetime import datetime
from typing import Optional, List
from model.vo.UsuarioVO import UsuarioVO
from model.vo.InterfazAudioVO import InterfazAudioVO
from model.vo.canalVO import CanalVO
from model.vo.EntradaVO import EntradaVO

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
        self.__Canales: List[CanalVO] = []
        self.__Entradas: List[EntradaVO] = []

    def getID(self) -> int:
        """
        Obtiene el ID de la configuración.

        Returns:
            int: El ID de la configuración.
        """
        return self.__ID

    def getFecha(self) -> datetime:
        """
        Obtiene la fecha de la configuración.

        Returns:
            datetime: La fecha de la configuración.
        """
        return self.__Fecha

    def setFecha(self, Fecha: datetime) -> None:
        """
        Establece la fecha de la configuración.

        Args:
            Fecha (datetime): La nueva fecha de la configuración.
        """
        self.__Fecha = Fecha

    def getUsuario(self) -> Optional[UsuarioVO]:
        """
        Obtiene el usuario asociado a la configuración.

        Returns:
            Optional[UsuarioVO]: El usuario asociado a la configuración, o None si no hay ninguno.
        """
        return self.__Usuario

    def setUsuario(self, Usuario: UsuarioVO) -> None:
        """
        Establece el usuario asociado a la configuración.

        Args:
            Usuario (UsuarioVO): El nuevo usuario a asociar con la configuración.
        """
        self.__Usuario = Usuario

    def getInterfaz(self) -> Optional[InterfazAudioVO]:
        """
        Obtiene la interfaz de audio asociada a la configuración.

        Returns:
            Optional[InterfazAudioVO]: La interfaz de audio asociada a la configuración, o None si no hay ninguna.
        """
        return self.__Interfaz

    def setInterfaz(self, Interfaz: InterfazAudioVO) -> None:
        """
        Establece la interfaz de audio asociada a la configuración.

        Args:
            Interfaz (InterfazAudioVO): La nueva interfaz de audio a asociar con la configuración.
        """
        self.__Interfaz = Interfaz

    def getCanales(self) -> List[CanalVO]:
        """
        Obtiene los canales asociados a la configuración.
        
        Returns:
            List[CanalVO]: Una lista con los canales asociados a la configuración.
        """
        return self.__Canales

    def getEntradas(self) -> List[EntradaVO]:
        """
        Obtiene las entradas asociadas a la configuración.

        Returns:
            List[EntradaVO]: Una lista con las entradas asociadas a la configuración.
        """
        return self.__Entradas

    def setCanales(self, canales: List[CanalVO]) -> None:
        """
        Establece la lista completa de canales de la configuración.

        Args:
            canales (List[CanalVO]): La nueva lista de canales.
        """
        self.__Canales = canales

    def setEntradas(self, entradas: List[EntradaVO]) -> None:
        """
        Establece la lista completa de entradas de la configuración.

        Args:
            entradas (List[EntradaVO]): La nueva lista de entradas.
        """
        self.__Entradas = entradas

    def setCanal(self, canal: CanalVO) -> None:
        """
        Agrega un canal a la configuración.

        Args:
            canal (CanalVO): El canal a agregar.
        """
        self.__Canales.append(canal)

    def setEntrada(self, entrada: EntradaVO) -> None:
        """
        Agrega una entrada a la configuración.

        Args:
            entrada (EntradaVO): La entrada a agregar.
        """
        self.__Entradas.append(entrada)

    def __str__(self) -> str:
        return (f"Configuración ID: {self.__ID}, "
                f"Fecha: {self.__Fecha}, "
                f"Usuario: {self.__Usuario.getEmail() if self.__Usuario else 'No asignado'}, "
                f"Interfaz: {self.__Interfaz.getNombreCorto() if self.__Interfaz else 'No asignada'}, "
                f"Canales: {len(self.__Canales)}, "
                f"Entradas: {len(self.__Entradas)}")

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
            "Interfaz": self.__Interfaz.to_dict() if self.__Interfaz else None,
            "Canales": [canal.to_dict() for canal in self.__Canales],
            "Entradas": [entrada.to_dict() for entrada in self.__Entradas]
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
        config = cls(
            ID=data.get('ID', -1),
            Fecha=datetime.fromisoformat(data['Fecha']) if 'Fecha' in data else datetime.now(),
            Usuario=UsuarioVO.from_dict(data['Usuario']) if data.get('Usuario') else None,
            Interfaz=InterfazAudioVO.from_dict(data['Interfaz']) if data.get('Interfaz') else None
        )
        config.setCanales([CanalVO.from_dict(canal) for canal in data.get('Canales', [])])
        config.setEntradas([EntradaVO.from_dict(entrada) for entrada in data.get('Entradas', [])])
        return config