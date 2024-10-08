from task_repository import TaskRepository
import yaml
import json
import paho.mqtt.client as mqtt
import threading  # Importa il modulo threading
import time

class TaskManager:
    def __init__(self, config_path='conf.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.task_repository = TaskRepository()
        self.mqtt_client = mqtt.Client(client_id="manager", protocol=mqtt.MQTTv5)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set("admin", "admin")

        self.mqtt_client.connect(
            self.config['message_broker']['host'],
            port=self.config['message_broker']['port']
        )

        self.mqtt_client.loop_forever()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code " + str(rc))
        if rc == 0:
            client.subscribe(self.config['message_broker']['topics']['subscribe_to'])
            print(f"Subscribed to {self.config['message_broker']['topics']['subscribe_to']}")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
    
        thread = threading.Thread(target=self.handle_message, args=(msg,))
        thread.start()

    def handle_message(self, msg):
        """
        Funzione che gestisce il messaggio ricevuto. Viene eseguita in un thread separato.
        """
        print(f"Received message on {msg.topic}")
        try:
            data = json.loads(msg.payload)
            time_t2 = time.time()
            print(f"Message data: {data}")
            token = data['token']
            agent_id = data['agent_id']
            compose = self.assign_task(agent_id)
            print(compose)
            if token is not None:
                response = {'agent_id': agent_id, 'task': compose, 'time_t2': time_t2}
                print(response)
                topic = self.config['message_broker']['topics']['publish_to']
                full_topic = f"{topic}{agent_id}"
                self.mqtt_client.publish(full_topic, json.dumps(response))
                print(f"Published token to {full_topic}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def assign_task(self, agent_id):
        task_content = self.task_repository.get_task(agent_id)
        if task_content:
            return task_content
        else:
            return None
