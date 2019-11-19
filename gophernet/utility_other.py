import socket
import sqlite3
import os
import datetime

from threading import Thread
from uuid import getnode as get_mac 
from socketserver import ThreadingMixIn

conn = sqlite3.connect('dbs/utility_dbs/nodes_other.db')
c = conn.cursor()

my_node_id = ("utility-" + str(get_mac()))

def create_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS nodes(
            node_id blob NOT NULL,
            node_type blob NOT NULL,
            node_ip blob NOT NULL,
            last_connect blob NOT NULL
        )''')
    
# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):     
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print ("[+] New server socket thread started for " + ip + ":" + str(port))
        
        node_type = ""
 
    def run(self):
        node_conn = sqlite3.connect('dbs/utility_dbs/nodes_other.db')
        node_c = node_conn.cursor()
        node_list = []
        
        while True : 
            data = str(conn.recv(2048), "utf-8")
            
            if "[NODEID]" in data:
                node_id = data.replace('[NODEID]: ', '', 1)
                node_c.execute('SELECT * FROM nodes WHERE node_id="' + node_id + '";')
                node_list = node_c.fetchall()
                
                if len(node_list) > 0:
                    print('node_already_exists')
                else:
                    if "utility" in data:
                        node_c.execute('INSERT INTO nodes (node_id, node_type, node_ip, last_connect) VALUES ("' + node_id + '", "utility", "' + data + '", "last_connect")')
                        node_conn.commit()
                    elif "storage" in data:
                        node_c.execute('INSERT INTO nodes (node_id, node_type, node_ip, last_connect) VALUES ("' + node_id + '", "storage", "' + data + '", "last_connect")')
                        node_conn.commit()
                        
            if "[VERIFY_NODE]" in data:
                tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcpClient.connect((ip, 2004))
                
                message = bytes("[CONFIRM_NODE]: utility-" + my_node_id, "utf-8")
                
                print(message)
                tcpClient.send(message)
                
            if "[SENDNODE]" in data:
                split_message = data.split(",")
                
                node_id = split_message[0].replace('[SENDNODE]: node_id=', '', 1)
                node_ip = split_message[1].replace(' node_ip=', '', 1)
                node_type = split_message[2].replace(' node_type=', '', 1)
                
                def insert_node():
                    with conn:
                        node_c.execute('INSERT INTO nodes (node_id, node_type, node_ip, last_connect) VALUES ("' + node_id + '", "' + node_type + '", "' + node_ip + '", "last_connect")')
            
            if "[GETNODES]" in data:
                print(data)
                            
                def node_lookup():
                    node_c.execute('SELECT * FROM nodes;')
                    return node_c.fetchall()
                    
                nodes = node_lookup()
                
                for node in nodes:
                    #print(node)
                    tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    tcpClient.connect(('0.0.0.0', 2003))
                    
                    message = bytes("[SENDNODE]: node_id=" + node[0] + ", node_ip=" + node[1] + ", node_type=" + node[2], "utf-8")
                    
                    tcpClient.send(message)
            
            if "[GET_STORAGE_NODES]:" in data:
                node_c.execute('SELECT * FROM nodes WHERE node_type="storage";')
                
                current_time = 
                storage_nodes = node_c.fetchall()
                active_nodes = []
                
                for node in storage_nodes:
                    if node[]
                            
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 1980 
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