#Written by Pranav Hegde
#Honey Labs

import socket
import sqlite3
import os
import hashlib
import threading
import time
import argparse
import pyeclib
import os
import string
import random
import base64
import pyAesCrypt
import hashlib
import json
import itertools
import hashlib
import numpy

from os import listdir
from os.path import isfile, join
from ftplib import FTP
from datetime import datetime
from pyeclib.ec_iface import ECDriver
from threading import Thread
from uuid import getnode as get_mac 
from socketserver import ThreadingMixIn

conn = sqlite3.connect('dbs/browser_dbs/browser.db')
c = conn.cursor()

def create_node_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS nodes(
            node_id blob NOT NULL,
            node_type blob NOT NULL,
            node_ip blob NOT NULL,
            last_connect blob NOT NULL
        )''')
        
create_node_table()

def create_satellite_table():
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS satellites(
            satellite_id blob NOT NULL,
            domain_name blob NOT NULL,
            satellite_ip blob NOT NULL
        )''')
        
create_satellite_table()

class ClientThread(Thread):     
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print ("[+] New server socket thread started for " + ip + ":" + str(port))
        
        node_type = ""
 
    def run(self):
        node_conn = sqlite3.connect('dbs/satellite_dbs/satellite.db')
        node_c = node_conn.cursor()
        node_list = []
        
        while True : 
            data = str(conn.recv(2048), "utf-8")
            
            print(data)

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
    print ("[+] Waiting for jobs...") 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join()
