from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class CryptographyMethods():
    #Encryption method
    def encrypt(self, key, encryption_mode, message, init_vec):
        encrypted_message = b''
        #Make sure message is in bytes
        if type(message) is not bytes:
            message = message.encode("utf8")
        #Check if message has lenght multiple of 16
        if len(message) % 16 != 0:
            message = add_white_space(message) 
        #Encrypt message by blocks of 16
        for index in range(0, len(message), 16):
            message_block = message[index:index+16]
            cipher = Cipher(algorithms.AES(key), modes.ECB())
            encryptor = cipher.encryptor()
            if encryption_mode == 'ECB':
                message_block = encryptor.update(message_block)
            elif encryption_mode == 'CFB':
                middle = encryptor.update(init_vec)
                message_block = byte_xor(message_block, middle)
            init_vec = message_block
            encrypted_message += message_block
        return encrypted_message

    #Decryption method
    def decrypt(self, key, encryption_mode, message_to_decrypt, init_vec):
        decrypted_message = b''
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        decryptor = cipher.decryptor()
        encryptor = cipher.encryptor()
        #Decrypt message by blocks of 16
        for index in range(0, len(message_to_decrypt), 16):
            message_block = message_to_decrypt[index:index+16]
            if encryption_mode == 'ECB':
                decrypted_block = decryptor.update(message_block)
            elif encryption_mode == 'CFB':
                middle = encryptor.update(init_vec)
                decrypted_block = byte_xor(middle, message_block)
            init_vec = message_block
            decrypted_message += decrypted_block
        return decrypted_message

#Add spaces to message until len(message) % 16 == 0
def add_white_space(message):
    for i in range(0, 16 - len(message) % 16):
        message += b' '
    return message

#XOR operation
def byte_xor(ba1, ba2):
    return bytes(a ^ b for a, b in zip(ba1, ba2))