import socket 
  
# import thread module 
from _thread import *
import threading 
from uuid import getnode as get_mac
import hashlib
  
print_lock = threading.Lock() 
  
 
def threaded(c): 
    while True: 
  
        # data received from client 
        data = c.recv(1024) 
        if not data: 
            print('Bye') 
              
            # lock released on exit 
            print_lock.release() 
            break
  
        # reverse the given string from client 
        data = data[::-1] 
  
        # send back reversed string to client 
        c.send(data) 
  
    # connection closed 
    c.close() 
  
  
def Server(): 
    host = "" 
  
    # reverse a port on your computer 
    # in our case it is 12345 but it 
    # can be anything 
    port = 12435
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
  
    # a forever loop until client wants to exit 
    while True: 
  
        # establish connection with client 
        c, addr = s.accept() 
  
        # lock acquired by client 
        print_lock.acquire() 
        print('Connected to :', addr[0], ':', addr[1]) 
  
        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,)) 
    s.close() 
  
known_nodes = []  
  
def Client(host, port): 
    # local host IP '127.0.0.1
  
    # Define the port on which you want to connect 
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    # connect to server on local computer 
    s.connect((host,port)) 
  
    # message you send to server 
    my_node_id = str(get_mac())
    initial_message = "[NODEID]: " + my_node_id
    
    while True: 
  
        # message sent to server 
        s.send(initial_message.encode('ascii')) 
  
        # messaga received from server 
        data = s.recv(1024) 
  
        # print the received message 
        # here it would be a reverse of sent message 
        
        node_message = str(data.decode('ascii'))
        
        print('[NODE-SENT] ', node_message) 
        
    # close the connection 
    s.close() 
  
if __name__ == '__main__':
    Client("127.0.0.1", 5472)
    Client("127.0.0.1", 5475)
    Server() 