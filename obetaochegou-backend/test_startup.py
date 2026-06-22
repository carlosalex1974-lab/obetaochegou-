import subprocess
import time
import sys

with open("backend_error.log", "w") as log_file:
    print("Iniciando uvicorn...")
    # Executa o uvicorn
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000"],
        stdout=log_file,
        stderr=subprocess.STDOUT
    )
    
    # Espera 5 segundos para ver se o processo morre ou levanta erro
    time.sleep(5)
    
    if process.poll() is not None:
        print("Processo morreu muito rápido. Verifique o log.")
    else:
        print("Processo parece estar rodando perfeitamente. Matando...")
        process.terminate()
