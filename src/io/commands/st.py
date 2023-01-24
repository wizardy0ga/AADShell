from src.utils.argparser import ArgumentParser
from argparse import Namespace
from src.io import stdout


# Define information about the command
dictInfo = {
    'Description': 'View available tenants or switch the current working tenant',
    'Usage': 'st [[-l | -t TENANT_CODE]]',
    'Examples': ['st -l', 'st -t xyz'],
    'List Arguments': {
        '-l': 'List all tenants loaded from the store',
    },
    'Switch Arguments': {
        '-t': 'Tenant code to switch to'
    }

}

# Command parser for st command
parser = ArgumentParser("st", dictInfo)

# Create mutex group for switch and list commands
groupSwitch = parser.add_mutually_exclusive_group()
groupSwitch.add_argument('-l', '--list', action='store_true')
groupSwitch.add_argument('-t', '--tenant', metavar='TENANT_CODE', type=str)


def doSwitchTenant(objAADShell, strLine: str) -> None:

    """
    Checks arguments, lists available tenants or switches tenant depending on cli args

    @params:
        objAADShell -> cmd.Cmd, contains attributes required for "stuff"
        line -> string, line of args passed from cli
    """

    # Parse args into namespace object
    parsed = objAADShell.doParseArgs(parser, strLine)

    # Ensure that parsed var is a namespace object
    if isinstance(parsed, Namespace):

        # Check for no call to list, proceed to tenant switch function
        if not parsed.list:

            # Check for empty tenant parameter
            if parsed.tenant is None:
                stdout.printError('No tenant was provided. Use -t TENANT_CODE')

            # Check for valid object in tenant parameter
            elif parsed.tenant is not None:

                # Set uppercasing to match keys in store dictionary
                parsed.tenant = parsed.tenant.upper()

                # Check for invalid tenant code
                if parsed.tenant not in objAADShell.listAvailTenants:
                    stdout.printError('invalid tenant -> {}. Directory remains on {}'.format(parsed.tenant, objAADShell.strCurrTenant))

                # Check for switching to CWT
                elif parsed.tenant == objAADShell.strCurrTenant:
                    stdout.printError('Current working tenant is already {}'.format(parsed.tenant))

                # Check for valid tenant code
                elif parsed.tenant in objAADShell.listAvailTenants:

                    # Delete the current session object
                    del objAADShell.session

                    # Set the current tenant to the validated argument and create a new session
                    objAADShell.strCurrTenant = parsed.tenant
                    objAADShell.initSession()

        # Check for list arg, list all available tenants.
        elif parsed.list is True:
            stdout.showTenantDir(objAADShell.dictDataStore)
