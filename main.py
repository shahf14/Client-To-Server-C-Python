from PyQt5 import QtWidgets
import server_logic
import socket
import message
import sys

class MainWindow(server_logic.Server_Logic):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.client_socket_list = list()
        self.connect = False
        self.click_get_ip()

    def connect(self,):
        super(MainWindow, self).connect()
        self.pushButton_connect.clicked.connect(self.click_connect)
        self.pushButton_disconnect.clicked.connect(self.click_disconnect)
        self.pushButton_get_ip.clicked.connect(self.click_get_ip)
        self.pushButton_exit.clicked.connect(self.close)

    def click_connect(self):
        self.udp_server_start()
        self.connect = True
        self.pushButton_disconnect.setEnabled(True)
        self.pushButton_connect.setEnabled(False)

    def click_disconnect(self):
        # Close the connection
        self.close_all()
        self.connect = False
        self.pushButton_disconnect.setEnabled(False)
        self.pushButton_connect.setEnabled(True)

    def click_get_ip(self):

        self.lineEdit_ip_local.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # this method get the IP of the local machine
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
            self.lineEdit_ip_local.setText(str(local_ip))

        except Exception as ret:
            # If you cannot connect to the Internet, the following method will be called.
            try:
                local_ip = socket.gethostbyname(socket.gethostname())
                self.lineEdit_ip_local.setText(str(local_ip))
            except Exception as ret_e:
                self.signal_update.emit("Unable to get ip, please connect to the network！\n")
        finally:
            s.close()

    def send(self):

        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 1:
            self.udp_send()

    def close_all(self):
        self.udp_close()
        self.reset()

    def reset(self):
        self.connect = False
        self.pushButton_disconnect.setEnabled(False)
        self.pushButton_connect.setEnabled(True)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())