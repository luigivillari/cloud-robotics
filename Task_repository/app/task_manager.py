
from task_repository import TaskRepository
import yaml
import json
import paho.mqtt.client as mqtt

class TaskManager:
    def __init__(self, config_path='conf.yaml'):
      
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.task_repository = TaskRepository()
        self.mqtt_client = mqtt.Client(client_id="manager", protocol=mqtt.MQTTv5)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        #self.mqtt_client.on_disconnect = self.on_disconnect
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
        print(f"Received message on {msg.topic}")
        
        try:
            data = json.loads(msg.payload)
            print(f"Message data: {data}")
            token = data['token']
            compose = self.assign_task()
            if token is not None:
                response = {'task': compose}
                print(response)
                self.mqtt_client.publish(self.config['message_broker']['topics']['publish_to'], json.dumps(response))
                print(f"Published token to {self.config['message_broker']['topics']['publish_to']}")
        except Exception as e:
            print(f"Error processing message: {e}")
                

    def assign_task(self):
        task_content = self.task_repository.get_task()
        if task_content:
            return task_content['docker_compose']
        else:
            return None
            