import streamlit as st
from funciones import agregar_entrada_bitacora, editar_entrada_bitacora, eliminar_entrada_bitacora
import pandas as pd
from datetime import datetime

def mostrar_vista_bitacora():
    """
    Función principal que muestra la vista de bitácora
    """
    st.header("Bitácora de Notas")
    st.markdown("Registra notas, ideas y observaciones sobre tus tareas y proyectos.")
    
    # Mostrar formulario para nueva entrada
    mostrar_formulario_nueva_entrada()
    
    # Mostrar entradas existentes
    mostrar_entradas_bitacora()

def mostrar_formulario_nueva_entrada():
    """
    Muestra el formulario para añadir una nueva entrada a la bitácora
    """
    with st.form("form_bitacora", clear_on_submit=True):
        st.subheader("Nueva Entrada")
        
        titulo = st.text_input("Título", key="titulo_bitacora")
        
        # Lista de tareas diarias y de proyectos para asociar
        opciones_tareas = ["Ninguna"]
        
        # Añadir tareas diarias
        for i, tarea in enumerate(st.session_state.tareas["diarias"]):
            if not tarea.get("completada", False):
                opciones_tareas.append(f"Diaria: {tarea['descripcion']}")
        
        # Añadir tareas de proyectos
        for proyecto_nombre, proyecto_info in st.session_state.tareas["proyectos"].items():
            for i, tarea in enumerate(proyecto_info["tareas"]):
                if not tarea.get("completada", False):
                    opciones_tareas.append(f"Proyecto {proyecto_nombre}: {tarea['descripcion']}")
        
        # Selector de tarea relacionada
        tarea_relacionada = st.selectbox("Tarea relacionada", opciones_tareas, key="tarea_relacionada")
        
        # Categoría
        categoria = st.selectbox("Categoría", ["General", "Idea", "Problema", "Solución", "Logro", "Recordatorio"], key="categoria_bitacora")
        
        # Contenido de la nota
        contenido = st.text_area("Contenido", height=200, key="contenido_bitacora")
        
        submitted = st.form_submit_button("Guardar Entrada")
    
    # Procesar formulario
    if submitted:
        tarea_rel = None if tarea_relacionada == "Ninguna" else tarea_relacionada
        if agregar_entrada_bitacora(titulo, contenido, categoria, tarea_rel):
            st.success("Entrada añadida a la bitácora correctamente")

def mostrar_entradas_bitacora():
    """
    Muestra las entradas existentes en la bitácora
    """
    if not st.session_state.tareas["bitacora"]:
        st.info("No hay entradas en la bitácora. Crea una para comenzar.")
        return
    
    # Opciones de filtrado
    st.subheader("Entradas")
    
    col1, col2 = st.columns(2)
    with col1:
        # Filtro por categoría
        todas_categorias = ["Todas"] + list(set(entrada["categoria"] for entrada in st.session_state.tareas["bitacora"]))
        filtro_categoria = st.selectbox("Filtrar por categoría", todas_categorias, key="filtro_categoria")
    
    with col2:
        # Ordenar por fecha
        orden = st.selectbox("Ordenar por", ["Más recientes primero", "Más antiguas primero"], key="orden_bitacora")
    
    # Aplicar filtros
    entradas_filtradas = st.session_state.tareas["bitacora"]
    if filtro_categoria != "Todas":
        entradas_filtradas = [e for e in entradas_filtradas if e["categoria"] == filtro_categoria]
    
    # Ordenar
    entradas_filtradas = sorted(
        entradas_filtradas, 
        key=lambda x: datetime.strptime(x["fecha"], "%Y-%m-%d %H:%M:%S"),
        reverse=(orden == "Más recientes primero")
    )
    
    # Mostrar entradas
    for i, entrada in enumerate(entradas_filtradas):
        with st.expander(f"📝 {entrada['titulo']} - {entrada['fecha'][:10]} ({entrada['categoria']})"):
            st.markdown(f"**{entrada['titulo']}**")
            if entrada.get("tarea_relacionada"):
                st.markdown(f"*Relacionada con:* {entrada['tarea_relacionada']}")
            
            st.markdown("---")
            st.markdown(entrada['contenido'])
            st.markdown("---")
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("🗑️ Eliminar", key=f"eliminar_bitacora_{i}"):
                    if eliminar_entrada_bitacora(i):
                        st.success("Entrada eliminada correctamente")
                        st.experimental_rerun()
            
            with col2:
                if st.button("✏️ Editar", key=f"editar_bitacora_{i}"):
                    st.session_state.editar_bitacora_index = i
                    st.session_state.editar_bitacora_titulo = entrada['titulo']
                    st.session_state.editar_bitacora_contenido = entrada['contenido']
                    st.session_state.editar_bitacora_categoria = entrada['categoria']
    
    # Formulario de edición si está en modo edición
    if 'editar_bitacora_index' in st.session_state:
        with st.form("form_editar_bitacora"):
            st.subheader("Editar Entrada")
            
            nuevo_titulo = st.text_input("Título", value=st.session_state.editar_bitacora_titulo, key="nuevo_titulo_bitacora")
            nueva_categoria = st.selectbox("Categoría", ["General", "Idea", "Problema", "Solución", "Logro", "Recordatorio"], 
                                        index=["General", "Idea", "Problema", "Solución", "Logro", "Recordatorio"].index(st.session_state.editar_bitacora_categoria),
                                        key="nueva_categoria_bitacora")
            nuevo_contenido = st.text_area("Contenido", value=st.session_state.editar_bitacora_contenido, height=200, key="nuevo_contenido_bitacora")
            
            col1, col2 = st.columns(2)
            with col1:
                cancelar = st.form_submit_button("Cancelar")
            with col2:
                guardar = st.form_submit_button("Guardar Cambios")
        
        if cancelar:
            del st.session_state.editar_bitacora_index
            del st.session_state.editar_bitacora_titulo
            del st.session_state.editar_bitacora_contenido
            del st.session_state.editar_bitacora_categoria
            st.experimental_rerun()
        
        if guardar:
            if editar_entrada_bitacora(st.session_state.editar_bitacora_index, nuevo_titulo, nuevo_contenido, nueva_categoria):
                st.success("Entrada actualizada correctamente")
                del st.session_state.editar_bitacora_index
                del st.session_state.editar_bitacora_titulo
                del st.session_state.editar_bitacora_contenido
                del st.session_state.editar_bitacora_categoria
                st.experimental_rerun()
