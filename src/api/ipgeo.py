from src.io import stdout
from src.utils.api import callAPI


def getIPGeoResponse(objAADShell, strIPaddr: str) -> dict or None:

    """
    Method will capture location data about the IP. Method returns none if no data is retrieved for any reason.

    @params:
        objAADShell -> Cmd, shell obj containing attribs required for method
        strIPaddr - str obj repr ip addr to check
    """

    # Create array with data to pull from the api response
    desired_data = [
        'ip',
        'continent_name',
        'country_name',
        'state_prov',
        'district',
        'city',
        'organization',
        'isp'
    ]

    dictAPIResponse = {}

    # Perform API call, capture object
    URL = 'https://api.ipgeolocation.io/ipgeo?apiKey={}&ip={}'.format(objAADShell.dictAPIKeyStore["IPGEO"], strIPaddr)
    response = callAPI(URL, {}, {})

    # If there's a message key in the dict, something has gone wrong
    if 'message' in response.keys():
        stdout.printError('Could not get location data for {}. Reason: {}'.format(strIPaddr, response['message']))
        return None

    # Else, print the data to stdout
    else:

        # Iterate over all items in the response, find the ones we want
        # and add them to the return dictionary in form header:response
        for key, data in response.items():
            if key in desired_data:
                dictAPIResponse[key] = data

        return dictAPIResponse
