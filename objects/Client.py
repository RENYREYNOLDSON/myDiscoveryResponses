# IMPORTS
from functions import *

# CLIENT CLASS
############################################################################################################
class Client:
    # Constructor 
    def __init__(self,name,files,master):
        self.name=name
        self.master=master
        self.files=files
        self.color=("black","white")
        if len(files)>0:
            self.current_file = files[0]
        else:
            self.current_file=""
        self.save=""
        self.saved=False
        #Each client keeps it's own editable firm details
        self.firm_details=get_firm_details()
    # Set the current client to self
    def set(self):
        self.master.set_client(self)
    # Set self.master to a value (for saving)
    def set_master(self,val):
        self.master=val
        for i in self.files:#Remove master from all of the sub objects etc
            i.set_master(val)