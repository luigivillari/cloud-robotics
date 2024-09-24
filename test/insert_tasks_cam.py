import pymongo
import yaml
import uuid


# Configurazione MongoDB
uri = "mongodb://root:example@localhost:27017/"
client = pymongo.MongoClient(uri)
db = client["Cloud"]
collection = db["tasks"]

num_containers = 10
base_port = 12012

def create_uuid_from_number(four_digit_number):
    
    name = str(four_digit_number)
    namespace = uuid.NAMESPACE_DNS
    new_uuid = uuid.uuid5(namespace, name)
    
    return new_uuid

def create_docker_compose_content(container_num, port):
    docker_compose_content = {
    'version': '3',
    'services': {
        f'camera_node_{container_num}': {
            'image': 'ros:noetic-ros-base',  # Immagine ROS Noetic
            'container_name': f'ros_camera_node_{container_num}', 
            'command': f'bash -c "source /opt/ros/noetic/setup.bash && python3 -c \\"print(\'camera on\')\\""',
            'environment': [
                f'ROS_MASTER_URI=http://localhost:{port}', 
                'ROS_HOSTNAME=localhost'  
            ],
            'ports': [f'{port}:{port}']  # Espone la porta 
        }
    }
}
    return yaml.dump(docker_compose_content,  sort_keys=False)

counter = 1


# Loop per creare e inserire i task
for j in range(1001, 2001):
    # Crea UUID
    agent_id = str(create_uuid_from_number(j))
    for i in range(1, num_containers + 1):
        port = base_port + i - 1
        print(port)
       
        compose_content = create_docker_compose_content(counter, port)
        # Converte l'UUID in formato compatibile con MongoDB
        task = {
            'id':counter,
            'agent_id': agent_id,
            'docker_compose': compose_content
        }
        
        # Inserisci il task nella collezione
        collection.insert_one(task)

        counter += 1
    base_port = port + 1


print(f"Successfully inserted {num_containers * (2001 - 1001)} Docker Compose tasks for camera into MongoDB.")
