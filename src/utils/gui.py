import tkinter as tk
from src.utils.paths import icoAadSec
from _tkinter import TclError


def getKeyFromUser() -> str and tk.Tk:

    """
    Creates GUI with entry box and button, returns input from entry box. Used
    for retrieving the decryption key from the user.
    """

    try:

        # Create canvas, window, set parameters and pack
        tkRootCanvas = tk.Tk()
        tkRootCanvas.title(13*" " + "AAD Shell")
        tkRootCanvas.iconphoto(True, tk.PhotoImage(file=icoAadSec))
        window = tk.Canvas(tkRootCanvas, width=400, height=100)
        window.pack()

        # Create a user message box
        userMessage = tk.Label(tkRootCanvas, width=50, text="Decryption key required to continue.")
        window.create_window(200, 20, window=userMessage)

        # Create input widget
        inputBox = tk.Entry(tkRootCanvas, show='*', width=48)
        window.create_window(200, 47.5, window=inputBox)

        # Create a button, set command to quit / destroy the main loop
        decryptButton = tk.Button(text='Decrypt Store', command=tkRootCanvas.quit)
        window.create_window(200, 81, window=decryptButton)

        # Run the window and return the str from the input box when the main loop is destroyed
        tkRootCanvas.mainloop()
        return inputBox.get(), tkRootCanvas

    # Catch GUI termination via X
    except TclError:
        exit(0)

    # Catch keyboard interrupt
    except KeyboardInterrupt:
        exit(0)