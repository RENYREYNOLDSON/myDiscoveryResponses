import converter_1 as cnv
from frames import *
from objects import *
import customtkinter as tk
import json,os
from PIL import Image
import pickle
import tkinter
########## PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023
########## Uses converter.py to open discovery request PDF's in order to respond
########## Provides a Windows GUI tool for opening files and saving as DOCX
########## Version 3.0 | 21/08/2023


# MAIN WINDOW CLASS
############################################################################################################


# Main root app, holds all frames
class App(tk.CTkToplevel):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.master=master
        master.call()
        self.after(100, self.refresher)
        self.bind("<Up>",self.up_pressed)
        self.bind("<Down>",self.down_pressed)
        self.bind("<Return>",self.enter_pressed)

        # Window setup
        #self.iconphoto(ICON)
        self.minsize(1000,720)
        self.geometry("1000x720")
        self.title("Discovery Responses")
        self.win=None # Extra popup window

        # Attributes
        self.files=[]
        self.current_file = ""
        self.reqs=[]
        self.req_type=""
        self.prev_type=""
        self.current_req=0
        self.doc_details=None
        self.objections = open_objections()
        self.PDF_ICON=tk.CTkImage(Image.open("assets/pdf.png"),size=(16,16))

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

    # Select a save from files
    def select_save(self):
        #Need to get the correct file location and then save
        filename=tk.filedialog.asksaveasfilename(filetypes=(("DOCX","*.docx"),('All files', '*.*')))
        self.save(filename)

    #Opens a window to select a folder
    def select_folder(self):
        filename = tk.filedialog.askdirectory(
            title='Open Folder')
        added=False
        for f in os.listdir(filename):
            if len(f)>4:
                if f[-4:]==".pdf":
                    if os.path.exists(filename+"/"+f):
                        self.open_file(filename+"/"+f)
                        added=True
        if added:# Set the file if been added!
            self.title("Discovery Responses   |   "+str(self.files[-1].name.split("/")[-1]))
            self.current_file=self.files[-1]
            self.set_request(self.reqs[0])
            # Add file
            self.requests_frame.show_files(self.files)
            self.requests_frame.show_list(self.reqs)
            self.update()

    #Opens a window to select a file
    def select_file(self):
        filetypes = (
            ('PDF files', '*.pdf'),
            ("Discovery Saves","*.obj"),
            ('All files', '*.*')
        )
        filename = tk.filedialog.askopenfilename(
            title='Open PDF file',
            filetypes=filetypes)

        if os.path.exists(filename):
            self.title("Discovery Responses   |   "+str(filename.split("/")[-1]))

            if filename[-4:]==".pdf":#PDF
                self.open_file(filename)
            else:#OBJ
                self.load_file(filename)

            #Else if a obj
            self.current_file=self.files[-1]
            self.set_request(self.reqs[0])
            # Add file
            self.requests_frame.show_files(self.files)
            self.requests_frame.show_list(self.reqs)
            self.update()


    #Opens a PDF file
    def open_file(self,filename):
        if os.path.exists(filename):
            reqs,req_type,doc_details = cnv.getRequests(filename)
            self.set_type(req_type)# Sets the current type
            self.doc_details = doc_details
            self.reqs=[]
            #Redraw for production
            self.response_frame.redraw(self.req_type)
            c=0
            for i in reqs:
                self.reqs.append(Request(i,"",c,self))
                self.auto_check(self.reqs[-1])
                c+=1
            self.files.append(File(filename,doc_details,self.req_type,self.reqs,self))

    # Auto checks off some objections if certain conditions are met
    def auto_check(self,request):
        #If ' all ' #ANY CASE!
        if ' ALL ' in request.req.upper():
            #Tick off Overbroad, Speculation
            pass
            if 'CONTEND' in request.req.upper() or 'CONTENTION' in request.req.upper():
                pass
                #Tick off premature
        # AND 'contend' or 'contention'

    #JUST ADDED
    # Set a request to submitted
    def submit(self):
        if self.current_req!=0:
            self.current_req.color="#50C878"
            self.requests_frame.show_list(self.reqs)
            #Go to next request
            index = self.reqs.index(self.current_req)
            if index<len(self.reqs)-1:
                self.set_request(self.reqs[index+1])

    # Clear a full request
    def clear(self):
        if self.current_req!=0:
            #Reset Color
            self.current_req.color="white"
            #Reset Response
            self.current_req.resp=""
            #Reset Checkboxes & Params
            for i in self.current_req.opts:
                i.selected=0
                i.param=""
            #Reset boxes
            self.response_frame.response_text.delete("0.0","end")
            self.objections_frame.redraw(self.current_req)
            self.requests_frame.show_list(self.reqs)
            #Reset RFP
            if self.req_type=="RFP":
                self.response_frame.resp_option.set("Available")
                self.response_frame.resp_text.delete(0,"end")
            self.update()

    def check(self):
        if self.current_req!=0:
            self.current_req.color="#FF0000"
            self.requests_frame.show_list(self.reqs)
            #Go to next request
            index = self.reqs.index(self.current_req)
            if index<len(self.reqs)-1:
                self.set_request(self.reqs[index+1])


    # Save as a word DOCX
    def save(self,filename):
        if self.current_file!="":#ADD CORRECT SAVING HERE!!!!
            reqs=[]
            resps=[]
            for r in self.reqs:#Get responses and requests
                #1. ADD REQUESTS
                reqs.append(r.req)
                #2. ADD RESPONSES
                full_text = self.get_objections(r.opts)
                #Add response to the end
                if self.req_type == "RFP":
                    option = r.RFP_option
                    txt = r.RFP_text
                    end = RFP_responses[option].replace("[VAR]",txt)
                else:
                    end = r.resp
                full_text = full_text+end
                resps.append(full_text)
            cnv.updateDOC(reqs,resps,self.doc_details,self.req_type,str(filename))

    def refresher(self):
        #Always update the 
        if self.current_req!=0:
            # Update Objections Box
            self.set_req_obj(self.current_req)
            temp = self.response_frame.objection_text.get("0.0","end")
            text = self.get_objections(self.current_req.opts)
            if text!=temp.replace("\n",""):
                #If text has changed
                self.response_frame.objection_text.configure(state="normal")
                self.response_frame.objection_text.delete("0.0","end")
                self.response_frame.objection_text.insert("0.0",text)
                self.response_frame.objection_text.configure(state="disabled")

            # Update Response Box
            if self.req_type=="RFP":
                self.response_frame.response_text.configure(state="normal")
                self.response_frame.response_text.delete("0.0","end")
                #Enter here
                option = self.response_frame.resp_option.get()
                resp = self.response_frame.resp_text.get()

                text = RFP_responses[option].replace("[VAR]",resp)
                self.response_frame.response_text.insert("0.0",text)

                self.response_frame.response_text.configure(state="disabled")
            else:
                #Do AUTOFILLS HERE
                resp = self.response_frame.response_text.get("0.0","end").replace("\n","")
                temp = resp
                resp = " "+str(resp)
                for fill in AUTOFILLS:# Replace all autofill phrases
                    resp = resp.replace(fill,AUTOFILLS[fill])
                resp = resp[1:]
                if temp!=resp:# If it has changed
                    self.response_frame.response_text.delete("0.0","end")
                    self.response_frame.response_text.insert("0.0",resp)

        self.after(100, self.refresher)


    def up_pressed(self,e):
        if self.current_req!=0:
            index = self.reqs.index(self.current_req)
            index = max(0,index-1)
            self.set_request(self.reqs[index])
    def down_pressed(self,e):
        if self.current_req!=0:
            index = self.reqs.index(self.current_req)
            index = min(len(self.reqs)-1,index+1)
            self.set_request(self.reqs[index])
    def enter_pressed(self,e):
        self.submit()


    def set_file(self,file):
        #NEED TO CHANGE THINGS HERE TOO!!!
        self.current_file = file
        self.doc_details = file.details
        self.reqs = file.reqs
        # Set is built for a single request type, need to change for files
        self.set_type(file.req_type)# Set first so refresher doesn't overwrite
        self.set_request(file.current_req)
        self.requests_frame.show_files(self.files)
        self.response_frame.redraw(file.req_type)
        self.title("Discovery Responses   |   "+str(file.name.split("/")[-1]))


    def set_request(self,req):
        #THIS SHOULD SET THE CURRENT REQ!

        # 1. SAVING PREVIOUS RESPONSE
        if self.current_req!=0:

            # Saving
            self.current_req.resp = self.response_frame.response_text.get("0.0","end").replace("\n","")
            #GET RFP data
            if self.prev_type=="RFP":
                self.current_req.RFP_option=self.response_frame.resp_option.get()
                self.current_req.RFP_text=self.response_frame.resp_text.get()



            #COLOR#########################################
            grey=False
            if self.current_req.resp.replace("\n","")!="" and self.req_type!="RFP":
                grey=True
            elif (self.current_req.RFP_option!="Available" or len(self.current_req.RFP_text)>0):
                grey=True
            for i in range(len(req.opts)):
                #Set Check
                self.current_req.opts[i].selected=self.objections_frame.opts[i].get()
                if self.objections_frame.opts[i].get()!=0:
                    grey=True
                #Set Param
                self.current_req.opts[i].param=self.objections_frame.params[i].get()
                if self.objections_frame.params[i].get()!="":
                    grey=True
            if self.current_req.color!="#FF0000" and self.current_req.color!="#50C878":
                if grey:
                    self.current_req.color="grey" 
                else:
                    self.current_req.color="white"
            ################################################
        # 2. ENTERING NEW RESPONSE INTO FRAME
        self.current_req=req
        self.current_file.current_req=req# Set the current req of the file
        #Save,Reset and add text
        self.response_frame.request_text.configure(state="normal")
        self.response_frame.request_text.delete("0.0","end")
        self.response_frame.request_text.insert("0.0",req.req)
        self.response_frame.request_text.configure(state="disabled")
        self.response_frame.request_label.configure(text="REQUEST NO. "+str(req.no+1)+":")



        #Response text
        self.response_frame.response_text.configure(state="normal")
        self.response_frame.response_text.delete("0.0","end")
        self.response_frame.response_text.insert("0.0",req.resp)
        #RFP
        if self.req_type=="RFP":
            self.response_frame.resp_option.set(req.RFP_option)
            self.response_frame.resp_text.delete(0,"end")
            self.response_frame.resp_text.insert(0,req.RFP_text)

        #Change the objections list!
        self.objections_frame.redraw(req)
        self.requests_frame.show_list(self.reqs)#Redraw the buttons
        self.set_type(self.req_type)
        self.update()   

    def set_req_obj(self,req):
        for i in range(len(req.opts)):
            #Set Check
            self.current_req.opts[i].selected=self.objections_frame.opts[i].get()
            #Set Param
            self.current_req.opts[i].param=self.objections_frame.params[i].get() 

    #SPECIAL WINDOW
    def cancel_win(self):
        self.win.destroy()
        self.win=None

    def save_win(self):
        self.doc_details["county"] = self.win.county.get("0.0","end").replace("\n","")
        self.doc_details["case_number"] = self.win.case.get("0.0","end").replace("\n","")
        self.doc_details["document"] = self.win.document.get("0.0","end").replace("\n","")
        self.doc_details["plaintiff"] = self.win.plaintiff.get("0.0","end").replace("\n","")
        self.doc_details["defendant"] = self.win.defendant.get("0.0","end").replace("\n","")
        self.cancel_win()

    # View and edit the details of the document
    def view_details(self):
        if self.current_file!="":
            if self.win!=None:
                self.win.destroy()
                self.win=None
            self.win = Detail(self)
            self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
            self.win.mainloop()



    def get_objections(self,opts):
        #Add all objections
        full_text = "Objections. "
        objs=[]
        for obj in opts:
            if obj.selected==1:
                objs.append([obj.key,obj.param])
        if len(objs)>0:
            for key in list(self.objections.keys()):
                # This will put it in order!
                for obj in objs:# For each objection
                    if key==obj[0]:
                        text=self.objections[key]
                        if text=="":
                            text=key
                        text = text.replace("[VAR]",obj[1])# Replace [VAR]
                        full_text = full_text+str(text)+". "#A dd new text!

            #Add final text
            if full_text!="" and ((self.req_type!="RFP" and len(self.response_frame.response_text.get("0.0","end").replace("\n",""))>0) or (self.req_type=="RFP" and len(self.response_frame.resp_text.get())>0)):#Response and not RFP. Resp and RFP
                final_text = "Notwithstanding the foregoing objections and subject thereto, Responding Party responds as follows: "
                extra = ""
                for obj in objs:
                    if obj[0] in alter_scope:
                        final_text = "Notwithstanding the foregoing objections and subject thereto, and as Responding Party understands the proper scope and/or meaning of this request, Responding Party responds as follows: "
                    elif obj[0]=="Compilation":
                        extra = "Responding Party exercises their right to produce writings in response to this interrogatory, pursuant to California Code of Civil Procedure section 2030.230. Please see [VAR] produced concurrently herewith. ".replace("[VAR]",obj[1])
                final_text = final_text + extra
                full_text = full_text + final_text
            return full_text

        return ""

    def create_window(self):
        create_window()

    
    #SAVING AND LOADING WITH PICKLE
    # Save the current file 
    def save_file(self):
        # Select a folder and save name
        filename=tk.filedialog.asksaveasfilename(filetypes=(("Discovery Save File","*.obj"),('All files', '*.*')))
        file = open(filename+".obj","wb")
        # Remove master from the save
        self.current_file.set_master(None)
        # Pickle the current File
        pickle.dump(self.current_file,file)
        # Add the master back
        self.current_file.set_master(self)

    def load_file(self,filename):
        # Create file obj
        file = open(filename,"rb")
        # Load the file object
        save_obj = pickle.load(file)
        # Set the new master to this window
        save_obj.set_master(self)
        # Add the object to the list of open files
        self.files.append(save_obj)
        # Set the current file as this obj
        self.set_file(save_obj)








