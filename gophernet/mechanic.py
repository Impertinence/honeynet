import socket
import sqlite3
import os
import hashlib
import threading
import time

from threading import Thread
from random import *
from uuid import getnode as get_mac 
from socketserver import ThreadingMixIn

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("root", "password", "mechanic_dir", perm="elradfmwMT")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 21), handler)


conn = sqlite3.connect('dbs/storage_dbs/nodes.db')
c = conn.cursor()

BUFFER_SIZE = 20
transmit_port = 1980

my_node_id = ("storage-" + str(get_mac()))

def create_node_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS nodes(
            node_id blob NOT NULL,
            node_type blob NOT NULL,
            node_ip blob NOT NULL,
            last_connect blob NOT NULL
        )''')
create_node_table()

def create_events_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS events(
            file_id blob NOT NULL,
            satellite_id blob NOT NULL,
            satellite_ip blob NOT NULL,
            event_type blob NOT NULL
        )''')
#create_events_table()

# Multithreaded Python server : TCP Server Socket Thread Pool
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
            
            if "[STORAGE_EVENT]" in data:
                print(data)
                
                
file_list = []                

def maintainConn():
    maintain_conn = sqlite3.connect('dbs/storage_dbs/nodes.db')
    maintain_c = maintain_conn.cursor()
    
    def node_lookup(node_id):
        maintain_c.execute('SELECT * FROM nodes;')
        return maintain_c.fetchall()
    
    node_list = node_lookup(my_node_id)
    
    for node in node_list:
        print(node)
    
    threading.Timer(60.0, maintainConn).start()

maintainConn()

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 2002 
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print ("[+] Waiting for jobs...") 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join()
    
