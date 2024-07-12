# Main Imports
from objects.__modules__ import *

# FILE CLASS
############################################################################################################
# Each file is stored as one of these
class File:
    def __init__(self,name,details,req_type,reqs,master):
        self.name = req_type+" "+name.split("/")[-1][:-4]
        self.details = details
        self.req_type = req_type
        self.reqs = reqs
        self.current_req = reqs[0]
        self.master=master
        self.color=("black","white")
        self.save=""

    #Reload all objections
    def reload_objections(self):
        for req in self.reqs:
            req.reload_objections()

    # Set current file as this
    def set(self):
        self.master.set_file(self)
    # Set self.master to a value (for saving)
    def set_master(self,val):
        self.master=val
        for i in self.reqs:
            i.set_master(val)

    def on_drop(self,event):
        x,y = event.widget.winfo_pointerxy()
        try:
            target = event.widget.winfo_containing(x,y).master
            client_name = target.cget("text")
            self.master.move_file(self,client_name)
        except:
            return
        #If a button see if the name is in clients