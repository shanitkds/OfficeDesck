from cryptography.fernet import Fernet
from django.conf import settings

MASTER_KEY = settings.FILE_MASTER_KEY.encode()


def genarate_file_KEY():
    return Fernet.generate_key()

def encrpt_file(file,key):
    fernet=Fernet(key)
    return fernet.encrypt(file)

def decript_file(file,key):
    fernet=Fernet(key)
    return fernet.decrypt(file)

def encrypt_key(key):
    fernet=Fernet(MASTER_KEY)
    return fernet.encrypt(key)

def decript_key(key):
    fernet=Fernet(MASTER_KEY)
    return fernet.decrypt(key)