class DispositivoVO:
    def __init__(self, pID_Dispo: int, pNombre: str = "", pDescripcion: str = ""):
        self.__Id = pID_Dispo
        self.__Nombre = pNombre
        self.__Descripcion = pDescripcion
    
    @property
    def Id(self):
        return self.__Id
    
    @property
    def Nombre(self):
        return self.__Nombre
    
    @property
    def Descripcion(self):
        return self.__Descripcion

    def setNombre(self, pNombre: str):
        self.__Nombre = pNombre

    def setDescripcion(self, pDescripcion: str):
        self.__Descripcion = pDescripcion

    def __str__(self) -> str:
        return f'ID: {self.__Id}\n Nombre: {self.__Nombre}\n Descripcion:{self.__Descripcion}\n'

    def to_dict(self) -> dict:
        return {
            "Id": self.__Id,
            "Nombre": self.__Nombre,
            "Descripcion": self.__Descripcion
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DispositivoVO':
        return cls(
            pID_Dispo=data.get('Id', -1),
            pNombre=data.get('Nombre', ''),
            pDescripcion=data.get('Descripcion', '')
        )