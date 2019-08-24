from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout , QTableWidgetItem
import sys
import xml.etree.ElementTree as ET
from message import *


class GUI(QDialog):

    signal_update = QtCore.pyqtSignal(message)

    def __init__(self):

        super(GUI, self).__init__()
        self._translate = QtCore.QCoreApplication.translate
        self.resize(1050, 580)

        self.icd = ET.parse('ICD.xml')
        self.root = self.icd.getroot()

        # we create number of columns by the number of xml Header element without income-outcome element.

        self.columns = len(self.root[0]) - 1

        self.income_rows = 10
        self.outcome_rows = 6

        self.current_income_row = 0
        self.current_outcome_row = 0

        # Buttons
        self.pushButton_get_ip = QtWidgets.QPushButton()
        self.pushButton_connect = QtWidgets.QPushButton()
        self.pushButton_disconnect = QtWidgets.QPushButton()
        self.pushButton_exit = QtWidgets.QPushButton()
        self.pushButton_config = QtWidgets.QPushButton()

        # Buttons side text
        self.label_port = QtWidgets.QLabel()
        self.label_ip = QtWidgets.QLabel()

        # Tables headlines
        self.label_income = QtWidgets.QLabel()
        self.label_outcome = QtWidgets.QLabel()

        # Input lines
        self.lineEdit_port = QtWidgets.QLineEdit()
        self.lineEdit_ip_local = QtWidgets.QLineEdit()
        self.textEdit_send = QtWidgets.QTextEdit()

        # Defining layout
        self.h_box_1 = QHBoxLayout()
        self.h_box_2 = QHBoxLayout()
        self.h_box_3 = QHBoxLayout()

        self.h_box_recv = QHBoxLayout()
        self.h_box_all = QHBoxLayout()
        self.h_box_exit = QHBoxLayout()

        self.v_box_set = QVBoxLayout()
        self.v_box_send = QVBoxLayout()
        self.v_box_right = QVBoxLayout()
        self.v_box_left = QVBoxLayout()
        self.v_box_exit = QVBoxLayout()

        self.GroupBox_income = QtWidgets.QGroupBox()
        self.GroupBox_outcome = QtWidgets.QGroupBox()

        self.income_table = QtWidgets.QTableWidget(self.GroupBox_income)
        self.outcome_table = QtWidgets.QTableWidget(self.GroupBox_outcome)

        # Set headline font
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)

        self.label_income.setFont(font)
        self.label_outcome.setFont(font)

        self.pushButton_disconnect.setEnabled(False)

        # Calling layout methods and methods for displaying text on controls
        self.layout_ui()
        self.set_names()
        self.connect()

    def layout_ui(self):

        # IP box
        self.h_box_1.addWidget(self.label_ip)
        self.h_box_1.addWidget(self.lineEdit_ip_local)
        self.h_box_1.addWidget(self.pushButton_get_ip)

        # Port Box
        self.h_box_2.addWidget(self.label_port)
        self.h_box_2.addWidget(self.lineEdit_port)
        self.h_box_2.addWidget(self.pushButton_config)

        # Connection Box
        self.h_box_3.addWidget(self.pushButton_connect)
        self.h_box_3.addWidget(self.pushButton_disconnect)


        # IP
        self.v_box_set.addLayout(self.h_box_1)

        # port
        self.v_box_set.addLayout(self.h_box_2)

        # connect/disconnect
        self.v_box_set.addLayout(self.h_box_3)

        self.v_box_send.addWidget(self.label_outcome)
        self.v_box_send.addWidget(self.outcome_table)
        self.v_box_exit.addWidget(self.pushButton_exit)
        self.h_box_exit.addLayout(self.v_box_exit)
        self.v_box_left.addLayout(self.v_box_set)
        self.v_box_left.addLayout(self.v_box_send)
        self.v_box_left.addLayout(self.h_box_exit)

        # Set rows and columns
        self.income_table.setRowCount(self.income_rows)
        self.income_table.setColumnCount(self.columns)


        # New columns
        for i in range(self.columns):
            self.income_table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())


        # Column headers
        self.GroupBox_income.setWindowTitle("Income Messages")


    # read columns names from ICD file
        for header in self.icd.iter('header'):
            j = 0
            for element in header:
                column_name = element.get('name')
                if(column_name != "income-outcome"):
                     self.income_table.horizontalHeaderItem(j).setText(column_name)
                     j += 1
        QtCore.QMetaObject.connectSlotsByName(self.GroupBox_income)

        self.outcome_table.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.SizeVerCursor))

        # Set rows and columns
        self.outcome_table.setRowCount(self.outcome_rows)
        self.outcome_table.setColumnCount(self.columns)

        # New columns
        for i in range(self.columns):
            self.outcome_table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())


        # Column headers
        self.GroupBox_outcome.setWindowTitle("Outcome Messages")

        for header in self.icd.iter('header'):
            j = 0
            for element in header:
                column_name = element.get('name')
                if (column_name != "income-outcome"):
                    self.outcome_table.horizontalHeaderItem(j).setText(column_name)
                    j += 1

        QtCore.QMetaObject.connectSlotsByName(self.GroupBox_outcome)

        # Add on the right side of the layout
        self.h_box_recv.addWidget(self.label_income)
        self.v_box_right.addLayout(self.h_box_recv)

        # Income messages table
        self.v_box_right.addWidget(self.income_table)

        # Add left and right layouts to the form layout
        self.h_box_all.addLayout(self.v_box_left)
        self.h_box_all.addLayout(self.v_box_right)

        # Set the form layout to the form
        self.setLayout(self.h_box_all)

    def set_names(self):

        self.pushButton_connect.setText("Connect")
        self.pushButton_disconnect.setText("Disconnect")
        self.pushButton_get_ip.setText("Get IP")
        self.pushButton_exit.setText("Exit program")
        self.pushButton_config.setText("Configuration file")
        self.label_ip.setText("IP:")
        self.label_port.setText("Port number:")
        self.label_income.setText("Income messages")
        self.label_outcome.setText("Outcome messages")

    def connect(self):
        self.signal_update.connect(self.update_income_table)


    def update_income_table(self, msg):
        self.income_table.setItem(self.current_income_row,0, QTableWidgetItem(msg))
        self.income_table.setItem(self.current_income_row,1, QTableWidgetItem(msg))
        self.income_table.setItem(self.current_income_row,2, QTableWidgetItem(msg))

        self.current_income_row = ( self.current_income_row + 1 ) % self.income_rows

        self.outcome_table.setItem(self.current_outcome_row, 0, QTableWidgetItem(msg))
        self.outcome_table.setItem(self.current_outcome_row, 1, QTableWidgetItem(msg))
        self.outcome_table.setItem(self.current_outcome_row, 2, QTableWidgetItem(msg))

        self.current_outcome_row = (self.current_outcome_row + 1) % self.outcome_rows



    def update_outcome_table(self, message):
        self.tableWidget.setItem(0, self.current_outcome_row, QTableWidgetItem(message))
        self.tableWidget.setItem(1, self.current_outcome_row, QTableWidgetItem(message))
        self.tableWidget.setItem(2, self.current_outcome_row, QTableWidgetItem(message))

        self.current_outcome_row = (self.current_outcome_row + 1) % self.income_rows

    def closeEvent(self, event):
        self.close_all()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())