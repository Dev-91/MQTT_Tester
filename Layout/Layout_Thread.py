from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore  # QtCore를 명시적으로 보여주기 위해
import time


class LayoutThread(QThread):
    # Thread custom event
    threadEvent = QtCore.pyqtSignal()
 
    def __init__(self, parent=None, loop=True, delay_time=0):
        super().__init__()
        
        # self.n = 0
        self.loop = loop
        self.main = parent
        self.isRun = False
        self.delay_time = delay_time
 
    def run(self):
        time.sleep(self.delay_time)
        if self.loop:
            while self.isRun:
                # print('쓰레드 : ' + str(self.n))
    
                # 'threadEvent' 이벤트 발생
                # 파라미터 전달 가능(객체도 가능)
                self.threadEvent.emit()
    
                # self.n += 1
        else:
            self.threadEvent.emit()
            # self.threadEvent.emit(self.n)