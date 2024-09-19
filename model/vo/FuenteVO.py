from model.vo.TipoVO import TipoVO

class FuenteVO:
    def __init__(
            self,
            pId: int=-1,
            pTipo: TipoVO = None
        ):
        self.__id = pId
        self.tipo = pTipo
        
    @property
    def id(self):
        return self.__id
    
    @property
    def tipo(self):
        return self.tipo
    
    def setTipo(self, nTipo):
        self.tipo = nTipo
        
    def __str__(self) -> str:
        return f'ID: {self.__id}, Tipo: {self.tipo}'