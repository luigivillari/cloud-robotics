
from task_repository import TaskRepository

class TaskManager:
    def __init__(self, task_repository):
        self.task_repository = task_repository

    def assign_task(self, agent_id, task_id):
        task_content = self.task_repository.get_task(task_id)
        if task_content:
            # Simula l'assegnazione del task all'agente specificato
            print(f"Task {task_id} assegnato all'agente {agent_id}.")
            # Salva il task in un file specifico per l'agente
            with open(f'{agent_id}_docker-compose.yml', 'w') as file:
                file.write(task_content)
        else:
            print(f"Task {task_id} non trovato.")

"""
if __name__ == "__main__":
    repo = TaskRepository('conf.yaml')
    manager = TaskManager(repo)
    agent_id = 'agent123'
    task_id = 'task1'
    manager.assign_task(agent_id, task_id)
"""