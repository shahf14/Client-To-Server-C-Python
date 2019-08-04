# Project classes
from Message import *

# Utilities
import sys
import random
import time

# GUI Libraries
from PyQt5 import QtCore
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QLabel,QDialogButtonBox, QApplication, QPushButton, QHBoxLayout,\
                            QDialog,QTableWidget,QTableWidgetItem,QVBoxLayout


class Thread(QThread):

    newMessage = pyqtSignal(Message)
    counter = 0

    # create random message
    # ID will always be 1
    # OPcode between 1-3
    # Counter increase by 1 for each

    def create_random_messages(self):

        self.counter += + 1
        message = Message()
        message.id = 1
        message.opcode = random.randint(1,3)
        message.counter = self.counter

        return message

    def run(self):

        while(True):
            message = self.create_random_messages()
            self.newMessage.emit(message)
            time.sleep(1)

class Window(QDialog):

    def __init__(self, parent=None):
        super().__init__()

        self.title = "Simulateur"
        self.height = 1000
        self.weight = 600
        self.top = 50
        self.left = 200

        self.initApp()

    def initApp(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.height,self.weight)
        self.create_tables()

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.income_table)
        self.horizontalLayout.addWidget(self.outcome_table)
        self.horizontalLayout.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.buttonBox)


        self.income_thread = Thread()
        self.outcome_thread = Thread()


        self.buttonBox.accepted.connect(self.updeteValues)
        self.buttonBox.rejected.connect(self.close)

    def updeteValues(self):
        self.income_thread.newMessage.connect(self.insert_income)
        self.outcome_thread.newMessage.connect(self.insert_outcome)

        self.income_thread.start()
        self.outcome_thread.start()


    def insert_income(self,message):
        self.income_table.setItem(0, 1, QTableWidgetItem(str(message.id)))
        self.income_table.setItem(1, 1, QTableWidgetItem(str(message.counter)))
        self.income_table.setItem(2, 1, QTableWidgetItem(str(message.opcode)))

    def insert_outcome(self,message):
        self.outcome_table.setItem(0, 1, QTableWidgetItem(str(message.id)))
        self.outcome_table.setItem(1, 1, QTableWidgetItem(str(message.counter)))
        self.outcome_table.setItem(2, 1, QTableWidgetItem(str(message.opcode)))

    def create_tables(self):

        # table for all the messages that resive from the client
        label = QLabel('Income', self)
        label.move(225, 0)
        self.income_table = QTableWidget()
        self.initTable(self.income_table)

        # table for all the messages that we send back
        label = QLabel('Outcome', self)
        label.move(725, 0)
        self.outcome_table = QTableWidget()
        self.initTable(self.outcome_table)

    def initTable(self, table,columns=2,rows=3):
        table.setColumnCount(columns)
        table.setRowCount(rows)
        table.setHorizontalHeaderItem(0, QTableWidgetItem("Parameters"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("Values"))

        table.setItem(0, 0, QTableWidgetItem("id"))
        table.setItem(1, 0, QTableWidgetItem("counter"))
        table.setItem(2, 0, QTableWidgetItem("opcode"))

        table.horizontalHeader().setStretchLastSection(True)



