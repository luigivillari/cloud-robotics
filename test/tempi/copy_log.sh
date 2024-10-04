#!/bin/bash

# Valori iniziali
initial_agent_id=1001
num_containers=120  # Cambia il numero di container

# Crea la directory per i log
mkdir -p ./logs

# Loop per copiare i file di log
for ((i=0; i<num_containers; i++))
do
    # Calcola l'AGENT_ID corrente
    agent_id=$((initial_agent_id + i))
    
    # Nome del container
    container_name="agente_$agent_id"

    # Copia il file di log dal container al sistema host
    docker cp $container_name:/app/logs/timing.log ./logs/log_$agent_id.log

    echo "Copiato il file di log per $container_name in ./logs/log_$agent_id.log"
done
