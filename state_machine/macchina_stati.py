import sys
import time
from os.path import join, realpath, dirname
import logging

sys.path.append(join(dirname(realpath(__file__)), ".."))

from transitions_gui import WebMachine  # noqa

logging.basicConfig(level=logging.INFO)

class StateMachineApp:
    def __init__(self):
        # Definizione degli stati
        self.states = ["init", "have token", "have compose", "running", "done"]

        # Definizione delle transizioni esplicite (senza "next_state")
        self.transitions = [
            ["request_token", "init", "have token"], 
            ["request_compose", "have token", "have compose"],  
            ["run", "have compose", "running"],  
            ["finish", "running", "done"], 
            ["request_compose", "done", "have compose"],  
        ]

       
        self.styling = [
           
            {"selector": 'node', "css": {"shape": "ellipse"}},
        ]

        
        self.machine = WebMachine(
            states=self.states,
            transitions=self.transitions,
            initial="init",
            name="Simple Machine",
            ordered_transitions=False,  
            ignore_invalid_triggers=True,
            auto_transitions=False, 
            graph_css=self.styling  
        )

    # def run(self):
    #     """Avvia la macchina a stati e gestisce le transizioni manualmente"""
    #     try:
    #         while True:
    #             time.sleep(5)
            
    #             if self.machine.state == 'init':
    #                 self.machine.request_token()
    #                 print(self.machine.state) 
    #             elif self.machine.state == 'have token':
    #                 self.machine.request_compose()  
    #             elif self.machine.state == 'have compose':
    #                 self.machine.run()  
    #             elif self.machine.state == 'running':
    #                 self.machine.finish() 
    #             elif self.machine.state == 'done':
    #                 self.machine.request_compose() 
    #     except KeyboardInterrupt:  
    #         self.machine.stop_server()
    #         logging.info("Macchina a stati interrotta manualmente.")


if __name__ == "__main__":
    app = StateMachineApp()
    app.machine.run()
    
    