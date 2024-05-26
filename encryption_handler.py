from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.number import bytes_to_long, long_to_bytes
from tcp_by_size import send_with_size, recv_by_size
import random as rnd

class EncryptionHandler:
    def  __init__(self, sock):
        # start with diffie hellman key agreement
        
        # Example parameters for Diffie-Hellman key exchange
        self.p = 23456789012345678901234567890123456789  # Prime number
        self.g = 5  # Generator
        
        #self.private_key = 1234567890123456789012345678901234567890
        self.private_key = rnd.randint(1, 10**20)
        
        self.public_key = pow(self.g, self.private_key, self.p)
        
        self.initiate_key_exchange(sock)
    
    def initiate_key_exchange(self, sock):
        send_with_size(sock, f"SENKEY|{self.public_key}")
        
        data = recv_by_size(sock).decode().split('|')
        
        if len(data) <= 1:
            return
        
        if data[0] == "SENKEY":
            other_public_key = int(data[1])
            
            self.shared_secret = pow(other_public_key, self.private_key, self.p)
            self.set_up_ciphering()
    
    def set_up_ciphering(self):
        # Example using PBKDF2
        shared_secret_bytes = long_to_bytes(self.shared_secret)  # Convert shared secret to bytes
        self.encryption_key = PBKDF2(shared_secret_bytes, salt=b'', dkLen=16)  # Derive a 128-bit key

        self.cipher = AES.new(self.encryption_key, AES.MODE_CBC)
        self.iv = self.cipher.iv
        self.decipher = AES.new(self.encryption_key, AES.MODE_CBC, iv=self.iv)
    
    def cipher_data(self, data):
        # Encryption
        #cipher = AES.new(self.encryption_key, AES.MODE_CBC)
        #self.iv = cipher.iv
        ciphertext = self.cipher.encrypt(pad(data.encode(), AES.block_size))
        return ciphertext
    
    def decipher_data(self, ciphered_data):
        # Decryption
        #decipher = AES.new(self.encryption_key, AES.MODE_CBC, iv=self.iv)
        decrypted_text = unpad(self.decipher.decrypt(ciphered_data), AES.block_size)
        return decrypted_text
