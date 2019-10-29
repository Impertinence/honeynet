import socket
import sqlite3
import os
from threading import Thread
from uuid import getnode as get_mac 
from socketserver import ThreadingMixIn

conn = sqlite3.connect('dbs/nodes.db')
c = conn.cursor()

BUFFER_SIZE = 20
transmit_port = 2003

def create_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS nodes(
            node_id blob NOT NULL,
            node_type blob NOT NULL,
            node_ip blob NOT NULL,
            last_connect blob NOT NULL
        )''')
print(create_table())
    
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
            else:
                print(data)
                
                if "[GETNODES]" and "utility" in data:
                    node_id = data.replace("[GETNODES]: utility-", "", 1)
                    
                    def find_node(node_id):
                        node_c.execute('SELECT * FROM nodes WHERE node_id="' + node_id + '";')
                        
                        return node_c.fetchall()
                    
                    if find_node(node_id) != []:
                        def node_lookup(node_id):
                            node_c.execute('SELECT * FROM nodes;')
                            
                            return node_c.fetchall()
                            
                        nodes = node_lookup(node_id)

                        for node in nodes:
                            def confirm_node(node_ip):
                                message = bytes("[CONFIRM_NODE]: utility-" + node_id, "utf-8")
                                tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                tcpClient.connect((node_ip, transmit_port))
                                
                                send_message = tcpClient.send(message)
                                    
                                if send_message:
                                    print('sent_message')
                            
                            confirm_node(node[2])
                                
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