# IMPORTS
from functions import *

# FILE CLASS
############################################################################################################
# Each file is stored as one of these
class File:
    def __init__(self,name,details,req_type,reqs,master):
        self.name = name.split("/")[-1][:-4]
        self.details = details
        self.req_type = req_type
        self.reqs = reqs
        self.current_req = reqs[0]
        self.master=master
        self.color=("black","white")
        self.save=""
    # Set current file as this
    def set(self):
        self.master.set_file(self)
    # Set self.master to a value (for saving)
    def set_master(self,val):
        self.master=val
        for i in self.reqs:
            i.master=val#Remove master from all of the sub objects etc
            for i2 in i.opts:
                i2.master=val
    def on_drop(self,event):
        x,y = event.widget.winfo_pointerxy()
        try:
            target = event.widget.winfo_containing(x,y).master
            client_name = target.cget("text")
            self.master.move_file(self,client_name)
        except:
            return
        #If a button see if the name is in clients