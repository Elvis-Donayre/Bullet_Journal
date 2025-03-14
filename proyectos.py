import streamlit as st
from datetime import datetime
from funciones import (
    crear_proyecto, anadir_tarea_proyecto, completar_tarea_proyecto,
    cambiar_prioridad_tarea_proyecto, establecer_fecha_limite_proyecto,
    eliminar_tarea_proyecto, eliminar_proyecto
)

def mostrar_vista_proyectos():
    """
    Función principal que muestra la vista de gestión de proyectos
    """
    st.header("Gestión de Proyectos")
    st.markdown("Organiza tus proyectos y desglósalos en tareas específicas.")
    
    # Barra lateral para crear proyectos
    col1, col2 = st.columns([3, 1])
    with col1:
        nuevo_proyecto = st.text_input("Nombre del nuevo proyecto", key="input_proyecto")
    with col2:
        if st.button("Crear proyecto"):
            if crear_proyecto(nuevo_proyecto):
                st.success(f"Proyecto '{nuevo_proyecto}' creado correctamente")
            else:
                st.error("Por favor, ingresa un nombre válido para el proyecto")
    
    # Selector de proyectos
    proyectos = list(st.session_state.tareas["proyectos"].keys())
    if proyectos:
        proyecto_seleccionado = st.selectbox("Seleccionar proyecto", proyectos, 
                                           index=proyectos.index(st.session_state.proyecto_actual) if st.session_state.proyecto_actual in proyectos else 0,
                                           key="selector_proyectos")
        st.session_state.proyecto_actual = proyecto_seleccionado
        
        # Mostrar detalles del proyecto seleccionado
        mostrar_detalles_proyecto(proyecto_seleccionado)
    else:
        st.info("No hay proyectos creados. Crea uno para comenzar.")

def mostrar_detalles_proyecto(proyecto_seleccionado):
    """
    Muestra los detalles de un proyecto específico
    
    Args:
        proyecto_seleccionado: Nombre del proyecto a mostrar
    """
    proyecto = st.session_state.tareas["proyectos"][proyecto_seleccionado]
    
    # Progreso del proyecto
    st.progress(proyecto["progreso"] / 100)
    st.write(f"Progreso: {proyecto['progreso']}%")
    
    # Información del proyecto
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Fecha de creación:** {proyecto['fecha_creacion']}")
    with col2:
        fecha_limite = st.date_input("Fecha límite", key="fecha_limite_proyecto",
                                   value=datetime.strptime(proyecto['fecha_limite'], "%Y-%m-%d") if proyecto['fecha_limite'] else None)
        if fecha_limite:
            establecer_fecha_limite_proyecto(proyecto_seleccionado, fecha_limite.strftime("%Y-%m-%d"))
    with col3:
        if st.button("🗑️ Eliminar proyecto", key="eliminar_proyecto"):
            eliminar_proyecto(proyecto_seleccionado)
            st.experimental_rerun()
    
    st.markdown("---")
    
    # Formulario para añadir tarea al proyecto
    mostrar_formulario_nueva_tarea(proyecto_seleccionado)
    
    # Tareas del proyecto
    mostrar_tareas_proyecto(proyecto_seleccionado, proyecto)

def mostrar_formulario_nueva_tarea(proyecto_seleccionado):
    """
    Muestra el formulario para añadir una nueva tarea al proyecto
    
    Args:
        proyecto_seleccionado: Nombre del proyecto
    """
    with st.form("form_tarea_proyecto", clear_on_submit=True):
        st.subheader("Añadir nueva tarea al proyecto")
        tarea_proyecto = st.text_input("Descripción de la tarea", key="input_tarea_proyecto")
        
        col1, col2 = st.columns(2)
        with col1:
            prioridad = st.selectbox("Prioridad", ["Baja", "Media", "Alta"], index=1, key="prioridad_tarea")
        with col2:
            fecha_tarea = st.date_input("Fecha límite (opcional)", key="fecha_tarea_proyecto")
        
        submit_tarea_proyecto = st.form_submit_button("Añadir tarea")
    
    if submit_tarea_proyecto:
        if anadir_tarea_proyecto(proyecto_seleccionado, tarea_proyecto, fecha_tarea.strftime("%Y-%m-%d")):
            st.success("Tarea añadida al proyecto correctamente")

def mostrar_tareas_proyecto(proyecto_seleccionado, proyecto):
    """
    Muestra las tareas de un proyecto con opciones para filtrar y gestionar
    
    Args:
        proyecto_seleccionado: Nombre del proyecto
        proyecto: Diccionario con los datos del proyecto
    """
    st.subheader("Tareas del proyecto")
    
    # Filtro por estado
    filtro_estado = st.radio("Mostrar:", ["Todas", "Pendientes", "Completadas"], horizontal=True, key="filtro_estado")
    
    # Mostrar tareas según el filtro
    if proyecto["tareas"]:
        for i, tarea in enumerate(proyecto["tareas"]):
            # Aplicar filtro
            if (filtro_estado == "Pendientes" and tarea.get("completada", False)) or (filtro_estado == "Completadas" and not tarea.get("completada", False)):
                continue
                
            col1, col2, col3, col4 = st.columns([0.1, 3, 1, 0.5])
            with col1:
                completada = st.checkbox("", value=tarea.get("completada", False), key=f"check_proyecto_{i}", 
                                      on_change=completar_tarea_proyecto, args=(proyecto_seleccionado, i))
            with col2:
                texto = tarea["descripcion"]
                if completada:
                    texto = f"~~{texto}~~"
                    
                # Mostrar fecha límite si existe
                fecha_info = ""
                if tarea["fecha_limite"]:
                    fecha_info = f" - *Límite: {tarea['fecha_limite']}*"
                    
                # Color según prioridad
                color = "orange" if tarea["prioridad"] == "Alta" else "green" if tarea["prioridad"] == "Baja" else "gray"
                
                st.markdown(f"{texto}{fecha_info} <span style='color:{color};'>({tarea['prioridad']})</span>", unsafe_allow_html=True)
            with col3:
                nueva_prioridad = st.selectbox("", ["Baja", "Media", "Alta"], 
                                             index=["Baja", "Media", "Alta"].index(tarea["prioridad"]),
                                             key=f"prioridad_select_{i}",
                                             on_change=cambiar_prioridad_tarea_proyecto,
                                             args=(proyecto_seleccionado, i, ["Baja", "Media", "Alta"][st.session_state[f"prioridad_select_{i}"]]))
            with col4:
                st.button("🗑️", key=f"eliminar_tarea_proyecto_{i}", help="Eliminar tarea", 
                       on_click=eliminar_tarea_proyecto, args=(proyecto_seleccionado, i))
    else:
        st.info("No hay tareas en este proyecto. Añade una para comenzar.")