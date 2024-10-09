#!/bin/bash


initial_agent_id=1001
initial_port=1890
num_containers=120

for ((i=0; i<num_containers; i++))
do

    agent_id=$((initial_agent_id + i))
    port=$((initial_port + i * 2)) 


    container_name="agente_$agent_id"


    docker create --network cloud -p $port:1883 -v /var/run/docker.sock:/var/run/docker.sock -e AGENT_ID=$agent_id --name $container_name device-image

    echo "Avviato container $container_name sulla porta $port con AGENT_ID=$agent_id"
done

#docker ps -a --filter "name=agente_" --format "{{.Names}}" | xargs docker start