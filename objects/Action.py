# IMPORTS
from functions import *
import copy

# ACTION CLASSES
############################################################################################################

class Action:#Action base class
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
        self.redo_function()

class ActionToggleObjection(Action):
    def undo_function(self):
        self.master.toggle_objection(self.obj,undo_command=True)

    def redo_function(self):
        self.undo()

class ActionSubmit(Action):
    def __init__(self, master, obj):
        super().__init__(master, obj)
        self.prev_color = self.req.color
    def undo_function(self):
        if self.prev_color == "#FF0000":
            self.master.check(undo_command=True)#If was red then check
        else:
            self.master.submit(undo_command=True)#Otherwise submit

    def redo_function(self):
        self.master.submit(undo_command=True)#Always submit

class ActionCheck(Action):
    def __init__(self, master, obj):
        super().__init__(master, obj)
        self.prev_color = self.req.color
    def undo_function(self):
        if self.prev_color == "#50C878":
            self.master.submit(undo_command=True)#Otherwise submit
        else:
            self.master.check(undo_command=True)#If was red then check

    def redo_function(self):
        self.master.check(undo_command=True)#Always check

class ActionTextBox(Action):
    def undo_function(self):
        #Access the relevant smart textbox and trigger undo command
        self.obj.undo()
    
    def redo_function(self):
        #Access the relevant smart textbox and trigger redo command
        self.obj.redo()

################################ UNFINISHED / UNTESTED METHODS 





class ActionClear(Action):
    def __init__(self, master, obj):
        super().__init__(master, obj)
        self.master.set_request(self.req)
        self.req.set_master(None)
        self.deep_req = copy.deepcopy(self.req)#NEEDS SAVING BEFORE IT IS COPIED!!!!!!
        self.req.set_master(self.master)
        
    def undo_function(self):
        #Set the current request to this stored one
        self.req.opts = copy.deepcopy(self.deep_req.opts)
        self.req.RFP_option = self.deep_req.RFP_option
        self.req.RFP_text = self.deep_req.RFP_text
        self.req.RFA_option = self.deep_req.RFA_option
        self.req.RFA_text = self.deep_req.RFA_text
        self.req.resp = self.deep_req.resp
        self.req.custom_objection_text = self.deep_req.custom_objection_text
        self.req.set_master(self.master)

        self.master.set_request(self.req,save_current=False)
        self.master.toggle_selected_objection(str(self.req.opts[0].key),None)

    
    def redo_function(self):
        self.master.clear(undo_command=True)


class ActionCopyPrevious(Action):
    def __init__(self, master, obj):
        super().__init__(master, obj)
        self.master.set_request(self.req)
        self.req.set_master(None)
        self.deep_req = copy.deepcopy(self.req)#NEEDS SAVING BEFORE IT IS COPIED!!!!!!
        self.req.set_master(self.master)
        
    def undo_function(self):
        #Set the current request to this stored one
        self.req.opts = copy.deepcopy(self.deep_req.opts)
        self.req.RFP_option = self.deep_req.RFP_option
        self.req.RFP_text = self.deep_req.RFP_text
        self.req.RFA_option = self.deep_req.RFA_option
        self.req.RFA_text = self.deep_req.RFA_text
        self.req.resp = self.deep_req.resp
        self.req.custom_objection_text = self.deep_req.custom_objection_text
        self.req.set_master(self.master)

        self.master.set_request(self.req,save_current=False)
        self.master.toggle_selected_objection(str(self.req.opts[0].key),None)

    
    def redo_function(self):
        self.master.copy_previous(undo_command=True)

#Sets the RFA entry button
class ActionRFAEntry(Action):
    def undo_function(self):
        #Set the button to the relevant value
        self.master.response_frame.set_RFA(self.obj[0],undo_command=True)
    def redo_function(self):
        #Set the button to the relevant value
        self.master.response_frame.set_RFA(self.obj[1],undo_command=True)

















