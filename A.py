import socket
import threading
from functions import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

sock = socket.socket()
server_addres = ('localhost', 2900)
threadCount = 0

k3 = b'cristinamititelu'
init_vec = b'mititelucristina' 

encrypted_key = 'none'
key = b''

#Create socket
try:
    sock.bind(server_addres)
except socket.error as e:
    print(str(e), type(e))

#Handler function for node A - KM connection
def handleKeyManager(connection):
    global encrypted_key
    #Receive encrypted key
    encrypted_key = connection.recv(2048)
    print('Encrypted key received \n')
    print('Waiting for sign from node B...\n')
    connection.close()

#Handler function for node A - node B connection
def handleBNode(connection): 
    #Send encrypted key to node B
    while encrypted_key == 'none':
        pass
    connection.sendall(encrypted_key)
    #Make new instance of CryptographyMethods class from functions.py
    crypto = CryptographyMethods()
    print('Waiting for key decryption...')
    #Decryption for key received from KM
    key = crypto.decrypt(k3, mode, encrypted_key, init_vec)
    print('Decrypted key: ' + str(key) + '\n')
    #Wait for decrypted key from node B
    key_node_B = connection.recv(2048)
    #Send node A decrypted key to node B
    connection.sendall(key)
    #Check node A - node B connection
    if key == key_node_B:
        message = connection.recv(2048).decode()
        print('Message from node B: ' + message)
        print('Connection with node B DONE..Communication can begin\n')
        #Read and encrypt file
        with open("fisier.txt", "rb") as file:
            file = file.read()
            encrypted_file = crypto.encrypt(key, mode, file, init_vec)
        #Send number of file blocks to node B
        nr_of_blocks = len(encrypted_file) / 16
        if len(encrypted_file) % 16 != 0: nr_of_blocks += 1
        connection.sendall(str(nr_of_blocks).encode())
        #Send encrypted file by blocks
        print('Sedining file encrypted...')
        for index in range(0, len(encrypted_file), 16):
            encrypted_block = encrypted_file[index:index + 16]
            connection.sendall(encrypted_block)
    print('File sent \n')
    print('Closing socket...')
    connection.close()
    

#Ask for input from user for the encryption mode
selection = input('Choose mode:\na = ECB \nb = CFB \n')
while selection not in 'ab':
    selection = input('Choose mode:\na = ECB \nb = CFB \n')
if selection == 'a':
    mode = 'ECB'
else:
    mode = 'CFB'
print('Working in ' + mode + ' mode...\n')
print('Waiting for encrypted key from KM..')

#Wait for connections
sock.listen(2)

#Handle new connection
try:
    while threadCount < 2:
        #Accept connections
        client, address = sock.accept()
        #Get node type
        node_type = client.recv(2048).decode()
        #Send encryption mode to connection
        client.sendall(mode.encode())
        threadCount += 1
        #Create new thread
        if node_type == 'Key manager':
            km = threading.Thread(target = handleKeyManager(client))
            km.start()
        else:
            bn = threading.Thread(target = handleBNode(client))
            bn.start()
finally:
    #Wait for the threads executions
    km.join()
    bn.join()
    sock.close()
