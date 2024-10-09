#!/bin/bash


initial_agent_id=1001
num_containers=120  


mkdir -p ./logs_fsm


for ((i=0; i<num_containers; i++))
do

    agent_id=$((initial_agent_id + i))
    
   
    container_name="agente_$agent_id"

   
    docker cp $container_name:/app/logs/timing.log ./logs_fsm/log_$agent_id.log

    echo "Copiato il file di log per $container_name in ./logs_fsm/log_$agent_id.log"
done
