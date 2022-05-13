# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 19:21:17 2020

@author: Gaston A. Nuñez - ingenganu@gmail.com
"""

import sys
from time import sleep
import logging
import paho.mqtt.client as mqtt
from threading import Thread
from copy import deepcopy, copy
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MqttClient(mqtt.Client):

    def __init__(self, client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp"):
        super(MqttClient, self).__init__(client_id, clean_session, userdata, protocol, transport)
        self.is_connected = False
        self.on_message_handles = []
        self.on_connect_handles = []
        self.on_disconnect_handles = []

        def on_connect(client: mqtt.Client, userdata, flags, rc):
            try:
                logger.info("mqttutils: Connected with result codeee " + str(rc), flags)

                if rc == 0:
                    self.is_connected = True
                    logger.info('mqttutils: rc == 0')
                else:
                    logger.info('mqttutils: rc != 0')
                
                for handle in self.on_connect_handles:
                    if callable(handle):
                        handle(client, userdata, flags, rc)
            except:
                logger.info("mqttutils: except  " + str(sys.exc_info()[0]))
                   
        def on_disconnect(client, userdata, rc):
            self.is_connected = False
            logger.info("mqttutils: Disconnect from broker with result code : " + str(rc))
            for handle in self.on_disconnect_handles:
                if callable(handle):
                    handle(client, userdata, rc)

        def on_message(client, userdata, msg: mqtt.MQTTMessage):
            for handle in self.on_message_handles:
                if callable(handle):
                    handle(client, userdata, msg)

        self.on_connect = on_connect
        self.on_message = on_message
        self.on_disconnect = on_disconnect

    def reinitialise(self, *args, **kwargs):
        try:
            copy_on_message_handles = copy(self.on_message_handles)
            copy_on_connect_handles = copy(self.on_connect_handles)
            copy_on_disconnect_handles = copy(self.on_disconnect_handles)
            super(MqttClient, self).reinitialise(*args, **kwargs)

            self.on_message_handles = copy_on_message_handles
            self.on_connect_handles = copy_on_connect_handles
            self.on_disconnect_handles = copy_on_disconnect_handles
        except Exception as e:
            print(e)

