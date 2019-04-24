import socket
import logging
from ctypes import *

class payload_t(Structure):
    _fields_ = [("s_number", c_uint), #the header of the message type : int 
                ("text", c_char_p)] # the body of the message type : string

def logger(): # new logging object 
    global logger
    logging.basicConfig(filename = 'Server_Record.log',level=logging.INFO)
    logger = logging.getLogger()
    

def create_socket():
    logger()
    try : 
        global logger
        global host
        global port
        global s
        host = '127.0.0.1' #local network ip
        port = 12345
        s = socket.socket()
        logger.info("New socket has been created")
    
    except socket.error as error: # If something goes wrong with creating new socket
        logger.error("socket creation error" + error)

def bind_socket():
    try:
        global host
        global port
        s.bind((host,port)) # binding host & port
        logger.info("binding the port : " + str(port))
        s.listen(5) # queue of five client allowed
    
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
        id = data.S_number
        if id % 2 == 0: # save all even numbers in a bin file
            export(id)
        
        client_respond = str(data.text,'utf-8') #this is the message that sent by client
        print(client_respond, end="")
        if not data:
            break
        
        conn.sendall(data)
          
        logging.info("Connection has been closed ")

def export(number):
        with open('Evennumber.bin', 'a+b') as file:
            file.write(number.encode())
    
def main():
    create_socket()
    bind_socket()
    socket_accept()
    
main()
