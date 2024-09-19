#Autores: Nicolas Cardona, kevin munoz oviedo y Alejandro Correa
class DispositivoVO:

    def __init__(self,pID_Dispo:int,pNombre:str,pDescripcion:str):
        self.__Id= pID_Dispo
        self.__Nombre= pNombre
        self.__Descripcion= pDescripcion
    
    @property
    def Id(self):
        #Desarrollar logica de validación
        return self.__Id
    
    @property
    def Nombre(self):
        return self.__Nombre
    
    @property
    def Descripcion(self):
        return self.__Descripcion

    def setNombre(self,pNombre:str):
        self.__Nombre = pNombre

    def setDescripcion(self,pDescripcion:str):
        self.__Descripcion = pDescripcion

    def __str__(self) -> str:
        return f'ID: {self.__Id}\n Nombre: {self.__Nombre}\n Descripcion:{self.__Descripcion}\n'