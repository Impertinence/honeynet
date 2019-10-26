import socket
import pickle
import shelve
import os
from threading import Thread
from uuid import getnode as get_mac 
from socketserver import ThreadingMixIn 

# Multithreaded Python server : TCP Server Socket Thread Pool



class ClientThread(Thread):     
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print ("[+] New server socket thread started for " + ip + ":" + str(port))
        
        node_type = ""
 
    def run(self):
        node_list = []
        while True : 
            data = str(conn.recv(2048), "utf-8")
            print(data)
            
            if "[NODEID]" in data:
                if "utility" in data:
                    node_type = "utility"
                    with shelve.open('nodes') as node_db:
                        new_node_id = data.replace("[NODEID]: utility-", "")
                        with shelve.open('nodes') as node_db:
                            print(node_db)
                            
                else:
                    node_type = "storage"
            else:
                print(data)
                
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