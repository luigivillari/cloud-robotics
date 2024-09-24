import sys

sys.path.append('/opt/homebrew/lib/python3.11/site-packages')

import os
import paho.mqtt.client as mqtt
import json
import subprocess
import time


script_dir = os.path.dirname(__file__)
state_machine_dir = os.path.join(script_dir, '..', 'state_machine')
sys.path.append(state_machine_dir)

from macchina_stati import StateMachineApp
#agent_id = "00:1A:2B:3C:4D:5E"
agent_id="1001"
Nodo_edge = StateMachineApp()

# Configurazione del broker MQTT
broker_host = "localhost"
broker_port = 1883
publish_topic = "/it/unime/fcrlab/robotics/register"
subscribe_topic = "/it/unime/fcrlab/robotics/register/token"
publish_topic_task = "/it/unime/fcrlab/robotics/task/request"
subscribe_topic_task = "/it/unime/fcrlab/robotics/task/response"

compose_file_path = os.path.join(os.path.dirname(__file__), 'docker-compose.yml')

def create_hidden_file(token):
    hidden_file = ".token"
    with open(hidden_file, "w") as file:
        file.write(token) 

def check_hidden_file():
    hidden_file = ".token"
    if os.path.isfile(hidden_file):
        with open(hidden_file, "r") as file:
            content = file.read().strip()
            if content:
                Nodo_edge.machine.request_token()
                return True, content
    return False, None

def check_local_compose():
    """Controlla se esiste un file docker-compose.yml locale"""
    return os.path.isfile(compose_file_path)

def run_local_compose():
    """Esegue il file docker-compose.yml locale"""
    print(f"Esecuzione di {compose_file_path}")
    try:
        Nodo_edge.machine.run()  # Aggiorna lo stato della macchina a "run"
        print(Nodo_edge.machine.state)
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        print("Servizi avviati con docker-compose locale")
    except Exception as e:
        print(f"Errore durante l'esecuzione di docker-compose locale: {e}")

def request_new_task(client, token):
    Nodo_edge.machine.request_compose()
    """Funzione per richiedere una nuova task"""
    request = {'agent_id': agent_id, 'token': token}
    print(f"Requesting new task with token: {token}")
    client.publish(publish_topic_task, json.dumps(request))

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))

    print(Nodo_edge.machine.state)
    file_exists, token = check_hidden_file()

    if not file_exists:
        client.subscribe(publish_topic)
        print(f"Subscribed to {subscribe_topic}")
        Nodo_edge.machine.request_token()
        request = {'agent_id': agent_id}
        client.publish(subscribe_topic, json.dumps(request))
        print(f"Published request to {publish_topic}")

    else:
        # Prima di richiedere nuove task, eseguiamo il docker-compose locale se esiste
        if check_local_compose():
            Nodo_edge.machine.request_compose()
            print("Compose locale trovato, eseguo il compose")
            run_local_compose()
            Nodo_edge.machine.finish()

        client.subscribe(subscribe_topic_task)
        print(f"Subscribed to task_topic {subscribe_topic_task}")

        request_new_task(client, token)

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}")
    response = json.loads(msg.payload)
    
    if msg.topic == publish_topic:
        if response['agent_id'] == agent_id:
            print("Received token:", response['token'])
            create_hidden_file(response['token'])

            Nodo_edge.machine.request_token()
            print(Nodo_edge.machine.state)

            client.subscribe(subscribe_topic_task)
            print(f"Subscribed to task_topic {subscribe_topic_task}")

            request_new_task(client, response['token'])

    elif msg.topic == subscribe_topic_task:
        if 'task' in response:
            task_content = response['task']
            compose_file_path = os.path.join(os.path.dirname(__file__), 'docker-compose.yml')

            Nodo_edge.machine.request_compose()
            print(Nodo_edge.machine.state)

            try:
                with open(compose_file_path, 'w') as file:
                    file.write(task_content)
                print(f"File docker-compose.yml creato in {compose_file_path}")
                
                Nodo_edge.machine.run()
                print(Nodo_edge.machine.state)

                # Esegui docker-compose up
                subprocess.run(['docker-compose', 'up', '-d'], check=True)
                print("Servizi avviati con docker-compose")
                Nodo_edge.machine.finish()
                # Richiedi una nuova task dopo l'esecuzione della precedente
                _, token = check_hidden_file()
                if token:
                    request_new_task(client, token)
                
            except Exception as e:
                print(f"Errore durante la gestione del task: {e}")
        else:
            print("No task received or invalid response")

agent_client = mqtt.Client(client_id=agent_id, protocol=mqtt.MQTTv5)
agent_client.on_connect = on_connect
agent_client.on_message = on_message
agent_client.username_pw_set("admin", "admin")

agent_client.connect(broker_host, broker_port)
agent_client.loop_forever()
