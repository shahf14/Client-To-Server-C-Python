from message import *
import logging

logger = logging.getLogger()

def export(opcode):
    text = "Opcode : " + str(opcode) + " "
    with open('opcode.bin', 'a+b') as file:
        file.write(text.encode('ascii'))

def terms(msg):

    if msg.opcode == 1:
        export(msg.opcode)

    elif msg.opcode == 2:
        msg.counter += 1

    else:
        logger.info("Unexpected opcode %d" % msg.opcode)

    return msg






