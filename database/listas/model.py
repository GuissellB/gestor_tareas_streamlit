from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from database.base import Base

class Lista(Base):
    __tablename__ = "listas"
    id = Column(String(36), primary_key=True)
    id_tablero = Column(String(36), ForeignKey("tableros.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    posicion = Column(Integer, nullable=False, default=0)
