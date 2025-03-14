import streamlit as st
from datetime import datetime
import calendar
from collections import defaultdict

def mostrar_vista_calendario():
    """
    Función principal que muestra la vista de calendario
    """
    st.header("Calendario de Tareas")
    st.markdown("Visualiza todas tus tareas organizadas por día en un calendario mensual.")
    
    # Selector de mes y año
    col1, col2 = st.columns(2)
    with col1:
        mes_actual = datetime.now().month
        mes_seleccionado = st.selectbox("Mes", range(1, 13), index=mes_actual-1, format_func=lambda x: calendar.month_name[x])
    with col2:
        año_actual = datetime.now().year
        año_seleccionado = st.selectbox("Año", range(año_actual-1, año_actual+3), index=1)
    
    # Recopilar tareas para el mes seleccionado
    tareas_del_mes = recopilar_tareas_del_mes(st.session_state.tareas, mes_seleccionado, año_seleccionado)
    
    # Mostrar el calendario
    mostrar_calendario(tareas_del_mes, mes_seleccionado, año_seleccionado)
    
    # Mostrar leyenda
    mostrar_leyenda()
    
    # Mostrar estadísticas
    mostrar_estadisticas(tareas_del_mes)

def mostrar_calendario(tareas_del_mes, mes_seleccionado, año_seleccionado):
    """
    Muestra un calendario mensual con las tareas correspondientes
    
    Args:
        tareas_del_mes: Diccionario con las tareas organizadas por día
        mes_seleccionado: Número del mes (1-12)
        año_seleccionado: Año
    """
    # Obtener el número de días del mes seleccionado
    _, num_dias = calendar.monthrange(año_seleccionado, mes_seleccionado)
    
    # Obtener el día de la semana del primer día del mes (0 = lunes, 6 = domingo)
    primer_dia = datetime(año_seleccionado, mes_seleccionado, 1)
    dia_semana_inicio = primer_dia.weekday()
    
    # Títulos de los días de la semana
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    
    # Crear tabla de calendario
    calendario_html = """
    <style>
    .calendario {
        width: 100%;
        border-collapse: collapse;
    }
    .calendario th {
        background-color: #4682B4;
        color: white;
        text-align: center;
        padding: 10px;
        border: 1px solid #ddd;
    }
    .calendario td {
        height: 100px;
        width: 14.28%;
        vertical-align: top;
        border: 1px solid #ddd;
        padding: 5px;
    }
    .calendario td.dia-actual {
        background-color: #e6f7ff;
    }
    .calendario .dia-numero {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .calendario .tarea {
        font-size: 0.8em;
        margin-bottom: 3px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .calendario .tarea-diaria {
        color: #1E90FF;
    }
    .calendario .tarea-proyecto {
        color: #DC143C;
    }
    .calendario .tarea-bitacora {
        color: #32CD32;
    }
    .calendario .tarea-completada {
        text-decoration: line-through;
        color: #888;
    }
    .calendario .vacio {
        background-color: #f5f5f5;
    }
    </style>
    <table class="calendario">
    <tr>
    """
    
    # Añadir encabezados de días de la semana
    for dia in dias_semana:
        calendario_html += f"<th>{dia}</th>"
    
    calendario_html += "</tr><tr>"
    
    # Añadir espacios en blanco para los días anteriores al primer día del mes
    for i in range(dia_semana_inicio):
        calendario_html += '<td class="vacio"></td>'
    
    # Día actual
    hoy = datetime.now()
    es_mes_actual = (hoy.month == mes_seleccionado and hoy.year == año_seleccionado)
    
    # Llenar el calendario con los días del mes
    dia_actual = 1
    dia_semana = dia_semana_inicio
    
    while dia_actual <= num_dias:
        # Verificar si es el día actual
        clase_dia = "dia-actual" if es_mes_actual and dia_actual == hoy.day else ""
        
        # Iniciar celda del día
        calendario_html += f'<td class="{clase_dia}">'
        calendario_html += f'<div class="dia-numero">{dia_actual}</div>'
        
        # Añadir tareas del día si existen
        if dia_actual in tareas_del_mes:
            for tarea in tareas_del_mes[dia_actual]:
                # Determinar la clase CSS según el tipo de tarea
                clase_tarea = ""
                if "diaria" in tarea["tipo"]:
                    clase_tarea = "tarea-diaria"
                elif "proyecto" in tarea["tipo"] or "deadline" in tarea["tipo"]:
                    clase_tarea = "tarea-proyecto"
                elif "bitacora" in tarea["tipo"]:
                    clase_tarea = "tarea-bitacora"
                
                # Añadir clase para tareas completadas
                if tarea.get("completada", False):
                    clase_tarea += " tarea-completada"
                
                # Añadir la tarea al calendario
                calendario_html += f'<div class="tarea {clase_tarea}" title="{tarea["descripcion"]}">{tarea["descripcion"]}</div>'
        
        # Cerrar celda del día
        calendario_html += '</td>'
        
        # Avanzar al siguiente día
        dia_actual += 1
        dia_semana = (dia_semana + 1) % 7
        
        # Si llegamos al domingo, cerrar la fila actual y comenzar una nueva
        if dia_semana == 0 and dia_actual <= num_dias:
            calendario_html += '</tr><tr>'
    
    # Añadir espacios en blanco para los días después del último día del mes
    for i in range(dia_semana, 7):
        calendario_html += '<td class="vacio"></td>'
    
    # Cerrar la tabla
    calendario_html += '</tr></table>'
    
    # Mostrar el calendario
    st.markdown(calendario_html, unsafe_allow_html=True)

