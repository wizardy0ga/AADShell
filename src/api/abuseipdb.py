from src.io import stdout
from src.utils.api import callAPI


def getAbuseDBData(objAADShell, strIpAddress: str, verbose, report_only=False) -> dict or None:

    """
    Retrieves data from Abuse IP DB API about the IP addr. Returns None if no data
    was retrieved from the API

    objAADShell: cmd, Calling shell object
    strIpAddress: string, IP address to check with AbDB API
    verbose: parsed arg, print additional information
    report_only: bool, only return report data rather than full data from api call
    """

    # Create return data set
    dictResponseData = {}

    # Set the URL for the IPABUSE API
    URL = 'https://api.abuseipdb.com/api/v2/check'

    # Create the query for the API
    threat_query = {
        'ipAddress': str(strIpAddress),
        'maxAgeInDays': 365,
        'verbose': 'yes'
    }

    # Set the request headers
    api_headers = {
        'Accept': 'application/json',
        'Key': objAADShell.dictAPIKeyStore["ABDB"]
    }

    # Parse JSON response, convert to dictionary object
    threat_data = callAPI(URL, api_headers, threat_query)

    # Check for error
    if 'error' in threat_data.keys():
        stdout.printError('Received error in API Call to Abuse IP DB. Error -> {}'.format(threat_data))
        return None

    # Check for successful response via data key
    elif 'data' in threat_data.keys():
        threat_data = threat_data['data']

        # Create list containing desired query data
        listDefinedData = [
                            'ipAddress',
                            'abuseConfidenceScore',
                            'countryCode',
                            'isp',
                            'domain',
                            'countryName',
                            'lastReportedAt',
                            'totalReports',
                            'reports'
                            ]

        # Check for report only kwarg, return reports if value is not 0 indicating reports are available
        if report_only is True and threat_data['totalReports'] != 0:
            return threat_data['reports']

        # Check for no reports available, return none to caller
        elif report_only is True and threat_data['totalReports'] == 0:

            # Print verbose
            if verbose is True:
                stdout.printInfo("No Abuse IP DB reports could be found for {}".format(strIpAddress))
            return None

        # Check for non report only mode
        elif not report_only:

            # Capture and return data from response
            for key, value in threat_data.items():
                if key in listDefinedData:
                    dictResponseData[key] = value


        return dictResponseData


