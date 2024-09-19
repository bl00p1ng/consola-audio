#Librerías
import sqlite3
from sqlite3 import Error

#Especificación de la ruta donde se encuentra la base de datos
especificacionRuta = 'db/Base_De_Datos.db'

#Construir una conexión
def crearConexion(rutaBD=especificacionRuta):
    try:
        conn = sqlite3.connect(rutaBD)
        
        # #Salida de diagnóstico
        # print("-------------------------")
        # print("Conexión realizada con éxito!")
        # print(f"Versión SQLite3: {sqlite3.version}")
        # print("-------------------------")       
        
    except Error as e:
        print("*Especificación del error generado al conectarse a la base de datos:")
        print(e)

    #Retornar instancia de la conexión    
    return conn