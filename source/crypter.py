from cryptography.fernet import Fernet
import base64
import hashlib
from pathlib import Path


def generate_key(password):
    password = password.encode()
    sha256_password = hashlib.sha256(password).digest()
    base64_password = base64.urlsafe_b64encode(sha256_password)
    return base64_password

def decrypt_file(password: str, source_file: Path) -> str:
    """
    Decrypts a file and returns the decrypted data as a string.
    
    Parameters
    ----------
    password : str
        The password used to decrypt the file.
    source_file : Path
        The path to the file to decrypt.
    """
    key = generate_key(password)
    fernet = Fernet(key)

    with open(source_file, 'rb') as file:
        encrypted = file.read()
    decrypted = fernet.decrypt(encrypted)

    return decrypted.decode()


def encrypt_file(password: str, source_file: Path) -> str:
    """
    Encrypts a file and returns the encrypted data as a string.

    Parameters
    ----------
    password : str
        The password used to encrypt the file.
    source_file : Path
        The path to the file to encrypt.
    """
    key = generate_key(password)
    fernet = Fernet(key)

    with open(source_file, 'rb') as file:
        data = file.read()
    encrypted = fernet.encrypt(data)

    return encrypted.decode()
