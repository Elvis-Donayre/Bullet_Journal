import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Función para cargar tareas desde un archivo
def cargar_tareas():
    try:
        if os.path.exists("tareas.json"):
            with open("tareas.json", "r") as file:
                datos = json.load(file)
                # Asegurar que existe la estructura para proyectos y bitácora
                if "proyectos" not in datos:
                    datos["proyectos"] = {}
                if "bitacora" not in datos:
                    datos["bitacora"] = []
                return datos
        else:
            return {"diarias": [], "proyectos": {}, "bitacora": []}
    except Exception as e:
        st.error(f"Error al cargar las tareas: {e}")
        return {"diarias": [], "proyectos": {}, "bitacora": []}

# Función para guardar tareas en un archivo
def guardar_tareas(tareas):
    try:
        with open("tareas.json", "w") as file:
            json.dump(tareas, file)
    except Exception as e:
        st.error(f"Error al guardar las tareas: {e}")

# Función para añadir tarea
def anadir_tarea(tipo, tarea, fecha=None):
    if tarea:
        nueva_tarea = {
            "descripcion": tarea,
            "fecha": fecha if fecha else datetime.now().strftime("%Y-%m-%d"),
            "completada": False,
            "tipo": tipo
        }
        
        if tipo == "diarias":
            st.session_state.tareas["diarias"].append(nueva_tarea)
        
        guardar_tareas(st.session_state.tareas)
        return True
    return False

# Función para marcar una tarea como completada
def completar_tarea(tipo, indice):
    if tipo == "diarias":
        # Asegurar que existe la clave "completada"
        if "completada" not in st.session_state.tareas["diarias"][indice]:
            st.session_state.tareas["diarias"][indice]["completada"] = False
        
        # Invertir el estado actual
        st.session_state.tareas["diarias"][indice]["completada"] = not st.session_state.tareas["diarias"][indice]["completada"]
    
    guardar_tareas(st.session_state.tareas)

# Función para eliminar una tarea
def eliminar_tarea(tipo, indice):
    if tipo == "diarias":
        st.session_state.tareas["diarias"].pop(indice)
    
    guardar_tareas(st.session_state.tareas)

# Función para crear un nuevo proyecto
def crear_proyecto(nombre):
    if nombre and nombre not in st.session_state.tareas["proyectos"]:
        st.session_state.tareas["proyectos"][nombre] = {
            "tareas": [],
            "progreso": 0,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
            "fecha_limite": ""
        }
        guardar_tareas(st.session_state.tareas)
        st.session_state.proyecto_actual = nombre
        return True
    return False

# Función para añadir tarea a un proyecto
def anadir_tarea_proyecto(proyecto, tarea, fecha_limite=None):
    if tarea and proyecto in st.session_state.tareas["proyectos"]:
        nueva_tarea = {
            "descripcion": tarea,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
            "fecha_limite": fecha_limite if fecha_limite else "",
            "completada": False,
            "prioridad": "Media",  # Por defecto prioridad media
            "tipo": "proyecto"
        }
        
        st.session_state.tareas["proyectos"][proyecto]["tareas"].append(nueva_tarea)
        
        # Actualizar el progreso del proyecto
        actualizar_progreso_proyecto(proyecto)
        
        guardar_tareas(st.session_state.tareas)
        return True
    return False

# Función para marcar una tarea de proyecto como completada
def completar_tarea_proyecto(proyecto, indice):
    if proyecto in st.session_state.tareas["proyectos"]:
        # Asegurar que existe la clave "completada"
        if "completada" not in st.session_state.tareas["proyectos"][proyecto]["tareas"][indice]:
            st.session_state.tareas["proyectos"][proyecto]["tareas"][indice]["completada"] = False
            
        # Invertir el estado actual
        st.session_state.tareas["proyectos"][proyecto]["tareas"][indice]["completada"] = not st.session_state.tareas["proyectos"][proyecto]["tareas"][indice]["completada"]
        
        # Actualizar el progreso del proyecto
        actualizar_progreso_proyecto(proyecto)
        
        guardar_tareas(st.session_state.tareas)

