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
_database = None

def get_database() -> SqliteDatabase:
    """
    Obtiene la instancia de la base de datos, inicializándola si es necesario.
    """
    global _database
    if _database is None:
        _database = initialize_database()
        database_proxy.initialize(_database)
    return _database

def initialize_database(db_path: str = 'db/Base_De_Datos.db') -> SqliteDatabase:
    """
    Inicializa la conexión a la base de datos SQLite.
    """
    try:
        # Asegurar que el directorio de la base de datos existe
        db_directory = Path(db_path).parent
        db_directory.mkdir(parents=True, exist_ok=True)
        
        # Configurar la base de datos con pragmas recomendados para SQLite
        database = SqliteDatabase(
            db_path,
            pragmas={
                'journal_mode': 'wal',
                'foreign_keys': 1,
                'cache_size': -1024 * 64
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
    """
    database = get_database()
    was_closed = database.is_closed()
    
    if was_closed:
        database.connect()
    
    try:
        yield database
    except Exception as e:
        if not was_closed:
            database.rollback()
        logger.error(f"Error en la operación de base de datos: {e}")
        raise
    finally:
        if was_closed and not database.is_closed():
            database.close()

class BaseModel(Model):
    class Meta:
        database = database_proxy