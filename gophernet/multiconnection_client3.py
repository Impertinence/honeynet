import socket
import os
import random
import string

# Python TCP Client B
import socket
from uuid import getnode as get_mac

def generateFileId(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))  

generateFileId(20)

def generate

host = socket.gethostname() 
port = 2004
BUFFER_SIZE = 2000
node_id = str(get_mac()) 
MESSAGE = bytes("[STORAGE_EVENT]: file_id=" + generateFileId(20) + ", filename=test.txt, filepath=/test/test/, storage_nodes='" + node_id + " " + node_id + " " + node_id + "'", "utf-8")
 
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientB.connect((host, port))

while MESSAGE != 'offline':
    tcpClientB.send(MESSAGE)     
    data = tcpClientB.recv(BUFFER_SIZE)
    print (" Client received data:", data)
    MESSAGE = bytes(input("tcpClientB: Enter message to continue/ Enter exit:"), "utf-8")

tcpClientB.close()