from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.number import bytes_to_long, long_to_bytes
from tcp_by_size import send_with_size, recv_by_size
import random as rnd

class EncryptionHandler:
    def __init__(self, sock):
        # start with diffie hellman key agreement

        # Example parameters for Diffie-Hellman key exchange
        self.p = 8683317618811886495518194401279999999  # Prime number
        self.g = 265252859812191058636308479999999  # Generator

        # self.private_key = 1234567890123456789012345678901234567890
        self.private_key = rnd.randint(1, pow(10, 20))

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
            self.encryption_key = PBKDF2(str(self.shared_secret), salt=b'', dkLen=16)  # Derive a 128-bit key

    def cipher_data(self, data):
        # Generate a random IV
        iv = get_random_bytes(AES.block_size)
        # Create a new AES cipher with the generated IV
        cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
        # Encrypt the data using the cipher and IV
        ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        # Return the IV concatenated with the ciphertext
        return iv + ciphertext

    def decipher_data(self, ciphered_data):
        # Extract the IV from the beginning of the ciphered data
        iv = ciphered_data[:AES.block_size]
        # Create a new AES cipher with the extracted IV
        decipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
        # Decrypt the data, excluding the IV
        decrypted_text = unpad(decipher.decrypt(ciphered_data[AES.block_size:]), AES.block_size)
        # Decode the decrypted data to string
        decrypted_text_str = decrypted_text.decode('utf-8')
        return decrypted_text_str
