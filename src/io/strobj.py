"""
Holds constant string code
"""

from src.io.colors import *

# Set box strings ex -> [!], [+]
boxPlus = str(bold + addColor('white', '[', stop=False) + addColor('green', '+', stop=False) + addColor('white', ']'))
boxExcl = str(bold + addColor('white', '[', stop=False) + addColor('red', '!', stop=False) + addColor('white', ']'))

# Set print banners, ex -> [INFO], [ERROR]
banInfo = str(bold + addColor('white', '[', stop=False) + addColor('green', 'INFO', stop=False) + addColor('white', ']'))
banError = str(bold + addColor('white', '[', stop=False) + addColor('red', 'STDERR', stop=False) + addColor('white', ']'))
banReport = str(bold + addColor('white', '[', stop=False) + addColor('red', 'REPORT', stop=False) + addColor('white', ']'))
banVT = str(bold + addColor('white', '[', stop=False) + addColor('green', 'VIRUS TOTAL', stop=False) + addColor('white', ']'))

# Create a cursor object for the shell, ex -> AADShell@TENANT_CODE
cursor = str(bold + addColor('blue', 'AADShell', stop=False))
at = str(addColor('white', '@', stop=False))
pointer = str(addColor('white', ' >>> '))


# Set banner headers with program info
VERSION = "1.0.0"
AUTHOR = "wizardy0ga"
GITHUB = "https://github.com/wizardy0ga"
REPO = "https://github.com/wizardy0ga/AADShell"

# Create banner with formatted headers
banMain = f"""
    :::         :::     :::::::::        ::::::::  :::    ::: :::::::::: :::        :::        
  :+: :+:     :+: :+:   :+:    :+:      :+:    :+: :+:    :+: :+:        :+:        :+:        
 +:+   +:+   +:+   +:+  +:+    +:+      +:+        +:+    +:+ +:+        +:+        +:+        
+#++:++#++: +#++:++#++: +#+    +:+      +#++:++#++ +#++:++#++ +#++:++#   +#+        +#+        
+#+     +#+ +#+     +#+ +#+    +#+             +#+ +#+    +#+ +#+        +#+        +#+        
#+#     #+# #+#     #+# #+#    #+#      #+#    #+# #+#    #+# #+#        #+#        #+#        
###     ### ###     ### #########        ########  ###    ### ########## ########## ##########

==============================================================================================
[+] Version: {VERSION}
[+] Author: {AUTHOR} // {GITHUB}
[+] Repository: {REPO}
"""