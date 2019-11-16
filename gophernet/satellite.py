#sudo python3 pyeclib_encode.py 6 12 liberasurecode_rs_vand ../../ test.txt ../../target_dir
#sudo python3 pyeclib_decode.py 6 12 ../../target_dir/test.txt.0
#./../target_dir/test.txt.1 ../../target_dir/test.txt.2 ../../target_dir/test.txt.3 ../../target_dir/test.txt.4 ../../target_dir/test.t
#t.5 ../../target_dir/test.txt.6 ../../target_dir/test.txt.7 ../../target_dir/test.txt.8 ../../target_dir/test.txt.9 ../../target_dir/te
#t.txt.10 ../../target_dir/test.txt.11 ../../target_dir/test.txt.12 ../../target_dir/test.txt.13 ../../target_dir/test.txt.14 ../../targ
#t_dir/test.txt.15 ../../target_dir/test.txt.16 ../../target_dir/test.txt.17

import socket
import sqlite3
import os
import hashlib
import threading
import time
import argparse

from threading import Thread
from random import *
from uuid import getnode as get_mac 
from socketserver import ThreadingMixIn

node_conn = sqlite3.connect('dbs/utility_dbs/nodes.db')
node_c = node_conn.cursor()
my_node_id = ("satellite-" + str(get_mac()))

print('''
    WELCOME TO THE HONEYNET CLI INTERFACE
''')

class ClientThread(Thread):     
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print ("[+] New server socket thread started for " + ip + ":" + str(port))
        
        node_type = ""
 
    def run(self):
        node_conn = sqlite3.connect('dbs/nodes.db')
        node_c = node_conn.cursor()
        node_list = []
        
        while True : 
            data = str(conn.recv(2048), "utf-8")
            
            if "[TRANSFER_READY]" in data:
                print(data)
                
            if "[SENDNODE]" in data:
                raw_message = data.replace('[SENDNODE]: node_id=', '', 1)
                message = raw_message.split(',')
                
                node_id = message[0]
                node_
                print(node_id)
                

def findNodes():
    node_c.execute('SELECT * FROM nodes;')
    
    current_node_list = node_c.fetchall()
    
    for node in current_node_list:
        node_ip = node[2]
        
        port = 1980
        host = "0.0.0.0"
        
        tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClient.connect((host, port))
        
        tcpClient.send(bytes("[GETNODES]: " + my_node_id, "UTF-8"))
findNodes()

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 2003 
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join()

