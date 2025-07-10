import streamlit as st
from database.tareas.router import create_task
from datetime import date

# Configuración de la página
st.set_page_config(page_title="Gestor de tareas", layout="centered")
st.title("Registrar nueva tarea")

# Formulario
with st.form("form_tarea"):
    titulo = st.text_input("Título de la tarea")
    descripcion = st.text_area("Descripción de la tarea")
    prioridad = st.selectbox("Prioridad", ["Baja", "Media", "Alta"])
    fecha_limite = st.date_input("Fecha límite", min_value=date.today())
    usuario_encargado = st.text_input("Usuario encargado")
    
    submitted = st.form_submit_button("Guardar tarea")

# Al hacer clic en el botón
if submitted:
    # Validaciones
    if not titulo.strip():
        st.warning("⚠️ Por favor complete el título.")
    elif not usuario_encargado.strip():
        st.warning("⚠️ Por favor indique el usuario encargado.")
    else:
        # Intentar guardar
        with st.spinner("Guardando tarea en la base de datos..."):
            try:
                create_task(
                    id_lista="3c153fa2-529d-11f0-94fb-00155da6e828",
                    titulo=titulo,
                    descripcion=descripcion,
                    prioridad=prioridad,
                    fecha_limite=fecha_limite,
                    usuario_encargado=usuario_encargado
                )
                st.success("✅ Tarea registrada exitosamente.")
            except Exception as e:
                st.error(f"❌ Error al guardar la tarea: {e}")

