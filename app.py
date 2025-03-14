import streamlit as st
from funciones import cargar_tareas

# Importar módulos de vistas actualizados
from diario import mostrar_vista_diaria
from proyectos import mostrar_vista_proyectos
from calendario import mostrar_vista_calendario
from bitacora import mostrar_vista_bitacora

# Configuración de la página
st.set_page_config(
    page_title="Mi Bullet Journal Digital",
    page_icon="📝",
    layout="wide"
)

# Inicializar el estado de la sesión
if 'tareas' not in st.session_state:
    st.session_state.tareas = cargar_tareas()
if 'proyecto_actual' not in st.session_state:
    st.session_state.proyecto_actual = ""
if 'pestana' not in st.session_state:
    st.session_state.pestana = "Diario"

# Título principal con estilo
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📝 Mi Bullet Journal Digital</h1>", unsafe_allow_html=True)

# Pestañas
tabs = st.tabs(["📆 Tareas Diarias", "📋 Proyectos", "📔 Bitácora", "🗓️ Calendario"])

# Pestaña Tareas Diarias
with tabs[0]:
    mostrar_vista_diaria()

# Pestaña Proyectos
with tabs[1]:
    mostrar_vista_proyectos()

# Pestaña Bitácora
with tabs[2]:
    mostrar_vista_bitacora()

# Pestaña Calendario
with tabs[3]:
    mostrar_vista_calendario()

# Pie de página
st.markdown("---")
st.markdown("<p style='text-align: center;'>Bullet Journal Digital - Creado con Streamlit</p>", unsafe_allow_html=True)