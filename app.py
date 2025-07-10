import streamlit as st
from database.tareas.router import create_task

st.set_page_config(page_title="Gestor de tareas", layout="centered")
st.title("Registrar nueva tarea")

with st.form("form_tarea"):
    titulo = st.text_input("Título de la tarea")
    descripcion = st.text_area("Descripción de la tarea")
    prioridad = st.selectbox("Prioridad", ["Baja", "Media", "Alta"])
    fecha_limite = st.date_input("Fecha límite")
    usuario_encargado = st.text_input("Usuario encargado")
    submitted = st.form_submit_button("Guardar tarea")

if submitted:
    if not titulo:
        st.warning("Por favor complete el título.")
    else:
        create_task(
            id_lista="3c153fa2-529d-11f0-94fb-00155da6e828",  # quemado
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            fecha_limite=fecha_limite,
            usuario_encargado=usuario_encargado
        )
        st.success("Tarea registrada exitosamente.")
