# Consola de Audio Perrona

Este proyecto implementa una interfaz de usuario para una consola de audio utilizando Python, Streamlit y SQLite.

**Integrantes:**
- Andrés Felipe López Molina
- Juan Sebastián Díaz Mas

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

## Configuración del Entorno

1. Crea un entorno virtual:
   ```
   python -m venv venv
   ```

2. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS y Linux:
     ```
     source venv/bin/activate
     ```

## Instalación de Dependencias

-  Instalar las dependencias del proyecto:
   ```
   pip install -r requirements.txt
   ```

## Ejecución de la Aplicación

1. Desde el directorio raíz del proyecto, ejecuta:
   ```
   streamlit run app.py
   ```

2. Abre un navegador web y ve a la dirección que aparece en la consola (normalmente `http://localhost:8501`).

### Estructura de archivos del proyecto

```
└── 📁(avance)sistemaConfiguracionPanelUltimaSesionPresencial
    └── 📁db
        └── Base_De_Datos.db
    └── 📁model
        └── 📁__pycache__
            └── base.cpython-38.pyc
            └── configuracion.cpython-38.pyc
            └── interfaz_audio.cpython-38.pyc
            └── usuario.cpython-38.pyc
        └── .DS_Store
        └── base.py
        └── canal.py
        └── configuracion.py
        └── dispositivo.py
        └── entrada.py
        └── frecuencia.py
        └── fuente.py
        └── interfaz_audio.py
        └── tipo.py
        └── usuario.py
    └── .DS_Store
    └── .gitignore
    └── app.py
    └── README.md
    └── requirements.txt
```
