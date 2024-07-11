import json
import paho.mqtt.client as mqtt

class MessageQueue:
    """This class implements a controller for MQTTv5
    """

    __instance = None

    def __new__(self) -> __instance:
        """Implement Singleton class.
				
        Returns
		    (MessageQueue) singleton instance of the class.
        """
        if self.__instance is None:
            print('creating the %s object ...' % (self.__name__))
            self.__instance = super(MessageQueue, self).__new__(self)
        return self.__instance
    

    def build_url(self, host: str) -> __instance:
        """Define the message broker host.

        Args:
            host (str): the message broker host.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__host = host
        print("Built the message broker host as %s" % (self.__host))
        return self.__instance
    
    def build_port(self, port: int) -> __instance:
        """Define the message broker URL.

        Args:
            port (int): the message broker port.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__port = port
        print("Built the message broker port as %s" % (self.__port))
        return self.__instance

    def build_client_name(self, name: str) -> __instance:
        """Define the client name.

        Args:
            port (int): the client name.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__name = name
        print("Built the message broker name as %s" % (self.__name))
        return self.__instance

    def build_username(self, username: str) -> __instance:
        """Define the message broker username.

        Args:
            username (str): the client name.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__username = username
        print("Built the message broker username as %s" % (self.__username))
        return self.__instance
    
    def build_password(self, password: str) -> __instance:
        """Define the message broker password.

        Args:
            password (str): the client name.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__password = password
        print("Built the message broker password as %s" % (self.__password))
        return self.__instance
    
    def build_publish_topic(self, topic: str) -> __instance:
        """Define the message broker topic where publishing messages.

        Args:
            topic (str): the message broker topic.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__publish_topic = topic
        print("Built the message broker topic for publication as %s" % (self.__publish_topic))
        return self.__instance
    
    def build_subscribe_topics(self, topics: list) -> __instance:
        """Define the message broker topics to which subscribe.

        Args:
            topics (list<str>): the message broker topics.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__subscribe_topics = topics
        print("Built the message broker topic for subscription as %s" % (self.__subscribe_topics))
        return self.__instance
    
    def build_message_callback(self, on_message_callback: dict) -> __instance:
        """Define the data structure <topic, callback> used to run 
        callback when a message is recevied..

        Args:
            on_message_callback (dict<str>): data structure <topic, callback>.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__on_message_callback = on_message_callback
        print("Built the data structure <topic, callback> for on_message features.")
        return self.__instance

    def build(self) -> __instance:
        """Build the class.

        Returns:
            (MessageQueue) the implemented class 
        """
        self.__mqtt_client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=self.__name,
            protocol=mqtt.MQTTv5
        )
        self.__mqtt_client.on_connect = self.__on_connect
        self.__mqtt_client.on_connect_fail = self.__on_connect_fail
        self.__mqtt_client.on_message = self.__on_message
        self.__mqtt_client.username_pw_set(self.__username, self.__password) 
        self.__mqtt_client.connect(
            self.__host,
            port=self.__port,
            clean_start = True
        )
        return self.__instance


    def destroy(self) -> None:
        """Close message queue connection
        """
        self.__mqtt_client.disconnect()
        return
    

    def __subscribe_topics(self, client) -> None:
        """Subscribe client to topics

        Args:
            client (paho.mqtt.client.Client): the client instance for this callback
        """
        try:
            for topics in self.__subscribe_topics:
                print("Subscription to %s" % (topics))
                result, _ = client.subscribe(topics)
                if (result != mqtt.MQTT_ERR_SUCCESS):
                    raise RuntimeError(result)
                print("Subscription to %s ... completed" % (topics))
        except Exception as e:
            print(e)

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


    def __on_connect_fail(self, client, userdata) -> None:
        """The callback called when the client failed to connect to the broker.

        Args:
            client (paho.mqtt.client.Client): the client instance for this callback
            userdata (): the private user data as set in Client() or user_data_set()
        """
        print("Failed to connect.")


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
        self.__on_message_callback[message.topic]( json.loads(message_str) )
        return