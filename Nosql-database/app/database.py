import pymongo
from pymongo import MongoClient
import yaml
import re
import jwt

class MongoDBHandler:
    def __init__(self, config_path='conf.yaml'):
        # Load configuration from the YAML file
        self.config = self.load_config(config_path)
        self.client = MongoClient(self.config['mongodb']['uri'])
        self.db = self.client[self.config['mongodb']['database']]
        self.collection = self.db[self.config['mongodb']['collection']]

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    
    def is_valid_mac(self, mac):
        # Validate MAC address
        mac_regex = r"^[0-9A-Fa-f]{2}([-:][0-9A-Fa-f]{2}){5}$"
        return re.match(mac_regex, mac) is not None
    
    def is_registered(self, agent_id):
        # Validate MAC address
        if not self.is_valid_mac(agent_id):
            raise ValueError("Invalid MAC address")
        # Check if the agent is already registered
        return self.collection.find_one({'agent_id': agent_id}) is not None

    def get_token(self, agent_id):
        # Retrieve the token if the agent is registered
        agent = self.collection.find_one({'agent_id': agent_id})
        return agent.get('token') if agent else None
    
    def __generate_token(self, message) -> str:
        """
        """
        return jwt.encode(message, "secret", algorithm="HS256")

    def register_agent(self, agent_id, agent_data):
        # Validate MAC address
        if not self.is_valid_mac(agent_id):
            raise ValueError("Invalid MAC address")
        # Register the agent if not registered
        if not self.is_registered(agent_id):
            # Generate a token
            token = self.__generate_token({'agent_id': agent_id})
            # Insert agent data along with the generated token
            self.collection.insert_one({'agent_id': agent_id, 'token': token, **agent_data})
            return True
        return False
    


    def request_token(self, agent_id, agent_data):
        # Validate MAC address
        if not self.is_valid_mac(agent_id):
            raise ValueError("Invalid MAC address")
        # Check if agent is registered
        if not self.is_registered(agent_id):
            self.register_agent(agent_id, agent_data)
        
        # Get the token for the agent
        token = self.get_token(agent_id)
        
        return token


