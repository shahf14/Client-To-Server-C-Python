import socket
import logging
from ctypes import *
import xml.etree.ElementTree as ET

class payload_t(Structure):
    _fields_ = [("Opcode", c_uint),  # the operation code of the message, type : int
                ("count", c_uint),   # the counter of the message, type : int
                ("text", c_char_p)]  # the body of the message, type : string


def logger():  # new logging object
    global logger
    logging.basicConfig(filename='Server_Record.log', level=logging.INFO)
    logger = logging.getLogger()


def create_socket():
    tree = ET.parse('config.xml')
    root = tree.getroot()

    try:
        # global logger
        global host
        global port
        global s
        host = root[0].text  # local network ip
        port = int(root[1].text)
        s = socket.socket()
        logger.info("New socket has been created")

    except socket.error as error:  # If something goes wrong with creating new socket
        logger.error("socket creation error" + error)


def bind_socket():
    try:
        global host
        global port
        s.bind((host, port))  # binding host & port
        logger.info("binding the port : " + str(port))
        s.listen(5)  # queue of five client allowed

    except socket.error as error:  # If something goes wrong with binding
        logger.error("socket binding error : " + error)


def socket_accept():
    conn, addr = s.accept()
    logger.info("connection has been established | IP " + addr[0] + " Port :" + addr[1])
    send_socket(conn)
    conn.close()


def send_socket(conn):
    while True:
        data = conn.recv(1024)
        id = data.Opcode

        if id == 1:  # if Opcode is 1 then record the massage.
             export(data)

        if id == 2:  # if Opcode is 2 then Increase the counter in 1.
            data.counter += 1

        if id == 3:  # if Opcode is 3 do nothing.
            continue

        client_respond = str(data.text, 'utf-8')  # this is the message that sent by client
        print(client_respond, end="")
        if not data:
            break

        conn.sendall(data)

        logging.info("Connection has been closed ")


def export(data):
    with open('RecordMassage.bin', 'a+b') as file:
        file.write((data.opcode+" "+data.counter+" "+data.text).encode())


def main():
    logger()
    create_socket()
    bind_socket()
    socket_accept()


main()
