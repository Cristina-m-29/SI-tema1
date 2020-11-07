import socket
from functions import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2900)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)

open = True
k3 = b'cristinamititelu'
init_vec = b'mititelucristina' 
key = b''

try:
    print('Connected...\n')
    while open:
        sock.sendall("B node".encode())        
        #Receive encryption mode from node A
        mode = sock.recv(2048).decode()   
        print('Working in '+ mode + ' mode...\n')
        #Receive encrypted key
        encrypted_key = sock.recv(2048)
        crypto = CryptographyMethods()
        #Decrypt key
        key = crypto.decrypt(k3, mode, encrypted_key, init_vec)
        print('Decrypted key: ' + str(key) + '\n')
        #Send node B decrypted key
        sock.sendall(key)
        #Receive decrypted key from node A
        key_node_A = sock.recv(2048)
        #Check connection between node A and node B
        if key == key_node_A:
            sock.sendall("We can talk now!".encode())  
            print('Connection with node A DONE..Communication can begin')
            print('Waiting for file to decrypt...')
            #Receive encrypted file number of blocks
            nr_of_blocks = sock.recv(2048).decode().split(".")[0]
            encrypted_file = b''
            #Receive encrypted file by blocks
            for index in range(0, int(nr_of_blocks)):
                encrypted_block = sock.recv(2048)
                encrypted_file += encrypted_block
            print('File received...\n')
            decrypted_file = crypto.decrypt(key, mode, encrypted_file, init_vec)
            print('Decrypted file:')
            print(decrypted_file)
        open = False         
finally:
    print('Closing socket..')
    sock.close()
    
