from prettytable.colortable import ColorTable, Theme
from src.io import strobj

# Simple Theme for pretty table
simple = Theme()
simple.default_color = strobj.bold + strobj.colors['white']
simple.vertical_char = ''
simple.horizontal_char = '─'
simple.junction_char = ''

# Box theme for pretty table
box = Theme()
box.default_color = strobj.bold + strobj.colors['blue']
box.vertical_char = strobj.bold + strobj.colors['blue'] + '|'
box.horizontal_char = strobj.bold + strobj.colors['blue'] + '-'
box.junction_char = strobj.bold + strobj.colors['blue'] + '+'


def showCommands(data: dict) -> None:

    """
    Display all available commands for AAD Shell

    @params:
        data: dictionary, contains information about the commands for the shell
    """

    # Create table object and populate with command data
    table = ColorTable(theme=simple, align='l')
    table.field_names = [strobj.addColor('yellow', "Command"), strobj.addColor('yellow', "Description")]
    table.add_rows([[strobj.addColor('green', comm), strobj.addColor('white', desc)] for comm, desc in data.items()])

    # Print and delete the table
    print(table.get_string())
    del table


def showTenantDir(data: dict) -> None:

    """
    Displays all tenant codes & names that were loaded from the data store

    @params
        data -> dictionary, contains
    """

    # Create table
    table = ColorTable(theme=box)

    # Populate data
    table.field_names = [strobj.addColor('green', "Tenant Code"), strobj.addColor('green', "Tenant Name")]
    table.add_rows([[strobj.addColor('yellow', key), strobj.addColor('yellow', dictValue['name'])] for key, dictValue in data.items()])

    # Print table
    print(table.get_string())
    del table


def showUserObjects(data: dict) -> None:

    """
    Displays user objects in current working tenant directory

    @params:
        data -> dictionary object, contains users by dn/upn
    """

    # Create table object, populate the column names
    table = ColorTable(theme=box)
    table.field_names = [strobj.addColor('green', "Display Name"), strobj.addColor('green', "User Principal Name")]

    # Iterate over display and user principal names in the dict, add rows for each
    for dn, upn in data.items():
        table.add_row([strobj.addColor('yellow', dn), strobj.addColor('yellow', upn)])

    # Print the table to stdout
    print(table.get_string())
    del table


def showABDBResponse(data: list) -> None:

    """
    Displays information received from abuse ip db.

    @params;
        data -> list, contains a list of dictionaries that were retrieved from the API.
    """

    # Create table and list object
    table = ColorTable(theme=simple)
    listRowData = []

    # Validate the first index as a dict
    if isinstance(data[0], dict):

        # Set the field names
        table.field_names = [strobj.addColor('green', name) for name in data[0].keys() if 'reports' not in name]

        # Loop through response, capture applicable data and append to table
        for response in data:
            listRowData.append([strobj.addColor('white', _data) for _, _data in response.items() if 'reports' not in _])

        # Add rows, print and delete table
        table.add_rows(listRowData)
        print(table.get_string())
        del table


def showIPGeoResponse(data: list) -> None:

    """
    Displays information received from IP Geo Locate

    @params:
        data -> list, contains dictionaries with data from the API
    """

    # Create a table, empty list
    table = ColorTable(theme=simple)
    listRowData = []

    # Validate the first index as a dict
    if isinstance(data[0], dict):

        # Add field names to table
        table.field_names = [strobj.addColor('green', name) for name in data[0].keys()]

        # Loop and append data to rows
        for response in data:
            listRowData.append([strobj.addColor('yellow', _data) for _, _data in response.items()])

        # Add Rows, print and delete table
        table.add_rows(listRowData)
        print(table.get_string())
        del table


def showAPIResponse(data: dict) -> None:

    """
    Displays table populated with data from the dictionary that. Dictionary
    is intended to be received from a listSignIns API response that has
    been stripped down to only defined entries

    @params:
        data -> dictionary, intended to be parsed response from graph API
    """

    # Create table object and empty list obj
    table = ColorTable(theme=simple)
    listRowData = []

    # Validate the first index as a dict
    if isinstance(data[0], dict):

        # Populate the field names for the table with the first entry in the dict
        # these will be static
        table.field_names = [strobj.addColor('yellow', key) for key in data[0].keys()]

        # Iterate over the sign-in events and append the corresponding values
        # per each key in the sign-in event.
        for _, dictSignInEvent in data.items():
            listRowData.append([strobj.addColor('green', data) for _, data in dictSignInEvent.items()])

        # Add the rows to the table and print to stdout
        table.add_rows(listRowData)
        print(table.get_string())
        del table


def showReport(ipaddr: str, reports: list) -> None:

    """
    Prints report data to screen
    """
    print('\n')
    printInfo('Reports found for {}'.format(ipaddr))

    for dictReport in reports:
        printReport(dictReport['reportedAt'], dictReport['comment'])

    print('\n')


def showVTResponse(data: dict, verbose: bool, strIP: str) -> None:

    """
    Show response from Virus Total

    @params;
        data -> dict, contains response from virus total
        verbose -> parsed arg bool, print extra information
        strIP -> IP address that was scanned
    """

    # Iterate over results
    for result in data['result']:

        # Only print results other than harmless unless verbose was invoked
        if result[0] == 'harmless' and verbose is True:
            printVTResponse(strobj.bold + strobj.addColor('white','{} vendors reported {} as {}.').format(result[1], strIP, result[0]))
        elif result[0] != 'harmless':
            printVTResponse(strobj.bold + strobj.addColor('white', '{} vendors reported {} as {}.').format(result[1], strIP, result[0]))


def printVTResponse(response: str) -> None:

    """
    Print function for virus total response

    @params:
        response: -> API Response data from Virus Total
    """

    print('{} {} {}'.format(strobj.boxPlus, strobj.banVT, response))


def printReport(time: str, report: str) -> None:

    """
    Prints reports from abuse IP db to screen.

    @params:
        time -> str, time report was reported at
        report -> str, report data from API
    """

    print('{} {} :: [Time: {}]\n{}'.format(strobj.boxExcl, strobj.banReport, strobj.addColor('yellow', time), strobj.addColor('red', report)))


def printError(error: str) -> None:

    """
    Display error information to stdout

    @params:
        error -> str, error to print
    """

    print('{} {} -> {}'.format(strobj.boxExcl, strobj.banError, strobj.bold + strobj.addColor('yellow', error)))


def printInfo(info: str) -> None:

    """
    Display information to user via stdout

    @params:
        info -> str, information to print to stdout
    """

    print('{} {} -> {}'.format(strobj.boxPlus, strobj.banInfo, strobj.bold + strobj.addColor('white', info)))
