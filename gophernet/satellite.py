#sudo python3 pyeclib_encode.py 6 12 liberasurecode_rs_vand ../../ test.txt ../../target_dir
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