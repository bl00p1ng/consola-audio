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

    def to_dict(self) -> dict:
        """
        Convierte la entrada a un diccionario.

        Returns:
            dict: Un diccionario que representa la entrada.
        """
        return {
            "id": self.__id,
            "dispositivo": self.__dispositivo.to_dict() if self.__dispositivo else None,
            "etiqueta": self.__etiqueta,
            "descripcion": self.__descripcion
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'EntradaVO':
        """
        Crea una instancia de EntradaVO a partir de un diccionario.

        Args:
            data (dict): Un diccionario que contiene los datos de la entrada.

        Returns:
            EntradaVO: Una nueva instancia de EntradaVO.
        """
        return cls(
            pId=data.get('id', -1),
            pDispositivo=DispositivoVO.from_dict(data['dispositivo']) if data.get('dispositivo') else None,
            pEtiqueta=data.get('etiqueta', ''),
            pDescripcion=data.get('descripcion', '')
        )