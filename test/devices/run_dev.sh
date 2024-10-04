#!/bin/bash

export COMPOSE_HTTP_TIMEOUT=500
BASE_DIR=$(pwd)


start_time=$(date +%s.%N)

for i in {1..250}; do
  DEV_FOLDER="$BASE_DIR/dev$i"
  AGENT_SCRIPT="$DEV_FOLDER/agente.py"

  if [ -f "$AGENT_SCRIPT" ]; then
    echo "Esecuzione di $AGENT_SCRIPT nella cartella $DEV_FOLDER..."
    
   
    (cd "$DEV_FOLDER" && python3 "$AGENT_SCRIPT") &
  else
    echo "File $AGENT_SCRIPT non trovato!"
  fi
done


wait


end_time=$(date +%s.%N)
execution_time=$(echo "$end_time - $start_time" | bc)

echo "Tutti gli script agente.py sono stati eseguiti."
echo "Tempo di esecuzione totale: $execution_time secondi"
