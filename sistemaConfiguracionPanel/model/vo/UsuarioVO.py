# UsuarioVO.py

class UsuarioVO:
    def __init__(self, uId: int = -1, email: str = "", password: str = ""):
        self.__id = uId
        self.__email = email
        self.__password = password

    def getId(self) -> int:
        return self.__id

    def getEmail(self) -> str:
        return self.__email
    
    def getPassword(self) -> str:
        return self.__password
    
    def setEmail(self, email: str) -> None:
        self.__email = email
    
    def setPassword(self, password: str) -> None:
        self.__password = password
        
    def __str__(self) -> str:
        return f"Usuario ID: {self.__id}, Email: {self.__email}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "email": self.__email,
            # No incluimos la contraseña por razones de seguridad
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'UsuarioVO':
        return cls(
            uId=data.get('id', -1),
            email=data.get('email', ''),
            password=data.get('password', '')  # Tener cuidado con esto en un entorno real
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UsuarioVO):
            return False
        return self.__id == other.getId() and self.__email == other.getEmail()

    def __hash__(self) -> int:
        return hash((self.__id, self.__email))