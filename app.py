import streamlit as st
from model.dao.FrecuenciaDAO import FrecuenciaDAO
from model.dao.UsuarioDAO import UsuarioDAO
from model.dao.ConfiguracionDAO import ConfiguracionDAO
from model.dao.DispositivoDAO import DispositivoDAO
from model.dao.CanalDAO import CanalDAO
from model.dao.FuenteDAO import FuenteDAO
from model.dao.TipoDAO import TipoDAO

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

# Inicializar DAOs
usuario_dao = UsuarioDAO()
configuracion_dao = ConfiguracionDAO()
dispositivo_dao = DispositivoDAO()
canal_dao = CanalDAO()
fuente_dao = FuenteDAO()
tipo_dao = TipoDAO()
frecuencia_dao = FrecuenciaDAO()

# Configuración de la página
st.set_page_config(page_title="Consola de Audio", layout="wide")

# Inyectar CSS personalizado
st.markdown(custom_css(), unsafe_allow_html=True)

st.title('Consola de Audio')

# Selección de usuario
usuarios = usuario_dao.getAll()
usuario_seleccionado = st.selectbox(
    'Selecciona un usuario:',
    options=usuarios,
    format_func=lambda x: x.getEmail()
)

if usuario_seleccionado:
    # Obtener la última configuración del usuario
    configuraciones = configuracion_dao.getConfiguracionesPorUsuario(usuario_seleccionado)
    if configuraciones:
        configuracion = configuraciones[0]
        
        # Mostrar información de la interfaz de audio
        interfaz = configuracion.getInterfaz()
        st.markdown(f"""
        <div class="custom-card">
            <div class="card-header">
                <h3>Interfaz de Audio: {interfaz.nombreComercial}</h3>
            </div>
            <div class="card-body">
                <p>
                    <b>Modelo:</b> {interfaz.modelo}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Selector de frecuencia
        todas_frecuencias = frecuencia_dao.getAll()
        frecuencia_actual = interfaz.frecuencia
        nueva_frecuencia = st.selectbox(
            'Frecuencia (kHz):',
            options=todas_frecuencias,
            index=todas_frecuencias.index(frecuencia_actual) if frecuencia_actual in todas_frecuencias else 0,
            format_func=lambda x: f"{x.valor} kHz"
        )
        
        # Contenedor para entradas y canales
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Entradas')
            for entrada in configuracion.getEntradas():
                st.markdown(f"""
                <div class="custom-card">
                    <div class="card-header">
                        <h3>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 13.5V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m12-3V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m-6-9V3.75m0 3.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 9.75V10.5" />
                            </svg>
                            Entrada {entrada.id}
                        </h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                dispositivo = st.selectbox(
                    'Dispositivo:',
                    options=dispositivo_dao.getAll(),
                    index=dispositivo_dao.getAll().index(entrada.dispositivo) if entrada.dispositivo in dispositivo_dao.getAll() else 0,
                    format_func=lambda x: x.Nombre,
                    key=f'dispositivo_{entrada.id}'
                )
        
        with col2:
            st.subheader('Canales')
            for canal in configuracion.getCanales():
                establece = canal_dao.getParametrosCanal(canal.id, configuracion.getID())
                st.markdown(f"""
                <div class="custom-card">
                    <div class="card-header">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
                        </svg>
                        <h3>Canal {canal.id}</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Selector de fuente
                fuente = st.selectbox(
                    'Fuente:',
                    options=fuente_dao.getAll(),
                    index=fuente_dao.getAll().index(canal.fuente) if canal.fuente in fuente_dao.getAll() else 0,
                    format_func=lambda x: x.tipo.nombre if x.tipo else "Sin tipo",
                    key=f'fuente_{canal.id}'
                )
                
                # Selector de tipo basado en la fuente seleccionada
                if fuente:
                    tipos_asociados = fuente_dao.getFuentesPorTipo(fuente.tipo)
                    tipo_actual = canal.fuente.tipo if canal.fuente else None
                    tipo = st.selectbox(
                        'Tipo:',
                        options=tipos_asociados,
                        index=tipos_asociados.index(tipo_actual) if tipo_actual in tipos_asociados else 0,
                        format_func=lambda x: x.tipo.id if x.tipo else "Sin tipo",
                        key=f'tipo_{canal.id}'
                    )
                
                volumen = st.slider('Volumen:', 0, 100, establece['Volumen'], 1, key=f'volumen_{canal.id}')
                col1, col2, col3 = st.columns(3)
                with col1:
                    solo = st.checkbox('Solo', establece['Solo'], key=f'solo_{canal.id}')
                with col2:
                    mute = st.checkbox('Mute', establece['Mute'], key=f'mute_{canal.id}')
                with col3:
                    link = st.checkbox('Link', establece['Link'], key=f'link_{canal.id}')

        # EDICIÓN DE CONFIGURACIÓN DESHABILITADA
        # if st.button('Guardar Configuración'):
        #     try:
        #         # Actualizar frecuencia
        #         interfaz.setFrecuencia(nueva_frecuencia)
                
        #         # Actualizar entradas
        #         for entrada in configuracion.getEntradas():
        #             nuevo_dispositivo = st.session_state[f'dispositivo_{entrada.id}']
        #             entrada.setDispositivo(nuevo_dispositivo)
                
        #         # Actualizar canales
        #         for canal in configuracion.getCanales():
        #             establece = canal_dao.getParametrosCanal(canal.id, configuracion.getID())
        #             nueva_fuente = st.session_state[f'fuente_{canal.id}']
        #             nuevo_tipo = st.session_state[f'tipo_{canal.id}']
        #             establece['Volumen'] = st.session_state[f'volumen_{canal.id}']
        #             establece['Solo'] = st.session_state[f'solo_{canal.id}']
        #             establece['Mute'] = st.session_state[f'mute_{canal.id}']
        #             establece['Link'] = st.session_state[f'link_{canal.id}']
                    
        #             nueva_fuente.setTipo(nuevo_tipo)
        #             canal.setFuente(nueva_fuente)
        #             canal_dao.actualizarParametrosCanal(canal.id, configuracion.getID(), establece)
                
        #         if configuracion_dao.updateConfiguracion(configuracion):
        #             st.success('Configuración guardada exitosamente!')
        #         else:
        #             st.error('Error al guardar la configuración. Por favor, intenta de nuevo.')
        #     except Exception as e:
        #         st.error(f'Ocurrió un error al guardar la configuración: {str(e)}')

else:
    st.info('Por favor, selecciona un usuario para ver y editar su configuración.')