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
    print('Connected...\n')
    while open:
        sock.sendall("B node".encode())        

        #Primire mod criptare de la nodul A
        mode = sock.recv(2048).decode()   
        print('Working in '+ mode + ' mode...\n')

        #Primire cheie criptata de la A
        encryptedKey = sock.recv(2048)

        #Decriptare cheie primita de la A
        if mode == 'ECB':
            cipher = Cipher(algorithms.AES(k3), modes.ECB())
            decr = cipher.decryptor()
            key = decr.update(encryptedKey) + decr.finalize()
        elif mode == 'CFB':
            cipher = Cipher(algorithms.AES(k3), modes.CFB(initVec))
            decr = cipher.decryptor()
            key = decr.update(encryptedKey) + decr.finalize()
        print('Decrypted key: ' + str(key) + '\n')

        #Trimitere cheie decriptata catre nodul A
        sock.sendall(key)
        #Primire cheie decriptata de la nodul lA
        nodeAKey = sock.recv(2048)
        
        #Verificare conexiune A si B
        if key == nodeAKey:
            print('Connection with node A DONE..Communication can begin')
            print('Waiting for file to decrypt...')

            #Primire nr bucati din file-ul de decriptat
            nrOfPieces = sock.recv(2048).decode()
            finalFile = b''
            i = 0
            #Primire bucati
            while i < int(nrOfPieces):
                piece = sock.recv(2048)
                #Decriptare bucata si adaugare la finalFile
                if mode == 'ECB':
                    cipher = Cipher(algorithms.AES(key), modes.ECB())
                    decr = cipher.decryptor()
                    code = decr.update(piece)
                    finalFile += code
                elif mode == 'CFB':
                    cipher = Cipher(algorithms.AES(key), modes.CFB(initVec))
                    decr = cipher.decryptor()
                    code = decr.update(piece)
                    finalFile += code
                i += 1

            print('File received...\n')
            print('File: \n' + str(finalFile) + '\n')
        open = False         
finally:
    print('Closing socket..')
    sock.close()
    
