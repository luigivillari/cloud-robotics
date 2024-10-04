import os
import re
import csv

# Directory dove sono salvati i file di log
log_directory = './logs'  # Assicurati che questa directory contenga i file di log es. log_1001.log

# File CSV di output
csv_file = 'timing_data_120.csv'

# Definisci la regex per trovare i tempi nel formato 't0-t1', 't1-t2', 't2-t3', 't3-t0'
time_pattern = re.compile(r"t(\d)-t(\d):\s*([\d.]+)")  # Trova pattern tipo "t0-t1: 0.010557889938354492"

# Lista per memorizzare i dati raccolti
log_data = []

# Scorri tutti i file di log nella directory
for log_file in os.listdir(log_directory):
    if log_file.endswith('.log'):
        # Estrai l'ID del container dal nome del file (es. log_1001.log -> ID=1001)
        container_id = log_file.split('_')[1].split('.')[0]  # Estrai l'ID del container

        # Inizializza i tempi con None
        t0_t1, t1_t2, t2_t3, t3_t0 = None, None, None, None

        # Leggi il contenuto del file di log
        with open(os.path.join(log_directory, log_file), 'r') as file:
            for line in file:
                match = time_pattern.search(line)
                if match:
                    # Estrai i tempi basati sulle corrispondenze con regex
                    t_start = match.group(1)
                    t_end = match.group(2)
                    time_value = float(match.group(3))

                    # Assegna il valore corretto a seconda del pattern trovato
                    if t_start == "0" and t_end == "1":
                        t0_t1 = time_value
                    elif t_start == "1" and t_end == "2":
                        t1_t2 = time_value
                    elif t_start == "2" and t_end == "3":
                        t2_t3 = time_value
                    elif t_start == "3" and t_end == "0":
                        t3_t0 = time_value
        
        # Se tutti i tempi sono stati trovati, aggiungili alla lista
        if t0_t1 is not None and t1_t2 is not None and t2_t3 is not None and t3_t0 is not None:
            log_data.append([container_id, t0_t1, t1_t2, t2_t3, t3_t0])

# Ordina i dati per ID del container
log_data.sort(key=lambda x: int(x[0]))

# Scrivi i dati in un file CSV
with open(csv_file, mode='w', newline='') as csv_output:
    csv_writer = csv.writer(csv_output)
    # Scrivi l'intestazione
    csv_writer.writerow(['ID', 't0-t1', 't1-t2', 't2-t3', 't3-t0'])
    # Scrivi i dati raccolti
    csv_writer.writerows(log_data)

print(f"Dati salvati in {csv_file}")
