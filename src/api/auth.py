import msal
from src.io import stdout
from requests import ConnectionError

def getAccessToken(dictDataStore: dict, tokenCache: msal.TokenCache) -> str or None:

    """
    Creates confidential client application object and retrieves bearer access token. Stores token
    in cache. When retrieving tokens, method checks cache first and then reaches out to Azure. If
    azure returns an error in the authN response, method returns None.

    dictDataStore -> dict obj, data store containing service principal information
    tokenCache -> msal.TokenCache, non-persistent cache for the access tokens
    """

    # Create static graph scope with default
    lstrGraphScope = ["https://graph.microsoft.com/.default"]

    try:

        # Create confidential client application instance
        msalConfClient = msal.ConfidentialClientApplication(dictDataStore['id'], authority=dictDataStore['auth'], client_credential=dictDataStore['secret'], token_cache=tokenCache)

        # Check for cached token, if None is returned no token was found
        dictCachedToken = msalConfClient.acquire_token_silent(lstrGraphScope, account=None)

    # Catch HTTPS errors
    except ConnectionError:
        stdout.printError('Failed to make HTTPS request, no auth token was acquired.')
        return None

    # If token was found, return the cached token
    if dictCachedToken is not None:
        stdout.printInfo('Access token was retrieved from the token cache')
        return dictCachedToken['access_token']

    # If no token found in cache, create and return new token.
    if dictCachedToken is None:

        # Capture new token response
        dictNewToken = msalConfClient.acquire_token_for_client(scopes=lstrGraphScope)

        # Check for error key in API authentication response,
        if 'error' in dictNewToken.keys():
            stdout.printError("Failed to get access token from Azure AD")
            return None

        # Check for access token in response
        elif 'access_token' in dictNewToken.keys():
            stdout.printInfo('New access token was retrieved from Azure AD')
            return dictNewToken['access_token']



