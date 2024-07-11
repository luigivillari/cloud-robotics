import uuid
import json
import os
import logging
import paho.mqtt.client as mqtt

class RobotRegister:

    __instance = None

    def __new__(self) -> __instance:
        """Implement Singleton class.
				
        Returns
		    (RobotRegister) singleton instance of the class.
        """
        if self.__instance is None:
            print('creating the %s object ...' % (self.__name__))
            self.__instance = super(RobotRegister, self).__new__(self)
        return self.__instance
    
    # def __init__(self):
    #     super().__init__('robot_register', allow_undeclared_parameters=True)

    
    def build_token_path(self, token_path: str) -> __instance:
        """
        Args:
            token_path (int): absolute path where the token is stored.

        Returns:
            (RobotRegister) the implemented class
        """
        self.__token_path = token_path
        return self.__instance

    def build_message_broker_url(self, url: str) -> __instance:
        """Define the message broker URL.

        Args:
            url (str): the message broker URL.

        Returns:
            (RobotRegister) the implemented class 
        """
        self.__message_broker_url = url
        print("Built the message broker URL as %s" % (self.__message_broker_url))
        return self.__instance
    
    def build_message_broker_port(self, port: int) -> __instance:
        """Define the message broker URL.

        Args:
            port (int): the message broker port.

        Returns:
            (RobotRegister) the implemented class 
        """
        self.__message_broker_port = port
        print("Built the message broker port as %s" % (self.__message_broker_port))
        return self.__instance
    
    def build_message_broker_publish_topic(self, topic: str) -> __instance:
        """Define the message broker topic where publishing messages.

        Args:
            topic (str): the message broker topic.

        Returns:
            (RobotRegister) the implemented class 
        """
        self.__message_broker_publish_topic = topic
        print("Built the message broker topic for publication as %s" % (self.__message_broker_publish_topic))
        return self.__instance
    
    def build_message_broker_subscribe_topic(self, topic: str) -> __instance:
        """Define the message broker topic to which subscribe.

        Args:
            topic (str): the message broker topic.

        Returns:
            (RobotRegister) the implemented class 
        """
        self.__message_broker_subscribe_topic = topic
        print("Built the message broker topic for subscription as %s" % (self.__message_broker_subscribe_topic))
        return self.__instance
    
    def build(self) -> __instance:
        """
        Returns:
            (RobotRegister) the implemented class
        """
        self.__mqtt_client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id="RobotRegister",
            protocol=mqtt.MQTTv5
        )
        self.__mqtt_client.on_connect = self.__on_connect
        self.__mqtt_client.on_connect_fail = self.__on_connect_fail
        self.__mqtt_client.on_message = self.__on_message
        #TODO: fix credentials
        self.__mqtt_client.username_pw_set("admin", "admin") 
        self.__mqtt_client.connect(
            self.__message_broker_url,
            port=self.__message_broker_port,
            clean_start = True
        )
        return self.__instance
    

    def destroy(self) -> None:
        """Close connections and destroy variables
        """
        self.__mqtt_client.disconnect()
        return


    def __subscribe_topics(self, client) -> None:
        """Subscribe client to topics

        Args:
            client (paho.mqtt.client.Client): the client instance for this callback
        """
        try:
            print("Subscription to %s" % (self.__message_broker_subscribe_topic))
            result, _ = client.subscribe(self.__message_broker_subscribe_topic)
            if (result != mqtt.MQTT_ERR_SUCCESS):
                raise RuntimeError(result)
            print("Subscription to %s ... completed" % (self.__message_broker_subscribe_topic))
        except Exception as e:
            logging.error(e)

    def __token_exist(self) -> bool:
        """Verify if the token file exists and it is not empty.
        
        Returns:
            (bool) True if the token file exist, False otherwise
        """
        return os.path.isfile(self.__token_path) and \
            os.path.getsize(self.__token_path)

    def __get_mac_address(self) -> str:
        """Get the MAC address of the robot.

        Returns:
            (str) the MAC address of the robot in hexademical
        """
        return hex(uuid.getnode())

    def __get_registration_message(self, mac_address: str) -> dict:
        """Create the registration message.

        Args:
            mac_address (str): MAC address of the machine.

        Returns:
            (dict) the message.
        """
        return {
            "mac_address": mac_address
        }

    def __publish(self, message: dict) -> None:
        """Publish the message over the message broker.

        Args:
            message (dict): the registration message
        """
        message_str = json.dumps(message) 
        self.__mqtt_client.publish(self.__message_broker_publish_topic, message_str)
        print("Published a message on %s." % (self.__message_broker_publish_topic))

    def __register(self) -> None:
        """Feature for the registration of the robot.
        """
        if not self.__token_exist():
            mac_address = self.__get_mac_address()
            message = self.__get_registration_message(mac_address)
            self.__publish(message)
        
    def __on_connect(self, client, _, __, reason_code, ___) -> None:
        """Called when the CONNACK from the broker is received. 
        
        Args:
            client (paho.mqtt.client.Client): the client instance for this callback
            reason_code (paho.mqtt.reasoncodes.ReasonCode): the connection reason 
                code received from the broken.
        """
        if reason_code.is_failure:
            print("Failed to connect: %s." % (reason_code))
        else:
            self.__subscribe_topics(client)
            self.__register()
        return
    

    def __on_connect_fail(self, client, userdata) -> None:
        """The callback called when the client failed to connect to the broker.

        Args:
            client (paho.mqtt.client.Client): the client instance for this callback
            userdata (): the private user data as set in Client() or user_data_set()
        """
        print("Failed to connect.")


    def __store_token(self, message_json) -> None:
        """Store the robot token assigned by the cloud.

        Args:
            message (dict): the received message.
        """
        directory = '/'.join( self.__token_path.split('/')[:-1] )
        print(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Created the token directory.")
        with open(self.__token_path, 'w') as f:
            f.write(message_json['token'])
        print("Stored the token.")
        return

    def __on_message(self, client, userdata, message) -> None:
        """The callback called when a message has been received on a
        topic that the client subscribes to.

        Args:
            client (paho.mqtt.client.Client): the client instance for this callback
            userdata (): the private user data as set in Client() or user_data_set()
            message (paho.mqtt.client.MQTTMessage): the received message. 
        """
        message_str = message.payload.decode('utf-8')
        print("Received message from %s: %s" % (message.topic, message_str))
        message_json = json.loads(message_str)
        self.__store_token(message_json)
        return
    

    def start(self) -> None:
        """Start the application.
        """
        try:
            self.__mqtt_client.loop_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.destroy()