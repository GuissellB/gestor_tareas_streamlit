from database.connection import SessionLocal
from database.listas.model import Lista
from sqlalchemy import func
import uuid

def get_all_listas():
    session = SessionLocal()
    try:
        listas = session.query(Lista).order_by(Lista.posicion).all()
        return listas
    finally:
        session.close()

def create_lista(nombre):
    session = SessionLocal()
    try:
        # Buscar posicion max actual
        max_pos = session.query(func.max(Lista.posicion)).scalar()
        nueva_posicion = (max_pos or 0) + 1

        nueva_lista = Lista(
            id=str(uuid.uuid4()),
            nombre=nombre.strip(),
            posicion=nueva_posicion
        )

        session.add(nueva_lista)
        session.commit()
        return nueva_lista.id
    finally:
        session.close()