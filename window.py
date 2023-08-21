import converter_1 as cnv
import customtkinter as tk
import json,os

# CUSTOM TKINTER CLASSES
############################################################################################################

# Contains details data
class Detail(tk.CTk):
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.geometry("400x500")
        self.title("Document Details")
        self.resizable(False,False)
        self.grid_columnconfigure((0,1),weight=1)
        #County
        county = tk.CTkLabel(master=self,text="County")
        county.grid(row=0,column=0,padx=20,sticky="w")
        self.county = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.county.grid(row=1,column=0,padx=30,columnspan=2,sticky="ew")
        self.county.insert("0.0",app.doc_details["county"])
        #Case Number
        case = tk.CTkLabel(master=self,text="Case Number")
        case.grid(row=2,column=0,padx=20,sticky="w")
        self.case = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.case.grid(row=3,column=0,padx=30,columnspan=2,sticky="ew")
        self.case.insert("0.0",app.doc_details["case_number"])
        #Document
        document = tk.CTkLabel(master=self,text="Document Name")
        document.grid(row=4,column=0,padx=20,sticky="w")
        self.document = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.document.grid(row=5,column=0,padx=30,columnspan=2,sticky="ew")
        self.document.insert("0.0",app.doc_details["document"])
        #Plaintiff
        plaintiff = tk.CTkLabel(master=self,text="Plaintiff")
        plaintiff.grid(row=6,column=0,padx=20,sticky="w")
        self.plaintiff = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.plaintiff.grid(row=7,column=0,padx=30,columnspan=2,sticky="ew")
        self.plaintiff.insert("0.0",app.doc_details["plaintiff"])
        #Defendant
        defendant = tk.CTkLabel(master=self,text="Defendant")
        defendant.grid(row=8,column=0,padx=20,sticky="w")
        self.defendant = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.defendant.grid(row=9,column=0,padx=30,columnspan=2,sticky="ew")
        self.defendant.insert("0.0",app.doc_details["defendant"])

        #Cancel Button
        self.cancel_button = tk.CTkButton(master=self,text="Cancel",command=cancel_win)#Just simply close
        self.cancel_button.grid(row=10,column=0,pady=20)

        #Submit Button
        self.submit_button = tk.CTkButton(master=self,text="Save",command=save_win)#Save and close
        self.submit_button.grid(row=10,column=1,pady=20)


# Contains request and response data
class Response_Frame(tk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #Frame Setup
        self.grid_columnconfigure((0,1),weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12),weight=1)
        self.prev=None

        #Label Font
        label_font = tk.CTkFont("Arial",16,underline=True,weight="bold")
        # Request Body
        self.request_label=tk.CTkLabel(master=self,text="REQUEST:",font=label_font)
        self.request_label.grid(row=0,column=0,sticky="w",columnspan=2,padx=20)
        self.request_text=tk.CTkTextbox(master=self,wrap="word",state="disabled",height=20)
        self.request_text.grid(row=1,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3)

        # Objections Body
        self.objection_label=tk.CTkLabel(master=self,text="OBJECTIONS:",font=label_font)
        self.objection_label.grid(row=4,column=0,sticky="w",columnspan=2,padx=20)
        self.objection_text=tk.CTkTextbox(master=self,wrap="word",state="disabled",height=20)
        self.objection_text.grid(row=5,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3)

        #Response body
        self.response_label=tk.CTkLabel(master=self,text="RESPONSE:",font=label_font)
        self.response_label.grid(row=8,column=0,sticky="w",columnspan=2,padx=20)
        self.response_text=tk.CTkTextbox(master=self,wrap="word",state="normal")
        self.response_text.grid(row=9,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3)

        #Clear
        self.clear_button = tk.CTkButton(master=self,text="Clear",command=clear)
        self.clear_button.grid(row=12,column=0)

        #Next
        self.next_button = tk.CTkButton(master=self,text="Submit",command=submit)
        self.next_button.grid(row=12,column=1)

        #RFP menu
        self.resp_label = tk.CTkLabel(master=self,text="Documents Location:")
        self.resp_text = tk.CTkEntry(master=self)
        self.resp_option = tk.CTkSegmentedButton(master=self,values=["Available","Not Exist","Not Possessed","Lost"])
        self.resp_option.set("Available")

    def redraw(self,req_type):
        if req_type=="RFP":
            if self.prev!="RFP":
                self.response_text.grid_forget()
                #Selector for option
                self.resp_option.grid(row=9,column=0,padx=30,sticky="ew",columnspan=2)
                #Text box for file etc
                self.resp_label.grid(row=10,column=0,sticky="ew",padx=0)
                self.resp_text.grid(row=10,column=0,sticky="ew",padx=(160,30),columnspan=2)

                self.response_text.grid(row=11,column=0,padx=30,stick="nsew",columnspan=2,rowspan=1)
                self.response_text.configure(state="disabled") 
            
        else:
            self.resp_label.grid_forget()
            self.resp_text.grid_forget()
            self.resp_option.grid_forget()
            #Just change text if it exists
            if self.prev=="RFP":
                self.response_text.grid_forget()
                self.response_text.grid(row=9,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3) 
            self.response_text.configure(state="normal") 
        self.prev = req_type



