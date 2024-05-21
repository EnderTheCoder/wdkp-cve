"""
@Time: 2024/5/21 11:11
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: secret.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class SecretUtil:
    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')

    def encrypt(self, plaintext):
        padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(padded_plaintext).hex()
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = bytes.fromhex(ciphertext)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_text = cipher.decrypt(ciphertext)
        return unpad(decrypted_text, AES.block_size).decode('utf-8')


# Example usage
key = "12345678900000001234567890000000"
iv = "1234567890000000"

secret_util = SecretUtil(key, iv)
