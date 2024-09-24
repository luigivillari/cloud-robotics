import sys
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')

from pymongo import MongoClient
import yaml
import os
import random
import uuid

class TaskRepository:

    global_dict = {i: [] for i in range(1001, 2001)}
    def __init__(self):

        script_dir = os.path.dirname(__file__)
        config_path = os.path.join(script_dir, 'conf.yaml')

        self.config = self.load_config(config_path)
        self.client = MongoClient(self.config['mongodb']['uri'])
        self.db = self.client[self.config['mongodb']['database']]
        self.task_collection = self.db['tasks']

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)
        
    def create_uuid(self,four_digit_number):
    
        name = str(four_digit_number)
        namespace = uuid.NAMESPACE_DNS
        new_uuid = uuid.uuid5(namespace, name)
        
        return new_uuid

    def get_task(self, agent_id):
        agent_id_task = str(self.create_uuid(agent_id))
        query = {"agent_id": agent_id_task}
        int_agent_id = int(agent_id)
        
        while True:
            tasks = list(self.task_collection.find(query))
            if tasks:
                task = random.choice(tasks)
                task_id = task["id"]  
                
                if task_id not in self.global_dict[int_agent_id]:
                
                    self.global_dict[int_agent_id].append(task_id)
                    
                    return task["docker_compose"]
            else:
                return None

    def store_task_from_file(self):
            script_dir = os.path.dirname(__file__)
            compose_file_path = os.path.join(script_dir, 'docker-compose.yml')

            print(compose_file_path)

            with open(compose_file_path, 'r') as file:
                compose_content = file.read()
            
            # Stampa il contenuto letto dal file per debug
            print("Contenuto del file docker-compose.yml:")
            print(compose_content)

            task = {
                'docker_compose': compose_content
            }
            self.task_collection.insert_one(task)
            print(f"Task con file docker-compose.yml inserito nel database.")


"""
if __name__ == "__main__":
    task_repository = TaskRepository()
    task_repository.store_task_from_file()
"""
