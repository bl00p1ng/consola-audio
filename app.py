import streamlit as st
import logging
from typing import List, Optional
from datetime import datetime

from model.base import initialize_database, database_connection
from model.frecuencia import Frecuencia
from model.tipo import Tipo
from model.fuente import Fuente, Clasifica, Maneja
from model.dispositivo import Dispositivo
from model.entrada import Entrada, Permite
from model.interfaz_audio import InterfazAudio, InterfazFrecuencia
from model.canal import Canal
from model.configuracion import Configuracion, Establece, Conectado
from model.usuario import Usuario, Personaliza


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

db = initialize_database()

@st.cache_resource
def obtener_db():
    return initialize_database()

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

# Función para guardar configuraciones en la base de datos
def guardar_cambios(configuracion, nueva_frecuencia, entrada_dispositivos, canal_fuentes):
    try:
        # Actualizar frecuencia
        configuracion.interfaz_audio.frecuencia = nueva_frecuencia
        configuracion.interfaz_audio.save()
        
        # Actualizar dispositivos en entradas
        for entrada, dispositivo in entrada_dispositivos.items():
            entrada.set_dispositivo_configuracion(configuracion.id, dispositivo)

        # Actualizar fuentes y parámetros en canales
        for canal, fuente_tipo in canal_fuentes.items():
            canal.set_fuente(fuente_tipo["fuente"])
            canal.save() # Guarda otros parámetros

        st.success("Cambios guardados exitosamente")
    except Exception as e:
        st.error("Error al guardar cambios")





def main():
    # Configuración de la página
    st.set_page_config(page_title="Consola de Audio", layout="wide")

    # Conectar a la base de datos si está cerrada
    db = obtener_db()
    if db.is_closed():
        db.connect()


    # Inyectar CSS personalizado
    st.markdown(custom_css(), unsafe_allow_html=True)

    st.title('Consola de Audio')

    # Selección de usuario
    usuarios = obtener_usuarios()  # Llama a la función fuera del contexto de Streamlit
    usuario_seleccionado = st.selectbox(
        'Selecciona un usuario:',
        options=usuarios,
        format_func=lambda x: x.email
    )

    if usuario_seleccionado:
        # Obtener la última configuración del usuario fuera de Streamlit
        configuracion = obtener_configuracion_usuario(usuario_seleccionado)
        
        if configuracion:
            interfaz = configuracion.get_interfaz()
            
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
            frecuencias = list(Frecuencia.select())
            frecuencia_actual = interfaz.frecuencia if hasattr(interfaz, 'frecuencia') else None
            nueva_frecuencia = st.selectbox(
                'Frecuencia (kHz):',
                options=frecuencias,
                index=frecuencias.index(frecuencia_actual) if frecuencia_actual in frecuencias else 0,
                format_func=lambda x: f"{x.valor} kHz"
            )

            # Dividir en columnas
            col1, col2 = st.columns(2)

            # Columna de Entradas
            with col1:
                st.subheader('Entradas')
                entradas = configuracion.get_entradas()  # Llama antes de Streamlit
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
                    st.selectbox(
                        'Dispositivo:',
                        options=dispositivos,
                        index=dispositivos.index(dispositivo_actual) if dispositivo_actual in dispositivos else 0,
                        format_func=lambda x: x.nombre,
                        key=f'dispositivo_{entrada.id_entrada}'
                    )

            # Columna de Canales
            with col2:
                st.subheader('Canales')
                canales = configuracion.get_canales()  # Llama antes de Streamlit
                for canal in canales:
                    parametros = obtener_parametros_canal(canal, configuracion)
                    
                    st.markdown(f"""
                    <div class="custom-card">
                        <div class="card-header">
                            <h3>Canal {canal.codigo_canal}</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    fuentes = list(Fuente.select())
                    fuente_actual = canal.get_fuente()
                    fuente = st.selectbox(
                        'Tipo:',
                        options=fuentes,
                        index=fuentes.index(fuente_actual) if fuente_actual in fuentes else 0,
                        format_func=lambda x: x.get_tipo() if x.get_tipo() else "Sin tipo",
                        key=f'tipo_{canal.codigo_canal}'
                    )

                    if fuente:
                        tipos = list(Tipo.select())
                        tipo_actual = fuente.get_tipo()
                        st.selectbox(
                            'Fuente:',
                            options=tipos,
                            index=tipos.index(tipo_actual) if tipo_actual in tipos else 0,
                            format_func=lambda x: x.nombre,
                            key=f'fuente_{canal.codigo_canal}'
                        )

                    volumen_inicial = int(parametros['Volumen']) if isinstance(parametros['Volumen'], (int, float)) else 0
                    st.slider(
                        'Volumen:',
                        0, 100,
                        volumen_inicial,
                        1,
                        key=f'volumen_{canal.codigo_canal}'
                    )

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.checkbox('Solo', parametros['Solo'], key=f'solo_{canal.codigo_canal}')
                    with col2:
                        st.checkbox('Mute', parametros['Mute'], key=f'mute_{canal.codigo_canal}')
                    with col3:
                        st.checkbox('Link', parametros['Link'], key=f'link_{canal.codigo_canal}')

        else:
            st.info('Este usuario no tiene configuraciones.')
    else:
        st.info('Por favor, selecciona un usuario para ver y editar su configuración.')

if __name__ == "__main__":
    main()
