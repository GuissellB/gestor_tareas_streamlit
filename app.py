import streamlit as st
from database.tareas.router import create_task, get_all_tasks
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
    submitted = st.form_submit_button("Guardar tarea")

if submitted:
    if not titulo.strip():
        st.warning("⚠️ Por favor complete el título.")
    elif not usuario_encargado.strip():
        st.warning("⚠️ Por favor indique el usuario encargado.")
    else:
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

# -------- TABLA DE REGISTROS -----------
st.subheader("📋 Tareas registradas")

try:
    tareas = get_all_tasks()
    if tareas:
        df = pd.DataFrame([{
            "Título": t.titulo,
            "Descripción": t.descripcion,
            "Prioridad": t.prioridad,
            "Fecha límite": t.fecha_limite,
            "Usuario encargado": t.usuario_encargado,
            "Posición": t.posicion
        } for t in tareas])
        st.dataframe(df)
    else:
        st.info("No hay tareas registradas.")
except Exception as e:
    st.error(f"❌ Error al cargar las tareas: {e}")