# Contains list of all the requests in file
class Requests_Frame(tk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        # Files Frame
        text = tk.CTkLabel(master=self,text="FILES",anchor="w")
        text.pack(fill="both",padx=10)
        self.file_frame = tk.CTkScrollableFrame(master=self,corner_radius=0,fg_color="transparent")
        self.file_frame.pack(padx=0,pady=0,fill="x")
        # Requests Frame
        text = tk.CTkLabel(master=self,text="REQUESTS",anchor="w")
        text.pack(fill="both",padx=10)
        self.list_frame = tk.CTkScrollableFrame(master=self,corner_radius=0,fg_color="transparent")
        self.list_frame.pack(padx=0,pady=0,expand=True,fill="both")

    def show_files(self,files):
        for w in self.file_frame.winfo_children():
            w.destroy()
        c=1
        for i in files:
            button = tk.CTkButton(master=self.file_frame,anchor="w",text=" 🗎 "+str(i.name).split("/")[-1][:22]+"...",corner_radius=0,fg_color="transparent",command=i.set)
            button.pack(fill="x",side="top")
            c+=1


    def show_list(self,reqs):
        for w in self.list_frame.winfo_children():
            w.destroy()
        c=1
        for i in reqs:
            fg_color="transparent"
            if i==app.current_req:
                fg_color="grey"

            color=i.color
            button = tk.CTkButton(master=self.list_frame,text="REQUEST NO. "+str(c),corner_radius=0,text_color=color,fg_color=fg_color,command=i.set)
            button.pack(fill="x",side="top")
            c+=1

# Contains list of all possible objections
class Objections_Frame(tk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #Frame Setup
        l=[]
        for i in range(len(list(master.objections.keys()))):
            l.append(i)
        self.grid_rowconfigure(l,weight=1)
        self.columnconfigure((0,1),weight=1)
        # Option (from file)
        self.options = sorted(list(master.objections.keys()))
        #Move ones with entries to the front

        c=0
        for opt in self.options:
            #For each key
            if "[VAR]" in master.objections[opt]:
                #Remove
                temp = opt
                self.options.remove(opt)
                #Insert at the start
                self.options.insert(c,temp)
                c+=1

        c=0
        self.opts=[]
        self.params=[]
        for opt in self.options:
            #Checkbox
            #Label
            #label = tk.CTkLabel(master=self,text=opt,anchor="e")
            #label.grid(row=c,column=0,sticky="e")

            optbox = tk.CTkCheckBox(master=self,text=opt,corner_radius=0)
            optbox.grid(row=c,column=0,sticky="w",padx=(10,0),pady=2)
            self.opts.append(optbox)

            #Text Input
            if "[VAR]" in master.objections[opt]:#Highlight valid inputs
                param = tk.CTkEntry(master=self,state="normal",fg_color="transparent")
            else:
                param = tk.CTkEntry(master=self,state="disabled")
            param.grid(row=c,column=1,padx=(10,5),sticky="ew")
            self.params.append(param)
            c+=1

    def redraw(self,req):
        for i in range(len(self.opts)):
            #Update checkbox
            if req.opts[i].selected==1:
                self.opts[i].select()#configure(variable=req.opts[i].selected)
            else:
                self.opts[i].deselect()
            #Update Entry
            self.params[i].delete(0,"end")
            self.params[i].insert(0,req.opts[i].param)

class Bar_Frame(tk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)

        # File
        var = tk.StringVar(value="File")
        self.file=tk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["New Window","Open File","Open Folder","Save File","Save All","Export File as DOCX","Export All as DOCX","Close File","Close All","Exit"],width=100,corner_radius=0,bg_color="transparent",command=self.call)
        self.file.configure(button_color="#161616",fg_color="#161616")
        self.file.pack(side="left")

        # Discovery
        var = tk.StringVar(value="Discovery")
        self.discovery=tk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["List Here"],width=100,corner_radius=0,bg_color="transparent",command=self.call)
        self.discovery.configure(button_color="#161616",fg_color="#161616")
        self.discovery.pack(side="left")

        # Details

        # View
        var = tk.StringVar(value="View")
        self.view=tk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["Theme","Text","Layout"],width=100,corner_radius=0,bg_color="transparent",command=self.call)
        self.view.configure(button_color="#161616",fg_color="#161616")
        self.view.pack(side="left")

    def call(self,val):
        self.file.set("File")
        if val=="Open File":
            select_file()
        elif val=="Exit":
            app.destroy()

