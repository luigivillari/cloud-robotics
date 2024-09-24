import pymongo
import yaml
import uuid


uri = "mongodb://root:example@localhost:27017/"
client = pymongo.MongoClient(uri)
db = client["Cloud"]
collection = db["tasks"]


num_containers = 10
base_port = 23012

def create_uuid_from_number(four_digit_number):
    # Converte il numero a 4 cifre in stringa
    name = str(four_digit_number)
    
    # Usa un namespace standard, come UUID per il DNS
    namespace = uuid.NAMESPACE_DNS
    
    # Genera un UUID versione 5 basato sul namespace e sul numero
    new_uuid = uuid.uuid5(namespace, name)
    
    return new_uuid

def create_docker_compose_content(container_num, port):
    docker_compose_content = {
    'version': '3',
    'services': {
        f'engine_node_{container_num}': {
            'image': 'ros:noetic-ros-base',  # Immagine ROS Noetic di base
            'container_name': f'ros_engine_node_{container_num}',  # Nome univoco del container
            'command': f'bash -c "source /opt/ros/noetic/setup.bash && python3 -c \\"print(\'engine on\')\\""',
            'environment': [
                f'ROS_MASTER_URI=http://localhost:{port}',  # Configura il ROS Master URI con porta dinamica
                'ROS_HOSTNAME=localhost'  # Configura ROS Hostname
            ],
            'networks': [
                'ros_network'  # Collegato alla rete ros_network
            ],
            'ports': [
                f'{port}:{port}'  # Mappatura delle porte dinamiche
            ]
        }
    },
    'networks': {
        'ros_network': {
            'driver': 'bridge'  # Definizione della rete a livello globale
        }
    }
}

    
    
    return yaml.dump(docker_compose_content)


counter = 10001
temp = 0

# Loop per creare e inserire i task
for j in range(1001, 2001):
    # Crea UUID
    agent_id = str(create_uuid_from_number(j))
    for i in range(1, num_containers + 1):
        port = base_port + i - 1
        print(port)
        name = temp + i
        compose_content = create_docker_compose_content(name, port)
        
        # Converte l'UUID in formato compatibile con MongoDB
        task = {
            'id':counter,
            'agent_id': agent_id,
            'docker_compose': compose_content
        }
        
        # Inserisci il task nella collezione
        collection.insert_one(task)

        counter += 1
        temp = name
    base_port = port + 1

print(f"Successfully inserted {num_containers} Docker Compose tasks into MongoDB.")
