from os import system
system("")

# Set text effects
bold = '\033[1m'
italics = '\033[3m'
underline = '\033[4m'
flash = '\033[5m'
_break = '\033[0m'

# Create colors dictionary mapping via name:ANSI Sequence
colors = {
    'green': '\033[38;2;0;255;0m',
    'red': '\033[38;2;255;0;0m',
    'blue': '\033[38;2;0;0;255m',
    'white': '\033[38;2;255;255;255m',
    'yellow': '\033[38;2;255;255;0m'
}

def addColor(color: str, string: str, stop=True) -> str:

    """
    Adds color to text via dictionary. Will either add stop code
    or not add stop code based on stop bool. Defaults to adding
    stop code.

    @params:
        color -> string, ANSI escape sequence for RGB 256
        string -> string, chars to color
        stop -> bool, defaults true, append ansi break sequence
    """

    if stop:
        return '{}{}{}'.format(colors[color], string, _break)

    elif not stop:
        return '{}{}'.format(colors[color], string)


def flowBlue(text: str) -> str:

    """
    Creates a gradient string by scaling the RGB scale per line and appending
    ANSI sequence codes for coloration based on the current line.

    @params:
        text -> str, text object to modify with color
    """

    # Create empty string
    strGradientText = ""

    # Set the green rgb value to 10
    green = 10

    # Iterate over each line in the text
    for line in text.splitlines():

        # Append the line to the text object with the ANSI codes
        strGradientText += (f"\033[38;2;0;{green};255m{line}\033[0m\n")

        # Ensure that green has not reached 255, add 15 points
        if not green == 255:
            green += 15

            # If green is greater than the RGB limit of 255, set green to 255
            if green > 255:
                green = 255

    return strGradientText
