from src.io import stdout
from argparse import Namespace
from src.utils.argparser import ArgumentParser
from src.api.abuseipdb import getAbuseDBData
from src.api.virustotal import getVTResponse
from src.api.ipgeo import getIPGeoResponse


# Define information dictionary about the command
dictInfo = {
    'Description': 'Capture the last 1000 sign-in events. Parse out unique IP\'s and check against Abuse IP DB, Virus Total and IP Geolocation.\n\tIf suspicious sign-ins are found, retrieve all sign-in events with those suspicious IP\'s.',
    'Usage': 'scan upn [-v | -s | -su]',
    'Examples': ['scan slim@shady.com', 'scan slick@rick.com -s -v'],
    'Positional Arguments': {
        'upn': 'User Principal Name of account to scan',
    },
    'Optional Arguments': {
        '-v': 'Enable verbose output',
        '-s': 'Enable sensitive mode. Mark IP\'s that have reports but contain abuse confidence score of 0.',
        '-su': 'Only retrieve successful sign-ins from risky addresses'
    }

}
# Create parser information
parser = ArgumentParser("scan", dictInfo)
parser.add_argument('upn', type=str)
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-s', '--sensitive', action='store_true', default=False)
parser.add_argument('-su', '--success', action='store_true', default=False)


def scanUpn(objAADShell, strCommandLine: str) -> None:

    """
    Retrieves all IP's utilized to create sign-in entries into an account. Runs IP's through Abuse IP DB, IP Geo locate
    and Virus total API's. Define malicious IP's by report count and / or abuse score from abuse ip db. Proceed to locate
    all sign-in events using malicious IP's and print data to stdout.

    @params:
        objAADShell -> cmd shell object
        strCommandLine -> string, args passed from cli
    """

    # Check for bad token
    if objAADShell.session.strAccessToken is None:
        stdout.printError('No access token available for API request.')
    elif objAADShell.session.strAccessToken is not None:

        # Parse the argument string into a namespace object
        objParsed = objAADShell.doParseArgs(parser, strCommandLine)

        # Ensure that parsed data returned a namespace object containing data retrieved from cli
        if isinstance(objParsed, Namespace):

            # Append tenant domain to upn parameter if it's not found ex: ls mirkesh
            objParsed.upn = objAADShell.buildUpn(objParsed.upn)

            # Check upn against list, show error & skip api call if user is found to be invalid
            if objParsed.upn not in objAADShell.listTenantUserUPNs:
                stdout.printError('invalid AAD user -> {}'.format(objParsed.upn))
            elif objParsed.upn in objAADShell.listTenantUserUPNs:

                # Capture a list of abusedb responses from the IP's utilized to sign-in to the account,
                # display responses to stdout
                listIPs = objAADShell.session.getSignInIPs(objParsed.upn)

                # Validate the list object returned from the getSignInIps Call
                if isinstance(listIPs, list):

                    stdout.printInfo('Gathering data on {} addresses from Abuse IP DB API...'.format(str(len(listIPs))))
                    listABDBResponse = [getAbuseDBData(objAADShell, strIP, objParsed.verbose) for strIP in listIPs]

                    # Show abuse IP DB response and IP Geo Locate response
                    stdout.showABDBResponse(listABDBResponse)
                    stdout.printInfo('Querying IP Geolocate API...')
                    stdout.showIPGeoResponse([getIPGeoResponse(objAADShell, strIP) for strIP in listIPs])

                    # Capture potentially malicious IP's for further analysis. Show report if verbose
                    listMarked = []
                    for dictReport in listABDBResponse:

                        # If not sensitive, mark IPs that have reports and an Abuse Confidence Score greater than 0
                        if not objParsed.sensitive:
                            if dictReport['totalReports'] != 0 and dictReport['abuseConfidenceScore'] > 0:
                                listMarked.append(dictReport['ipAddress'])
                                if objParsed.verbose:
                                    stdout.showReport(dictReport['ipAddress'], dictReport['reports'])

                        # If sensitive, append IP's with reports OR score greater than 0
                        elif objParsed.sensitive:
                            if dictReport['totalReports'] != 0 or dictReport['abuseConfidenceScore'] > 0:
                                listMarked.append(dictReport['ipAddress'])
                                if objParsed.verbose and dictReport['totalReports'] != 0:
                                    stdout.showReport(dictReport['ipAddress'], dictReport['reports'])


                    # Run IP's through virus total
                    stdout.printInfo('Checking {} addresses against Virus Total'.format(len(listIPs)))
                    for strIP in listIPs:

                        # Capture the Virus total response, ensure call returned dictionary
                        dictVTResponse = getVTResponse(objAADShell, strIP)
                        if isinstance(dictVTResponse, dict):
                            stdout.showVTResponse(dictVTResponse, objParsed.verbose, strIP)

                    # If the list has been populated with Risky IP's, retrieve sign-ins with those IP's
                    if listMarked:
                        stdout.printInfo('Gathering logs for sign-ins determined to have come from risky hosts...')
                        for strIP in listMarked:

                            # Check for success argument, create filter accordingly
                            if objParsed.success:
                                dictFilter = {'ip': strIP, 'stat':'0'}
                            elif not objParsed.success:
                                dictFilter = {'ip': strIP}

                            # Format filter, print info, call api and show response
                            filter = objAADShell.session.buildFilter(dictFilter)
                            stdout.printInfo('Display sign-ins for risky address @ {}'.format(strIP))
                            stdout.showAPIResponse(objAADShell.session.getSignIns(objParsed.upn, filter=True, _filter=filter))

                        # Show location data for addresses determined to be risky
                        stdout.printInfo('Gathering location data for risky addresses...')
                        stdout.showIPGeoResponse([getIPGeoResponse(objAADShell, strIP) for strIP in listMarked])

                    # Notify user if no sign-ins were determined to be risky
                    elif not listMarked:
                        stdout.printInfo('No sign-ins were determined to be risky.')


