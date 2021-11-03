from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import Layout.Layout_Thread as Layout_Thread
import Util.MQTT_Util as MQTT_Util
import Layout.Tool_Window as tool_w


form_class = uic.loadUiType("Layout/main_layout.ui")[0]
dialog_class = uic.loadUiType("Layout/tool_dialog.ui")[0]


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

        self.sub_topic_msg_diclist = list()

        self.connection_flag_label.setText("Disconnected")
        self.tool_btn.setEnabled(True)
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.publish_btn.setEnabled(False)
        self.subscribe_btn.setEnabled(False)

        # UI Thread
        self.connect_th = Layout_Thread.LayoutThread(self, False)
        self.disconnect_th = Layout_Thread.LayoutThread(self, False)
        self.publish_th = Layout_Thread.LayoutThread(self, False)
        self.subscribe_th = Layout_Thread.LayoutThread(self, False)
        self.mqtt_icon_th = Layout_Thread.LayoutThread(self, False)
        self.mqtt_sub_th = Layout_Thread.LayoutThread(self, False)
        self.subscribe_list_th = Layout_Thread.LayoutThread(self, False)
        self.sub_topic_list_th = Layout_Thread.LayoutThread(self, False)

        # 쓰레드 이벤트 연결
        self.connect_th.threadEvent.connect(self.connect_th_handler)
        self.disconnect_th.threadEvent.connect(self.disconnect_th_handler)
        self.publish_th.threadEvent.connect(self.publish_th_handler)
        self.subscribe_th.threadEvent.connect(self.subscribe_th_handler)
        self.mqtt_icon_th.threadEvent.connect(self.mqtt_icon_th_handler)
        self.mqtt_sub_th.threadEvent.connect(self.mqtt_sub_th_handler)
        self.subscribe_list_th.threadEvent.connect(self.subscribe_list_th_handler)
        self.sub_topic_list_th.threadEvent.connect(self.sub_topic_list_th_handler)

        self.subscribe_list.itemDoubleClicked.connect(self.subscribe_list_func)
        self.sub_topic_list.itemClicked.connect(self.sub_topic_list_func)

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
        self.sub_topic_num = self.sub_topic_list.currentRow()
        self.sub_topic_list_th.start()

    def mqtt_sub_msg(self, topic, msg):
        print("topic : " + topic + "    msg : " + msg)
        topic_msg_dic = { "topic" : topic, "msg" : msg }
        self.sub_topic_msg_diclist.append(topic_msg_dic)
        self.mqtt_sub_th.start()

    def list_ui_func(self):
        tool_dialog = tool_w.DialogWindow()
        tool_dialog.exec()

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
            self.mqtt_process.publish_func(self.publish_topic_line.text(),
                                           self.publish_textedit.toPlainText())

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
            
            self.sub_topic_msg_diclist.clear()

            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            self.tool_btn.setEnabled(True)
            self.publish_btn.setEnabled(False)
            self.subscribe_btn.setEnabled(False)
            self.connection_flag_label.setText("Disconnected")

    @pyqtSlot()
    def mqtt_sub_th_handler(self):
        self.sub_topic_list.addItem(self.sub_topic_msg_diclist[-1]["topic"])
        self.sub_msg_textedit.clear()
        self.sub_msg_textedit.append(self.sub_topic_msg_diclist[-1]["msg"])

    def subscribe_list_th_handler(self):
        self.publish_topic_line.setText(self.subscribe_list_th_text)

    def sub_topic_list_th_handler(self):
        self.sub_msg_textedit.clear()
        self.sub_msg_textedit.append(self.sub_topic_msg_diclist[self.sub_topic_num]["msg"])
