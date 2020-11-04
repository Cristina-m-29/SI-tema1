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

#Creare socket
try:
    sock.bind(server_addres)
except socket.error as e:
    print(str(e), type(e))

#Functie management conexiune nod A - KM
def handleKeyManager(connection):
    global encryptedKey
    connection.send(mode.encode())
    encryptedKey = connection.recv(2048)
    print('Encrypted key received \n')
    print('Waiting for sign from node B...\n')
    connection.close()

#Functie management conexiune nod A - nod B
def handleBNode(connection): 
    #Trimitere mod cripatre catre nodul B
    connection.sendall(mode.encode())
    
    #Trimitere cheie criptata catre nodul B
    while encryptedKey == 'none':
        pass
    connection.sendall(encryptedKey)

    print('Waiting for key decryption...')
    #Decriptare cheie primita de la KM
    if mode == 'ECB':
        cipher = Cipher(algorithms.AES(k3), modes.ECB())
        decr = cipher.decryptor()
        key = decr.update(encryptedKey) + decr.finalize()
    elif mode == 'CFB':
        cipher = Cipher(algorithms.AES(k3), modes.CFB(initVec))
        decr = cipher.decryptor()
        key = decr.update(encryptedKey) + decr.finalize()
    print('Decrypted key: ' + str(key) + '\n')

    #Primire cheie decriptata de la nodul B
    nodeBKey = connection.recv(2048)
    #Trimitere cheie decriptata la nodul B
    connection.sendall(key)

    #Verificare conexiune A si B
    if key == nodeBKey:
        print('Connection with node B DONE..Communication can begin')

        #Read and break file in binary pieces
        #Each piece has 512 bytes
        filePieces = []
        with open("fisier.txt", "rb") as file:
            while True:
                piece = file.read(len(key))
                if piece == b"":
                    break
                else: 
                    if len(piece) < len(key):
                        i = 0
                        while i < len(key) - len(piece):
                            piece += b' '
                    filePieces.append(piece)

        print('Sedining file encrypted...')
        #Trimitere nr de bucati din file catre nodul B
        connection.sendall(str(len(filePieces)).encode())

        #Criptare fiecare bucata si trimitere catre nodul B
        if mode == 'ECB':
            cipher = Cipher(algorithms.AES(key), modes.ECB())
            encript = cipher.encryptor()
            for piece in filePieces:
                code = encript.update(piece)
                connection.sendall(code)
        elif mode == 'CFB':
            cipher = Cipher(algorithms.AES(key), modes.CFB(initVec))
            encript = cipher.encryptor()
            decr = cipher.decryptor()
            for piece in filePieces:
                code = encript.update(piece)
                print(decr.update(code))
                connection.sendall(code)
    print('File sent \n')
    print('Closing socket...')
    connection.close()
    

#Cerere input de la user pentru modul de criptare
selection = input('Choose mode:\na = ECB \nb = CFB \n')
while selection not in 'ab':
    selection = input('Choose mode:\na = ECB \nb = CFB \n')
if selection == 'a':
    mode = 'ECB'
else:
    mode = 'CFB'
print('Working in ' + mode + ' mode...\n')
print('Waiting for encrypted key from KM..')

#Asteptare conexiuni
sock.listen(2)

#Handle new connection
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
