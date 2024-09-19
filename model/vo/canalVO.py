
class CanalVO:
    def __init__(
            self, 
            pId: int=-1, 
            pEtiqueta: str="", 
            pVolumen: float=-1.0, 
            pLink: bool=False, 
            pMute: bool=False, 
            pSolo: bool=False
        ):
        self.__id = pId
        self.__etiqueta = pEtiqueta
        self.__volumen = pVolumen
        self.__link = pLink
        self.__mute = pMute
        self.__solo = pSolo


    @property
    def id(self):
        return self.__id

    @property
    def etiqueta(self):
        return self.__etiqueta

    @property
    def volumen(self):
        return self.__volumen

    @property
    def link(self):
        return self.__link

    @property
    def mute(self):
        return self.__mute

    @property
    def solo(self):
        return self.__solo
    
    def setEtiqueta(self, nEtiqueta):
        self.__etiqueta = nEtiqueta

    def setVolumen(self, nVolumen):
        self.__etiqueta = nVolumen

    def setLink(self, nLink):
        self.__link = nLink

    def setMute(self, nMute):
        self.__mute = nMute

    def setSolo(self, nSolo):
        self.__solo = nSolo

    def conectar():
        pass

    def __str__(self) -> str:
        return f'ID: {self.__id}\n Etiqueta: {self.__etiqueta}\n Volumen:{self.__volumen}\n Link: {self.__link}\n Mute: {self.__mute}\n Solo: {self.__solo}\n'
    
    