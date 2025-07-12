from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from database.base import Base

class Lista(Base):
    __tablename__ = "listas"
    id = Column(String(36), primary_key=True)
    nombre = Column(String(100), nullable=False)
    posicion = Column(Integer, nullable=False, default=0)
