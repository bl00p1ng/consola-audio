import streamlit as st
import logging
from typing import List, Optional
from datetime import datetime
import time
from model.base import get_database, initialize_database, database_connection
from model.frecuencia import Frecuencia
from model.tipo import Tipo
from model.fuente import Fuente, Clasifica, Maneja
from model.dispositivo import Dispositivo
from model.entrada import Entrada, Permite
from model.interfaz_audio import InterfazAudio, InterfazFrecuencia
from model.canal import Canal
from model.configuracion import Configuracion, Establece, Conectado
from model.usuario import Usuario, Personaliza

# Configuración de la página
st.set_page_config(page_title="Consola de Audio", layout="wide")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Usar @st.cache_resource para mantener la conexión viva
@st.cache_resource
def init_db():
    """
    Inicializa y retorna la conexión a la base de datos.
    """
    return get_database()

# Inicializar la base de datos al inicio
db = init_db()

# Función para crear estilos personalizados
def custom_css():
    return """
    <style>
    .custom-card {
        border-radius: 10px;
        margin: 10px 0;
    }
    .card-header {
       background: #f12711;
        background: -webkit-linear-gradient(to right, #f12711, #f5af19);
        background: linear-gradient(to right, #f12711, #f5af19);
        padding: 10px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .card-header svg {
        margin-right: 10px;
        width: auto;
        height: 35px;
    }
    .card-header h3 {
        padding-bottom: 0;
    }
    .card-body {
        padding: 0px 20px 10px 20px;
    }
    </style>
    """

def obtener_usuarios() -> List[Usuario]:
    """
    Obtiene todos los usuarios del sistema.
    """
    with database_connection():
        return list(Usuario.select())

def obtener_configuracion_usuario(usuario: Usuario) -> Optional[Configuracion]:
    """
    Obtiene la última configuración del usuario.
    """
    with database_connection():
        try:
            return (Configuracion
                    .select()
                    .join(
                        Personaliza,
                        on=(Configuracion.id_configuracion == Personaliza.configuracion)
                    )
                    .where(Personaliza.usuario == usuario.id_usuario)
                    .order_by(Configuracion.fecha.desc())
                    .first())
        except Exception as e:
            logger.error(f"Error al obtener configuración: {str(e)}")
            return None

def obtener_parametros_canal(canal: Canal, configuracion: Configuracion) -> dict:
    """
    Obtiene los parámetros de un canal para una configuración específica.
    """
    with database_connection():
        try:
            establece = (Establece
                        .get((Establece.canal == canal) &
                                (Establece.configuracion == configuracion)))
            return {
                'Volumen': establece.volumen,
                'Solo': establece.solo,
                'Mute': establece.mute,
                'Link': establece.link
            }
        except Establece.DoesNotExist:
            return {
                'Volumen': 0,
                'Solo': False,
                'Mute': False,
                'Link': False
        }

def guardar_cambios(configuracion: Configuracion, frecuencia: Frecuencia, entradas_data: dict, canales_data: dict) -> bool:
    """
    Guarda los cambios realizados en la configuración.
    
    Args:
        configuracion: Configuración actual
        frecuencia: Nueva frecuencia seleccionada
        entradas_data: Diccionario con los cambios en las entradas
        canales_data: Diccionario con los cambios en los canales
    """
    try:
        with database_connection():
            # 1. Actualizar la frecuencia de la interfaz
            interfaz = configuracion.get_interfaz()
            if interfaz:
                # Eliminar las frecuencias existentes
                InterfazFrecuencia.delete().where(
                    InterfazFrecuencia.interfaz == interfaz.id_interfaz
                ).execute()
                
                # Crear nueva relación con la frecuencia seleccionada
                InterfazFrecuencia.create(
                    interfaz=interfaz.id_interfaz,
                    frecuencia=frecuencia.id_frecuencia
                )

            # 2. Actualizar dispositivos en entradas
            for entrada_id, dispositivo_id in entradas_data.items():
                entrada = Entrada.get_by_id(entrada_id)
                if entrada:
                    entrada.set_dispositivo_configuracion(
                        configuracion.id_configuracion,
                        dispositivo_id
                    )

            # 3. Actualizar parámetros de canales
            for canal_id, params in canales_data.items():
                canal = Canal.get_by_id(canal_id)
                if canal:
                    # Actualizar fuente si se especificó
                    if 'fuente_id' in params:
                        Establece.update(
                            fuente=params['fuente_id']
                        ).where(
                            (Establece.canal == canal) &
                            (Establece.configuracion == configuracion)
                        ).execute()
                    
                    # Actualizar parámetros del canal
                    Establece.update({
                        Establece.volumen: params.get('volumen', 0),
                        Establece.solo: params.get('solo', False),
                        Establece.mute: params.get('mute', False),
                        Establece.link: params.get('link', False)
                    }).where(
                        (Establece.canal == canal) &
                        (Establece.configuracion == configuracion)
                    ).execute()

            return True
    except Exception as e:
        logger.error(f"Error al guardar cambios: {e}")
        return False
    
