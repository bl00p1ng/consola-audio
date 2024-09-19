import sys
from model.dao.UsuarioDAO import UsuarioDAO
from model.dao.ConfiguracionDAO import ConfiguracionDAO
from model.vo.UsuarioVO import UsuarioVO

def mostrar_configuracion_usuario(id_usuario):
    usuario_dao = UsuarioDAO()
    configuracion_dao = ConfiguracionDAO()

    # Obtener el usuario
    usuario = usuario_dao.getUsuario(UsuarioVO(uId=id_usuario))
    if not usuario:
        print(f"No se encontró un usuario con ID {id_usuario}")
        return

    print(f"\n{'='*50}")
    print(f"Configuración del Usuario: {usuario.getEmail()}")
    print(f"{'='*50}\n")

    # Obtener las configuraciones del usuario
    configuraciones = configuracion_dao.getConfiguracionesPorUsuario(usuario)

    if not configuraciones:
        print("Este usuario no tiene configuraciones guardadas.")
        return

    for config in configuraciones:
        print(f"\n{'-'*50}")
        print(f"Configuración ID: {config.getID()}")
        print(f"Fecha: {config.getFecha()}")
        print(f"{'-'*50}")

        # Mostrar detalles de la interfaz de audio
        interfaz = config.getInterfaz()
        print(f"\nInterfaz de Audio:")
        print(f"  Nombre: {interfaz.nombreComercial}")
        print(f"  Modelo: {interfaz.modelo}")
        print(f"  Frecuencia: {interfaz.frecuencia.valor} Hz")

        # Mostrar canales
        print(f"\nCanales:")
        for canal in config.getCanales():
            print(f"  Canal {canal.id}:")
            print(f"    Etiqueta: {canal.etiqueta}")
            print(f"    Volumen: {canal.volumen}")
            print(f"    Mute: {'Sí' if canal.mute else 'No'}")
            print(f"    Solo: {'Sí' if canal.solo else 'No'}")
            print(f"    Link: {'Sí' if canal.link else 'No'}")
            if canal.fuente:
                print(f"    Fuente: {canal.fuente.tipo.nombre}")

        # Mostrar entradas
        print(f"\nEntradas:")
        for entrada in config.getEntradas():
            print(f"  Dispositivo: {entrada.dispositivo.Nombre}")
            print(f"    Descripción: {entrada.dispositivo.Descripcion}")

        print(f"\n{'='*50}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <id_usuario>")
        sys.exit(1)

    try:
        id_usuario = int(sys.argv[1])
        mostrar_configuracion_usuario(id_usuario)
    except ValueError:
        print("Error: El ID de usuario debe ser un número entero.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)
        