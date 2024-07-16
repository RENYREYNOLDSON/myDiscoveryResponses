# Bare Minimum imports as this opens at the start
from functions import *
from tkinter import *
#This ensures that screen size recognized correctly, won't work on windows 7
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2) # your windows version should >= 8.1,it will raise exception.

class Splash(tk.CTk):
    #Constructor
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Splash Screen Title")
        
        self.overrideredirect(True)
        
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-transparentcolor", "black")

        self.image = open_splash_image()
        label = Label(self, image=self.image, bg='black')
        label.pack()
        self.eval('tk::PlaceWindow . center')

