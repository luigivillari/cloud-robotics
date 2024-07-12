from pymongo import MongoClient
import yaml

class TaskRepository:
    def __init__(self, config_path='conf.yaml'):
        self.config = self.load_config(config_path)
        self.client = MongoClient(self.config['mongodb']['uri'])
        self.db = self.client[self.config['mongodb']['database']]
        self.task_collection = self.db['Task']

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def get_task(self, task_id):
        task = self.task_collection.find_one({'task_id': task_id})
        if task:
            return task['docker_compose']
        else:
            print(f"Task {task_id} non trovato.")
            return None

    def store_task_from_file(self, task_id, compose_file_path):
        with open(compose_file_path, 'r') as file:
            compose_content = file.read()
        
        task = {
            'task_id': task_id,
            'docker_compose': compose_content
        }
        self.task_collection.insert_one(task)
        print(f"Task {task_id} con file docker-compose.yml inserito nel database.")

