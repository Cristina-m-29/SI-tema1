import socket
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2900)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)

open = True
k3 = b'cristinamititelu'
initVec = b'mititelucristina' 

try:
    print('Connected...')
    while open:
        sock.sendall("Key manager".encode())
        mode = sock.recv(2048).decode()

        #Random generate keys and use AES with k3 on that key
        if mode == 'ECB':
            print('Need KEY for ECB')
            k1 = os.urandom(32)
            print('Decrypted key: \n' + str(k1))
            cipher = Cipher(algorithms.AES(k3), modes.ECB())
            encrypthor = cipher.encryptor()
            code = encrypthor.update(k1) + encrypthor.finalize()
            print('Encrypted key: \n' + str(code))
            sock.sendall(code)
        elif mode == 'CFB':
            print('Need KEY for CFB')
            k2 = os.urandom(32)
            print('Decrypted key: \n' + str(k2))
            cipher = Cipher(algorithms.AES(k3), modes.CFB(initVec))
            encrypthor = cipher.encryptor()
            code = encrypthor.update(k2) + encrypthor.finalize()
            print('Encrypted key: \n' + str(code))
            sock.sendall(code)

        open = False
finally:
    print('Closing socket..')
    sock.close()
    
