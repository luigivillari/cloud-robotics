#!/bin/bash


SCRIPT1="dev1/agente.py"
SCRIPT2="dev2/agente.py"


if [ ! -f "$SCRIPT1" ]; then
    echo "Errore: $SCRIPT1 non esiste."
    exit 1
fi

if [ ! -f "$SCRIPT2" ]; then
    echo "Errore: $SCRIPT2 non esiste."
    exit 1
fi


echo "Eseguendo $SCRIPT1..."
python3 "$SCRIPT1" &

echo "Eseguendo $SCRIPT2..."
python3 "$SCRIPT2" &


wait

echo "Entrambi gli script sono stati eseguiti."
