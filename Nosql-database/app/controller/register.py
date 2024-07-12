from database import MongoDBHandler

class Register:
    def __init__(self, config_path='conf.yaml'):
        self.db_handler = MongoDBHandler(config_path)

    def verify_and_register(self, agent_id, agent_data):
        """
        Verifica se l'agente è registrato. Se non è registrato, registra l'agente e restituisce il token.
        
        Args:
            agent_id (str): L'ID dell'agente (indirizzo MAC).
            agent_data (dict): I dati dell'agente.
        
        Returns:
            str: Il token dell'agente.
        """
        if self.db_handler.is_registered(agent_id):

            return self.db_handler.get_token(agent_id)
        else:
            
            self.db_handler.register_agent(agent_id, agent_data)
            return self.db_handler.get_token(agent_id)


