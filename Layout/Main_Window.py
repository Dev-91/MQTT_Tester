from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import json

import Layout.Layout_Thread as Layout_Thread
import Util.MQTT_Util as MQTT_Util
import Layout.Tool_Window as tool_w


form_class = uic.loadUiType("Layout/main_layout.ui")[0]


def close_func():
    return QCoreApplication.instance().quit()
    
def close_msg_box():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Message")
    msg.setText("프로그램을 종료하시겠습니까?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    reply = msg.exec_()
    if reply == QMessageBox.Yes:
        close_func()
    else:
        pass

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tool_btn.clicked.connect(self.tool_btn_func)
        self.connect_btn.clicked.connect(self.connect_btn_func)
        self.disconnect_btn.clicked.connect(self.disconnect_btn_func)
        self.publish_btn.clicked.connect(self.publish_btn_func)
        self.subscribe_btn.clicked.connect(self.subscribe_btn_func)

        # self.circle_img = QPixmap("Layout/circle.png").scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
        
        # self.circle_img_label.setPixmap(self.circle_img)
        # self.circle_img_label.setScaledContents(True)

        self.connection_flag = False

        self.sub_topic_msg_list = list()

        self.connection_flag_label.setText("Disconnected")
        self.tool_btn.setEnabled(True)
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.publish_btn.setEnabled(False)
        self.subscribe_btn.setEnabled(False)

        self.radio_btn_check = self.text_type_radio_btn.isChecked()

        # UI Thread
        self.connect_th = Layout_Thread.LayoutThread(self, False)
        self.disconnect_th = Layout_Thread.LayoutThread(self, False)
        self.publish_th = Layout_Thread.LayoutThread(self, False)
        self.subscribe_th = Layout_Thread.LayoutThread(self, False)
        self.mqtt_icon_th = Layout_Thread.LayoutThread(self, False)
        self.mqtt_sub_th = Layout_Thread.LayoutThread(self, False)
        self.subscribe_list_th = Layout_Thread.LayoutThread(self, False)
        self.sub_topic_list_th = Layout_Thread.LayoutThread(self, False)
        self.sub_type_th = Layout_Thread.LayoutThread(self, False)

        # 쓰레드 이벤트 연결
        self.connect_th.threadEvent.connect(self.connect_th_handler)
        self.disconnect_th.threadEvent.connect(self.disconnect_th_handler)
        self.publish_th.threadEvent.connect(self.publish_th_handler)
        self.subscribe_th.threadEvent.connect(self.subscribe_th_handler)
        self.mqtt_icon_th.threadEvent.connect(self.mqtt_icon_th_handler)
        self.mqtt_sub_th.threadEvent.connect(self.mqtt_sub_th_handler)
        self.subscribe_list_th.threadEvent.connect(self.subscribe_list_th_handler)
        self.sub_topic_list_th.threadEvent.connect(self.sub_topic_list_th_handler)
        self.sub_type_th.threadEvent.connect(self.sub_type_th_handler)

        self.subscribe_list.itemDoubleClicked.connect(self.subscribe_list_func)
        self.sub_topic_list.itemClicked.connect(self.sub_topic_list_func)
        self.text_type_radio_btn.clicked.connect(self.sub_type_func)
        self.hex_type_radio_btn.clicked.connect(self.sub_type_func)

    def tool_btn_func(self):
        tool_dialog = tool_w.DialogWindow()
        tool_dialog.exec()

    def connect_btn_func(self):
        self.connect_th.start()

    def disconnect_btn_func(self):
        self.disconnect_th.start()
    
    def publish_btn_func(self):
        self.publish_th.start()

    def subscribe_btn_func(self):
        self.subscribe_th.start()

    def mqtt_connection_flag(self, flag):
        self.connection_flag = flag
        self.mqtt_icon_th.start()

    def mqtt_connection_rc(self, rc):
        self.rc = rc

    def subscribe_list_func(self):
        self.subscribe_list_th_text = self.subscribe_list.currentItem().text()
        self.subscribe_list_th.start()

    def sub_topic_list_func(self):
        self.sub_topic_list_th.start()

    def sub_type_func(self):
        self.sub_type_th.start()

    def mqtt_sub_msg(self, msg):
        print("topic : " + str(msg.topic) + "    payload : " + str(msg.payload))
        self.sub_topic_msg_list.append(msg)
        self.mqtt_sub_th.start()

    def list_ui_func(self):
        tool_dialog = tool_w.DialogWindow()
        tool_dialog.exec()

    def is_json(self, obj):
        try:
            json_object = json.loads(obj)
            # { } 가 포함된 string이 invalid json 인 경우 Exception
            iterator = iter(json_object)
            # { } 가 없는 경우는 string의 경우 Exception
        except Exception as e:
            return False
        return True
    
    def is_hex_string(self, obj):
        try:
            # EX) [FF FE 04 67 33] 
            if obj[0] == "[" and obj[-1] == "]":
                return True
            else:
                return False
        except Exception as e:
            return False
        return True

    def payload_func(self, num):
        self.radio_btn_check = self.text_type_radio_btn.isChecked()
        if len(self.sub_topic_msg_list) > 0:
            self.sub_msg_textedit.clear()
            if self.radio_btn_check == True:
                try:
                    json_payload = json.dumps(json.loads(self.sub_topic_msg_list[num].payload), indent=2)
                    self.sub_msg_textedit.append(str(json_payload))
                except:
                    self.sub_msg_textedit.append(str(self.sub_topic_msg_list[num].payload).replace('b', '').replace('\'', ''))
                    
                self.length_num_label.setText(str(len(self.sub_topic_msg_list[num].payload)))
            else:
                byte_obj = bytes(self.sub_topic_msg_list[num].payload)
                text_byte_obj = ""
                for bo in byte_obj:
                    text_byte_obj += format(bo, '02X') + " "
                self.sub_msg_textedit.append(text_byte_obj)
                self.length_num_label.setText(str(len(byte_obj)))

    def closeEvent(self, event):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Message")
        msg.setText("프로그램을 종료하시겠습니까?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot()
    def connect_th_handler(self):
        self.mqtt_process = MQTT_Util.MQTT_Process(self)
        self.mqtt_process.connect_func()
        self.mqtt_process.start()

    @pyqtSlot()
    def disconnect_th_handler(self):
        self.mqtt_process.disconnect_func()

    @pyqtSlot()
    def publish_th_handler(self):
        if self.connection_flag:
            pub_topic = self.publish_topic_line.text()
            textbox_msg = self.publish_textedit.toPlainText()
            
            
            if self.is_json(textbox_msg):  # Json
                json_object = json.loads(textbox_msg)
                pub_payload = textbox_msg
            else:
                if self.is_hex_string(textbox_msg):  # Hex
                    hex_str_list = textbox_msg.split(" ")
                    # print(hex_str_list)
                    hex_bytearray = bytearray()
                    for hex_s in hex_str_list[1:-1]:
                        hex_bytearray.append(int(hex_s, 16))
                    pub_payload = hex_bytearray
                else:  # String
                    pub_payload = textbox_msg
                
            self.mqtt_process.publish_func(pub_topic, pub_payload)

    @pyqtSlot()
    def subscribe_th_handler(self):
        if self.connection_flag:
            sub_topic = self.subscribe_topic_line.text()
            self.mqtt_process.subscribe_func(sub_topic)
            self.subscribe_list.addItem(sub_topic)

    @pyqtSlot()
    def mqtt_icon_th_handler(self):
        if self.connection_flag:
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.tool_btn.setEnabled(False)
            self.publish_btn.setEnabled(True)
            self.subscribe_btn.setEnabled(True)
            self.connection_flag_label.setText("Connected")
        else:
            self.publish_topic_line.clear()
            self.subscribe_topic_line.clear()
            self.publish_textedit.clear()
            self.subscribe_list.clear()
            self.sub_topic_list.clear()
            self.sub_msg_textedit.clear()

            self.sub_topic_msg_list.clear()
            self.length_num_label.setText("0")

            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            self.tool_btn.setEnabled(True)
            self.publish_btn.setEnabled(False)
            self.subscribe_btn.setEnabled(False)
            self.connection_flag_label.setText("Disconnected")

    @pyqtSlot()
    def mqtt_sub_th_handler(self):
        self.sub_topic_list.addItem(self.sub_topic_msg_list[-1].topic)
        self.payload_func(-1)
    
    @pyqtSlot()
    def sub_type_th_handler(self):
        sub_topic_num = self.sub_topic_list.currentRow()
        self.payload_func(sub_topic_num)
    
    @pyqtSlot()
    def subscribe_list_th_handler(self):
        self.publish_topic_line.setText(self.subscribe_list_th_text)

    @pyqtSlot()
    def sub_topic_list_th_handler(self):
        sub_topic_num = self.sub_topic_list.currentRow()
        self.payload_func(sub_topic_num)