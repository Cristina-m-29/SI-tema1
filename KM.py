import socket
import os
from functions import * 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2900)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)

open = True
k3 = b'cristinamititelu'
initVec = b'mititelucristina' 

try:
    print('Connected...\n')
    while open:
        sock.sendall("Key manager".encode())
        mode = sock.recv(2048).decode()
        #Make new instance of CryptographyMethods class from functions.py
        crypto = CryptographyMethods()
        #Random generate key and call encryption function from crypto on that key
        print('Need KEY for ' + mode + '\n')
        key = os.urandom(32)
        print('Generated key: ' + str(key) + ' \n')
        encrypted_key = crypto.encrypt(k3, mode , key, initVec)
        print('Encrypted key: ' + str(encrypted_key) +  '\n')
        #Send encrypted key
        sock.sendall(encrypted_key)
        open = False
finally:
    print('Closing socket..')
    sock.close()
    
