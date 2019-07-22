import sys
import socket
import logging
from ctypes import *
import xml.etree.ElementTree as ET
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel,QDialogButtonBox, QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout,QGridLayout ,QApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtCore import QThread

""" This class defines a C-like struct """

class Payload(Structure):
    _fields_ = [("id", c_uint32),
                ("counter", c_uint32),
                ("opcode", c_uint32)]


class MyThread(QThread):
    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent=parent)


    def run(self):
        time.sleep(3)


def logger():  # new logging object
    global logger
    logging.basicConfig(filename='Server_Record2.log', level=logging.INFO)
    logger = logging.getLogger()

def create_socket():
    tree = ET.parse('config.xml')
    root = tree.getroot()

    try:
        global logger
        global host
        global port
        global s
        host = root[0].text  # local network ip
        port = int(root[1].text)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logger.info("New socket has been created")
        print('Starting up on {} port {}'.format(host,port))
        return s

    except socket.error as error:  # If something goes wrong with creating new socket
        logger.error("socket creation error" + error)


def bind_socket():

    try:
        global host
        global port
        s.bind((host, port))  # binding host & port
        logger.info("binding the port : " + str(port))
        print("binding the port : " + str(port))
        s.listen(5)  # queue of five client allowed

    except socket.error as error:  # If something goes wrong with binding
        logger.error("socket binding error : " + error)



def export(opcode):
    text = "Opcode : " + str(opcode) + " "
    with open('opcode.bin', 'a+b') as file:
             file.write(text.encode('ascii'))


def recv():
    print("start recv")
    app = QApplication(sys.argv)
    global income
    global table2
    print("open new app")
    ex = App()

    msg = Payload(0, 0, 0)

    while (True):

        print('waiting for a connection..')
        conn, addr = s.accept()
        print("connection has been established | " + repr(addr))
        logger.info("connection has been established | " + repr(addr))

        while conn:
            myThread = MyThread()

            buff = conn.recv(sizeof(msg))

            print("recv %d bytes" % sizeof(msg))
            payload_in = Payload.from_buffer_copy(buff)

            print(f"Received id={payload_in.id}, counter={payload_in.counter}, opcode={payload_in.opcode}")

            payload_out = payload_in

            opcode = payload_in.opcode

            if opcode == 1:
                export(opcode)
            elif opcode == 2:
                payload_out.counter += 1
            else:
                logger.info("Unexpected opcode %d" % opcode)

            nsent = conn.send(payload_out)
            print("send %d bytes" % nsent)
            print("send id=%d, counter=%d, opcode=%d" % (payload_out.id,
                                                         payload_out.counter,
                                                         payload_out.opcode))
            print("start insert")
            insertValues(table1, payload_in)
            insertValues(table2, payload_out)
            print("show")

            ex.show()
            print("end show")
            app.exec_()
            print("loop end")


    print("Closing connection to client")
    print("----------------------------")

    sys.exit()


def insertValues(table, payload):
    table.setItem(0, 1, QTableWidgetItem(str(payload.id)))
    table.setItem(1, 1, QTableWidgetItem(str(payload.counter)))
    table.setItem(2, 1, QTableWidgetItem(str(payload.opcode)))

class App(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=parent)
        global table1
        global table2
        QTableWidget.setMinimumSize(self, 1000, 500)
        QTableWidget.setWindowTitle(self, "Server Massages")
        self.table1 = QTableWidget()
        self.configureTable(self.table1)

        label = QLabel('Income', self)
        label.move(235, 0)

        self.table2 = QTableWidget()
        self.configureTable(self.table2)

        label = QLabel('Outcome', self)
        label.move(725, 0)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout = QVBoxLayout(self)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.table1)
        self.horizontalLayout.addWidget(self.table2)
        self.horizontalLayout.setContentsMargins(0, 20, 0, 0)
        table1= self.table1
        table2 = self.table2
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.close)
        self.buttonBox.rejected.connect(self.close)

    def configureTable(self, table):
        rowf = 3
        table.setColumnCount(2)
        table.setRowCount(rowf)
        table.setHorizontalHeaderItem(0, QTableWidgetItem("Parameters"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("Values"))

        table.setItem(0, 0, QTableWidgetItem("id"))
        table.setItem(1, 0, QTableWidgetItem("counter"))
        table.setItem(2, 0, QTableWidgetItem("opcode"))

        table.horizontalHeader().setStretchLastSection(True)




def main():
    logger()
    create_socket()
    bind_socket()
    recv()

if __name__ == '__main__':
    main()

