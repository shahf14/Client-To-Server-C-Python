from PyQt5 import QtWidgets
import GUI
from message import *

import logging
import stopThreading
import socket
import threading
import sys
import xml.etree.ElementTree as ET

class Server_Logic(GUI.GUI):
    def __init__(self):
        super(Server_Logic, self).__init__()

        logging.basicConfig(filename='Server_Record2.log', level=logging.INFO)
        self.logger = logging.getLogger()

        self.UDP_socket = None
        self.address = None
        self.sever_thread = None

    def udp_server_start(self):
        self.UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # load configuration file from XML
            tree = ET.parse('config.xml')
            root = tree.getroot()

            # define IP and Port from configuration file
            host = root[0].text
            port = int(root[1].text)
            address = (host, port)

            self.UDP_socket.bind(address)

            self.logger.info("New socket has been created")
            print('Starting up on {} port {}'.format(host, port))

        # if something goes wrong
        except Exception as ret:
            print(ret)
            msg = 'Please check the port number'
            self.signal_update.emit(msg)

        else:
            self.sever_thread = threading.Thread(target=self.udp_server_concurrency)
            self.sever_thread.start()
            print('UDP server is listening on the port:{}\n'.format(port))

    def udp_server_concurrency(self):
        print("udp_server_concurrency ")
        while True:
            print(threading.get_ident())
            buff, address = self.UDP_socket.recvfrom(1024)
            income_message = message.from_buffer_copy(buff)

            print(f"Received id={income_message.id}, counter={income_message.counter}, "
                  f"opcode={income_message.opcode}")

            if buff:
                sent = self.UDP_socket.sendto(income_message,address)

            self.signal_update.emit(income_message)


    def udp_close(self):
        try:
            if self.link is True:
                msg = 'Disconnected from the network\n'
                self.signal_update.emit(msg)
        except Exception as ret:
            pass
        try:
            stopThreading.stop_thread(self.sever_thread)
        except Exception:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Server_Logic()
    ui.show()
    sys.exit(app.exec_())
