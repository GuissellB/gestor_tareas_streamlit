from database.tareas.model import Tarea
from database.connection import SessionLocal 
import uuid

def create_task(id_lista, titulo, descripcion, prioridad="Media", fecha_limite=None, usuario_encargado=""):
    session = SessionLocal()

    # Contar cuántas tareas ya hay en esa lista
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


def get_all_tasks(filtro_prioridad=None):
    """
    Obtiene todas las tareas almacenadas en la base de datos.
    
    Args:
        filtro_prioridad (str, optional): Filtrar por prioridad específica.
                                        Valores válidos: "Baja", "Media", "Alta"
    
    Returns:
        list: Lista de objetos Tarea
    """
    session = SessionLocal()
    try:
        query = session.query(Tarea)
        
        # Aplicar filtro de prioridad si se especifica
        if filtro_prioridad:
            query = query.filter(Tarea.prioridad == filtro_prioridad)
        
        # Ordenar por posición (opcional)
        tareas = query.order_by(Tarea.posicion).all()
        return tareas
    finally:
        session.close()


def get_tasks_by_priority(prioridad):
    """
    Función alternativa específica para filtrar por prioridad.
    
    Args:
        prioridad (str): Prioridad a filtrar ("Baja", "Media", "Alta")
    
    Returns:
        list: Lista de tareas con la prioridad especificada
    """
    session = SessionLocal()
    try:
        tareas = session.query(Tarea).filter(Tarea.prioridad == prioridad).order_by(Tarea.posicion).all()
        return tareas
    finally:
        session.close()


def get_tasks_by_user(usuario_encargado):
    """
    Función adicional para filtrar por usuario encargado.
    
    Args:
        usuario_encargado (str): Usuario encargado a filtrar
    
    Returns:
        list: Lista de tareas del usuario especificado
    """
    session = SessionLocal()
    try:
        tareas = session.query(Tarea).filter(Tarea.usuario_encargado == usuario_encargado).order_by(Tarea.posicion).all()
        return tareas
    finally:
        session.close()

