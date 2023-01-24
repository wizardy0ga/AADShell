import msal

from src.api import auth
from requests import get, ConnectionError
from src.io import stdout


class Session(object):

    """
    Represents an authenticated session under a specific tenant. Contains methods for interacting
    with the graph API under the authenticated session.

    @params:
        dataStore: dict object, contains all client/app data for graph API
        strCurrentTenant: str, the string for the current tenant, represented as tenant code
        tokenCache: msal.TokenCache object, client side token cache to store the access tokens
    """

    # Define graph API endpoint URLs
    endpoints = {
        'signin': 'https://graph.microsoft.com/v1.0/auditLogs/signIns?$top={}&$filter=userPrincipalName eq \'{}\'',
        'filter': 'https://graph.microsoft.com/v1.0/auditLogs/signIns?$top={}&$filter=userPrincipalName eq \'{}\'{}',
        'users': 'https://graph.microsoft.com/v1.0/users'
    }

    # Desired main keys in API response
    listDefinedKeys = [
        'createdDateTime',
        'userDisplayName',
        'clientAppUsed',
        'appDisplayName',
        'deviceDetail',
        'correlationId',
        'location',
        'ipAddress',
        'status',
    ]
    # OLD KEYS, not in use right now. To be put into use at a later time
    # 'id',
    # 'conditionalAccessStatus',

    # Desired sub keys for main keys with dictionary values in API Response
    listSubKeys = [
        'errorCode',
        'state',
        'countryOrRegion',
        'deviceId',
        'displayName',
        'operatingSystem',
        'browser'
    ]

    # Authentication code dictionary for status of sign-in
    dictAuthCodes = {
        0: 'Success',
        50126: 'Bad user/pass',
        50053: 'Lockout'
    }

    # Filter dictionary for graph API
    dictFilters = {
        'ip': 'ipAddress',
        'stat': 'status/errorcode'
    }


    def __init__(self, dataStore: dict, currentTenant: str, tokenCache: msal.TokenCache):

        # Get tenant data from the store
        self.dictDataStore = dataStore[currentTenant]

        # Capture the access token
        self.strAccessToken = auth.getAccessToken(self.dictDataStore, tokenCache)

        # If the session token is valid
        if self.strAccessToken is not None:

            # Create headers dict with auth token
            self.headers = {'Authorization': self.strAccessToken}
            stdout.printInfo('New session initialized for tenant -> {}'.format(self.dictDataStore['name']))


    def buildFilter(self, dictFilterKeys: dict) -> str:

        """
        Builds a filter based on arguments and returns it as string for appending to API endpoint url prior to call.

        @params:
            dictFilterKeys -> dict, contains key:value mapping for filter to convert. {filter:filteredValue}
        """

        # Create empty filter var, iterate over the filters dict
        strFilter = ''
        for key, filter in self.dictFilters.items():

            # Validate the parameter, begin key iteration
            if isinstance(dictFilterKeys, dict):
                if key in dictFilterKeys.keys():

                    # Check for status key, remove quotes as data type must be int.
                    if key == 'stat':
                        strFilter += " and {} eq {}".format(filter, dictFilterKeys[key])
                    else:
                        strFilter += " and {} eq '{}'".format(filter, dictFilterKeys[key])

        # Return the filter
        return strFilter


    def getAllUsers(self) -> dict:

        """
        Captures all users in tenant directory, returns users as dict obj with structure:
            {displayName: UserPrincipalName}
        """

        stdout.printInfo('Fetching users for tenant -> {}'.format(self.dictDataStore['name']))

        # Create empty dict and perform API request
        users = {}
        listAPIResponse = dict(get(url=self.endpoints['users'], verify=True, headers=self.headers).json())['value']

        # Parse out each user obj as dict in response, append display name & user principal name per user to users dict
        for dictUser in listAPIResponse:
            users[dictUser['displayName']] = dictUser['userPrincipalName']

        # Return the dictionary
        return users


    def parseResponse(self, dictAPIResponse: dict) -> dict:

        """
        Parses out graph API response and returns only desired data from response as dictionary

        @params:
            dictAPIResponse: dictionary, contains data from the graph API response to parse out
        """

        dictSignInData = {}

        # Iterate over the API response. Set ID number for each sign-in event. In the response, every sign-in event
        # is a nested dictionary.
        for dictSignInEvent, intID in zip(dictAPIResponse, range(len(dictAPIResponse))):

            # Create sub-dictionary based on sign-in ID counter
            dictSignInData[intID] = {}

            # Iterate over the data inside the sign-in event, locate keys that are defined
            for key, value in dictSignInEvent.items():

                # Skip over non-interactive sign-ins for now. The option to allow interactive sign-ins
                # will be added as an argument at a later date
                if dictSignInEvent['isInteractive'] is not True:
                    pass
                elif dictSignInEvent['isInteractive'] is True:
                    if key in self.listDefinedKeys:

                        # Check for values that are dictionaries with further data, iterate and append to sign-in data dict
                        if isinstance(value, dict):
                            for _key, _value in value.items():
                                if _key in self.listSubKeys:

                                    # Check for status key error code and convert the code int to string from dict. Defaults
                                    # to int code if value is not defined
                                    if _key == 'errorCode':
                                        if _value not in self.dictAuthCodes.keys():
                                            dictSignInData[intID]['Status'] = str(_value)
                                        elif _value in self.dictAuthCodes.keys():
                                            dictSignInData[intID]['Status'] = self.dictAuthCodes[_value]

                                    # Key is not an error code. No str converstion required. Append to dict.
                                    else:
                                        dictSignInData[intID][_key] = _value

                        # Value is string, not dict. Add key and value to the current sign-in event
                        else:
                            dictSignInData[intID][key] = value

        # Return the sign-in data retrieved from the request
        return dictSignInData


    def getSignIns(self, strUpn: str, filter=False, _filter=None, amount='1000') -> dict or None:

        """
        Performs get request on the sign-in API end-point, captures user
        sign-in set and returns it as dictionary. Returns none if no data was retrieved

        https://learn.microsoft.com/en-us/graph/api/signin-list?view=graph-rest-1.0&tabs=http

        @params:
            amount: str int, the amount of sign-ins to pull
            filter: str, filter for the API endpoint to retrieve data with

        Return dict Data Struct

        {
            Event_ID : {
                Key: Value
                ip:   127.0.0.1
                etc:
            }
        }
        """

        # Check for filter parameter. Call API with filter or no filter based on bool.
        try:
            if filter is True:
                dictAPIResponse = dict(get(url=self.endpoints['filter'].format(amount, strUpn, _filter), verify=True, headers=self.headers).json())
            elif not filter:
                dictAPIResponse = dict(get(url=self.endpoints['signin'].format(amount, strUpn), verify=True, headers=self.headers).json())

        # Catch connection error
        except ConnectionError:
            stdout.printError('Failed to make HTTPS call to MS Graph API')
            return None

        # Check for empty response or error in response, return None
        if 'error' in dictAPIResponse.keys() or dictAPIResponse['value'] == []:
            stdout.printError('No data was returned from the request. Code: {}. Message: {}.'.format(dictAPIResponse['error']['code'], dictAPIResponse['error']['message']))
            return None

        # Check for value key w/ sign-in data in response, ensure value isn't empty list
        elif 'value' in dictAPIResponse.keys() and dictAPIResponse['value'] is not []:

            # Return parsed data dictionary
            return self.parseResponse(dictAPIResponse['value'])


    def getSignInIPs(self, strUpn: str) -> list or None:

        """
        Checks the last 1000 sign-ins for the user, retrieves the IP addresses
        and returns the IP's that were found, ensuring that no matching IP's are
        returned.
        """

        # Get sign-in data for user. Pull last 1000 reports, max amount allowed by $top query param
        dictIPData = self.getSignIns(strUpn)

        # Check for no response, proceed accordingly
        if dictIPData is None:
            return None
        elif dictIPData is not None:

            # Create local list
            listIPData = []

            # iterate over the sign-in events
            for event, dictSignInData in dictIPData.items():

                # If IP hasn't already been appended, append the IP.
                if dictSignInData['ipAddress'] not in listIPData:
                    listIPData.append(dictSignInData['ipAddress'])

            stdout.printInfo('Retrieved {} sign-in events. {} IP\'s were used to create these events.'.format(str(len(dictIPData)), str(len(listIPData))))

            # Return the list of IP's
            return listIPData


