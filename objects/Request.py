# IMPORTS
from functions import *
from .Objection import *
# REQUEST CLASS
############################################################################################################
# Class for each request/response

RFP_responses={"Available":"Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
                    "Not Exist":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist.",
                    "Not Possessed":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party.",
                    "Lost":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen."}

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
        #Special Options
        self.RFP_option="Available"
        self.RFP_text=""
        self.RFA_option="Admit"
        self.RFA_text="(a) "+str(no+1)+". Responding Party reasserts any and all objections to this request and incorporates them here by reference.\n(b) Facts supporting response\n(c) People with knowledge of facts supporting response\n(d) Documents supporting repsonse"

        self.auto_obj()
        self.req_type=req_type
        if custom_key!="":
            self.custom_key = custom_key
        else:
            self.custom_key = no+1
        self.current_objection = ""

    #Fill objections automatically using saved answers
    def auto_obj(self):
        for obj in self.master.objections:
            added=0
            if self.master.objections[obj][3]:
                for word in self.master.objections[obj][4]:
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
        full_text = get_objection_text(self.opts,self.master.objections,False)
        #Add response to the end
        if self.req_type == "RFP":
            option = self.RFP_option
            if option!="Custom":
                extra = " Any responsive documents are believed to be in the possession, custody, or control of [VAR]."
                end = RFP_responses[option].replace("[VAR]",self.RFP_text)
                if option!="Available" and self.RFP_text!="":
                    end = (end+extra).replace("[VAR]",self.RFP_text)
            else:
                end = self.master.response_frame.get_response()
        else:
            end = self.master.response_frame.get_response()
        if full_text.replace(" ","").replace("\n","")!="":
            full_text = full_text + "\n"
        full_text = full_text + end
        return full_text