# Función para actualizar el progreso de un proyecto
def actualizar_progreso_proyecto(proyecto):
    if proyecto in st.session_state.tareas["proyectos"]:
        tareas = st.session_state.tareas["proyectos"][proyecto]["tareas"]
        if tareas:
            completadas = sum(1 for tarea in tareas if tarea.get("completada", False))
            total = len(tareas)
            progreso = (completadas / total) * 100 if total > 0 else 0
            st.session_state.tareas["proyectos"][proyecto]["progreso"] = round(progreso, 1)
        else:
            st.session_state.tareas["proyectos"][proyecto]["progreso"] = 0

# Función para cambiar la prioridad de una tarea de proyecto
def cambiar_prioridad_tarea_proyecto(proyecto, indice, prioridad):
    if proyecto in st.session_state.tareas["proyectos"]:
        st.session_state.tareas["proyectos"][proyecto]["tareas"][indice]["prioridad"] = prioridad
        guardar_tareas(st.session_state.tareas)

# Función para establecer fecha límite del proyecto
def establecer_fecha_limite_proyecto(proyecto, fecha):
    if proyecto in st.session_state.tareas["proyectos"]:
        st.session_state.tareas["proyectos"][proyecto]["fecha_limite"] = fecha
        guardar_tareas(st.session_state.tareas)

# Función para eliminar una tarea de proyecto
def eliminar_tarea_proyecto(proyecto, indice):
    if proyecto in st.session_state.tareas["proyectos"]:
        st.session_state.tareas["proyectos"][proyecto]["tareas"].pop(indice)
        actualizar_progreso_proyecto(proyecto)
        guardar_tareas(st.session_state.tareas)

# Función para eliminar un proyecto completo
def eliminar_proyecto(proyecto):
    if proyecto in st.session_state.tareas["proyectos"]:
        del st.session_state.tareas["proyectos"][proyecto]
        if st.session_state.proyecto_actual == proyecto:
            st.session_state.proyecto_actual = ""
        guardar_tareas(st.session_state.tareas)

# Función para agregar entrada a la bitácora
def agregar_entrada_bitacora(titulo, contenido, categoria="General", tarea_relacionada=None):
    if titulo and contenido:
        nueva_entrada = {
            "titulo": titulo,
            "contenido": contenido,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categoria": categoria,
            "tarea_relacionada": tarea_relacionada
        }
        
        st.session_state.tareas["bitacora"].append(nueva_entrada)
        guardar_tareas(st.session_state.tareas)
        return True
    return False

# Función para editar entrada de bitácora
def editar_entrada_bitacora(indice, titulo, contenido, categoria):
    if indice >= 0 and indice < len(st.session_state.tareas["bitacora"]):
        entrada = st.session_state.tareas["bitacora"][indice]
        entrada["titulo"] = titulo
        entrada["contenido"] = contenido
        entrada["categoria"] = categoria
        entrada["editado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        guardar_tareas(st.session_state.tareas)
        return True
    return False

# Función para eliminar entrada de bitácora
def eliminar_entrada_bitacora(indice):
    if indice >= 0 and indice < len(st.session_state.tareas["bitacora"]):
        st.session_state.tareas["bitacora"].pop(indice)
        guardar_tareas(st.session_state.tareas)
        return True
    return False

# Función para agregar tarea al diccionario de tareas del mes (para el calendario)
def agregar_a_tareas_del_mes(tareas_del_mes, fecha_str, tarea, tipo, mes_seleccionado, año_seleccionado, completada=False):
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        if fecha.month == mes_seleccionado and fecha.year == año_seleccionado:
            dia = fecha.day
            if dia not in tareas_del_mes:
                tareas_del_mes[dia] = []
            tareas_del_mes[dia].append({
                "descripcion": tarea, 
                "tipo": tipo,
                "completada": completada
            })
    except:
        pass
    return tareas_del_mes
