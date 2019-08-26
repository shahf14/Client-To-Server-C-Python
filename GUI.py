from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout , QTableWidgetItem
import sys
import message
import copy
from app_logic import *
from icd import *

class GUI(QDialog):

    signal_update = QtCore.pyqtSignal(message)


    def __init__(self):

        super(GUI, self).__init__()
        self._translate = QtCore.QCoreApplication.translate
        self.resize(1050, 580)
        self.icd = icd()

        self.headers = self.icd.get_number_of_headers()

        self.income_rows = 10
        self.outcome_rows = 6

        self.current_income_row = 0
        self.current_outcome_row = 0

        # message containers
        self.income_msg = message()
        self.outcome_msg = message()

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

        # read income columns name from icd file
        self.column_incomeMSG = self.icd.read_income_messages()
        self.columns_names = self.icd.read_headers()
        self.column_incomeMSG.extend(self.columns_names)
        self.column_incomeMSG = list(reversed((self.column_incomeMSG)))

        # read outcome columns name from icd file
        self.column_outcomeMSG = self.icd.read_outcome_messages()
        self.columns_names = self.icd.read_headers()
        self.column_outcomeMSG.extend(self.columns_names)
        self.column_outcomeMSG = list(reversed((self.column_outcomeMSG)))


        # Set rows and headers

        self.income_table.setRowCount(self.income_rows)
        self.income_table.setColumnCount(len(self.column_incomeMSG))

        # create new income headers
        column_incomeMSG = self.icd.read_income_messages()

        self.columns_names = self.icd.read_headers()
        column_incomeMSG.extend(self.columns_names)
        print(column_incomeMSG)
        column_outcomeMSG = self.icd.read_outcome_messages()

        for i in range(len(self.column_incomeMSG)):
            self.income_table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())

        # Column headers
        self.GroupBox_income.setWindowTitle("Income Messages")

        # set headers names from ICD file
        for name,index in zip(self.column_incomeMSG, range(len(self.column_incomeMSG))):
                self.income_table.horizontalHeaderItem(index).setText(name)


        QtCore.QMetaObject.connectSlotsByName(self.GroupBox_income)

        self.outcome_table.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.SizeVerCursor))

        # Set rows and headers
        self.outcome_table.setRowCount(self.outcome_rows)
        self.outcome_table.setColumnCount(len(self.column_outcomeMSG))

        # New headers
        for i in range(len(self.column_outcomeMSG)):
            self.outcome_table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())

        # Column headers
        for name, index in zip(self.column_outcomeMSG, range(len(self.column_outcomeMSG))):
            self.outcome_table.horizontalHeaderItem(index).setText(name)

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

    def update_income_table(self,msg):
        self.income_msg = msg
        self.outcome_msg = terms(copy.copy(msg))
        print(self.outcome_msg.opcode)

        self.income_table.setItem(self.current_income_row,0, QTableWidgetItem(str(self.income_msg.id)))
        self.income_table.setItem(self.current_income_row,1, QTableWidgetItem(str(self.income_msg.counter)))
        self.income_table.setItem(self.current_income_row,2, QTableWidgetItem(str(self.income_msg.opcode)))

        self.current_income_row = ( self.current_income_row + 1 ) % self.income_rows

        self.outcome_table.setItem(self.current_outcome_row, 0, QTableWidgetItem(str(self.outcome_msg.id)))
        self.outcome_table.setItem(self.current_outcome_row, 1, QTableWidgetItem(str(self.outcome_msg.counter)))
        self.outcome_table.setItem(self.current_outcome_row, 2, QTableWidgetItem(str(self.outcome_msg.opcode)))

        self.current_outcome_row = (self.current_outcome_row + 1) % self.outcome_rows


    def update_outcome_table(self, message):
        self.tableWidget.setItem(0, self.current_outcome_row, QTableWidgetItem(message))
        self.tableWidget.setItem(1, self.current_outcome_row, QTableWidgetItem(message))
        self.tableWidget.setItem(2, self.current_outcome_row, QTableWidgetItem(message))

        self.current_outcome_row = (self.current_outcome_row + 1) % self.income_rows

    def closeEvent(self, event):
        self.close_all()

    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = GUI()
    ui.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")