# Main Imports
from objects.__modules__ import *
from functions import *

# OBJECTION CLASS
############################################################################################################
# Class for each objection for each response
class Objection:
    def __init__(self,key,master):
        self.key=key
        self.master=master
        self.selected=False
        self.param=""
        self.additional_param=""

        self.need_param = ("[VAR]" in self.master.objections[key][0])
        self.need_additional_param = ("[VAR]" in self.master.objections[key][1])

        #Store this for writing objections
        self.additional_text=self.master.objections[key][1]
        self.alter_scope=self.master.objections[key][2]
        self.autofill=self.master.objections[key][3]

    # Set self.master to a value (for saving)
    def set_master(self,val):
        self.master=val


    #Toggle if this objection is selected
    def toggle(self):
        self.selected = not self.selected