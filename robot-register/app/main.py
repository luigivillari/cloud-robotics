import yaml
import os
from robot_register import RobotRegister

def main():
    
    script_dir = os.path.dirname(__file__)
    conffile = os.path.join(script_dir, 'conf.yaml')
    
    with open(conffile, 'r') as f:
        conf = yaml.safe_load(f)

    robot_register_proxy = RobotRegister() \
        .build_token_path(conf['token_path']) \
        .build_message_broker_url(conf['message_broker']['host']) \
        .build_message_broker_port(conf['message_broker']['port']) \
        .build_message_broker_publish_topic(conf['message_broker']['topics']['publish_to']) \
        .build_message_broker_subscribe_topic(conf['message_broker']['topics']['subscribe_to']) \
        .build()
    robot_register_proxy.start()
    
if __name__ == '__main__':
    main()