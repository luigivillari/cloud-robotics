import yaml
from robot_register_proxy import RobotRegisterProxy
from controllers.message_queue import MessageQueue
from domain.register import Register


def main():
    conffile = 'conf.yaml'
    with open(conffile, 'r') as f:
        conf = yaml.safe_load(f)

    register = Register().get()

    callbacks = {
        conf['message_broker']['topics']['subscribe_to']: register
    }

    message_queue = MessageQueue() \
        .build_url(conf['message_broker']['host']) \
        .build_port(conf['message_broker']['port']) \
        .build_client_name(conf['message_broker']['client_name']) \
        .build_username(conf['message_broker']['username']) \
        .build_password(conf['message_broker']['password']) \
        .build_publish_topic(conf['message_broker']['topics']['publish_to']) \
        .build_subscribe_topics(conf['message_broker']['topics']['subscribe_to']) \
        .build_message_callback(callbacks) \
        .build()
    
        
    proxy = RobotRegisterProxy() \
        .build_message_queue(message_queue) \
        .build()
    proxy.start()
    
if __name__ == '__main__':
    main()