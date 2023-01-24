"""
Decrypt the JSON Database, write output to file
"""

from cryptography.fernet import Fernet
import json

"""
1. Comment out ONE of the store vars. data.txt is the app secret store, kdata is the api key store 
"""
store = '../store/data.txt'
#store = '../store/kdata.txt'

"""
2. Set the symmetric key
"""
KEY = b''

# Check for no key
if KEY == b'':
    exit('No key was provided.')


crypter = Fernet(KEY)

# Capture the encrypted data
with open(store, 'rb') as file:
    data = json.loads(crypter.decrypt(file.read()))

# Write to plain.json file
with open('plain.json', 'w') as file:
    file.write(str(json.dumps(data)))

print('[SUCCESS] {} was decrypted and placed in plain.json'.format(store))