# Main root app, holds all frames
class App(tk.CTk):
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()

        # Window setup
        self.minsize(1000,700)
        self.geometry("1000x700")
        self.title("Discovery Responses")

        # Attributes
        self.files=[]
        self.current_file = ""
        self.reqs=[]
        self.req_type=""
        self.prev_type=""
        self.current_req=0
        self.doc_details=None
        self.objections = open_objections()

        # Navigation Bar Frame
        self.bar_frame = Bar_Frame(master=self,corner_radius=0,fg_color="#161616")
        self.bar_frame.pack(padx=0,pady=0,fill="both")

        # Requests Frame
        self.requests_frame = Requests_Frame(master=self,corner_radius=0)
        self.requests_frame.pack(padx=0,pady=0,expand=True,side="left",fill="both")

        # Objections Frame
        self.objections_frame = Objections_Frame(master=self,corner_radius=0)
        self.objections_frame.pack(padx=0,pady=0,expand=True,side="right",fill="both")

        # Response Frame
        self.response_frame = Response_Frame(master=self)
        self.response_frame.pack(ipadx=200,padx=20,pady=20,expand=True,side="left",fill="both")
    def set_type(self,req_type):
        if self.prev_type=="":
            self.prev_type = req_type
        else:
            self.prev_type = self.req_type
        self.req_type = req_type 

# NORMAL CLASSES
############################################################################################################

# Each file is stored as one of these
class File:
    def __init__(self,name,details,req_type,reqs):
        self.name = name
        self.details = details
        self.req_type = req_type
        self.reqs = reqs
        self.current_req = reqs[0]
    def set(self):
        #NEED TO CHANGE THINGS HERE TOO!!!
        app.current_file = self
        app.doc_details = self.details
        app.reqs = self.reqs

        # Set is built for a single request type, need to change for files
        app.set_type(self.req_type)# Set first so refresher doesn't overwrite
        self.current_req.set()
        app.response_frame.redraw(self.req_type)
        app.title("Discovery Responses   |   "+str(self.name.split("/")[-1]))
        

# Class for each request/response
class Request:
    def __init__(self,req,resp,no):
        self.req=req
        self.resp=resp
        self.no=no
        self.additional_text=""
        self.opts=[]
        for i in app.objections_frame.options:
            self.opts.append(Objection(i))
        self.color="white"
        self.RFP_option="Available"
        self.RFP_text=""

    def set(self):
        #THIS SHOULD SET THE CURRENT REQ!

        # 1. SAVING PREVIOUS RESPONSE
        if app.current_req!=0:

            # Saving
            app.current_req.resp = app.response_frame.response_text.get("0.0","end").replace("\n","")
            #GET RFP data
            if app.prev_type=="RFP":
                app.current_req.RFP_option=app.response_frame.resp_option.get()
                app.current_req.RFP_text=app.response_frame.resp_text.get()



            #COLOR#########################################
            grey=False
            if app.current_req.resp.replace("\n","")!="" and app.req_type!="RFP":
                grey=True
            elif (app.current_req.RFP_option!="Available" or len(app.current_req.RFP_text)>0):
                grey=True
            for i in range(len(self.opts)):
                #Set Check
                app.current_req.opts[i].selected=app.objections_frame.opts[i].get()
                if app.objections_frame.opts[i].get()!=0:
                    grey=True
                #Set Param
                app.current_req.opts[i].param=app.objections_frame.params[i].get()
                if app.objections_frame.params[i].get()!="":
                    grey=True
            if grey and app.current_req.color!="#50C878":
                app.current_req.color="grey" 
            elif app.current_req.color!="#50C878":
                app.current_req.color="white"
            ################################################
        # 2. ENTERING NEW RESPONSE INTO FRAME
        app.current_req=self
        app.current_file.current_req=self# Set the current req of the file
        #Save,Reset and add text
        app.response_frame.request_text.configure(state="normal")
        app.response_frame.request_text.delete("0.0","end")
        app.response_frame.request_text.insert("0.0",self.req)
        app.response_frame.request_text.configure(state="disabled")
        app.response_frame.request_label.configure(text="REQUEST NO. "+str(self.no+1)+":")



        #Response text
        app.response_frame.response_text.configure(state="normal")
        app.response_frame.response_text.delete("0.0","end")
        app.response_frame.response_text.insert("0.0",self.resp)
        #RFP
        if app.req_type=="RFP":
            app.response_frame.resp_option.set(self.RFP_option)
            app.response_frame.resp_text.delete(0,"end")
            app.response_frame.resp_text.insert(0,self.RFP_text)

        #Change the objections list!
        app.objections_frame.redraw(self)
        app.requests_frame.show_list(app.reqs)#Redraw the buttons
        app.set_type(app.req_type)
        app.update()   


    def set_obj(self):
        for i in range(len(self.opts)):
            #Set Check
            app.current_req.opts[i].selected=app.objections_frame.opts[i].get()
            #Set Param
            app.current_req.opts[i].param=app.objections_frame.params[i].get() 

