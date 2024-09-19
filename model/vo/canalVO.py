from typing import Optional
from model.vo.FuenteVO import FuenteVO

class CanalVO:
    """
    Value Object que representa un Canal en el sistema de audio.
    
    Esta clase encapsula los datos de un canal, incluyendo su ID, etiqueta,
    volumen, estado de link, mute, solo y la fuente asociada.
    """

    def __init__(
            self, 
            pId: int = -1, 
            pEtiqueta: str = "", 
            pVolumen: float = -1.0, 
            pLink: bool = False, 
            pMute: bool = False, 
            pSolo: bool = False,
            pFuente: Optional[FuenteVO] = None
        ):
        """
        Inicializa una nueva instancia de CanalVO.

        Args:
            pId (int): Identificador único del canal. Por defecto es -1.
            pEtiqueta (str): Etiqueta descriptiva del canal. Por defecto es una cadena vacía.
            pVolumen (float): Nivel de volumen del canal. Por defecto es -1.0.
            pLink (bool): Estado de enlace del canal. Por defecto es False.
            pMute (bool): Estado de silencio del canal. Por defecto es False.
            pSolo (bool): Estado solo del canal. Por defecto es False.
            pFuente (Optional[FuenteVO]): Fuente asociada al canal. Por defecto es None.
        """
        self.__id = pId
        self.__etiqueta = pEtiqueta
        self.__volumen = pVolumen
        self.__link = pLink
        self.__mute = pMute
        self.__solo = pSolo
        self.__fuente = pFuente

    @property
    def id(self) -> int:
        """Obtiene el ID del canal."""
        return self.__id

    @property
    def etiqueta(self) -> str:
        """Obtiene la etiqueta del canal."""
        return self.__etiqueta

    @property
    def volumen(self) -> float:
        """Obtiene el nivel de volumen del canal."""
        return self.__volumen

    @property
    def link(self) -> bool:
        """Obtiene el estado de enlace del canal."""
        return self.__link

    @property
    def mute(self) -> bool:
        """Obtiene el estado de silencio del canal."""
        return self.__mute

    @property
    def solo(self) -> bool:
        """Obtiene el estado solo del canal."""
        return self.__solo

    @property
    def fuente(self) -> Optional[FuenteVO]:
        """Obtiene la fuente asociada al canal."""
        return self.__fuente

    def setEtiqueta(self, nEtiqueta: str) -> None:
        """Establece una nueva etiqueta para el canal."""
        self.__etiqueta = nEtiqueta

    def setVolumen(self, nVolumen: float) -> None:
        """Establece un nuevo nivel de volumen para el canal."""
        self.__volumen = nVolumen  # Corregido: era self.__etiqueta = nVolumen

    def setLink(self, nLink: bool) -> None:
        """Establece el estado de enlace del canal."""
        self.__link = nLink

    def setMute(self, nMute: bool) -> None:
        """Establece el estado de silencio del canal."""
        self.__mute = nMute

    def setSolo(self, nSolo: bool) -> None:
        """Establece el estado solo del canal."""
        self.__solo = nSolo

    def setFuente(self, nFuente: Optional[FuenteVO]) -> None:
        """Establece la fuente asociada al canal."""
        self.__fuente = nFuente

    def conectar(self) -> None:
        """Método para conectar el canal (implementación pendiente)."""
        pass

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del canal.

        Returns:
            str: Representación del canal en formato de cadena.
        """
        return (f'ID: {self.__id}\n'
                f'Etiqueta: {self.__etiqueta}\n'
                f'Volumen: {self.__volumen}\n'
                f'Link: {self.__link}\n'
                f'Mute: {self.__mute}\n'
                f'Solo: {self.__solo}\n'
                f'Fuente: {self.__fuente}\n')

    def __eq__(self, other: object) -> bool:
        """
        Compara este canal con otro objeto para determinar si son iguales.

        Args:
            other (object): Objeto a comparar con este canal.

        Returns:
            bool: True si son iguales, False en caso contrario.
        """
        if not isinstance(other, CanalVO):
            return False
        return self.__id == other.id

    def __hash__(self) -> int:
        """
        Calcula el hash del canal basado en su ID.

        Returns:
            int: Valor hash del canal.
        """
        return hash(self.__id)