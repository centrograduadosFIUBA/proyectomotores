# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:51:41 2020

@author: Gaston A. Nuñez - ingenganu@gmail.com
"""

import os
import random
import sys
import uuid
from PyQt5 import Qt
from time import sleep
import datetime
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
import paho.mqtt.client as mqtt
from mqtt import MqttClient
from ui.ui_main_window import Ui_MainWindow
from pymongo import MongoClient
from getmac import get_mac_address as gma
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

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.checkBoxCleanSession.setChecked(True)
        self.spinBoxKeepAlive.setValue(60)
        self.lineEditHostIOT.setText(DEFAULT_HOST)
        self.comboBoxSubTopics.setEditable(True)
        self.statusbar.show()
        self.IOT_Connected = False
        self.mqtt_client = None
        self.DB_Connected = False
        self.checkBoxAutoConnect.setChecked(True)
        self.lineEditPortClientId.setText(gma())
        if self.checkBoxAutoConnect.isChecked():
            self.ConnectIOT()
            self.ConnectDB()
 
    @pyqtSlot(int)
    def on_comboBoxSubTopics_currentIndexChanged(self, i):
        logger.debug("current index {}".format(i))

    def on_mqtt_msg(self, client, userdata, message: mqtt.MQTTMessage):
        msg = message.payload.decode()
        logger.info("client received msg: topic:{0} ||  payload:{1}".format(message.topic, msg[0:199]))
        msg = str(datetime.datetime.now())[:-7] + ": " + message.topic + " == " + msg[0:199]
        self.textBrowserReceived.append(msg)
        
        if self.DB_Connected:
            self.db.MensajesMQTT.insert_one(muestreoJson)
            insResult = db.MensajesMQTT.insert_one(muestreoJson)   
            if insResult.acknowledged:
                self.textBrowserReceived.append('/n/tDATOS IOT GUARDADOS OK/n')
            else:
                self.textBrowserReceived.append('/n/tERROR: NO SE PUEDO INSERTAR EL DOCUMENTO EN DB/n')
                logger.info("ERROR: NO SE PUEDO INSERTAR EL DOCUMENTO EN DB")
        else:
            self.textBrowserReceived.append('/n/tSIN CONEXION AL SERVIDOR DB. IMPOSIBLE GUARDAR DATOS IOT/n')

    def on_mqtt_connect(self, client, userdata, flags, rc):
        logger.info("client connected userdata:{0} || flags:{1} ||  rc:{2}".format(userdata, flags, rc))
        
        try:
            topic=self.comboBoxSubTopics.currentText()
            
            if self.mqtt_client.is_connected:
                logger.info(" sub to mqtt topic: {}".format(topic))
                self.mqtt_client.subscribe(topic, qos=2)
                self.IOT_Connected = True
                if self.DB_Connected:
                    self.statusbar.showMessage("cliente IOT conectado - cliente DB conectado")
                else:
                    self.statusbar.showMessage("cliente IOT conectado - cliente DB DESCONECTADO")
            else:
                logger.info("sub failed, client is not connected")
        except:
            logger.info("except: on_mqtt_connect  " + str(sys.exc_info()[0]) + ' ' + str(sys.exc_info()[1]) + ' ' + str(sys.exc_info()[2]))

    def on_mqtt_disconnect(self, client, userdata, rc):
        logger.info("client disconnected userdata:{0} || rc:{1}".format(userdata, rc))
        topic=self.comboBoxSubTopics.currentText()
        logger.info("unsub to mqtt topic: {}".format(topic))
        self.mqtt_client.unsubscribe(topic=topic)
        self.IOT_Connected = False
        if self.DB_Connected:
            self.statusbar.showMessage("cliente IOT DESCONECTADO - cliente DB conectado") 
        else:
            self.statusbar.showMessage("cliente IOT DESCONECTADO - cliente DB DESCONECTADO")
        
        if self.checkBoxAutoConnect.isChecked():
            ConnectIOT(self)
      
    @pyqtSlot(bool)
    def on_pushButtonConnect_clicked(self, para):
        self.ConnectIOT(self)
        
    def ConnectIOT(self):
        host = self.lineEditHostIOT.text()
        port = int(self.lineEditPortIOT.text())
        logger.info("connecting to IOT host: {0}:{1}".format(host, port))
        client_id = self.lineEditPortClientId.text()
        keepalive = int(self.spinBoxKeepAlive.value())
        clean_session = self.checkBoxCleanSession.isChecked()
        username = self.lineEditPortUserNameI.text()
        password = self.lineEditPortPassword.text()
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.reinitialise(client_id=client_id, clean_session=clean_session)
        else:
            self.mqtt_client = MqttClient(client_id=client_id, clean_session=clean_session)
            self.mqtt_client.on_message_handles.append(self.on_mqtt_msg)
            self.mqtt_client.on_connect_handles.append(self.on_mqtt_connect)
            self.mqtt_client.on_disconnect_handles.append(self.on_mqtt_disconnect)
        try:
            self.mqtt_client.username_pw_set(username=username, password=password)
            rc = self.mqtt_client.connect(host=host, port=port, keepalive=keepalive) 
            
            logger.info("client called connect with rc: {}".format(rc))
            if rc == 0:
                self.pushButtonConnectIOT.setEnabled(False)
            self.statusbar.showMessage("mqtt client is connecting!")
            self.mqtt_client.loop_start()
        except Exception as e:
            logger.info(e)

    def ConnectDB(self):
        host = self.lineEditHostDB.text()
        port = int(self.lineEditPortDB.text())
        logger.info("connecting to DB server: {0}:{1}".format(host, port))
        username = self.lineEditPortUserName_3.text()
        password = self.lineEditPortPassword_3.text() 
        try:
            self.clientDB = MongoClient('mongodb+srv://' + username + ':' + password + '@' + host + ':' + str(port))
            self.clientDB.server_info() # will throw an exception
            self.db = self.clientDB['MotorTests']
            logger.info("connected to DB server: {0}:{1}".format(host, port))
            self.DB_Connected = True
            if self.IOT_Connected:
                self.statusbar.showMessage("cliente IOT conectado - cliente DB conectado") 
            else:
                self.statusbar.showMessage("cliente IOT DESCONECTADO - cliente DB conectado")
        except:
            e = sys.exc_info()[0]
            logger.info("Exception connecting to server: {0}".format(e))
            self.DB_Connected = False
            if self.IOT_Connected:
                self.statusbar.showMessage("cliente IOT conectado - cliente DB DESCONECTADO") 
            else:
                self.statusbar.showMessage("cliente IOT DESCONECTADO - cliente DB DESCONECTADO")

    def on_(self):
        self.close


APP_STYLE_SHEET = """
QPushButton {
    background-color: rgb(200,200,200);
    border-style: outset;
    border-width: 1px;
    border-radius: 5px;
    border-color: beige;
    font: bold 14px;
    min-width: 5em;
    padding: 5px;
}
QPushButton:pressed {
    background-color: rgb(0, 100, 200);
    border-style: inset;
}

QPushButton#pushButtonConnectIOT {
    background-color: rgb(255, 255, 255);
}
QPushButton#pushButtonConnectIOT:pressed {
    background-color: rgb(0, 255, 255);
}
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet("QLineEdit{border:1px solid rgb(255, 180, 180); background:rgb(100,100,250);}")
    app.setStyleSheet(APP_STYLE_SHEET)

    mw = MainWindow()
    mw.show()
    app.exec()
