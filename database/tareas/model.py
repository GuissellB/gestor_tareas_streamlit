from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Enum, Integer, ForeignKey, DateTime, Date
from datetime import datetime
from database.base import Base
from database.listas.model import Lista  

class Tarea(Base):
    __tablename__ = "tareas"
    id = Column(String(36), primary_key=True)
    id_lista = Column(String(36), ForeignKey("listas.id", ondelete="CASCADE"))
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    prioridad = Column(Enum('Baja', 'Media', 'Alta'), default="Media")
    fecha_limite = Column(Date)
    usuario_encargado = Column(String(100))
    posicion = Column(Integer, default=0)
    creado_en = Column(DateTime, default=datetime.utcnow)