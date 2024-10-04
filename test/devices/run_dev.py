import os
import threading
import time
import subprocess

# Funzione per eseguire ogni agente
def execute_agent(dev_folder):
    agent_script = os.path.join(dev_folder, "agente.py")
    
    if os.path.isfile(agent_script):
        print(f"Esecuzione di {agent_script} nella cartella {dev_folder}...")
        subprocess.run(["python3", agent_script], cwd=dev_folder)
    else:
        print(f"File {agent_script} non trovato!")

# Impostazione base della directory e conteggio degli agenti
base_dir = os.getcwd()

# Imposta il tempo di avvio
start_time = time.time()

# Lista dei thread
threads = []

# Numero di agenti da eseguire
num_agents = 250  # Puoi modificare questo valore per eseguire più agenti

# Avvia ogni agente in un thread separato
for i in range(1, num_agents + 1):
    dev_folder = os.path.join(base_dir, f"dev{i}")
    thread = threading.Thread(target=execute_agent, args=(dev_folder,))
    threads.append(thread)
    thread.start()

# Attende che tutti i thread completino l'esecuzione
for thread in threads:
    thread.join()

# Calcola il tempo di esecuzione totale
end_time = time.time()
execution_time = end_time - start_time

print("Tutti gli script agente.py sono stati eseguiti.")
print(f"Tempo di esecuzione totale: {execution_time} secondi")
