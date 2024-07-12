# Main Imports
from objects.__modules__ import *


# CUSTOM SMART TEXT BOX CLASS, BUILT IN SPELL CHECKER
class SmartToolTip(CustomTooltipLabel):
    #Constructor 
    def __init__(self,wraplength=400,**kwargs):
        #FRAME SETUP
        super().__init__(background="#141414",
                         foreground="white", 
                         wraplength=wraplength,
                         justify="left",
                         font=("Arial",20),
                         border=10,
                         hover_delay=600,
                         **kwargs)
