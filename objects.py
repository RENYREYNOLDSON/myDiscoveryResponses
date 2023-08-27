

RFP_responses={"Available":"Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
                    "Not Exist":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist.",
                    "Not Possessed":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party.",
                    "Lost":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen."}

# NORMAL CLASSES
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
    def set(self):
        self.master.set_file(self)
    def set_master(self,val):#Remove master from all of the sub objects etc
        self.master=val
        for i in self.reqs:
            i.master=val
            for i2 in i.opts:
                i2.master=val


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
        self.auto_obj()
        self.req_type=req_type
        self.custom_key = custom_key
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
    #Add a parameter to the string
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
    #Get full response text
    def get_full_resp(self):
        full_text = self.master.get_objections(self.opts,False)
        #Add response to the end
        if self.req_type == "RFP":
            option = self.RFP_option
            txt = self.RFP_text
            extra = " Any responsive documents are believed to be in the possession, custody, or control of [VAR]."
            end = RFP_responses[option].replace("[VAR]",self.RFP_text)
            if option!="Available" and self.RFP_text!="":
                end = (end+extra).replace("[VAR]",self.RFP_text)
        else:
            end = self.master.response_frame.response_text.get("0.0","end")
            print("ye")
        full_text = full_text+end
        return full_text


# Class for each objection for each response
class Objection:
    def __init__(self,key,master):
        self.key=key
        self.master=master
        self.text=self.master.objections[key]
        if self.text=="":
            self.text=key
        self.selected=0
        self.param=""

class Save:
    def __init__(self,files):
        self.files = files



    

