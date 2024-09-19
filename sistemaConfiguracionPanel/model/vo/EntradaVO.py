from model.vo.DispositivoVO import DispositivoVO

class EntradaVO:
    def __init__(self, pId: int = -1, pDispositivo: DispositivoVO = None, pEtiqueta: str = "", pDescripcion: str = ""):
        self.__id = pId
        self.__dispositivo = pDispositivo
        self.__etiqueta = pEtiqueta
        self.__descripcion = pDescripcion

    @property
    def id(self):
        return self.__id

    @property
    def dispositivo(self):
        return self.__dispositivo

    @property
    def etiqueta(self):
        return self.__etiqueta

    @property
    def descripcion(self):
        return self.__descripcion

    def setDispositivo(self, pDispositivo: DispositivoVO):
        self.__dispositivo = pDispositivo

    def setEtiqueta(self, pEtiqueta: str):
        self.__etiqueta = pEtiqueta

    def setDescripcion(self, pDescripcion: str):
        self.__descripcion = pDescripcion

    def __str__(self) -> str:
        return f'ID: {self.__id}, Etiqueta: {self.__etiqueta}, Descripción: {self.__descripcion}, Dispositivo: {self.__dispositivo}'