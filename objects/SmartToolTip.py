# Main Imports
from objects.__modules__ import *


# CUSTOM SMART TEXT BOX CLASS, BUILT IN SPELL CHECKER
class SmartToolTip(CustomTooltipLabel):
    #Constructor 
    def __init__(self,wraplength=400,**kwargs):
        #FRAME SETUP
        super().__init__(background="black",
                         foreground="white", 
                         wraplength=wraplength,
                         justify="left",
                         font=("Arial",10),
                         border=10,
                         hover_delay=600,
                         **kwargs)

# CUSTOM SMART TEXT BOX CLASS, BUILT IN SPELL CHECKER
class SmartToolTipWarning(CustomTooltipLabel):
    #Constructor 
    def __init__(self,wraplength=400,**kwargs):
        #FRAME SETUP
        super().__init__(background="black",
                         foreground="white", 
                         wraplength=wraplength,
                         justify="left",
                         font=("Arial",10),
                         border=10,
                         hover_delay=0,
                         **kwargs)