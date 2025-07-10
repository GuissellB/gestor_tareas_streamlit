from database.tareas.model import Tarea
from database.connection import SessionLocal 
import uuid

def create_task(id_lista, titulo, descripcion, prioridad="Media", fecha_limite=None, usuario_encargado=""):
    session = SessionLocal()

    # Contar cuántas tareas ya hay en esa listas
    from sqlalchemy import func
    cantidad_actual = session.query(func.count()).select_from(Tarea).filter_by(id_lista=id_lista).scalar()
    nueva_posicion = cantidad_actual + 1

    nueva_tarea = Tarea(
        id=str(uuid.uuid4()),
        id_lista=id_lista,
        titulo=titulo.strip(),
        descripcion=descripcion.strip(),
        prioridad=prioridad,
        fecha_limite=fecha_limite,
        usuario_encargado=usuario_encargado.strip(),
        posicion=nueva_posicion
    )

    session.add(nueva_tarea)
    session.commit()
    session.close()

