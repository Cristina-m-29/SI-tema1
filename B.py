import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2900)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)

open = True
k3 = b'cristinamititelu'
initVec = b'mititelucristina' 
key = b''

try:
    print('Connected...')
    while open:
        sock.sendall("B node".encode())          
        mode = sock.recv(2048).decode()   
        print('Working in '+ mode + ' mode...')
        encryptedKey = sock.recv(2048)
        if mode == 'ECB':
            cipher = Cipher(algorithms.AES(k3), modes.ECB())
            decr = cipher.decryptor()
            key = decr.update(encryptedKey) + decr.finalize()
        elif mode == 'CFB':
            cipher = Cipher(algorithms.AES(k3), modes.CFB(initVec))
            decr = cipher.decryptor()
            key = decr.update(encryptedKey) + decr.finalize()
        print('Decrypted key: \n' + str(key))
        sock.sendall(key)
        nodeAKey = sock.recv(2048)
        if key == nodeAKey:
            print('Connection DONE..Communication can begin')
        open = False         
finally:
    print('Closing socket..')
    sock.close()
    
