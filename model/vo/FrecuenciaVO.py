class FrecuenciaVO:
    
    
    def __init__(self, pId: int=-1, pValor: float=-1.0):
        self.__id = pId
        self.__valor = pValor
    
    @property
    def id(self):
        # Desarrollar lógica de validación
        return self.__id
    
    @property
    def valor(self):
        # Desarrollar lógica de validación
        return self.__valor
    
    def setValor(self,pValor:float):
        self.__valor = pValor

    def __str__(self) -> str:
        return f'ID: {self.__id}\n Valor: {self.__valor}\n'
        
        
# #Ejemplo de uso del value object
# frecuencia = FrecuenciaVO(33,444.000)
# print(f"ID -> {frecuencia.id}")
# print(f"Valor -> {frecuencia.valor}")
