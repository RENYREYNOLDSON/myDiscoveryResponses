###### OBJECTS
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023
######
###### Code for the 4 classes used by main program CLIENT,FILE,REQUEST,OBJECTION (and SAVE)
######


# IMPORTS 
############################################################################################################

from functions import *

# CONSTANTS 
############################################################################################################

RFP_responses={"Available":"Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
                    "Not Exist":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist.",
                    "Not Possessed":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party.",
                    "Lost":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen."}

# CLIENT CLASS
############################################################################################################
class Client:
    # Constructor 
    def __init__(self,name,files,master):
        self.name=name
        self.master=master
        self.files=files
        self.color=("black","white")
        self.current_file = files[0]
    # Set the current client to self
    def set(self):
        self.master.set_client(self)
    # Set self.master to a value (for saving)
    def set_master(self,val):
        self.master=val
        for i in self.files:#Remove master from all of the sub objects etc
            i.set_master(val)

# FILE CLASS
############################################################################################################
# Each file is stored as one of these
class File:
    def __init__(self,name,details,req_type,reqs,master):
        self.name = name
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

# REQUEST CLASS
############################################################################################################
# Class for each request/response
class Request:
    def __init__(self,req,resp,no,master,req_type,custom_key=""):
        self.req=req
        self.resp=resp
        self.no=no
        self.additional_text=""
        self.opts=[]
        self.master=master
        for i in self.master.objections_frame.options:
            self.opts.append(Objection(i,master))
        self.color=("black","white")
        self.RFP_option="Available"
        self.RFP_text=""
        self.RFA_option="Admit"
        self.auto_obj()
        self.req_type=req_type
        self.custom_key = custom_key
        self.current_objection = ""
    #Fill objections automatically using saved answers
    def auto_obj(self):
        for obj in self.master.auto_objections:
            added=0
            for word in self.master.auto_objections[obj]:
                if word in self.req:
                    self.add_param(obj,word)#Add param to the params
                    added+=1
            if added>1:#Set final , to and
                for i in self.opts:
                    if i.key==obj:
                        i.param = ", and ".join(i.param.rsplit(", ", 1))#Add the AND
    #Add a parameter from autofill list to the string
    def add_param(self,obj,param):
        for i in self.opts:
            if i.key==obj:
                if i.param=="":
                    self.check_off(obj)
                    i.param = "as to ‘"+param+"’"
                    return
                i.param=i.param+", ‘"+param+"’"
                return
    #Set self as the current request
    def set(self):
        self.master.set_request(self)
    #Check off an objection
    def check_off(self,obj):
        for i in self.opts:
            if i.key==obj:
                i.selected=1
                return
    #Get the full response text
    def get_full_resp(self):
        full_text = self.master.get_objections(self.opts,False)
        #Add response to the end
        if self.req_type == "RFP":
            option = self.RFP_option
            if option!="Custom":
                txt = self.RFP_text
                extra = " Any responsive documents are believed to be in the possession, custody, or control of [VAR]."
                end = RFP_responses[option].replace("[VAR]",self.RFP_text)
                if option!="Available" and self.RFP_text!="":
                    end = (end+extra).replace("[VAR]",self.RFP_text)
            else:
                end = self.master.response_frame.response_text.get("0.0","end")
        else:
            end = self.master.response_frame.response_text.get("0.0","end")
        full_text = full_text+"\n"+end
        return full_text

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

        #Store this for writing objections
        self.additional_text=self.master.objections[key][1]
        self.alter_scope=self.master.objections[key][2]
        self.autofill=self.master.objections[key][3]
    #Toggle if this objection is selected
    def toggle(self):
        self.selected = not self.selected

# SAVE CLASS (minor)
############################################################################################################
# Just holds all of the files for saving
class Save:
    def __init__(self,files):
        self.files = files



    
