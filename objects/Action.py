# IMPORTS
from functions import *

# CLIENT CLASS
############################################################################################################

class Action:
    def __init__(self,master,client,obj):
        self.master = master
        self.client = client
        self.file = client.current_file
        self.req = self.file.current_req
        self.obj = obj

    def undo(self):
        if self.master.current_req!=self.req:
            self.master.set_client(self.client)
            self.master.set_file(self.file)
            self.master.set_request(self.req)

        self.master.toggle_objection(self.obj,undo_command=True)

    def redo(self):
        self.undo()###### TURN THIS INTO A NICE BASE CLASS TO BASE THE OTHERS OFF OF, THIS METHOD WILL WORK WELL!


class ActionToggleObjection(Action):
    def __init__(self,master,client,file,req,obj):
        self.master = master
        self.client = client
        self.file = file
        self.req = req
        self.obj = obj

    def undo(self):
        if self.master.current_req!=self.req:
            self.master.set_client(self.client)
            self.master.set_file(self.file)
            self.master.set_request(self.req)

        self.master.toggle_objection(self.obj,undo_command=True)

    def redo(self):
        self.undo()###### TURN THIS INTO A NICE BASE CLASS TO BASE THE OTHERS OFF OF, THIS METHOD WILL WORK WELL!