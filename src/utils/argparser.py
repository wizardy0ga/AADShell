from src.io import colors
import argparse
from src.io import stdout


class KeyValue(argparse.Action):

    """
    Custom argparse action object. Allows user to pass dictionary of arguments in format {arg1:value1, arg2:value2,*}
    within argument that has its action set to this class

    @params:
        parser: ArgumentParser, contains the action for this call
        namespace: Namespace obj, contains all arguments after parsing
        values: list, contains all values received from argument with this action assigned
    """

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: list, option_string=None):

        # Set the name space objects dest to a dict obj
        setattr(namespace, self.dest, dict())

        # Create splitter object
        split = ':'

        try:
            # Iterate over the items that were receieved in the argument
            for item in values:

                # Split the pairs into keys and values by the split var
                key, value = item.split(split)

                # Get the namespace dest and set the dictionary to the key/value pair
                getattr(namespace, self.dest)[key] = value

        # Throw error on invalid split object
        except ValueError:
            stdout.printError('Invalid split. Use ":". Example -f ip:127.0.0.1')


class ArgumentParser(argparse.ArgumentParser):

    """
    Sub-class for argument parser object to over-ride the print help command with our own as it allows
    for more control over formatting of the help data.

    @params:
        prog -> name of the command to show in argparse based usage string
        argDict -> dictionary containing info about the command on AADShell side of things.
    """


    def __init__(self, prog, argDict):
        super(ArgumentParser, self).__init__(prog=prog)
        self.dictArguments = argDict


    def print_help(self) -> None:

        """
        Over-ride function for print_help to allow ease of formatting output with colors

        @params:
            dictArgs -> dict, contains information about the command
        """

        # For each item in the dictionary
        for key, value in self.dictArguments.items():

            # Print the key as this will be the header for the entry
            print('\n{}\n'.format(colors.bold + colors.addColor('green', key + ':')))

            # If the value is a string, it's either usage or description. Print.
            if isinstance(value, str):
                print('\t{}'.format(colors.bold + colors.addColor('white', value)))

            # If list, data will be usage examples. Iterate & print
            elif isinstance(value, list):
                for strUsage in value:
                    print('\t{}'.format(colors.bold + colors.addColor('white', strUsage)))

            # If dict, will be positional or optional args. Iterate and print.
            elif isinstance(value, dict):
                for arg, help in value.items():
                    print('\t{:<30} || {:<10}'.format(colors.bold + colors.addColor('yellow', arg), colors.bold + colors.addColor('white', help)))


    def error(self, message: str):

        """
        Over-ride for error message function

        @params:
            message -> str, error to print
        """

        # Create and print error message
        error = 'Usage:' + '\t{}\n'.format(self.dictArguments['Usage']) + '\t\t{}\n'.format(message)
        stdout.printError(error)

        # Raise attribute error. OG Docstring says error must not return and must raise error instead.
        raise AttributeError