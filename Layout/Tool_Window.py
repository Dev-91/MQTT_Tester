from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import configparser


from PyQt5.uic.properties import QtGui


dialog_class = uic.loadUiType("Layout/tool_dialog.ui")[0]


class DialogWindow(QDialog, dialog_class):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)

        self.config = configparser.ConfigParser()
        self.config.read('./Config/config.ini')

        self.ip = ""
        self.port = ""
        self.username = ""
        self.password = ""
        self.client_id = ""
        
        try:
            self.ip = self.config.get('MQTT', 'ip')
            self.port = self.config.get('MQTT', 'port')
            self.username = self.config.get('MQTT', 'username')
            self.password = self.config.get('MQTT', 'password')
            self.client_id = self.config.get('MQTT', 'client_id')
        except:
            pass
            
        self.broker_ip_line.setText(self.ip)
        self.broker_port_line.setText(self.port)
        self.username_line.setText(self.username)
        self.password_line.setText(self.password)
        self.client_id_line.setText(self.client_id)

        # Data load & setText

        self.dialog_ok_btn.clicked.connect(self.ok_btn_func)
        self.dialog_cancel_btn.clicked.connect(self.cancel_btn_func)

    def ok_btn_func(self):
        self.ip = self.broker_ip_line.text()
        self.port = self.broker_port_line.text()
        self.username = self.username_line.text()
        self.password = self.password_line.text()
        self.client_id = self.client_id_line.text()
        
        self.config.set('MQTT', 'ip', self.ip)
        self.config.set('MQTT', 'port', self.port)
        self.config.set('MQTT', 'username', self.username)
        self.config.set('MQTT', 'password', self.password)
        self.config.set('MQTT', 'client_id', self.client_id)

        with open('Config/config.ini', 'w') as f:
            self.config.write(f)
            self.ip = self.config.get('MQTT', 'ip')
            self.port = int(self.config.get('MQTT', 'port'))
            self.username = self.config.get('MQTT', 'username')
            self.password = self.config.get('MQTT', 'password')
            self.client_id = self.config.get('MQTT', 'client_id')
        
        self.close()
        
    def cancel_btn_func(self):
        self.close()