from sqlalchemy import create_engine, text
from app.core.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

def run():
    with engine.connect() as conn:
        try:
            # Tenta adicionar a coluna. Se falhar, é porque possivelmente já existe ou outra coisa
            conn.execute(text("ALTER TABLE matches ADD COLUMN predictions_data JSON;"))
            conn.commit()
            print("Coluna 'predictions_data' adicionada com sucesso na tabela 'matches'.")
        except Exception as e:
            print(f"Erro ao adicionar coluna (pode já existir): {e}")

if __name__ == "__main__":
    run()
