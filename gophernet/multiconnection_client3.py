import socket
import os

# Python TCP Client B
import socket
from uuid import getnode as get_mac  

host = socket.gethostname() 
port = 2004
BUFFER_SIZE = 2000
node_id = str(get_mac()) 
MESSAGE = bytes("[CONFIRM_NODE]: utility-" + node_id, "utf-8")
 
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientB.connect((host, port))

while MESSAGE != 'offline':
    tcpClientB.send(MESSAGE)     
    data = tcpClientB.recv(BUFFER_SIZE)
    print (" Client received data:", data)
    MESSAGE = bytes(input("tcpClientB: Enter message to continue/ Enter exit:"), "utf-8")

tcpClientB.close()