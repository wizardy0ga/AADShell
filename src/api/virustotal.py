from src.utils.api import callAPI
from src.io import stdout


def getVTResponse(objAADShell, strIP: str) -> dict or None:

    """
    Method will retrieve data from the VirusTotal API. Returns None if no data was received for any reason.

    @params:
        ip_address -> str obj repr IP addr to scan
    """

    # Create dictionary object with empty list in result key
    dictReturnData = {}
    dictReturnData['result'] = []

    # Set API URL for Virus Total
    URL = 'https://www.virustotal.com/api/v3/ip_addresses/{}'.format(strIP)

    # Create a query for an IP address report
    api_query = {
        'ip': strIP
    }

    # Set request headers with api key
    request_headers = {
        'x-apikey': objAADShell.dictAPIKeyStore["VTDB"]
    }

    # Create a dictionary object with the threat data received from the api call function
    threat_data = callAPI(URL, request_headers, api_query)

    # Check for error or successful response. Return none on error
    if 'error' in threat_data.keys():
        stdout.printError('Error was returned from Virus Total API Call. Error: {}'.format(threat_data['error']['code']))
        return None

    # Set the threat data var to the portion of the response containing the data about the threat
    elif 'data' in threat_data.keys():
        threat_data = threat_data['data']['attributes']


    # Create a list of unwanted results from the query
    unwanted_results = ['timeout', 'clean', 'undetected', 'unrated']

    # Capture the number of times the IP address was reported with each status
    analysis_stats = threat_data['last_analysis_stats'].items()

    # iterate over API response
    for key, value in analysis_stats:

        # if the key is not unwanted and contains reports
        if key not in unwanted_results and value != 0:
            dictReturnData['result'].append([key, value])

    # Capture the reputation objects by vendor
    vendor_reputations = threat_data['last_analysis_results'].items()

    # Iterate over each scan performed per vendor, print to terminal
    for vendor_name, vendor_result in vendor_reputations:

        # Check for wanted result, add to dict with vendor name as key, finding as value
        if vendor_result['result'] not in unwanted_results:
            dictReturnData[vendor_name] = vendor_result

    return dictReturnData