def mostrar_leyenda():
    """Muestra la leyenda de colores para los diferentes tipos de tareas"""
    st.markdown("### Leyenda")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div style="color: #1E90FF;">● Tareas diarias</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="color: #DC143C;">● Proyectos</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="color: #32CD32;">● Entradas de bitácora</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="text-decoration: line-through; color: #888;">● Tareas completadas</div>', unsafe_allow_html=True)

def mostrar_estadisticas(tareas_del_mes):
    """
    Muestra estadísticas del mes actual
    
    Args:
        tareas_del_mes: Diccionario con las tareas organizadas por día
    """
    st.markdown("### Estadísticas del mes")
    tareas_totales = sum(len(tareas) for tareas in tareas_del_mes.values())
    
    # Contar por tipo y estado (completadas/pendientes)
    tipos_tareas = defaultdict(int)
    completadas = 0
    pendientes = 0
    
    for dia, tareas in tareas_del_mes.items():
        for tarea in tareas:
            tipo_base = tarea["tipo"].split(":")[0]
            tipos_tareas[tipo_base] += 1
            
            if tarea.get("completada", False):
                completadas += 1
            else:
                pendientes += 1
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total tareas en el mes", tareas_totales)
    with col2:
        # Encontrar el día con más tareas
        if tareas_del_mes:
            dia_mas_ocupado = max(tareas_del_mes.items(), key=lambda x: len(x[1]))
            st.metric("Día más ocupado", f"{dia_mas_ocupado[0]} ({len(dia_mas_ocupado[1])} tareas)")
        else:
            st.metric("Día más ocupado", "Ninguno")
    
    # Mostrar estado de completitud
    if tareas_totales > 0:
        col1, col2 = st.columns(2)
        with col1:
            porcentaje_completadas = (completadas / tareas_totales) * 100 if tareas_totales > 0 else 0
            st.metric("Completadas", f"{completadas} ({porcentaje_completadas:.1f}%)")
        with col2:
            st.metric("Pendientes", pendientes)
    
    # Mostrar distribución por tipo de tarea
    if tipos_tareas:
        st.subheader("Distribución por tipo")
        for tipo, cantidad in tipos_tareas.items():
            st.text(f"{tipo}: {cantidad} tareas")

def recopilar_tareas_del_mes(tareas, mes_seleccionado, año_seleccionado):
    """
    Recopila todas las tareas para el mes y año seleccionados
    
    Args:
        tareas: Diccionario con todas las tareas
        mes_seleccionado: Número del mes (1-12)
        año_seleccionado: Año
        
    Returns:
        Diccionario con las tareas organizadas por día del mes
    """
    from funciones import agregar_a_tareas_del_mes
    
    tareas_del_mes = {}
    
    # Recopilar tareas diarias
    for tarea in tareas["diarias"]:
        # Convertir fecha a objeto datetime
        try:
            fecha = datetime.strptime(tarea["fecha"], "%Y-%m-%d")
            if fecha.month == mes_seleccionado and fecha.year == año_seleccionado:
                dia = fecha.day
                if dia not in tareas_del_mes:
                    tareas_del_mes[dia] = []
                
                # Crear copia de la tarea para el calendario
                tarea_calendario = {
                    "descripcion": tarea["descripcion"],
                    "tipo": "diaria",
                    "completada": tarea.get("completada", False)
                }
                
                tareas_del_mes[dia].append(tarea_calendario)
        except:
            pass
    
    # Recopilar tareas de proyectos (fechas límite)
    for proyecto_nombre, proyecto_info in tareas["proyectos"].items():
        # Fecha límite del proyecto
        if proyecto_info["fecha_limite"]:
            try:
                fecha = datetime.strptime(proyecto_info["fecha_limite"], "%Y-%m-%d")
                if fecha.month == mes_seleccionado and fecha.year == año_seleccionado:
                    dia = fecha.day
                    if dia not in tareas_del_mes:
                        tareas_del_mes[dia] = []
                    
                    # Crear descripción para el calendario
                    tarea_calendario = {
                        "descripcion": f"Fecha límite: {proyecto_nombre}",
                        "tipo": "deadline-proyecto",
                        "completada": False
                    }
                    
                    tareas_del_mes[dia].append(tarea_calendario)
            except:
                pass
        
        # Tareas de proyecto con fechas límite
        for tarea in proyecto_info["tareas"]:
            if tarea["fecha_limite"]:
                try:
                    fecha = datetime.strptime(tarea["fecha_limite"], "%Y-%m-%d")
                    if fecha.month == mes_seleccionado and fecha.year == año_seleccionado:
                        dia = fecha.day
                        if dia not in tareas_del_mes:
                            tareas_del_mes[dia] = []
                        
                        # Crear descripción para el calendario
                        tarea_calendario = {
                            "descripcion": f"{tarea['descripcion']} ({proyecto_nombre})",
                            "tipo": f"tarea-proyecto: {tarea['prioridad']}",
                            "completada": tarea.get("completada", False)
                        }
                        
                        tareas_del_mes[dia].append(tarea_calendario)
                except:
                    pass
    
    # Recopilar entradas de bitácora
    for entrada in tareas["bitacora"]:
        fecha_str = entrada["fecha"].split()[0]  # Obtener solo la parte de la fecha (sin hora)
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            if fecha.month == mes_seleccionado and fecha.year == año_seleccionado:
                dia = fecha.day
                if dia not in tareas_del_mes:
                    tareas_del_mes[dia] = []
                
                # Crear descripción para el calendario
                tarea_calendario = {
                    "descripcion": f"Nota: {entrada['titulo']}",
                    "tipo": "bitacora",
                    "completada": False  # Las notas no se completan
                }
                
                tareas_del_mes[dia].append(tarea_calendario)
        except:
            pass
    
    return tareas_del_mes
