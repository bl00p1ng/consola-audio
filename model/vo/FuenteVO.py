from model.vo.TipoVO import TipoVO

class FuenteVO:
    def __init__(
            self,
            pId: int=-1,
            pTipo: TipoVO = None
        ):
        self.__id = pId
        self.__tipo = pTipo
        
    @property
    def id(self):
        return self.__id
    
    @property
    def tipo(self):
        return self.__tipo
    
    def setTipo(self, nTipo):
        self.__tipo = nTipo
        
    def __str__(self) -> str:
        return f'ID: {self.__id}, Tipo: {self.__tipo}'