from model.vo.FrecuenciaVO import FrecuenciaVO

class InterfazAudioVO:
    def __init__(
            self,
            pId: int=-1,
            pNombreCorto: str="",
            pModelo: str="",
            pNombreComercial: str="",
            pPrecio: float= 0.0,
            pFrecuencia: FrecuenciaVO = None
        ):
        self.__id= pId
        self.__nombreCorto= pNombreCorto
        self.__modelo= pModelo
        self.__nombreComercial= pNombreComercial
        self.__precio= pPrecio
        self.__frecuencia = pFrecuencia
        
    @property
    def id(self):
        return self.__id
    
    @property
    def frecuencia(self):
        return self.frecuencia
    
    @property
    def nombreCorto(self):
        return self.__nombreCorto
    
    @property
    def modelo(self):
        return self.__modelo
    
    @property
    def nombreComercial(self):
        return self.__nombreComercial
    
    @property
    def precio(self):
        return self.__precio
    
    def setFrecuencia(self, nFrecuencia):
        self.__frecuencia = nFrecuencia
        
    def setNombreCorto(self, nNombreCorto):
        self.__nombreCorto = nNombreCorto
    
    def __str__(self) -> str:
        return f'ID: {self.__id}, Nombre Corto: {self.__nombreCorto}, Modelo: {self.__modelo}, Nombre Comercial: {self.__nombreComercial}, Precio: {self.__precio}, Frecuencia: {self.__frecuencia}'