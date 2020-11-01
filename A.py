import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

sock = socket.socket()
server_addres = ('localhost', 2900)
threadCount = 0

k3 = b'cristinamititelu'
initVec = b'mititelucristina'

encryptedKey = 'none'
key = b''

try:
    sock.bind(server_addres)
except socket.error as e:
    print(str(e), type(e))

def handleKeyManager(connection):
    global encryptedKey
    connection.send(mode.encode())
    encryptedKey = connection.recv(2048)
    connection.close()

def handleBNode(connection): 
    connection.sendall(mode.encode())
    while encryptedKey == 'none':
        pass
    connection.sendall(encryptedKey)
    if mode == 'ECB':
        cipher = Cipher(algorithms.AES(k3), modes.ECB())
        decr = cipher.decryptor()
        key = decr.update(encryptedKey) + decr.finalize()
    elif mode == 'CFB':
        cipher = Cipher(algorithms.AES(k3), modes.CFB(initVec))
        decr = cipher.decryptor()
        key = decr.update(encryptedKey) + decr.finalize()
    print('Decrypted key: \n' + str(key))
    nodeBKey = connection.recv(2048)
    connection.sendall(key)
    if key == nodeBKey:
        print('Connection DONE..Communication can begin')
    connection.close()

selection = input('Choose mode:\na = ECB \nb = CFB \n')
while selection not in 'ab':
    selection = input('Choose mode:\na = ECB \nb = CFB \n')
if selection == 'a':
    mode = 'ECB'
else:
    mode = 'CFB'

sock.listen(2)

try:
    while threadCount < 2:
        client, address = sock.accept()
        nodeType = client.recv(2048).decode()
        threadCount += 1
        if nodeType == 'Key manager':
            km = threading.Thread(target = handleKeyManager(client))
            km.start()
        else:
            bn = threading.Thread(target = handleBNode(client))
            bn.start()
finally:
    km.join()
    bn.join()
    sock.close()
