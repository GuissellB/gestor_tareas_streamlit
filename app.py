import streamlit as st
from database.tareas.router import create_task, get_all_tasks
from database.listas.router import get_all_listas, create_lista
import pandas as pd
from datetime import date

st.set_page_config(page_title="Gestor de tareas", layout="centered")
st.title("Registrar nueva tarea")

with st.form("form_tarea"):
    titulo = st.text_input("Título de la tarea")
    descripcion = st.text_area("Descripción de la tarea")
    prioridad = st.selectbox("Prioridad", ["Baja", "Media", "Alta"])
    fecha_limite = st.date_input("Fecha límite", min_value=date.today())
    usuario_encargado = st.text_input("Usuario encargado")

    try:
        listas_existentes = get_all_listas()
    except:
        listas_existentes = []

    if not listas_existentes:
        st.info("No hay listas creadas. Ingrese un nombre para la nueva lista:")
        nombre_lista = st.text_input("Nombre de la nueva lista")
        id_lista = None
    else:
        opciones = ["Crear nueva lista"] + [l.nombre for l in listas_existentes]
        seleccion = st.selectbox("Seleccionar lista o crear nueva:", opciones)

        if seleccion == "Crear nueva lista":
            nombre_lista = st.text_input("Nombre de la nueva lista")
            id_lista = None
        else:
            nombre_lista = seleccion
            id_lista = next((l.id for l in listas_existentes if l.nombre == nombre_lista), None)


    submitted = st.form_submit_button("Guardar tarea")

if submitted:
    if not nombre_lista.strip():
        st.warning("⚠️ Por favor indique un nombre de lista.")
    else:
        if id_lista is None:
            id_lista = create_lista(nombre_lista)

    if not titulo.strip():
        st.warning("⚠️ Por favor complete el título.")
    elif not usuario_encargado.strip():
        st.warning("⚠️ Por favor indique el usuario encargado.")
    else:
        with st.spinner("Guardando tarea en la base de datos..."):
            try:
                create_task(
                    id_lista=id_lista,
                    titulo=titulo,
                    descripcion=descripcion,
                    prioridad=prioridad,
                    fecha_limite=fecha_limite,
                    usuario_encargado=usuario_encargado
                )
                st.success("✅ Tarea registrada exitosamente.")
            except Exception as e:
                st.error(f"❌ Error al guardar la tarea: {e}")

# -------- TABLA DE REGISTROS CON FILTROS -----------
st.subheader("📋 Tareas registradas")

# Crear columnas para los filtros
col1, col2 = st.columns(2)

with col1:
    filtro_prioridad = st.selectbox(
        "🔍 Filtrar por prioridad:", 
        ["Todas", "Baja", "Media", "Alta"],
        index=0
    )

with col2:
    # Obtener usuarios únicos para el filtro
    try:
        todas_tareas = get_all_tasks()
        usuarios_unicos = ["Todos"] + list(set([t.usuario_encargado for t in todas_tareas if t.usuario_encargado]))
        filtro_usuario = st.selectbox(
            "👤 Filtrar por usuario:",
            usuarios_unicos,
            index=0
        )
    except:
        filtro_usuario = "Todos"

# Aplicar filtros
try:
    # Obtener tareas según el filtro de prioridad
    if filtro_prioridad == "Todas":
        tareas = get_all_tasks()
    else:
        tareas = get_all_tasks(filtro_prioridad=filtro_prioridad)
    
    # Aplicar filtro de usuario en el frontend
    if filtro_usuario != "Todos":
        tareas = [t for t in tareas if t.usuario_encargado == filtro_usuario]
    
    if tareas:
        # Crear DataFrame
        df = pd.DataFrame([{
            "Título": t.titulo,
            "Descripción": t.descripcion,
            "Prioridad": t.prioridad,
            "Fecha límite": t.fecha_limite,
            "Usuario encargado": t.usuario_encargado,
            "Lista": t.lista.nombre

        } for t in tareas])
        
        # Mostrar estadísticas
        st.info(f"📊 Mostrando {len(tareas)} tarea(s)")
        
        # Configurar colores para prioridades
        def highlight_priority(row):
            if row['Prioridad'] == 'Alta':
                return ['background-color: #ffebee'] * len(row)
            elif row['Prioridad'] == 'Media':
                return ['background-color: #fff3e0'] * len(row)
            elif row['Prioridad'] == 'Baja':
                return ['background-color: #e8f5e8'] * len(row)
            return [''] * len(row)
        
        # Mostrar tabla con colores
        st.dataframe(
            df.style.apply(highlight_priority, axis=1),
            use_container_width=True
        )
        
        # Mostrar resumen por prioridad
        st.subheader("📈 Resumen por prioridad")
        resumen = df['Prioridad'].value_counts()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔴 Alta", resumen.get('Alta', 0))
        with col2:
            st.metric("🟡 Media", resumen.get('Media', 0))
        with col3:
            st.metric("🟢 Baja", resumen.get('Baja', 0))
            
    else:
        st.info("No hay tareas registradas con los filtros seleccionados.")
        
except Exception as e:
    st.error(f"❌ Error al cargar las tareas: {e}")
    st.error(f"Detalles del error: {str(e)}")
