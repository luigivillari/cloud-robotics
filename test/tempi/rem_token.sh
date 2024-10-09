#!/bin/bash


file_to_delete="/app/.token"


for container_name in $(docker ps --filter "name=agente" --format "{{.Names}}"); do
  echo "Eliminando $file_to_delete dal container $container_name..."


  docker exec $container_name rm -f $file_to_delete
  

  if [ $? -eq 0 ]; then
    echo "File eliminato con successo dal container $container_name."
  else
    echo "Errore durante l'eliminazione del file nel container $container_name."
  fi
done