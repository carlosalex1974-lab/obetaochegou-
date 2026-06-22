import sys
import traceback

try:
    import app.main
    print("Importado com sucesso!")
except Exception as e:
    print("Erro ao importar:")
    traceback.print_exc()
