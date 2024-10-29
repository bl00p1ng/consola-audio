import streamlit as st
import logging
from typing import List, Optional
from datetime import datetime

from model.base import initialize_database
from model.frecuencia import Frecuencia
from model.tipo import Tipo
from model.fuente import Fuente, Clasifica, Maneja
from model.dispositivo import Dispositivo
from model.entrada import Entrada, Permite
from model.interfaz_audio import InterfazAudio, InterfazFrecuencia
from model.canal import Canal
from model.configuracion import Configuracion, Establece, Conectado
from model.usuario import Usuario, Personaliza

# Inicializar la base de datos existente
db = initialize_database()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    with db.connection_context():
        return list(Usuario.select())

def obtener_configuracion_usuario(usuario: Usuario) -> Optional[Configuracion]:
    """
    Obtiene la última configuración del usuario.
    """
    with db.connection_context():
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
    with db.connection_context():
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

def main():
    # Configuración de la página
    st.set_page_config(page_title="Consola de Audio", layout="wide")

    # Inyectar CSS personalizado
    st.markdown(custom_css(), unsafe_allow_html=True)

    st.title('Consola de Audio')

    # Selección de usuario
    with db.connection_context():
        usuarios = obtener_usuarios()
        usuario_seleccionado = st.selectbox(
            'Selecciona un usuario:',
            options=usuarios,
            format_func=lambda x: x.email
        )

        if usuario_seleccionado:
            # Obtener la última configuración del usuario
            configuracion = obtener_configuracion_usuario(usuario_seleccionado)
            
            if configuracion:
                # Obtener la interfaz de audio
                interfaz = configuracion.get_interfaz()
                
                # Mostrar información de la interfaz de audio
                st.markdown(f"""
                <div class="custom-card">
                    <div class="card-header">
                        <h3>Interfaz de Audio: {interfaz.nombre_comercial}</h3>
                    </div>
                    <div class="card-body">
                        <p>
                            <b>Modelo:</b> {interfaz.modelo}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Selector de frecuencia
                frecuencias = list(Frecuencia.select())
                frecuencia_actual = interfaz.frecuencia if hasattr(interfaz, 'frecuencia') else None
                nueva_frecuencia = st.selectbox(
                    'Frecuencia (kHz):',
                    options=frecuencias,
                    index=frecuencias.index(frecuencia_actual) if frecuencia_actual in frecuencias else 0,
                    format_func=lambda x: f"{x.valor} kHz"
                )

                # Contenedor para entradas y canales
                col1, col2 = st.columns(2)

                # Columna de Entradas
                with col1:
                    st.subheader('Entradas')
                    for entrada in configuracion.get_entradas():
                        st.markdown(f"""
                        <div class="custom-card">
                            <div class="card-header">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 13.5V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m12-3V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m-6-9V3.75m0 3.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 9.75V10.5" />
                                </svg>
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
                    for canal in configuracion.get_canales():
                        parametros = obtener_parametros_canal(canal, configuracion)
                        
                        st.markdown(f"""
                        <div class="custom-card">
                            <div class="card-header">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
                                </svg>
                                <h3>Canal {canal.codigo_canal}</h3>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        fuentes = list(Fuente.select())
                        # obtener la fuente actual del canal
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
                            tipo = st.selectbox(
                                'Fuente:',
                                options=tipos,
                                index=tipos.index(tipo_actual) if tipo_actual in tipos else 0,
                                format_func=lambda x: x.nombre,
                                key=f'fuente_{canal.codigo_canal}'
                            )

                        volumen_inicial = int(parametros['Volumen']) if isinstance(parametros['Volumen'], (int, float)) else 0
                        volumen = st.slider(
                            'Volumen:',
                            0, 100,
                            volumen_inicial,
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

            else:
                st.info('Este usuario no tiene configuraciones.')
        else:
            st.info('Por favor, selecciona un usuario para ver y editar su configuración.')

if __name__ == "__main__":
    main()