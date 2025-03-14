import streamlit as st
from funciones import anadir_tarea, completar_tarea, eliminar_tarea

def mostrar_vista_diaria():
    """
    Función principal que muestra la vista de tareas diarias
    """
    st.header("Registro Diario")
    st.markdown("Añade tus tareas diarias y marca las que vayas completando.")
    
    # Formulario para añadir tarea diaria
    with st.form("form_tarea_diaria", clear_on_submit=True):
        tarea_diaria = st.text_input("Nueva tarea diaria", key="input_diaria")
        col1, col2 = st.columns([3, 1])
        with col1:
            submit_diaria = st.form_submit_button("Añadir tarea")
        with col2:
            fecha_diaria = st.date_input("Fecha", key="fecha_diaria")
    
    if submit_diaria:
        if anadir_tarea("diarias", tarea_diaria, fecha_diaria.strftime("%Y-%m-%d")):
            st.success("Tarea añadida correctamente")
    
    # Mostrar tareas diarias
    if st.session_state.tareas["diarias"]:
        for i, tarea in enumerate(st.session_state.tareas["diarias"]):
            col1, col2, col3 = st.columns([0.1, 3, 0.5])
            with col1:
                completada = st.checkbox("", value=tarea.get("completada", False), key=f"check_diaria_{i}", 
                                       on_change=completar_tarea, args=("diarias", i))
            with col2:
                texto = tarea["descripcion"]
                if completada:
                    texto = f"~~{texto}~~"
                st.markdown(f"{texto} - *{tarea['fecha']}*")
            with col3:
                st.button("🗑️", key=f"eliminar_diaria_{i}", help="Eliminar tarea", 
                       on_click=eliminar_tarea, args=("diarias", i))
    else:
        st.info("No hay tareas diarias pendientes")
