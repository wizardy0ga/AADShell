from src.io import stdout
from argparse import Namespace
from src.utils.argparser import ArgumentParser
from src.api import abuseipdb

# Command information dictionary
dictInfo = {
    "Description": 'Parse last 1000 sign-in events and retrieve unique IP\'s. Pull Abuse IP DB reports on IP addr\'s.\n\tIf reports are found on IP, reports are printed to stdout.',
    "Usage": 'reports UPN',
    "Examples": ["reports wu@tang.com"],
    'Positional Arguments': {
        'upn': 'User Principal Name of account to retrieve history for',
    },
}


# Command parser object
parser = ArgumentParser("reports", dictInfo)
parser.add_argument('upn', type=str)
parser.add_argument('-v', '--verbose', action='store_true', default=False)


def getReport(objAADShell, strArgs: str) -> None:

    """
    Retrieves IP's utilized to sign-in to user account, checks for reports within abuse ip db and prints to stdout.

    @params:
        objAADShell -> cmd obj, shell object
        strArgs -> string, passed from the CLI
    """

    # Check for bad token
    if objAADShell.session.strAccessToken is None:
        stdout.printError('No access token available for API request.')
    elif objAADShell.session.strAccessToken is not None:

        #Parse the argument string into a namespace object
        objParsed = objAADShell.doParseArgs(parser, strArgs)

        # Ensure that parsed data returned a namespace object containing data retrieved from cli
        if isinstance(objParsed, Namespace):

            # Append tenant domain to upn parameter if it's not found ex: ls mirkesh
            objParsed.upn = objAADShell.buildUpn(objParsed.upn)

            # Check upn against list, show error & skip api calls if user is found to be invalid
            if objParsed.upn not in objAADShell.listTenantUserUPNs:
                stdout.printError('invalid AAD user -> {}'.format(objParsed.upn))
            elif objParsed.upn in objAADShell.listTenantUserUPNs:

                # Get list of IP's used to sign-in to account
                listIPData = objAADShell.session.getSignInIPs(objParsed.upn)

                # Ensure that data was returned from the API call
                if isinstance(listIPData, list):

                    # Check the IP's against abuse ipdb and captures the response in list object
                    listResponseData = [abuseipdb.getAbuseDBData(objAADShell, strIP, objParsed.verbose, report_only=True) for strIP in listIPData]

                    # Capture all reports that aren't none
                    reports = [report for report in listResponseData if report is not None]

                    # If reports are available
                    if reports:

                        # Show each report that was collected
                        stdout.printInfo('Retrieved reports on addresses utilized to sign-in.')
                        for report, intIPIndex in zip(listResponseData, range(len(reports))):
                            stdout.showReport(listIPData[intIPIndex], [_report for _report in report])

                    # If no reports available, inform user
                    elif not reports:
                        stdout.printInfo('No reports found for any addresses used for authN events.')



