import customtkinter as tk


# CUSTOM TKINTER FRAME CLASSES
############################################################################################################

# Contains details data
class Detail(tk.CTk):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master
        self.geometry("400x500")
        self.title("Document Details")
        self.resizable(False,False)
        self.grid_columnconfigure((0,1),weight=1)
        #County
        county = tk.CTkLabel(master=self,text="County")
        county.grid(row=0,column=0,padx=20,sticky="w")
        self.county = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.county.grid(row=1,column=0,padx=30,columnspan=2,sticky="ew")
        self.county.insert("0.0",self.master.doc_details["county"])
        #Case Number
        case = tk.CTkLabel(master=self,text="Case Number")
        case.grid(row=2,column=0,padx=20,sticky="w")
        self.case = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.case.grid(row=3,column=0,padx=30,columnspan=2,sticky="ew")
        self.case.insert("0.0",self.master.doc_details["case_number"])
        #Document
        document = tk.CTkLabel(master=self,text="Document Name")
        document.grid(row=4,column=0,padx=20,sticky="w")
        self.document = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.document.grid(row=5,column=0,padx=30,columnspan=2,sticky="ew")
        self.document.insert("0.0",self.master.doc_details["document"])
        #Plaintiff
        plaintiff = tk.CTkLabel(master=self,text="Plaintiff")
        plaintiff.grid(row=6,column=0,padx=20,sticky="w")
        self.plaintiff = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.plaintiff.grid(row=7,column=0,padx=30,columnspan=2,sticky="ew")
        self.plaintiff.insert("0.0",self.master.doc_details["plaintiff"])
        #Defendant
        defendant = tk.CTkLabel(master=self,text="Defendant")
        defendant.grid(row=8,column=0,padx=20,sticky="w")
        self.defendant = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.defendant.grid(row=9,column=0,padx=30,columnspan=2,sticky="ew")
        self.defendant.insert("0.0",self.master.doc_details["defendant"])

        #Cancel Button
        self.cancel_button = tk.CTkButton(master=self,text="Cancel",command=self.master.cancel_win)#Just simply close
        self.cancel_button.grid(row=10,column=0,pady=20)

        #Submit Button
        self.submit_button = tk.CTkButton(master=self,text="Save",command=self.master.save_win)#Save and close
        self.submit_button.grid(row=10,column=1,pady=20)


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
    def __init__(self,req,resp,no,master):
        self.req=req
        self.resp=resp
        self.no=no
        self.additional_text=""
        self.opts=[]
        self.master=master
        for i in self.master.objections_frame.options:
            self.opts.append(Objection(i,master))
        self.color="white"
        self.RFP_option="Available"
        self.RFP_text=""

    def set(self):
        self.master.set_request(self)

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

