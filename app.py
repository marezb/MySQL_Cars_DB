import tkinter as tk
from tkinter import ttk
from main_window import DisplayWindow

# -- Windows only configuration --
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
# -- End Windows only configuration --


class WestCoastCars(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('West Coast Cars')

        self.geometry("1900x1000+10+20")
        self.minsize(1100, 800)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # we need to create an instance of our display window class
        self.display_window = DisplayWindow(self)
        self.display_window.grid(column=0, row=0, sticky='NSEW')

        self.button_quit = ttk.Button(self.display_window.right_side_buttons,
                                      text='Quit', command=self.destroy)
        self.button_quit.grid(column=0, row=10, pady=10, padx=15, sticky='EWS',columnspan=4)


root = WestCoastCars()


root.mainloop()
