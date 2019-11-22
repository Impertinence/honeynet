#Written by Pranav Hegde

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
import hashlib

from os import listdir
from os.path import isfile, join
from ftplib import FTP
from datetime import datetime
from pyeclib.ec_iface import ECDriver
from threading import Thread
from uuid import getnode as get_mac 
from socketserver import ThreadingMixIn

node_conn = sqlite3.connect('dbs/satellite_dbs/satellite.db')
node_c = node_conn.cursor()
my_node_id = ("satellite-" + str(get_mac()))

if not os.path.exists('staging_dir'):
    os.mkdir('staging_dir')
    
if not os.path.exists('retrieval_dir'):
    os.mkdir('retrieval_dir')
    
def getStagedFiles():
    return os.listdir('staging_dir')

def create_node_table():
    with node_conn:
        node_c.execute('''CREATE TABLE IF NOT EXISTS nodes(
            node_id blob NOT NULL,
            node_type blob NOT NULL,
            node_ip blob NOT NULL,
            last_connect blob NOT NULL
        )''')
        
create_node_table()

def create_file_table():
    with node_conn:
        node_c.execute('''CREATE TABLE IF NOT EXISTS files(
            file_id blob NOT NULL,
            bucket_id blob NOT NULL,
            encryption_key blob NOT NULL,
            file_ext blob NOT NULL,
            filename blob NOT NULL
        )''')
create_file_table()
        
def create_buckets_table():
    with node_conn:
        node_c.execute('''CREATE TABLE IF NOT EXISTS buckets(
            bucket_id blob NOT NULL,
            satellite_id blob NOT NULL,
            bucket_name blob NOT NULL,
            bucket_master blob NOT NULL
        )''')
create_buckets_table()

def createMasterBucket():
    node_c.execute('SELECT * FROM buckets;')
    bucket_list = node_c.fetchall()
    
    if len(bucket_list) == 0:
        node_c.execute('INSERT INTO buckets (bucket_id, satellite_id, bucket_name, bucket_master) VALUES ("MASTER", "' + my_node_id + '", "MASTER", "this_is_master");')
        node_conn.commit()
createMasterBucket()

print('''
    WELCOME TO THE HONEYNET CLI INTERFACE
''')

filepath = input('filepath>')
filename = input('filename>')

raw_file = filepath + '/' + filename
file_ext = os.path.splitext(raw_file)[1]

node_c.execute('SELECT * FROM buckets;')
bucketList = node_c.fetchall()

if len(bucketList) == 1:
    print('''
        CHOOSE A BUCKET
    ''')
    print('1. Master Bucket')
    print('2. Create Bucket')
    
    bucket_num = input('bucket(number)>')
    
    if bucket_num == "1":
        now = datetime.now()
        time = now.strftime("%m/%d/%Y, %H:%M:%S")
        raw_file_id = str(base64.b64encode(bytes(time, "UTF-8")))
        first_replace = raw_file_id.replace("b'", '', 1)
        
        print(raw_file_id)
        exit()
        
        file_id = first_replace.replace("'", "", 1)
        bucket_id = "MASTER"
        
        bufferSize = 64 * 1024
        
        encryption_key = str(random.getrandbits(128))
        encrypted_file = "staging_dir/" + file_id + ".aes"
        
        pyAesCrypt.encryptFile(raw_file, encrypted_file, encryption_key, bufferSize)
        
        k_element = "10"
        m_element = "20"
        
        ec_driver = ECDriver(k=k_element, m=m_element, ec_type="liberasurecode_rs_vand")
        
        with open(encrypted_file, "rb") as fp:
            whole_file_str = fp.read()
            
        fragments = ec_driver.encode(whole_file_str)
        
        i = 0
        for fragment in fragments:
            with open(encrypted_file + "." + str(i), "wb") as fp:
                fp.write(fragment)
            i += 1
            
        node_c.execute('INSERT INTO files (file_id, bucket_id, encryption_key, file_ext, filename) VALUES ("' + file_id + '", "' + bucket_id + '", "' + encryption_key + '", "' + file_ext + '", "' + filename + '")')
        node_conn.commit()
        
        def findUtility():
            conn = sqlite3.connect('dbs/utility_dbs/nodes.db')
            c = conn.cursor()
        
            c.execute('SELECT * FROM nodes WHERE node_type="utility";')
            return c.fetchall()
        
        def findStorage():
            conn = sqlite3.connect('dbs/utility_dbs/nodes.db')
            c = conn.cursor()
            
            c.execute('SELECT * FROM nodes WHERE node_type="storage";')
            return c.fetchall()
            
        utility_nodes = findUtility()
        storage_nodes = findStorage()
        
        #for node in utility_nodes:
        #    node_ip = node[2]
        #    node_type = node[1]
        #    node_id = node[0]
            
        #    tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        #    command_success = 0
        #    
        #    host = "0.0.0.0"
        #    port = 1980
        #    message = bytes("[STORAGE_EVENT]: file_id=" + file_id + ", filename=" + filename + ", filepath=" + filepath + ", ", "UTF-8")
        #    
        #    while command_success is 0:
        #        try:
        #            tcpClient.connect((host, port))
        #            tcpClient.send(message)
        #        except:
        #            pass
        
        staged_files = [f for f in listdir('staging_dir') if isfile(join('staging_dir', f))]
        
        
        #for node in storage_nodes_list
        #node_c.execute('INSERT INTO files (file_id, bucket_id, bucketname, filepath, filename) VALUES ("' + file_id + '", "' + bucket_id + '", "' + bucket_name + '", "' + filepath'", "' + filename + '")')
        #node_c.commit()
            
def fileCheck():
    node_c.execute('SELECT * FROM files;')
    files = node_c.fetchall()
    
    if files.length > 0:
        node_c.execute('SELECT * FROM nodes WHERE node_type="storage";')
        nodelist = node_c.fetchall()
        
        for node in nodelist:
            print(node)
        
    threading.Timer(10.0, fileCheck).start()
           
def findNodes():
    conn = sqlite3.connect('dbs/satellite_dbs/satellite.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM nodes;')
    
    current_node_list = c.fetchall()
    
    for node in current_node_list:
        node_ip = node[2]
        
        port = 1980
        host = "0.0.0.0"
        
        tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        message_success = 0
        
        while message_success is 0:
            try:
                tcpClient.connect((host, port))
                tcpClient.send(bytes("[GETNODES]: " + my_node_id, "UTF-8"))
            except:
                pass
                
    threading.Timer(300.0, findNodes).start()
        
findNodes()

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
                
                node_ip = message[2]
                node_id = message[0]
                
                print(node_id)

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

