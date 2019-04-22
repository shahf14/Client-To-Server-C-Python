from flask import Flask, request
import logging

logging.basicConfig(filename = 'Server_Record.log',level=logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)

@app.route('/addMessage', methods=['POST'])
def add_message():
    with open('Evennumber.bin', 'a+b') as file:
        logger.info(request.json['id'])

        id = int (request.json['id'])

        if id % 2 == 0 :
             file.write(.encode())

    return 'Message has recived succsufully'



app.run(debug=True)