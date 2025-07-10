from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexión a MySQL con PyMySQL
DB_URL = "mysql+pymysql://root:123Queso@127.0.0.1:3306/gestor_tareas_app"

engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)