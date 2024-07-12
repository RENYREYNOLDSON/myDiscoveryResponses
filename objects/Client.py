# Main Imports
from objects.__modules__ import *
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
        #Use for 17.1's
        self.special_responses = []

    #Reload all objections
    def reload_objections(self):
        for file in self.files:
            file.reload_objections()

        #Update the selected objection here! Only for the open request
        if self.master.current_req!=0:
            self.master.toggle_selected_objection(str(self.master.current_req.current_objection.key),None)


    # Set the current client to self
    def set(self):
        self.master.set_client(self)

    # Set self.master to a value (for saving)
    def set_master(self,val):
        self.master=val
        for i in self.files:#Remove master from all of the sub objects etc
            i.set_master(val)

    #Adds a 17.1 response in order
    def add_special_response(self,resp):
        if hasattr(self,"special_responses")==False:
            self.special_responses=[]
        #Add new item
        present = False
        c=0
        for item in self.special_responses:
            if item[0]==resp[0]:
                print("same")
                self.special_responses[c] = resp
                print(resp)
                present = True
            c+=1
        if present == False:
            self.special_responses.append(resp)
        #Reorder array
        self.special_responses = sorted(self.special_responses,key=lambda x: x[0])