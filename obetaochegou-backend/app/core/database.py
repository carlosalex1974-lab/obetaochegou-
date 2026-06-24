import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usa estritamente o Postgres do Render
DATABASE_URL = "postgresql://obetaochegou_db_user:xRJ0tgDtGOnMetjNWCFY4lLROgzHKVwx@dpg-d8t9mgkm0tmc73c40s1g-a/obetaochegou_db"

# Se for SQLite, precisa de parâmetros especiais (não será, mas mantemos por segurança caso mude)
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
