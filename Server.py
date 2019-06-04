import sys
import socket
import logging
from ctypes import *
import xml.etree.ElementTree as ET

""" This class defines a C-like struct """
class Payload(Structure):
    _fields_ = [("id", c_uint32),
                ("counter", c_uint32),
                ("opcode", c_uint32)]


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

def recv():
    msg = Payload(0, 0, 0)

    while(1):
        print('waiting for a connection..')
        conn, addr = s.accept()
        print("connection has been established | " + repr(addr))
        logger.info("connection has been established | " + repr(addr))
        while conn:
            buff = conn.recv(sizeof(msg))

            print("recv %d bytes" % sizeof(msg))
            payload_in = Payload.from_buffer_copy(buff)
            opcode = payload_in.opcode

            if opcode == 1 :
                export(opcode)

            elif  opcode == 2 :
                payload_in.counter = payload_in.counter + 1
            else:
                logger.info("Unexpected opcode %d"  %opcode)


            print("Received id=%d, counter=%d, opcode=%d" % (payload_in.id,
                                                           payload_in.counter,
                                                           payload_in.opcode))

            nsent = conn.send(payload_in)

    print("Closing connection to client")
    print("----------------------------")
    ssock.close()

def export(opcode):
    with open('opcode.bin', 'a+b') as file:
            file.write(opcode.encode())

def main():
    global s
    logger()
    create_socket()
    bind_socket()
    recv()

main()
