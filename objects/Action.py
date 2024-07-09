# IMPORTS
from functions import *

# CLIENT CLASS
############################################################################################################

class Action:
    def __init__(self,master,obj):
        self.master = master
        self.client = master.current_client
        self.file = self.client.current_file
        self.req = self.file.current_req
        self.obj = obj

    def navigate_to_request(self):
        #Navigate to client
        if self.master.current_client!=self.client:#ALTER THIS TO ONLY DO WHAT IS NEEDED, SAVE AS BASE CLASS!
            self.master.set_client(self.client)
        #Navigate to file
        if self.master.current_client.current_file!=self.file:
            self.master.set_file(self.file)
        #Navigate to request
        if self.master.current_req!=self.req:
            self.master.set_request(self.req)

    def undo_function(self):
        return
    
    def redo_function(self):
        return

    def undo(self):#Undo function, goes to request and then calls
        self.navigate_to_request()
        self.undo_function()

    def redo(self):#Redo function, goes to request and then calls
        self.navigate_to_request()
        self.redo_function()###### TURN THIS INTO A NICE BASE CLASS TO BASE THE OTHERS OFF OF, THIS METHOD WILL WORK WELL!

class ActionToggleObjection(Action):
    def undo_function(self):
        self.master.toggle_objection(self.obj,undo_command=True)

    def redo_function(self):
        self.undo()###### TURN THIS INTO A NICE BASE CLASS TO BASE THE OTHERS OFF OF, THIS METHOD WILL WORK WELL!

class ActionSubmit(Action):
    def undo_function(self):
        self.master.submit(undo_command=True)

    def redo_function(self):
        self.undo()

class ActionCheck(Action):
    def undo_function(self):
        self.master.check(undo_command=True)

    def redo_function(self):
        self.undo()



################################ UNFINISHED / UNTESTED METHODS 

class ActionTextBox(Action):
    def undo_function(self):
        #Access the relevant smart textbox and trigger undo command
        self.obj.undo()
        print("UNDO")
    
    def redo_function(self):
        #Access the relevant smart textbox and trigger redo command
        self.obj.redo()
        print("REDO")




class ActionClear(Action):
    def undo_function(self):
        pass
    
    def redo_function(self):
        pass

class ActionDeleteClient(Action):
    def undo_function(self):
        #Add the client back into the client list
        pass
    
    def redo_function(self):
        #Remove the client from the client list
        pass

class ActionAddClient(Action):
    def undo_function(self):
        #Remove client from the client list
        pass
    
    def redo_function(self):
        #Add client back to the client list
        pass