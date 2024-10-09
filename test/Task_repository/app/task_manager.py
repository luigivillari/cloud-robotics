import os
import logging
import yaml
import json
import threading
import paho.mqtt.client as mqtt
from task_repository import TaskRepository
import time

class TaskManager:
    def __init__(self, config_path='conf.yaml'):
      
        log_dir = "/app/logs"
        os.makedirs(log_dir, exist_ok=True)  
        logging.basicConfig(
            filename=os.path.join(log_dir, 'task_manager.log'),
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

      
        logging.info("Starting TaskManager service")

       
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.task_repository = TaskRepository()

        # Configura il client MQTT
        self.mqtt_client = mqtt.Client(client_id="manager", protocol=mqtt.MQTTv5)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set("admin", "admin")

        # Connetti al broker MQTT
        try:
            self.mqtt_client.connect(
                self.config['message_broker']['host'],
                port=self.config['message_broker']['port']
            )
            logging.info("Connected to MQTT broker")
        except Exception as e:
            logging.error(f"Error connecting to MQTT broker: {e}")
        
        # Avvia il loop MQTT
        self.mqtt_client.loop_forever()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logging.info(f"Connected with result code {rc}")
            client.subscribe(self.config['message_broker']['topics']['subscribe_to'])
            logging.info(f"Subscribed to {self.config['message_broker']['topics']['subscribe_to']}")
        else:
            logging.error(f"Failed to connect, return code {rc}")


    def on_message(self, client, userdata, msg):
       
        thread = threading.Thread(target=self.handle_message, args=(client,userdata,msg))
        thread.start()

    def handle_message(self, client, userdata, msg):
        logging.info(f"Received message on {msg.topic}")
        
        try:
            data = json.loads(msg.payload)
            time_t2 = time.time()
            logging.info(f"Message data: {data}")
            token = data['token']
            agent_id = data['agent_id']
            compose = self.assign_task(agent_id)
            logging.info(f"Assigned task: {compose}")
            if token is not None:
                response = {'agent_id': agent_id, 'task': compose,'time_t2': time_t2}
                logging.info(f"Publishing response: {response}")
                topic = self.config['message_broker']['topics']['publish_to']
                full_topic = f"{topic}{agent_id}"
                self.mqtt_client.publish(full_topic, json.dumps(response))
                logging.info(f"Published token to {full_topic}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def assign_task(self, agent_id):
        task_content = self.task_repository.get_task(agent_id)
        if task_content:
            return task_content
        else:
            return None
