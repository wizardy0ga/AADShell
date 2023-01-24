from src.utils import gui, crypto
from src.io.shell import AADShell
from src.utils.paths import store
from src.utils.paths import keys
from os import system
from src.io.stdout import printInfo


if __name__ == '__main__':
    system("")

    # Get the key string and canvas object
    key, canvas = gui.getKeyFromUser()

    # Attempt to decrypt the data store. Program will exit if decryption is invalid
    dictDataStore = crypto.decryptCipherText(store, key)

    # Get the external API Keys
    dictKeyStore = crypto.decryptCipherText(keys, key)

    # Validate the data and key variables as a dicts to continue to the shell.
    if isinstance(dictDataStore, dict) and isinstance(dictKeyStore, dict):

        # Destroy the GUI
        canvas.destroy()
        printInfo('Decryption was successful, proceeding...')

        # Delete decryption key
        del key

        # Launch the main shell
        AADShell(dictDataStore, dictKeyStore).cmdloop()
