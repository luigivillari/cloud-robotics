import subprocess
import threading


def start_agent_container(agent_id):
    container_name = f"agente_{agent_id}"
    command = f"docker start {container_name}"
    subprocess.run(command, shell=True)


def launch_agents_in_parallel(start_id, num_agents):
    threads = []
    for i in range(num_agents):
        agent_id = start_id + i
        thread = threading.Thread(target=start_agent_container, args=(agent_id,))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()


launch_agents_in_parallel(1001, 120)
