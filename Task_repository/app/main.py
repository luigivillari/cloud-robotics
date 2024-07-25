from task_manager import TaskManager
import os


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    conffile = os.path.join(script_dir, 'conf.yaml')

    register = TaskManager(conffile)