from src.io import stdout
from argparse import Namespace
from src.utils.argparser import ArgumentParser
from src.utils.argparser import KeyValue


# Define information dictionary about the command
dictInfo = {
    'Description': 'Display a variable amount of sign-in events for a user account',
    'Usage': 'ls upn [-n | EVENT_NUMBER, -f | filter:value]',
    'Examples': ['ls slim', 'ls slim@shady.com -n 50 -f stat:0'],
    'Positional Arguments': {
        'upn': 'User Principal Name of account to retrieve history for',
    },
    'Optional Arguments': {
        '-n': 'Number of sign-ins to retrieve from API',
        '-f': 'Filter for sign-in data. [ip, stat]'
    }

}

# Create parser object for arguments
parser = ArgumentParser("ls", dictInfo)
parser.add_argument('upn', type=str)
parser.add_argument('-n', '--eventno', metavar='100', default=20, type=int)
parser.add_argument('-f', '--filter', default=None, nargs='*', action=KeyValue)


def listSignInData(objAADShell, strArgs: str) -> None:

    """
    List a variable amount of sign-in entries for a tenant user

    @params:
        objAADShell -> cmd obj, contains attributes for command to access
        strArgs -> str, command line from stdin to parse
    """


    # Check for bad token
    if objAADShell.session.strAccessToken is None:
        stdout.printError('No access token available for API request.')
    elif objAADShell.session.strAccessToken is not None:

        # Parse the argument string into a namespace object
        objParsed = objAADShell.doParseArgs(parser, strArgs)

        # Ensure that parsed data returned a namespace object containing data retrieved from cli
        if isinstance(objParsed, Namespace):

            # Append tenant domain to upn parameter if it's not found ex: ls mirkesh
            objParsed.upn = objAADShell.buildUpn(objParsed.upn)

            # Check upn against list, show error & skip api call if user is found to be invalid
            if objParsed.upn not in objAADShell.listTenantUserUPNs:
                stdout.printError('invalid AAD user -> {}'.format(objParsed.upn))
            elif objParsed.upn in objAADShell.listTenantUserUPNs:

                # Check for the filter argument, build the filter and call the api with the filter parameter
                if objParsed.filter is not None:
                    strFilter = objAADShell.session.buildFilter(objParsed.filter)
                    dictResult = objAADShell.session.getSignIns(objParsed.upn, amount=objParsed.eventno, filter=True, _filter=strFilter)

                # Call API without filter if filter arg was not passed
                elif objParsed.filter is None:

                    # Perform API request and capture parsed results
                    dictResult = objAADShell.session.getSignIns(objParsed.upn, amount=objParsed.eventno)

                # Ensure return data is dict, Show the data returned from the result if data was returned
                if isinstance(dictResult, dict):
                    stdout.showAPIResponse(dictResult)
