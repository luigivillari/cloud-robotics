import sys

# Aggiungi il percorso della libreria al sys.path
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')

import paho.mqtt.client as mqtt
import json
import subprocess
import os
from getmac import get_mac_address
import time
start_time_t0 = 0
start_time_t1 = 0


agent_id = os.getenv("AGENT_ID", "default_id")

# Configurazione del broker MQTT
broker_host = "172.30.101.3"
broker_port = 1883
publish_topic = "/it/unime/fcrlab/robotics/register1001"
subscribe_topic = "/it/unime/fcrlab/robotics/register/token"
publish_topic_task = "/it/unime/fcrlab/robotics/task/request"
subscribe_topic_task = "/it/unime/fcrlab/robotics/task/response1001"

def create_hidden_file(token):
    hidden_file = os.path.join(os.getcwd(), ".token")
    with open(hidden_file, "w") as file:
        file.write(token) 
    print(f"Creato il file .token in: {hidden_file}")

def check_hidden_file():
    hidden_file = ".token"
    if os.path.isfile(hidden_file):
        with open(hidden_file, "r") as file:
            content = file.read().strip()
            if content:
                return True, content
    return False, None


def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    global start_time_t0
    file_exists, token = check_hidden_file()

    if not file_exists:
        
        client.subscribe(publish_topic)
        print(f"Subscribed to {subscribe_topic}")
        start_time_t0 = time.time()
        request = {'agent_id': agent_id}
        client.publish(subscribe_topic, json.dumps(request))
        print(f"Published request to {publish_topic}")

    else:
        client.subscribe(subscribe_topic_task)
        print(f"Subscribed to task_topic {subscribe_topic_task}")

        request = {'agent_id': agent_id, 'token': token}
        client.publish(publish_topic_task, json.dumps(request))
        print(f"Published request to task_topic {publish_topic_task}")

    


def on_message(client, userdata, msg):
    global start_time_t1
    print(f"Received message on {msg.topic}")
    response = json.loads(msg.payload)
    
    if msg.topic == publish_topic:
        end_time_t1 = time.time()
        print(f"tempo dall'invio della richiesta alla risposta: {end_time_t1 - start_time_t0}")
        print(f"tempo dall'invio della richiesta alla ricezione della richiesta: {response['time_t1'] - start_time_t0}")
        if response['agent_id'] == agent_id:
            print("Received token:", response['token'])
            create_hidden_file(response['token'])

            client.subscribe(subscribe_topic_task)
            print(f"Subscribed to task_topic {subscribe_topic_task}")

            request = {'agent_id': agent_id, 'token': response['token']}
            print(request)
            start_time_t1 = time.time()
            client.publish(publish_topic_task, json.dumps(request))
            print(f"Published request to task_topic {publish_topic_task}")
            
    elif msg.topic == subscribe_topic_task:
        # Filtra per agent_id, ma non disconnetterti se l'ID non corrisponde
        end_time_t2 = time.time()
        print(f"tempo dall'invio della richiesta alla risposta: {end_time_t2 - start_time_t1}")
        print(f"tempo dall'invio della richiesta alla ricezione della richiesta: {response['time_t2'] - start_time_t1}")
        if response['agent_id'] == agent_id:
            if response['task']:
                task_content = response['task']
                compose_file_path = os.path.join(os.path.dirname(__file__), 'docker-compose.yml')

                try:
                    start_time_t2 = time.time()
                    with open(compose_file_path, 'w') as file:
                        file.write(task_content)
                    print(f"File docker-compose.yml creato in {compose_file_path}")
                    
                    # Esegui docker-compose up
                    #subprocess.run(['docker-compose', 'up', '-d'], check=True)
                    #docker run --network cloud -p 1885:1883 -v /var/run/docker.sock:/var/run/docker.sock -it device-image
                    os.system('docker-compose up -d')
                    end_time_t3 = time.time()
                    print(f"tempo di avvio compose: {end_time_t3 - start_time_t2} ")
                    print("Servizi avviati con docker-compose")
                    
                except Exception as e:
                    print(f"Errore durante la gestione del task: {e}")
                
                # Disconnessione solo dopo aver completato il task corretto
                client.disconnect()
            else:
                print("No task received for this agent")
        else:
            print(f"Invalid response for this agent_id: {response['agent_id']}")

agent_client = mqtt.Client(client_id=agent_id, protocol=mqtt.MQTTv5)

agent_client.on_connect = on_connect
agent_client.on_message = on_message
agent_client.username_pw_set("admin", "admin")

agent_client.connect(broker_host, broker_port)
agent_client.loop_forever()
