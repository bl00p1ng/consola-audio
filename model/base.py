from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Generator

from peewee import Model, SqliteDatabase, DatabaseProxy, DeferredForeignKey

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

database_proxy = DatabaseProxy()

class BaseModel(Model):
    """
    Modelo base para todos los modelos de la aplicación.
    
    Proporciona funcionalidad común y configuración para todos los modelos
    que heredarán de esta clase. Utiliza el proxy de base de datos para
    permitir la configuración dinámica de la conexión.
    """
    
    class Meta:
        database = database_proxy
    
    @classmethod
    def get_by_id_or_none(cls, id):
        """
        Obtiene un registro por su ID o retorna None si no existe.
        
        Args:
            id: Identificador del registro a buscar.
            
        Returns:
            Model or None: Instancia del modelo si se encuentra, None en caso contrario.
        """
        try:
            return cls.get_by_id(id)
        except cls.DoesNotExist:
            return None

def initialize_database(db_path: str = 'db/Base_De_Datos.db') -> SqliteDatabase:
    """
    Inicializa la conexión a la base de datos SQLite.
    
    Args:
        db_path (str): Ruta al archivo de la base de datos SQLite.
        
    Returns:
        SqliteDatabase: Instancia de la base de datos configurada.
        
    Raises:
        RuntimeError: Si hay un error al inicializar la base de datos.
    """
    try:
        # Asegurar que el directorio de la base de datos existe
        db_directory = Path(db_path).parent
        db_directory.mkdir(parents=True, exist_ok=True)
        
        # Configurar la base de datos con pragmas recomendados para SQLite
        database = SqliteDatabase(
            db_path,
            pragmas={
                'journal_mode': 'wal',  # Mejor concurrencia
                'foreign_keys': 1,      # Habilitar claves foráneas
                'cache_size': -1024 * 64  # 64MB de caché
            }
        )
        
        # Inicializar el proxy con la instancia real de la base de datos
        database_proxy.initialize(database)
        
        logger.info(f"Base de datos inicializada exitosamente en: {db_path}")
        return database
        
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise RuntimeError(f"No se pudo inicializar la base de datos: {e}")

@contextmanager
def database_connection() -> Generator[SqliteDatabase, None, None]:
    """
    Context manager para manejar la conexión a la base de datos.
    
    Garantiza que la conexión se abre y cierra apropiadamente, y maneja
    las transacciones automáticamente.
    
    Yields:
        SqliteDatabase: Instancia de la base de datos conectada.
    """
    database = database_proxy.obj
    
    if database.is_closed():
        database.connect()
    
    try:
        yield database
    except Exception as e:
        if not database.is_closed():
            database.rollback()
        logger.error(f"Error en la operación de base de datos: {e}")
        raise
    finally:
        if not database.is_closed():
            database.close()

# def create_tables(models: list) -> None:
#     """
#     Crea las tablas en la base de datos para los modelos especificados.
    
#     Args:
#         models (list): Lista de clases de modelos Peewee a crear.
        
#     Raises:
#         RuntimeError: Si hay un error al crear las tablas.
#     """
#     try:
#         with database_connection() as db:
#             db.create_tables(models, safe=True)
#             logger.info("Tablas creadas exitosamente")
#     except Exception as e:
#         logger.error(f"Error al crear las tablas: {e}")
#         raise RuntimeError(f"No se pudieron crear las tablas: {e}")