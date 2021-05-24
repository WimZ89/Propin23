'''
Created on May 23, 2021

@author: wimz
'''
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import sys
import socket
import queue
import threading
from PyQt5.QtSvg import QSvgRenderer
# from future.backports.test.ssl_servers import server

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65430        # Port to listen on (non-privileged ports are > 1023)



def drawserver():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True :
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print (data)
                if not data:
                    break
                try:
                    print(data.decode("utf-8"))
                except:
                    break;
                conn.sendall(data)
#             s.close()
        print('Disconnected', addr)

threading.Thread(target=drawserver, daemon = True).start()

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Drawing Tutorial"
        self.top= 150
        self.left= 150
        self.width = 500
        self.height = 500
        self.InitWindow()
        self.mysvg = QSvgRenderer("test.svg")

    def InitWindow(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def RxData(self,data): 
        
        pass
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.mysvg.render(painter)
        painter.setPen(QPen(Qt.green,  8, Qt.DashLine))
        painter.drawEllipse(40, 40, 400, 400)
        painter.setPen(QPen(Qt.red,  8, Qt.SolidLine))
        painter.drawEllipse(50, 50, 100, 100)
        
        
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())