# Class for each objection for each response
class Objection:
    def __init__(self,key):
        self.key=key
        self.text=app.objections[key]
        if self.text=="":
            self.text=key
        self.selected=0
        self.param=""


# FUNCTIONS 
############################################################################################################

def cancel_win():
    global win
    win.destroy()
    win=None

def save_win():
    app.doc_details["county"] = win.county.get("0.0","end").replace("\n","")
    app.doc_details["case_number"] = win.case.get("0.0","end").replace("\n","")
    app.doc_details["document"] = win.document.get("0.0","end").replace("\n","")
    app.doc_details["plaintiff"] = win.plaintiff.get("0.0","end").replace("\n","")
    app.doc_details["defendant"] = win.defendant.get("0.0","end").replace("\n","")
    cancel_win()

# View and edit the details of the document
def view_details():
    global win
    if app.current_file!="":
        if win!=None:
            win.destroy()
            win=None
        win = Detail()
        win.protocol("WM_DELETE_WINDOW", cancel_win)
        win.mainloop()





# Select a save from files
def select_save():
    #Need to get the correct file location and then save
    filename=tk.filedialog.asksaveasfilename(filetypes=(("DOCX","*.docx"),('All files', '*.*')))
    save(filename)

#Opens a window to select a file
def select_file():
    filetypes = (
        ('PDF files', '*.pdf'),
        ('All files', '*.*')
    )
    filename = tk.filedialog.askopenfilename(
        title='Open PDF file',
        filetypes=filetypes)

    if os.path.exists(filename):
        app.title("Discovery Responses   |   "+str(filename.split("/")[-1]))
        reqs,req_type,app.doc_details = cnv.getRequests(filename)
        app.set_type(req_type)# Sets the current type
        app.reqs=[]

        #Redraw for production
        app.response_frame.redraw(app.req_type)
        c=0
        for i in reqs:
            app.reqs.append(Request(i,"",c))
            c+=1

        app.files.append(File(filename,app.doc_details,app.req_type,app.reqs))
        app.current_file=app.files[-1]
        app.reqs[0].set()

        # Add file
        app.requests_frame.show_files(app.files)
        app.requests_frame.show_list(app.reqs)
        app.update()

# Opens the objections file
def open_objections():# Return API key from file if possible
    if os.path.exists("objections.json"):
        with open('objections.json', 'r') as file:
            data = json.load(file)
        return data
    return None

# Set a request to submitted
def submit():
    if app.current_req!=0:
        app.current_req.color="#50C878"
        app.requests_frame.show_list(app.reqs)
        #Go to next request
        index = app.reqs.index(app.current_req)
        if index<len(app.reqs)-1:
            app.reqs[index+1].set()

# Clear a full request
def clear():
    if app.current_req!=0:
        #Reset Color
        app.current_req.color="white"
        #Reset Response
        app.current_req.resp=""
        #Reset Checkboxes & Params
        for i in app.current_req.opts:
            i.selected=0
            i.param=""
        #Reset boxes
        app.response_frame.response_text.delete("0.0","end")
        app.objections_frame.redraw(app.current_req)
        app.requests_frame.show_list(app.reqs)
        #Reset RFP
        if app.req_type=="RFP":
            app.response_frame.resp_option.set("Available")
            app.response_frame.resp_text.delete(0,"end")
        app.update()

