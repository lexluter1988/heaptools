from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature

# should be stored in settings.py

secret_key = b'xxxx='

class Fnt():
    def __init__(self):
        self.helper = Fernet(secret_key)

    def encrypt(self, msg):
        if isinstance(msg, str):
            msg = bytes(msg, 'utf-8')
        return self.helper.encrypt(msg)
        
    def decrypt(self, msg):
        if isinstance(msg, str):
            msg = bytes(msg, 'utf-8')
        try:
            return self.helper.decrypt(msg).decode()
        except InvalidSignature:
            raise('Wrong or empty key provided')
