#!/bin/bash

export COMPOSE_HTTP_TIMEOUT=500
BASE_DIR=$(pwd)

start_time=$(date +%s.%N)

# Esegui 50 agenti in parallelo, ognuno indipendente
for i in {1..125}; do
  DEV_FOLDER="$BASE_DIR/dev$i"
  AGENT_SCRIPT="$DEV_FOLDER/agente.py"

  if [ -f "$AGENT_SCRIPT" ]; then
    echo "Esecuzione di $AGENT_SCRIPT nella cartella $DEV_FOLDER..."
    
    # Usa nohup per eseguire lo script in background e disconnetterlo dal terminale
    (cd "$DEV_FOLDER" && nohup python3 "$AGENT_SCRIPT" > "$DEV_FOLDER/agent_log_$i.log" 2>&1 &) 
  else
    echo "File $AGENT_SCRIPT non trovato!"
  fi
done

# Attende che tutti i processi abbiano terminato
wait

end_time=$(date +%s.%N)
execution_time=$(echo "$end_time - $start_time" | bc)

echo "Tutti gli script agente.py sono stati eseguiti."
echo "Tempo di esecuzione totale: $execution_time secondi"