def get_nombre_fuente(fuente):
    """
    Obtiene el nombre formateado de una fuente.
    """
    if not fuente:
        return "Sin fuente"
    try:
        with database_connection():
            tipo = fuente.get_tipo()
            if tipo and hasattr(tipo, 'nombre'):
                return tipo.nombre
            return "Fuente sin tipo"
    except Exception as e:
        logger.error(f"Error al obtener nombre de fuente: {e}")
        return "Error al obtener tipo"

def main():
    # Inyectar CSS personalizado
    st.markdown(custom_css(), unsafe_allow_html=True)

    st.title('Consola de Audio')

    # Selección de usuario
    with database_connection():
        usuarios = list(obtener_usuarios())  # Convertir a lista para materializar la consulta

    usuario_seleccionado = st.selectbox(
        'Selecciona un usuario:',
        options=usuarios,
        format_func=lambda x: x.email
    )

    if usuario_seleccionado:
        # Obtener la última configuración del usuario
        with database_connection():
            configuracion = obtener_configuracion_usuario(usuario_seleccionado)
        
        if configuracion:
            with database_connection():
                interfaz = configuracion.get_interfaz()
                
               # Obtener entradas y canales y materializarlos en listas
                entradas = list(configuracion.get_entradas())
                canales = list(configuracion.get_canales())
            
            # Mostrar la interfaz de audio
            if interfaz:
                st.markdown(f"""
                <div class="custom-card">
                    <div class="card-header">
                        <h3>Interfaz de Audio: {interfaz.nombre_comercial}</h3>
                    </div>
                    <div class="card-body">
                        <p><b>Modelo:</b> {interfaz.modelo}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Cargar frecuencias
            with database_connection():
                frecuencias = list(Frecuencia.select())
                interfaz = configuracion.get_interfaz()
                # Obtener la frecuencia actual de la interfaz
                frecuencia_actual = None
                if interfaz:
                    try:
                        frecuencia_actual = (InterfazFrecuencia
                                            .select(InterfazFrecuencia.frecuencia)
                                            .where(InterfazFrecuencia.interfaz == interfaz.id_interfaz)
                                            .get()
                                            .frecuencia)
                    except InterfazFrecuencia.DoesNotExist:
                        pass

            nueva_frecuencia = st.selectbox(
                'Frecuencia (kHz):',
                options=frecuencias,
                index=frecuencias.index(frecuencia_actual) if frecuencia_actual in frecuencias else 0,
                format_func=lambda x: f"{x.valor} kHz"
            )

            # Dividir en columnas
            col1, col2 = st.columns(2)

            # Almacenar los cambios realizados
            cambios_entradas = {}
            cambios_canales = {}

            # Columna de Entradas
            with col1:
                st.subheader('Entradas')
                for entrada in entradas:
                    st.markdown(f"""
                    <div class="custom-card">
                        <div class="card-header">
                            <h3>Entrada {entrada.id_entrada}</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    dispositivos = list(Dispositivo.select())
                    dispositivo_actual = entrada.get_dispositivo_configuracion(configuracion.id)
                    dispositivo_seleccionado = st.selectbox(
                        'Dispositivo:',
                        options=dispositivos,
                        index=dispositivos.index(dispositivo_actual) if dispositivo_actual in dispositivos else 0,
                        format_func=lambda x: x.nombre,
                        key=f'dispositivo_{entrada.id_entrada}'
                    )

                    # Guardar cambio
                    cambios_entradas[entrada.id_entrada] = dispositivo_seleccionado.id_dispositivo

            # Columna de Canales
            with col2:
                st.subheader('Canales')
                for canal in canales:
                    with database_connection():
                        parametros = obtener_parametros_canal(canal, configuracion)
                        # fuentes = list(Fuente.select())
                        # fuente_actual = canal.get_fuente()
                        # tipos = list(Tipo.select())
                    
                    st.markdown(f"""
                    <div class="custom-card">
                        <div class="card-header">
                            <h3>Canal {canal.codigo_canal}</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    with database_connection():
                        fuentes = list(Fuente.select())
                        fuente_actual = canal.get_fuente()

                        # Obtener tipo actual si existe
                        tipo_actual = None
                        if fuente_actual:
                            tipo_actual = fuente_actual.get_tipo()

                        tipos = list(Tipo.select())

                    # Selector de tipo
                    tipo_seleccionado = st.selectbox(
                        'Tipo:',
                        options=tipos,
                        index=tipos.index(tipo_actual) if tipo_actual in tipos else 0,
                        format_func=lambda x: f"{x.id_tipo}" if x else "Sin tipo",  # Modificado para mostrar el ID
                        key=f'tipo_{canal.codigo_canal}'
                    )

                    # Filtrar fuentes por tipo seleccionado
                    with database_connection():
                        fuentes_filtradas = [
                            f for f in fuentes 
                            if f.get_tipo() and tipo_seleccionado and f.get_tipo().id_tipo == tipo_seleccionado.id_tipo
                        ]

                    # Si no hay fuentes filtradas, mostrar opción vacía
                    if not fuentes_filtradas:
                        fuentes_filtradas = [None]
                        fuente_actual = None

                    fuente_seleccionada = st.selectbox(
                        'Fuente:',
                        options=fuentes_filtradas,
                        index=fuentes_filtradas.index(fuente_actual) if fuente_actual in fuentes_filtradas else 0,
                        format_func=lambda x: get_nombre_fuente(x) if x else "Sin fuente",
                        key=f'fuente_{canal.codigo_canal}'
                    )

                    volumen_inicial = int(parametros['Volumen']) if isinstance(parametros['Volumen'], (int, float)) else 0
                    volumen = st.slider(
                        'Volumen:',
                        0, 100,
                        int(parametros['Volumen']),
                        1,
                        key=f'volumen_{canal.codigo_canal}'
                    )

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        solo = st.checkbox('Solo', parametros['Solo'], key=f'solo_{canal.codigo_canal}')
                    with col2:
                        mute = st.checkbox('Mute', parametros['Mute'], key=f'mute_{canal.codigo_canal}')
                    with col3:
                        link = st.checkbox('Link', parametros['Link'], key=f'link_{canal.codigo_canal}')

                    # Guardar cambios del canal
                    cambios_canales[canal.codigo_canal] = {
                        'fuente_id': fuente_seleccionada.id_fuente if fuente_seleccionada else None,
                        'volumen': volumen,
                        'solo': solo,
                        'mute': mute,
                        'link': link
                    }

            # Botón para guardar cambios
            if st.button('Guardar Cambios'):
                if guardar_cambios(configuracion, nueva_frecuencia, cambios_entradas, cambios_canales):
                    st.success('Cambios guardados exitosamente')
                    # Esperar un momento para que el usuario vea el mensaje
                    time.sleep(1)
                    # Actualizar el estado de la página sin recargarla
                    st.session_state.update_needed = True
                else:
                    st.error('Error al guardar los cambios')

        else:
            st.info('Este usuario no tiene configuraciones.')
    else:
        st.info('Por favor, selecciona un usuario para ver y editar su configuración.')

if __name__ == "__main__":
    main()