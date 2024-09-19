from typing import List
from datetime import datetime
from model.vo.UsuarioVO import UsuarioVO
from model.vo.InterfazAudioVO import InterfazAudioVO
from model.vo.canalVO import CanalVO
from model.vo.DispositivoVO import DispositivoVO

class ConfiguracionVO:
    def __init__(self, ID: int = -1, Fecha: datetime = datetime.now()):
        self.__ID = ID
        self.__Fecha = Fecha
        self.__usuario: UsuarioVO = None
        self.__interfaz: InterfazAudioVO = None
        self.__canales: List[CanalVO] = []
        self.__entradas: List[DispositivoVO] = []

    @property
    def ID(self) -> int:
        return self.__ID

    @property
    def Fecha(self) -> datetime:
        return self.__Fecha

    def setFecha(self, Fecha: datetime) -> None:
        self.__Fecha = Fecha

    def getUsuario(self) -> UsuarioVO:
        return self.__usuario

    def setUsuario(self, usuario: UsuarioVO) -> None:
        self.__usuario = usuario

    def getInterfaz(self) -> InterfazAudioVO:
        return self.__interfaz

    def setInterfaz(self, interfaz: InterfazAudioVO) -> None:
        self.__interfaz = interfaz

    def getCanales(self) -> List[CanalVO]:
        return self.__canales

    def setCanales(self, canales: List[CanalVO]) -> None:
        self.__canales = canales

    def getEntradas(self) -> List[DispositivoVO]:
        return self.__entradas

    def setEntradas(self, entradas: List[DispositivoVO]) -> None:
        self.__entradas = entradas

    def ajustarVolumen(self, canal: CanalVO, nuevoVolumen: float) -> bool:
        for c in self.__canales:
            if c.id == canal.id:
                c.setVolumen(nuevoVolumen)
                return True
        return False

    def cargarConfiguracion(self) -> bool:
        # Este método sería una simulación de carga de configuración
        # En una implementación real, aquí se aplicarían los cambios al sistema
        print(f"Cargando configuración: {self.__ID}")
        return True

    def __str__(self) -> str:
        return (f"Configuración ID: {self.__ID}\n"
                f"Fecha: {self.__Fecha}\n"
                f"Usuario: {self.__usuario}\n"
                f"Interfaz: {self.__interfaz}\n"
                f"Canales: {len(self.__canales)}\n"
                f"Entradas: {len(self.__entradas)}")