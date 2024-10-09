import sys

sys.path.append('/opt/homebrew/lib/python3.11/site-packages')

import os
import logging
import paho.mqtt.client as mqtt
import json
import yaml
import threading
from database import MongoDBHandler
import time

class Register:
    def __init__(self, config_path='conf.yaml'):

        log_dir = "/app/logs"
        os.makedirs(log_dir, exist_ok=True) 
        logging.basicConfig(
            filename=os.path.join(log_dir, 'register.log'),
            filemode='a',  
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

  
        logging.info("Starting Register service")

        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.db_handler = MongoDBHandler(config_path)

        self.mqtt_client = mqtt.Client(client_id="register", protocol=mqtt.MQTTv5)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.username_pw_set("admin", "admin")

        try:
            self.mqtt_client.connect(
                self.config['message_broker']['host'],
                port=self.config['message_broker']['port']
            )
            logging.info("Connected to MQTT broker")
        except Exception as e:
            logging.error(f"Error connecting to MQTT broker: {e}")
        
        self.mqtt_client.loop_forever()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logging.info("Connected with result code " + str(rc))
        if rc == 0:
            client.subscribe(self.config['message_broker']['topics']['subscribe_to'])
            logging.info(f"Subscribed to {self.config['message_broker']['topics']['subscribe_to']}")
        else:
            logging.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc,proprieties=None):
        logging.info("Disconnected with result code " + str(rc))
        if rc != 0:
            logging.warning("Unexpected disconnection.")

    def on_message(self, client, userdata, msg):
        thread = threading.Thread(target=self.handle_message, args=(client,userdata,msg))
        thread.start()
    

    def handle_message(self, client, userdata, msg):
        logging.info(f"Received message on {msg.topic}")
        try:
            data = json.loads(msg.payload)
            time_t1 = time.time()
            logging.info(f"Message data: {data}")
            agent_id = data['agent_id']
            token = self.verify_and_register(agent_id)
            logging.info(f"Token generated: {token}")
            response = {'agent_id': agent_id, 'token': token, 'time_t1': time_t1}
            topic = self.config['message_broker']['topics']['publish_to']
            full_topic = f"{topic}{agent_id}"
            self.mqtt_client.publish(full_topic, json.dumps(response))
            logging.info(f"Published token to {full_topic}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")


    def verify_and_register(self, agent_id):
        """
        Verifica se l'agente è registrato. Se non è registrato, registra l'agente e restituisce il token.
        
        Args:
            agent_id (str): L'ID dell'agente (indirizzo MAC).
        
        Returns:
            str: Il token dell'agente.
        """
        if self.db_handler.is_registered(agent_id):
            return self.db_handler.get_token(agent_id)
        else:
            token = self.db_handler.generate_token({'agent_id': agent_id})
            if not isinstance(token, str):
                token = str(token) 

            self.db_handler.register_agent(agent_id, token)
            return token
