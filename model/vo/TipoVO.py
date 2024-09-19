class TipoVO:
    def __init__(
            self,
            pId: int= -1,
            pNombre: str="",
            pDescripcion: str=""
        ):
        self.__id = pId
        self.__nombre = pNombre
        self.__descripcion = pDescripcion
        
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    def setNombre(self, nNombre):
        self.__nombre = nNombre
        
    def setDescripcion(self, nDescripcion):
        self.__descripcion = nDescripcion
        
    def __str__(self) -> str:
        return f'ID: {self.__id}, Etiqueta: {self.nombre}, Descripción: {self.descripcion}'