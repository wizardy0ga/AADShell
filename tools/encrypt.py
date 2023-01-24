"""
Used to encrypt the json database. Will create a backup of the current store first.
Script only executes if key bytes have been provided.
Reads JSON from plain.json file.
"""

from cryptography.fernet import Fernet

"""
1. Comment out a single pair of variables. Data.txt is the store where the app secrets are held. Kdata.txt is the 
   file for the API keys
"""
#store = '../store/data.txt'
#storeBak = '../store/data.txt.bak'

store = '../store/kdata.txt'
storeBak = '../store/kdata.txt.bak'

"""
2. Set the symmetric key
"""
KEY = b''

json = open('plain.json', 'r').read()

# Check for empty parameters
if json == '':
    print('No json was provided. Exiting')
    exit(0)
elif KEY == b'':
    print('No key was provided. Exiting')
    exit(0)

# Get user confirmation
if input('[!] {} is about to be encrypted. Type "yes" to confirm. -> '.format(store)) == 'yes':
    crypter = Fernet(KEY)

    # Create a backup of the current store
    with open(storeBak, 'w') as backupFile:

        try:
            with open(store, 'r') as publishingFile:
                backupFile.write(publishingFile.read())

        except FileNotFoundError:
            print('[!] {} not found. Skipping backup'.format(store))

    # Ceate a new store
    with open(store, 'w') as file:
        file.write(crypter.encrypt(json.encode()).decode())

    print('[+] [SUCCESS] -> {} was successfully encrypted.'.format(store))

else:
    print('[!] Failed to decrypt {}. User did not provide "yes" for confirmation.'.format(store))

