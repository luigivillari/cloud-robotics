#!/bin/bash


BASE_DIR=$(pwd)


for i in {1..100}; do

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
echo "Tutti gli script agente.py sono stati eseguiti."
