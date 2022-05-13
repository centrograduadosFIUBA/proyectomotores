# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:31:17 2020

@author: Gaston A. Nuñez - ingenganu@gmail.com
"""

import os
import paho.mqtt.client as mqtt
from mqttutils import MqttClient
import logging
LOG_PATH = "../log/"
LOG_FILENAME = "log.txt"
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH, exist_ok=True)

fileLogHandler = logging.FileHandler(os.path.join(LOG_PATH, LOG_FILENAME))
streamLogHandler = logging.StreamHandler()
logging.basicConfig(handlers=[fileLogHandler, streamLogHandler],
                    format="%(levelname)s: %(name)s: %(asctime)s ==> %(message)s",
                    datefmt="%y-%m-%d %H:%M:%S",
                    level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
DEFAULT_HOST = "broker.mqttdashboard.com"
from pymongo import MongoClient
import json
import datetime

try:
    myfile = open('..//..//JSONs//20191209_151320_borrar.json', 'r')
    data=myfile.read()
    muestreoJson = json.loads(data) 
    clientDB = MongoClient('mongodb://localhost:27017/')
    db = clientDB['MotorTests']
    insResult = db.MensajesMQTT.insert_one(muestreoJson)
    if insResult.acknowledged:
        print('insertado ok')
    else:
        pint('no se inserto')
    clientDB.server_info()
except:
    print('el cliente se desconecto')

