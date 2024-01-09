from cryptography.fernet import Fernet
import base64
import hashlib
from pathlib import Path
import io
import zipfile
import os


DECRYPTED_DATA_FOLDER = Path(__file__).parent.parent / "decrypted_data"
ENCRYPTED_DATA_FILE = Path(__file__).parent.parent / "encrypted_data.bin"
#SOURCE_FOLDER = Path(__file__).parent.parent / "source"


def generate_key(password):
    password = password.encode()
    sha256_password = hashlib.sha256(password).digest()
    base64_password = base64.urlsafe_b64encode(sha256_password)
    return base64_password

def decrypt_file(password: str, source_file: Path) -> bytes:
    """
    Decrypts a file and returns the decrypted data as bytes.
    
    Parameters
    ----------
    password : str
        The password used to decrypt the file.
    source_file : Path
        The path to the file to decrypt.

    Returns
    -------
    decrypted : bytes
        The decrypted data.
    """
    key = generate_key(password)
    fernet = Fernet(key)

    with open(source_file, 'rb') as file:
        encrypted = file.read()
    decrypted_bytes = fernet.decrypt(encrypted)

    return decrypted_bytes


def encrypt_bytes(password: str, source_file: bytes) -> bytes:
    """
    Encrypts a file and returns the encrypted data as bytes.

    Parameters
    ----------
    password : str
        The password used to encrypt the file.
    source_file : bytes
        The bytes to encrypt.
    """
    key = generate_key(password)
    fernet = Fernet(key)

    encrypted_bytes = fernet.encrypt(source_file)

    return encrypted_bytes


def decrypt_database(password: str, encrypted_data_file_path: Path = ENCRYPTED_DATA_FILE):

    decrypted_file = decrypt_file(password, encrypted_data_file_path)
    
    # Create a BytesIO object from the zipped bytes
    zipped_io = io.BytesIO(decrypted_file)

    # Create a ZipFile object from the BytesIO object
    with zipfile.ZipFile(zipped_io, 'r') as zip_ref:
        # Extract all files to the destination directory
        zip_ref.extractall(DECRYPTED_DATA_FOLDER.parent)
    # Close the BytesIO object
    zipped_io.close()


def encrypt_database(password: str, decrypted_data_folder_path: Path = DECRYPTED_DATA_FOLDER):
    """
    Creates a zip file from the decrypted_data folder and ecrypts the bytes of the zip file it with the given password.
    """
    # Create a BytesIO object
    zipped_io = io.BytesIO()

    # Zip the whole decrypted_data folder and its contents and write the zipped bytes to the BytesIO object
    with zipfile.ZipFile(zipped_io, 'w') as zip_file:
        for file in decrypted_data_folder_path.rglob("*"):
            # Get the relative path of the file to the folder you want to zip
            relative_path = file.relative_to(decrypted_data_folder_path.parent)
            # Write the file to the zip file with the new arcname
            zip_file.write(file, arcname=relative_path)

    # Get the bytes of the zipped file
    zipped_bytes = zipped_io.getvalue()

    # Encrypt the zipped bytes
    encrypted_bytes = encrypt_bytes(password, zipped_bytes)

    # Write the encrypted bytes to the encrypted_data file
    with open(ENCRYPTED_DATA_FILE, "wb") as file:
        file.write(encrypted_bytes)