# Save as a word DOCX
def save(filename):
    if app.current_file!="":#ADD CORRECT SAVING HERE!!!!
        reqs=[]
        resps=[]
        for r in app.reqs:#Get responses and requests
            #1. ADD REQUESTS
            reqs.append(r.req)
            #2. ADD RESPONSES
            full_text = get_objections(r.opts)
            #Add response to the end
            if app.req_type == "RFP":
                option = r.RFP_option
                txt = r.RFP_text
                end = RFP_responses[option].replace("[VAR]",txt)
            else:
                end = r.resp
            full_text = full_text+end
            resps.append(full_text)
        cnv.updateDOC(reqs,resps,app.doc_details,app.req_type,str(filename))

def get_objections(opts):
    #Add all objections

    full_text = "Objections. "
    objs=[]
    for obj in opts:
        if obj.selected==1:
            objs.append([obj.key,obj.param])
    if len(objs)>0:
        for key in list(app.objections.keys()):
            # This will put it in order!
            for obj in objs:# For each objection
                if key==obj[0]:
                    text=app.objections[key]
                    if text=="":
                        text=key
                    text = text.replace("[VAR]",obj[1])# Replace [VAR]
                    full_text = full_text+str(text)+". "#A dd new text!

        #Add final text
        alter_scope=[
            "Unintelligible as written",
            "Not limited in time and scope",
            "Vague and ambiguous",
            "Speculation",
            "Overbroad"
            ]

        if full_text!="":
            final_text = "Notwithstanding the foregoing objections and subject thereto, Responding Party responds as follows. "
            extra = ""
            for obj in objs:
                if obj[0] in alter_scope:
                    final_text = "Notwithstanding the foregoing objections and subject thereto, and as Responding Party understands the proper scope and/or meaning of this request, Responding Party responds as follows. "
                elif obj[0]=="Compilation":
                    extra = "Responding Party exercises their right to produce writings in response to this interrogatory, pursuant to California Code of Civil Procedure section 2030.230. Please see [VAR] produced concurrently herewith. ".replace("[VAR]",obj[1])
            
            final_text = final_text + extra
            full_text = full_text + final_text
            return full_text
    else:
        return ""
#WINDOW UTILITY########################################################################


# Refreshes RFP response text
def refresher():
    #Always update the 
    if app.current_req!=0:
        # Update Objections Box
        app.current_req.set_obj()
        temp = app.response_frame.objection_text.get("0.0","end")
        text = get_objections(app.current_req.opts)
        if text!=temp.replace("\n",""):
            #If text has changed
            app.response_frame.objection_text.configure(state="normal")
            app.response_frame.objection_text.delete("0.0","end")
            app.response_frame.objection_text.insert("0.0",text)
            app.response_frame.objection_text.configure(state="disabled")

        # Update Response Box
        if app.req_type=="RFP":
            app.response_frame.response_text.configure(state="normal")
            app.response_frame.response_text.delete("0.0","end")
            #Enter here
            option = app.response_frame.resp_option.get()
            resp = app.response_frame.resp_text.get()

            text = RFP_responses[option].replace("[VAR]",resp)
            app.response_frame.response_text.insert("0.0",text)

            app.response_frame.response_text.configure(state="disabled")
    app.after(100, refresher)

def up_pressed(e):
    if app.current_req!=0:
        index = app.reqs.index(app.current_req)
        index = max(0,index-1)
        app.reqs[index].set()
def down_pressed(e):
    if app.current_req!=0:
        index = app.reqs.index(app.current_req)
        index = min(len(app.reqs)-1,index+1)
        app.reqs[index].set()
def enter_pressed(e):
    submit()


# MAIN PROGRAM LOOP
if __name__ == "__main__":
    win=None
    RFP_responses={"Available":"Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
                    "Not Exist":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist. Any responsive documents are believed to be in the possession, custody, or control of [VAR].",
                    "Not Possessed":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party. Any responsive documents are believed to be in the possession, custody, or control of [VAR].",
                    "Lost":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen. Any responsive documents are believed to be in the possession, custody, or control of [VAR]."}
                    
    tk.set_appearance_mode("dark")
    app=App()
    app.after(100, refresher)
    app.bind("<Up>",up_pressed)
    app.bind("<Down>",down_pressed)
    app.bind("<Return>",enter_pressed)
    app.mainloop()


# Add pdf logo and app icon
# Scoll to submitted request
# Reset scroll wheel when changing file!
# Darkmode button!
# Add saving and loading of the workspace
# Add date to docx

# Make performance of arrows better
# Add method like show_list which just updates one. Have it only update them!

# Compilation needs 2 boxes!
# Need to save with italics included
# Add prompt if not all done
# Fix request having other doc info
# Fix broken chars
# Remove extra data from details
# Add tooltips
# Add help section

# Clean all code
