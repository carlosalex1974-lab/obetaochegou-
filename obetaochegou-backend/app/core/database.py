import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Lê as credenciais do ambiente ou usa o padrão do Docker (Postgres local)
# Mas na nuvem, podemos usar sqlite
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://betao:betaopassword@localhost:5432/obetaochegou"
)

# Se for SQLite, precisa de parâmetros especiais
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Criação da engine de conexão
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Fábrica de sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependência para injetar a sessão do DB nas rotas"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