# FUNCTIONS 
############################################################################################################

# Opens the objections file
def open_objections():# Return API key from file if possible
    if os.path.exists("assets/objections.json"):
        with open('assets/objections.json', 'r') as file:
            data = json.load(file)
        return data
    return None





# MAIN LOOP
############################################################################################################

def create_window():
    App(root)
    root.mainloop()


if __name__ == "__main__":
    #CONSTANTS
    alter_scope=["Unintelligible as written","Not limited in time and scope","Vague and ambiguous","Speculation","Overbroad"]
    RFP_responses={"Available":"Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
                    "Not Exist":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist. Any responsive documents are believed to be in the possession, custody, or control of [VAR].",
                    "Not Possessed":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party. Any responsive documents are believed to be in the possession, custody, or control of [VAR].",
                    "Lost":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen. Any responsive documents are believed to be in the possession, custody, or control of [VAR]."}
    AUTOFILLS={" rp ":" Responding Party ",
                " rpib ":" Responding Party is informed and believes ",
                " dic ":" Discovery continues and Responding Party reserves the right to supplement this response with later acquired information. "}
    #APPLICATION UTILITY SETUP
    tk.set_appearance_mode("dark")
    root=tk.CTk()
    root.withdraw()
    create_window()









# CHANGES
############################################################################################################


# Add submit file button
# Number files

# Scoll to submitted request
# Reset scroll wheel when changing file!
# Fix glitch on file change and loading folders/files

# Darkmode button!

# Add saving and loading of the workspace
# Need to save with italics included
# Add date to docx

# Make performance of arrows better
# Add method like show_list which just updates one. Have it only update them!

# Compilation needs 2 boxes!
# Add prompt if not all done
# Fix request having other doc info
# Fix broken chars
# Remove extra data from details
# Add tooltips
# Add help section

# Clean all code
