import streamlit as st
from model.dao.UsuarioDAO import UsuarioDAO
from model.dao.ConfiguracionDAO import ConfiguracionDAO
from model.dao.DispositivoDAO import DispositivoDAO
from model.dao.CanalDAO import CanalDAO
from model.dao.FuenteDAO import FuenteDAO

# Función para crear un contenedor con borde estilizado
def styled_container(content, key):
    st.markdown(f"""
    <style>
    .styledContainer-{key} {{
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, rgba(49, 51, 63, 0.1) 0%, rgba(49, 51, 63, 0.05) 100%);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="styledContainer-{key}">{content}</div>', unsafe_allow_html=True)

# Inicializar DAOs
usuario_dao = UsuarioDAO()
configuracion_dao = ConfiguracionDAO()
dispositivo_dao = DispositivoDAO()
canal_dao = CanalDAO()
fuente_dao = FuenteDAO()

st.title('Consola de Audio Perrona')

# Selección de usuario
usuarios = usuario_dao.getAll()
usuario_seleccionado = st.selectbox(
    'Selecciona un usuario:',
    options=usuarios,
    format_func=lambda x: x.getEmail()
)

if usuario_seleccionado:
    # Obtener configuraciones del usuario
    configuraciones = configuracion_dao.getConfiguracionesPorUsuario(usuario_seleccionado)
    
    if configuraciones:
        # Selección de configuración
        configuracion = st.selectbox(
            'Selecciona una configuración:',
            options=configuraciones,
            format_func=lambda x: f"Configuración {x.getID()} - {x.getFecha()}"
        )
        
        if configuracion:
            # Mostrar y editar frecuencia
            interfaz = configuracion.getInterfaz()
            st.subheader(f"Interfaz de Audio: {interfaz.nombreComercial}")
            st.write(f"Modelo: {interfaz.modelo}")
            
            frecuencia_actual = interfaz.frecuencia.valor
            nueva_frecuencia = st.selectbox(
                'Frecuencia:',
                options=[44.1, 48, 96],
                index=[44.1, 48, 96].index(frecuencia_actual)
            )
            
            # Mostrar y editar entradas
            st.subheader('Entradas')
            dispositivos = dispositivo_dao.getAll()
            entradas_actualizadas = []
            for entrada in configuracion.getEntradas():
                content = f"""
                <h4>Entrada {entrada.id}</h4>
                <div id="dispositivo-{entrada.id}"></div>
                """
                styled_container(content, f"entrada-{entrada.id}")
                
                nuevo_dispositivo = st.selectbox(
                    'Dispositivo:',
                    options=dispositivos,
                    index=dispositivos.index(entrada.dispositivo) if entrada.dispositivo in dispositivos else 0,
                    format_func=lambda x: x.Nombre,
                    key=f'dispositivo_{entrada.id}'
                )
                entrada.setDispositivo(nuevo_dispositivo)
                entradas_actualizadas.append(entrada)
            
            # Mostrar y editar canales
            st.subheader('Canales')
            fuentes = fuente_dao.getAll()
            canales_actualizados = []
            for canal in configuracion.getCanales():
                # Obtenemos los valores específicos de Establece para este canal y esta configuración
                establece = canal_dao.getParametrosCanal(canal.id, configuracion.getID())
                
                content = f"""
                <h4>Canal {canal.id}</h4>
                <div id="canal-content-{canal.id}"></div>
                """
                styled_container(content, f"canal-{canal.id}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    nueva_fuente = st.selectbox(
                        'Fuente:',
                        options=fuentes,
                        index=fuentes.index(canal.fuente) if canal.fuente in fuentes else 0,
                        format_func=lambda x: x.tipo.nombre if x.tipo else "Sin tipo",
                        key=f'fuente_{canal.id}'
                    )
                    establece['ID_Fuente'] = nueva_fuente.id
                
                with col2:
                    # El volumen ya está entre 0 y 100, no necesitamos convertirlo
                    nuevo_volumen = st.slider('Volumen:', 0, 100, establece['Volumen'], 1, key=f'volumen_{canal.id}')
                    establece['Volumen'] = nuevo_volumen
                
                with col3:
                    establece['Solo'] = st.checkbox('Solo', establece['Solo'], key=f'solo_{canal.id}')
                    establece['Mute'] = st.checkbox('Mute', establece['Mute'], key=f'mute_{canal.id}')
                    establece['Link'] = st.checkbox('Link', establece['Link'], key=f'link_{canal.id}')
                
                canales_actualizados.append((canal, establece))
            
            # Botón para guardar cambios
            if st.button('Guardar Configuración'):
                try:
                    # Actualizar frecuencia
                    interfaz.setFrecuencia(nueva_frecuencia)
                    
                    # Actualizar configuración
                    for canal, establece in canales_actualizados:
                        canal_dao.actualizarParametrosCanal(canal.id, configuracion.getID(), establece)
                    
                    configuracion.setEntradas(entradas_actualizadas)
                    
                    # Guardar en la base de datos
                    if configuracion_dao.updateConfiguracion(configuracion):
                        st.success('Configuración guardada exitosamente!')
                    else:
                        st.error('Error al guardar la configuración. Por favor, intenta de nuevo.')
                except Exception as e:
                    st.error(f'Ocurrió un error al guardar la configuración: {str(e)}')
else:
    st.info('Por favor, selecciona un usuario para ver y editar su configuración.')