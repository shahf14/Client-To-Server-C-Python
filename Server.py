import socket
import logging

def logger():
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
        host = '127.0.0.1'
        port = 12345
        s = socket.socket()
        logger.info("New socket has been created")
    
    except socket.error as error: 
        logger.error("socket creation error" + error)

def bind_socket():
    try:
        global host
        global port
        s.bind((host,port))
        logger.info("binding the port : " + str(port))
        s.listen(5)
    
    except socket.error as error: 
        logger.error("socket binding error : " + error)
    
def socket_accept():
    
    conn, addr = s.accept()
    logger.info("connection has been established | IP " + addr[0] + " Port :" + addr[1])
    send_socket(conn)
    conn.close()
    
def send_socket(conn):
    while True:
        data = conn.recv(1024)
        client_respond = str(data,'utf-8')
        print(client_respond, end="")
        if not data:
            break
        conn.sendall(data)
          
        logging.info("Connection has been closed ")


def main():
    create_socket()
    bind_socket()
    socket_accept()
    
main()
