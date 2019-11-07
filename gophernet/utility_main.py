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

conn = sqlite3.connect('dbs/nodes.db')
c = conn.cursor()

BUFFER_SIZE = 20
transmit_port = 1980

my_node_id = ("utility-" + str(get_mac()))

def create_node_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS nodes(
            node_id blob NOT NULL,
            node_type blob NOT NULL,
            node_ip blob NOT NULL,
            last_connect blob NOT NULL
        )''')
    
    
create_node_table()

def create_confirmed_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS confirmed_nodes(
            node_id blob NOT NULL,
            node_type blob NOT NULL
        )''')
create_confirmed_table()

def create_tasks_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS tasks(
            task_id blob NOT NULL,
            node_type blob NOT NULL
        )''')
        
def create_metadata_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS storage_info(
            file_id blob NOT NULL,
            filepath blob NOT NULL,
            file_name blob NOT NULL,
            nodes blob not NULL
        )''')
create_metadata_table()
    
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
            
            if "[NODEID]" in data:
                if "utility" in data:
                    node_id = data.replace("[NODEID]: utility-", "", 1)
                    def node_lookup(node_id):
                        node_c.execute('SELECT * FROM nodes WHERE node_id="' + node_id + '";')
                        
                        return node_c.fetchall()
                    if node_lookup(node_id) == []:
                        def insert_node(node_id):
                            node_c.execute('INSERT INTO nodes (node_id, node_type, node_ip, last_connect) VALUES ("' + node_id + '", "utility", "' + ip + '", "last_connect")')
                            node_conn.commit()
                        insert_node(node_id)
                    else:
                        print(node_lookup(node_id))
                else:
                    node_type = "storage"
            elif "[GETNODES]" in data:
                print(data)
                            
                def node_lookup():
                    node_c.execute('SELECT * FROM nodes;')
                    return node_c.fetchall()
                    
                nodes = node_lookup()
                
                for node in nodes:
                    #print(node)
                    tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    tcpClient.connect(('0.0.0.0', 1980))
                    
                    message = bytes("[SENDNODE]: node_id=" + node[0] + ", node_ip=" + node[2] + ", node_type=" + node[2], "utf-8")
                    
                    tcpClient.send(message)
                    
            elif "[CONFIRM_NODE]" in data:
                if "utility" in data:
                    node_id = data.replace("[CONFIRM_NODE]: utility-", "", 1)
                    
                    def confirm_node(node_id):
                        node_c.execute('INSERT INTO confirmed_nodes (node_id, node_type) VALUES ("' + node_id + '", "utility")')
                            
                        node_conn.commit()
                        
                    confirm_node(node_id)
                else:
                    node_id = data.replace("[CONFIRM_NODE]: storage-", "", 1)
                        
                    def confirm_node(node_id):
                        node_c.execute('INSERT INTO confirmed_nodes (node_id, node_type) VALUES ("' + node_id + '", "storage")')
                            
                        node_conn.commit()
                        
                    confirm_node(node_id)
                    
            elif "[TASK]" in data:
                print(data)
            
            elif "[STORAGE_EVENT]" in data:
                initial_replace = data.replace('[STORAGE_EVENT]: ', '', 1)
                metadata = initial_replace.split(',')
                
                node_list = metadata[3].replace(' storage_nodes=', '', 1)
                file_id = metadata[0].replace('file_id=', '', 1)
                file_name = metadata[1].replace(' filename=', '', 1)
                file_path = metadata[2].replace(' filepath=', '', 1)
                
                def insertStorageEvent(storageNodes, fileId, fileName, filePath):
                    node_c.execute('INSERT INTO storage_info (file_id, filepath, file_name, nodes) VALUES ("' + file_id + '",  "' + file_path + '", "' + file_name + '", "' + node_list + '");')
                    node_conn.commit()
                    
                insertStorageEvent(node_list, file_id, file_name, file_path)
                
                
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 2004 
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