#!/bin/bash

containers=$(docker ps -a --filter "name=agente" --format "{{.ID}} {{.Names}}")

# Controlla se ci sono container con "agente" nel nome
if [ -z "$containers" ]; then
    echo "Nessun container trovato con 'agente' nel nome."
else
    echo "Container trovati:"
    echo "$containers"
    

    container_count=$(echo "$containers" | wc -l)
    
    
    docker ps -a --filter "name=agente" --format "{{.ID}}" | xargs docker rm -f
    
    echo "$container_count container eliminati."
fi
