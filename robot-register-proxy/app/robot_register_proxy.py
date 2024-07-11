import jwt
import json
import logging

class RobotRegisterProxy:

    __instance = None

    def __new__(self) -> __instance:
        """Implement Singleton class.
				
        Returns
		    (RobotRegisterProxy) singleton instance of the class.
        """
        if self.__instance is None:
            print('creating the %s object ...' % (self.__name__))
            self.__instance = super(RobotRegisterProxy, self).__new__(self)
        return self.__instance


    def build_message_queue(self, message_queue) -> __instance:
        """Build the message queue object.

        Args:
            message_queue (MessageQueue): the message queue controller

        Returns:
            (RobotRegisterProxy) the implemented class 
        """
        self.__message_queue = message_queue
        return self.__instance
    
    def build(self) -> __instance:
        """Build the class.

        Returns:
            (RobotRegisterProxy) the implemented class 
        """
        # TODO
        callbacks = {
            "": self.__register
        }
        self.__message_queue.build_message_callback(callbacks) \
            .build()
        return self.__instance
    

    def destroy(self) -> None:
        """Close connections and destroy variables
        """
        self.__message_queue.destroy()
        return
    

    # TODO: comment it
    def __robot_exist(self) -> bool:
        return True
    
    # TODO: comment it
    def __generate_token(self, message) -> str:
        """
        """
        return jwt.encode(message, "secret", algorithm="HS256")

    # TODO: comment it
    def __retrieve_token(self) -> str:
        return ''
    
    # TODO: comment it
    def __create_registration_response(self, token: str) -> str:
        """
        """
        return {
            "token": token
        }
    
    # TODO: comment it
    def __publish(self, message: dict) -> None:
        """
        """
        message_str = json.dumps(message) 
        self.__mqtt_client.publish(self.__message_broker_publish_topic, message_str)
        print("Published a message on %s" % (self.__message_broker_publish_topic))

    def __register(self, message) -> None:
        """

        Args:
            message (json): the message received by the robot.
        """
        if not self.__robot_exist(message):
            token = self.__generate_token(message)
        else:
            token = self.__retrieve_token(message)
        response = self.__create_registration_response(token)
        self.__publish(response)


    def start(self) -> None:
        """Start the application.
        """
        try:
            self.__mqtt_client.loop_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.destroy()