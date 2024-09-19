class TipoVO:
    def __init__(
            self,
            pId: int= -1,
            pNombre: str="",
            pDescripcion: str=""
        ):
        self.__id = pId
        self.nombre = pNombre
        self.descripcion = pDescripcion
        
    @property
    def nombre(self):
        return self.nombre
    
    @property
    def descripcion(self):
        return self.descripcion
    
    def setNombre(self, nNombre):
        self.nombre = nNombre
        
    def setDescripcion(self, nDescripcion):
        self.descripcion = nDescripcion
        
    def __str__(self) -> str:
        return f'ID: {self.__id}, Etiqueta: {self.nombre}, Descripción: {self.descripcion}'