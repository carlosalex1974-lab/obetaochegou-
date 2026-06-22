from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api import matches

# Cria as tabelas do banco de dados na inicialização se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OBetãoChegou!!! API",
    description="Backend para a plataforma preditiva de análise esportiva.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os roteadores da API
app.include_router(matches.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "OBetãoChegou API está online! 🚀⚽"}
