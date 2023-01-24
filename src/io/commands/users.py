from src.io import stdout
from src.utils.argparser import ArgumentParser

# Command information dictionary
dictInfo = {
    'Description': 'Show all available user objects in the CWT by Display Name and User Principal Name',
    'Usage': 'users'
}

# Parser object
parser = ArgumentParser("users", dictInfo)


def showUsers(objAADShell) -> None:

    """
    Display all user objects by UPN and display name within the current working tenant.

    @params:
        objAADShell - cmd shell object
    """

    # Check for bad token, only show users if token is available since user data is
    # retrieved at session init along with access token. If no token could be had at init,
    # then logically, the user data will not be available.
    if objAADShell.session.strAccessToken is None:
        stdout.printError('User data not available due to lack of access token.')
    elif objAADShell.session.strAccessToken is not None:
        stdout.showUserObjects(objAADShell.dictTenantUserObjs)