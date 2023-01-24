from cmd import Cmd
from src.api.session import Session
from src.io import stdout
from src.io import strobj
from msal import TokenCache
from src.io import commands
from src.utils.argparser import ArgumentParser
import os

class AADShell(Cmd):

    """
    Main command shell that the user lives in throughout runtime.

    @params:
        dataStore: dict, contains tenant information required to access graph API
        keyStore: dict, contains API keys for API's other than graph
    """

    # Show banner when user drops into shell
    intro = strobj.flowBlue(strobj.banMain)

    # Create command dictionary in format {commmand: description}
    dictCommands = {
        'ls': 'List variable amount of sign-in entries for user. Defaults to 20 if report amount not specified.',
        'st ': 'Switch the current working tenant directory or view available tenant directories.',
        'users': 'Show all users by display name and user principal name in the current working tenant directory.',
        'reports': 'Retrieve IP\'s utilized to authN to account, retrieve reports on IP\'s from Abuse IP DB API.',
        'scan': 'Retrieve IP\'s, process them through various API\'s and determine risky sign-ins.',
    }

    def __init__(self, dataStore: dict, keyStore: dict):

        super(AADShell, self).__init__()
        self.session = None                                         # Session object for interacting with API
        self.dictTenantUserObjs = None                              # Tenant user dictionary in {displayname:userprincipalname}
        self.listTenantUserUPNs = None                              # List of users by upn
        self.dictAPIKeyStore = keyStore                             # API Keys for API's other than graph
        self.dictDataStore = dataStore                              # Storage for API authN data
        self.strCurrTenant = ''                                     # The tenant code for the current working tenant
        self.strTenantDomain = None                                 # Domain string for tenant in format @company.com
        self.listAvailTenants = [key for key in dataStore.keys()]   # List available tenants from the data store
        self.objAccessTokenCache = TokenCache()                     # Root token cache to store non-persistent tokens in
        self.nohelp = 'Unknown syntax -> {}'                        # Over-ride error message on unknown command

        self.initSession()


    def getCursorString(self) -> str:

        """
        Creates a formatted cursor with the current tenants code appended
        """

        return '\n' + strobj.cursor + strobj.at + strobj.addColor('yellow', self.strCurrTenant.upper(), stop=False) + strobj.pointer


    def initSession(self) -> None:

        """
        Creates a new AAD session object under the specified tenant changes the shell prompt to reflect the current
        tenant, gets all users from the directory and sets the tenants current domain from the data in the store
        """

        # Set the tenant domain and create a session object for tenant
        self.strTenantDomain = self.dictDataStore[self.strCurrTenant]['domain']
        self.session = Session(self.dictDataStore, self.strCurrTenant, self.objAccessTokenCache)

        # Check for invalid session token before calling API
        if self.session.strAccessToken is None:
            stdout.printError('Failed to initialize session. No access token available. Quitting...')
            exit(0)
        elif self.session.strAccessToken is not None:

            # Get all users from API call and populate data
            self.dictTenantUserObjs = self.session.getAllUsers()
            self.listTenantUserUPNs = [upn for _, upn in self.dictTenantUserObjs.items()]

            # Format the prompt
            self.prompt = self.getCursorString()


    def buildUpn(self, upn: str) -> str:

        """
        Adds tenant domain to UPN if domain isn't present. Allows user to pass username rather
        than full upn, ex -> ls smith // ls sglemons@corporation.com

        @params:
            upn -> str, user principal name
        """

        # Append tenant domain to upn parameter if it's not found ex: ls mirkesh
        if self.strTenantDomain.replace('@', '') not in upn.split('@'):
            upn += self.strTenantDomain
        return upn


    def doParseArgs(self, parser: ArgumentParser, line: str):

        """
        Method attempts to parse arguments with parser object. Returns Namespace obj containing args
        if parsing is successful. If parser calls sysexit, returns line parameter.

        @params:
            parser -> argparser object, command parser for the command
            line -> str, line to parse.
        """
        try:
            # Attempt to return Namespace object from argparse
            return parser.parse_args(line.split())

        # Catch attrib error from argparse error over-ride so program doesn't quit on bad error. Return the raw line
        except AttributeError:
            return line


    # List sign-ins command
    def help_ls(self) -> None: commands.ls.parser.print_help()
    def do_ls(self, args: str) -> None: commands.ls.listSignInData(self, args)

    # Switch tenant command
    def help_st(self): commands.st.parser.print_help()
    def do_st(self, line: str) -> None: commands.st.doSwitchTenant(self, line)

    # Users command
    def help_users(self) -> None: commands.users.parser.print_help()
    def do_users(self, null: None) -> None: commands.users.showUsers(self)

    # reports command
    def do_reports(self, line: str) -> None: commands.reports.getReport(self, line)
    def help_reports(self) -> None: commands.reports.parser.print_help()

    # Scan command
    def do_scan(self, line: str) -> None: commands.scan.scanUpn(self, line)
    def help_scan(self) -> None: commands.scan.parser.print_help()

    # Exit command
    def do_exit(self, null: None) -> exit: stdout.printInfo('User called exit.');exit(0)

    # Clear command
    def do_clear(self, null: None) -> None:

        """
        Checks for windows or nix, sets the command and clears the terminal.
        """

        if os.name == 'nt':
            cmd = 'cls'
        elif os.name == 'posix':
            cmd = 'clear'
        os.system(cmd)

    # Over-ride syntax error
    def default(self, line: str) -> None: stdout.printError(self.nohelp.format(line))


    def do_help(self, arg):

        """
        Over-ride method for customized global help printing
        """

        if arg:
            try:
                getattr(self, 'help_' + arg)()
            except AttributeError:
                stdout.printError(self.nohelp.format(arg))

        elif not arg:
            self.stdout.write("%s\n"%str(self.doc_leader))
            stdout.showCommands(self.dictCommands)
