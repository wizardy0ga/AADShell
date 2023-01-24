import cryptography.fernet

from cryptography.fernet import Fernet
from binascii import Error
import json
from tkinter import messagebox
from src.io.stdout import printError


def decryptCipherText(strCipherFile, strKey: str) -> dict:

    """
    Reads cipher text and attempts to decrypt into json object. Returns
    dictionary object from json obj if decryption is successful. Quits
    program if decryption fails.

    @params:
        key -> str, encryption key received from GUI / User
    """

    # Capture encrypted data as bytes
    with open(strCipherFile, 'rb') as file:
        data = file.read()

    try:

        # Create crypter object with the key string encoded in bytes
        decrypter = Fernet(strKey.encode())

        # Return the dict obj from the json obj after decryption
        return json.loads(decrypter.decrypt(data).decode())

    # Catch decryption errors, quit program
    except(Error, ValueError, cryptography.fernet.InvalidToken):
        messagebox.showerror('Decryption Failed!', 'Failed to decrypt data store. \nQuitting.')
        printError('Failed to decrypt data store')
        exit(0)