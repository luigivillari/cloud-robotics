import sys
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')

from pymongo import MongoClient
import yaml
import os

class TaskRepository:
    def __init__(self):

        script_dir = os.path.dirname(__file__)
        config_path = os.path.join(script_dir, 'conf.yaml')

        self.config = self.load_config(config_path)
        self.client = MongoClient(self.config['mongodb']['uri'])
        self.db = self.client[self.config['mongodb']['database']]
        self.task_collection = self.db['Task']

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def get_task(self):
        pipeline = [
            { "$sample": { "size": 1 } }
        ]
        random_task = list(self.task_collection.aggregate(pipeline))
        if random_task:
            return random_task[0]
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
