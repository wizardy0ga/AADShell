import requests
from json import loads


def callAPI(url: str, headers: dict, params: dict) -> dict:

    """

    Calls API w/ get request, gets data and returns it as a dictionary.

    @params:
        url -> url for api endpoint
        headers -> dict, headers for request
        params -> dict, parameters for the request body
    """

    dictRepsponse = requests.request(
        method='GET',
        url=url,
        headers=headers,
        params=params,
        verify=True
    )

    return loads(dictRepsponse.text)
