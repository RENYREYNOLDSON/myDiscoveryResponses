###### APP
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023
###### Uses converter.py to open discovery request PDF's in order to respond
###### Provides a Windows GUI tool for opening files and saving as DOCX
###### Version 4.0 | 05/09/2023

# Rules for clean code space
# 1. Use snake_case unless a class name (then camel case)
# 2. Comment everything!
# 3. If possible make something a simple & standard function
# 4. Break everything down into small components and files
# 5. ROOT->Main Windows->Each can have 1 sub window


# IMPORTS
############################################################################################################

import converter as cnv
from windows import *
from frames import *
from objects import *
from functions import *
from functions import *
import customtkinter as tk
import json,os
import pickle
from threading import Thread
import re

# MAIN WINDOW CLASS
############################################################################################################

# MAIN WINDOW CLASS
class App(tk.CTkToplevel):
    #CONSTRUCTOR 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        # CLASS ATTRIBUTES
        self.master=master#Master is root of the program (Top level tk)
        master.call()
        self.files=[]#Holds all open files
        self.clients=[]
        self.reqs=[]#Holds all requests in the selected file

        self.current_client = ""
        self.current_file = ""#Current selected file
        self.quick_save_file=""#Current quick save option
        self.req_type=""#Type of the current request
        self.prev_type=""#Type of the previous request
        self.current_req=0#Currently selected request
        self.doc_details=None#Dict of the document details

        self.objections = open_objections()#Get the list of objections
        self.get_auto_objections()#Set the autofill objections dict
        self.win=None#Container for the pop out window

        # WINDOW SETUP
        self.wm_iconbitmap("assets/icon.ico")#Icon
        self.minsize(1050,720)#Min Size
        self.geometry("1050x720")#Start size
        self.title("myDiscoveryResponses")#Window title
        self.after(100, self.refresher)

        # KEY BINDINGSS
        self.bind("<Up>",self.up_pressed)
        self.bind("<Down>",self.down_pressed)
        self.bind("<Return>",self.enter_pressed)
        self.bind("<Escape>",self.escape_pressed)
        self.bind("<Button-1>",self.mouse_pressed)
        self.protocol("WM_DELETE_WINDOW", self.exit_window)

        # POPULATE WINDOW WITH OBJECTS
        self.populate_window()
        

    ### WINDOW UTILITY
    ########################################################################################################

    #Add Frames to the window
    def populate_window(self):
        # Navigation Bar Frame
        self.bar_frame = Bar_Frame(master=self,corner_radius=0,fg_color="#161616")
        self.bar_frame.pack(padx=0,pady=0,fill="both")
        # Requests Frame
        self.requests_frame = Requests_Frame(master=self,corner_radius=0,width=100)
        self.requests_frame.pack(padx=0,pady=0,expand=False,side="left",fill="both")


        # Objections Frame
        self.objections_frame = Objections_Frame2(master=self,corner_radius=0,width=250)
        self.objections_frame.pack(padx=0,pady=0,expand=False,side="right",fill="both")

        # Response Frame
        self.response_frame = Response_Frame(master=self)
        self.response_frame.pack(padx=20,pady=20,expand=True,side="left",fill="both")

        self.set_theme("text")#Set theme just for text, as main theme loaded at start
        
    # Create a new MAIN window
    def create_window(self):
        create_window(self.master)

    # REFRESH WINDOW PERIODICALLY, (MUST BE EFFICIENT FOR PERFORMANCE)
    def refresher(self):
        if self.current_req!=0:
            # 1. UPDATE OBJECTION TEXTBOX
            #Set the current objection parameters
            if self.current_req.current_objection!="":
                self.current_req.current_objection.param = self.objections_frame.objection_input.get()
                self.current_req.current_objection.additional_param = self.objections_frame.additional_input.get()

            temp = self.response_frame.objection_text.get("0.0","end")#Get prev text from box
            remove_end=False
            if not ((self.req_type!="RFP" and len(self.response_frame.response_text.get("0.0","end").replace("\n",""))>0) or (self.req_type=="RFP" and len(self.response_frame.resp_text.get())>0)):
                remove_end = True
            text = self.get_objections(self.current_req.opts,remove_end)#Get objections with no end if text in response
            if text!=temp.replace("\n",""):#If the text has changed REDRAW
                self.response_frame.objection_text.configure(state="normal")
                self.response_frame.objection_text.delete("0.0","end")
                self.response_frame.objection_text.insert("0.0",text)
                self.response_frame.objection_text.configure(state="disabled")

            # 2. UPDATE RESPONSE TEXTBOX
            if self.req_type=="RFA":
                option = self.response_frame.resp_optionRFA.get()
            else:
                option = self.response_frame.resp_option.get()
            
            # RFP
            if self.req_type=="RFP" and option!="Custom":
                temp = self.response_frame.response_text.get("0.0","end")#Get prev text from box
                resp = self.response_frame.resp_text.get()
                text = RFP_responses[option].replace("[VAR]",resp)
                if option!="Available" and resp!="":
                    text = (text+RFP_EXTRA).replace("[VAR]",resp)
                if text!=temp.replace("\n",""):#If the text has changed REDRAW
                    #Change response text
                    self.response_frame.response_text.configure(state="normal")
                    self.response_frame.response_text.delete("0.0","end")
                    self.response_frame.response_text.insert("0.0",text)
                    self.response_frame.response_text.configure(state="disabled")
                    #Change color of request
                    self.current_req.color="grey"
                    self.current_client.current_file.color=("black","white")
                    self.requests_frame.update_files(self.current_client.files)
            # RFA
            elif self.req_type=="RFA" and option!="Custom":
                temp = self.response_frame.response_text.get("0.0","end")#Get prev text from box
                text = RFA_responses[option]
                if text!=temp.replace("\n",""):#If the text has changed REDRAW
                    #Change response text
                    self.response_frame.response_text.configure(state="normal")
                    self.response_frame.response_text.delete("0.0","end")
                    self.response_frame.response_text.insert("0.0",text)
                    self.response_frame.response_text.configure(state="disabled")
                    #Change color of request
                    self.current_req.color="grey"
                    self.current_client.current_file.color=("black","white")
                    self.requests_frame.update_files(self.current_client.files)


            # NORMAL
            else:#If NOT RFP
                #Do AUTOFILLS HERE
                insert_index = self.response_frame.response_text.index(tk.INSERT)#Current index
                resp = " "+self.response_frame.response_text.get("0.0","end-1c")#Current response text
                use_fill=None
                use_pos=0
                start=0
                for fill in AUTOFILLS:# Replace all autofill phrases
                    position = -1
                    position = resp.find(fill)#Pos of index
                    if position<0:
                        position = resp.find("\n"+fill[1:])# Try new line instances
                        if position>=0:
                            start=1
                    if position>=0:
                        use_fill = fill# Set this to fill
                        use_pos = position
                if use_fill!=None:# IF AN AUTOFILL USED
                    text = resp[1:]#Remove space
                    # Update index if grown in length, must add suffic n + chars
                    text_index="0.0 + "+str(use_pos)+" chars"
                    text_end_index="0.0 + "+str(use_pos+len(use_fill)-1)+" chars"
                    # Put the text here 
                    self.response_frame.response_text.delete(text_index,text_end_index)
                    self.response_frame.response_text.insert(text_index,AUTOFILLS[use_fill][start:])
                    # Reset index
                    insert_index+=" + "+str(len(AUTOFILLS[use_fill])-len(use_fill)+1)+" chars"
                    self.response_frame.response_text.mark_set("insert",insert_index)
                if resp[1:]!=self.current_req.resp.replace("\n",""):# Change colour back if edited
                    self.current_req.color="grey"
                    self.current_client.current_file.color=("black","white")
                    self.requests_frame.update_files(self.current_client.files)
        self.after(100, self.refresher)#REFRESH AGAIN

    #Destroy this windows sub window
    def cancel_win(self):
        if self.win!=None:
            self.win.destroy()
            self.win=None

    # Save details from the details window
    def save_win(self):
        self.doc_details["county"] = self.win.county.get("0.0","end").replace("\n","")
        self.doc_details["case_number"] = self.win.case.get("0.0","end").replace("\n","")
        self.doc_details["document"] = self.win.document.get("0.0","end").replace("\n","")
        self.doc_details["plaintiff"] = self.win.plaintiff.get("0.0","end").replace("\n","")
        self.doc_details["defendant"] = self.win.defendant.get("0.0","end").replace("\n","")
        self.cancel_win()

    # View and edit the details of the document
    def view_details(self):
        if self.current_client!="":
            self.cancel_win()
            self.win = Detail(self)
            self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
            self.win.mainloop()

    # View and edit the OBJECTIONS JSON
    def view_objections(self):
        self.cancel_win()
        self.win = EditObjections(self)
        self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
        self.win.mainloop()

    # View and edit the theme of the software
    def view_hotkeys(self):
        self.cancel_win()
        self.win = Hotkeys(self)
        self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
        self.win.mainloop()

    # View and edit the theme of the software
    def view_theme(self):
        self.cancel_win()
        self.win = Theme(self)
        self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
        self.win.mainloop()

    # View a text preview of the objections+response
    def view_preview(self):
        if self.current_client!="":
            self.cancel_win()
            # Create a temporary docx
            self.export(self.current_client.current_file,"assets/temp")
            self.win = Preview(self)
            self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
            self.win.mainloop()

    # View a DOCX preview of the output file
    def preview_text(self):
        if self.current_client!="":
            self.cancel_win()
            self.win = PreviewText(self)
            self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
            self.win.mainloop()

    # Exit this window and delete
    def exit_window(self):
        self.destroy()
        c=0
        for w in root.winfo_children():
            c+=1
        if c==0:
            root.destroy()


    ### KEY PRESSES
    ########################################################################################################

    # If up arrow
    def up_pressed(self,e):
        #If focus is app
        if self.current_req!=0 and self.focus_get()==self:
            index = self.reqs.index(self.current_req)
            index = max(0,index-1)
            self.set_request(self.reqs[index])
            self.requests_frame.scroll_to()

    # If down arrow
    def down_pressed(self,e):
        #If focus is app
        if self.current_req!=0 and self.focus_get()==self:
            index = self.reqs.index(self.current_req)
            index = min(len(self.reqs)-1,index+1)
            self.set_request(self.reqs[index])
            self.requests_frame.scroll_to()

    #If enter
    def enter_pressed(self,e):
        #If focus is app
        if self.current_req!=0 and self.focus_get()==self:
            self.submit()

    #If escape
    def escape_pressed(self,e):
        self.focus_set()

    #Get mouse press and set focus!
    def mouse_pressed(self,e):
        if "ctktextbox" not in str(e.widget) and "ctkentry" not in str(e.widget):
            self.focus_set()




    ### SAVING AND LOADING OF FILES & FOLDERS
    ########################################################################################################




    # Open a folder of files
    def select_folder(self):
        filename = tk.filedialog.askdirectory(
            title='Open Folder')
        if filename=="":
            return
        added=False
        for f in os.listdir(filename):
            if len(f)>4:
                if f[-4:]==".pdf":
                    if os.path.exists(filename+"/"+f):
                        self.open_file(filename+"/"+f)
                        added=True
        if added:# Set the file if been added!
            self.title("myDiscoveryResponses   |   "+str(self.current_client.files[-1].name.split("/")[-1]))
            self.current_client.current_file=self.current_client.files[-1]
            # Add file
            self.requests_frame.show_clients(self.clients)
            if self.current_client!="":
                self.requests_frame.show_files(self.current_client.files)
            self.requests_frame.show_list(self.reqs)
            self.set_request(self.reqs[0])
            self.requests_frame.scroll_to(True)
            self.update()

    # Open a single file
    def select_file(self):
        filetypes = (
            ('Files', '*.pdf *.discovery'),
            ('All files', '*.*')
        )
        filenames = tk.filedialog.askopenfilenames(
            title='Open PDF file',
            filetypes=filetypes)

        for filename in filenames:
            if os.path.exists(filename):
                if filename[-4:].lower()==".pdf":#PDF
                    self.title("myDiscoveryResponses   |   "+str(filename.split("/")[-1]))
                    self.open_file(filename)
                    #Else if a obj
                    self.current_client.current_file =self.current_client.files[-1]
                    # Add file
                    self.requests_frame.show_clients(self.clients)
                    if self.current_client!="":
                        self.requests_frame.show_files(self.current_client.files)
                    self.requests_frame.show_list(self.reqs)
                    self.set_request(self.reqs[0])
                    self.requests_frame.scroll_to(True)
                    self.update()
                elif filename[-10:]==".discovery":#OBJ
                    self.load_file(filename)

    # Opens a PDF file specifically
    def open_file(self,filename):
        if os.path.exists(filename):
            reqs,req_type,doc_details = cnv.getRequests(filename)
            self.set_type(req_type)# Sets the current type
            self.doc_details = doc_details
            self.reqs=[]
            #Redraw for production
            self.response_frame.redraw(self.req_type)
            if req_type=="FROG":
                c=0
                for i in FROGS:
                    if i in reqs and "(" not in i:
                        new = Request(FROGS[i],"",c,self,req_type,i)
                        self.reqs.append(new)
                    c+=1
            else:
                c=0
                for i in reqs:
                    self.reqs.append(Request(i,"",c,self,req_type,""))
                    c+=1

            ### ADD NEW FILE TO CLIENT, IF NONE THEN CREATE NEW CLIENT!
            new_file = File(filename,doc_details,self.req_type,self.reqs,self)
            for c in self.clients:
                if c.name.replace(" ","").upper() == doc_details["defendant"].replace(" ","").upper():
                    # Add to a current client
                    c.files.append(new_file)
                    self.set_client(c)
                    return
            self.clients.append(Client(doc_details["defendant"],[new_file],self))
            self.set_client(self.clients[-1])


    #SAVING AND LOADING WITH PICKLE
    # Save the current file 
    def save_file(self):
        # Select a folder and save name
        filename=tk.filedialog.asksaveasfilename(title="Save Current File",filetypes=(("Discovery Save File","*.discovery"),('All files', '*.*'))).replace(".discovery","")
        if filename=="":
            return
        file = open(filename+".discovery","wb")
        # Set this for quicksave
        self.current_client.current_file.save = filename
        # Remove master from the save
        self.current_client.current_file.set_master(None)
        # Create save object
        save_obj = Save([self.current_file])
        # Pickle the current File
        pickle.dump(save_obj,file)#Need to fix saving with the name
        # Add the master back
        self.current_client.current_file.set_master(self)

    # Load a single obj file
    def load_file(self,filename):
        # Create file obj
        file = open(filename,"rb")
        # Load the file object
        save_obj = pickle.load(file)
        # Get files array
        files = save_obj.files
        if len(files)==1:# If just a saved file
            # Set this for quicksave
            files[0].save = filename
            files[0].set_master(self)
            self.current_client.files.append(files[0])
            # Add file
            self.requests_frame.show_clients(self.clients)
            if self.current_client != "":
                self.requests_frame.show_files(self.current_client.files)
            self.set_file(files[0])
            self.requests_frame.show_list(self.reqs)
            self.requests_frame.scroll_to(True)
            self.requests_frame.scroll_to_file()
            self.update()
        else:
            if len(self.current_client.files)==0:#Use this window!
                # Set this for quicksave
                self.quick_save_file = filename.replace(".discovery","")
                for f in files:
                    # Set the new master to this window
                    f.set_master(self)
                    # Add the object to the list of open files
                    self.current_client.files.append(f)

                #Else if a obj
                # Add file
                self.requests_frame.show_clients(self.clients)
                if self.current_client != "":
                    self.requests_frame.show_files(self.current_client.files)
                #Set current file as this object
                self.set_file(self.current_client.files[0])
                self.requests_frame.show_list(self.reqs)
                self.requests_frame.scroll_to(True)
                self.requests_frame.scroll_to_file()
                self.update()
            else:#New Window!
                load_window(self.master,files,filename)


    # Save all open files together
    def save_workspace(self):
        # Select a folder and save name
        filename=tk.filedialog.asksaveasfilename(title="Save Full Set",filetypes=(("Discovery Save File","*.discovery"),('All files', '*.*'))).replace(".discovery","")
        print(filename)
        if filename=="":
            return
        file = open(filename+".discovery","wb")
        # Set this for quicksave
        self.quick_save_file = filename
        # Remove master from the save
        for i in self.current_client.files:
            i.set_master(None)
        # Create save object
        save_obj = Save(self.current_client.files)
        # Pickle the current File
        pickle.dump(save_obj,file)#Need to fix saving with the name
        # Add the master back
        for i in self.current_client.files:
            i.set_master(self)

    #Save the file/folder quickly using the last operation
    def quick_save(self):
        if self.current_client=="":#Exit if no valid file
            return
        filename = self.quick_save_file
        if filename=="" and self.current_client.current_file.save=="":
            self.save_file()
        elif self.current_client.current_file.save!="":#single or multi
            #Save the single file
            file = open(self.current_client.current_file.save+".discovery","wb")
            # Remove master from the save
            self.current_client.current_file.set_master(None)
            # Create save object
            save_obj = Save([self.current_client.current_file])
            # Pickle the current File
            pickle.dump(save_obj,file)#Need to fix saving with the name
            # Add the master back
            self.current_client.current_file.set_master(self)
        else:#If multi file
            file = open(filename+".discovery","wb")
            # Remove master from the save
            for i in self.current_client.files:
                i.set_master(None)
            # Create save object
            save_obj = Save(self.current_client.files)
            # Pickle the current File
            pickle.dump(save_obj,file)#Need to fix saving with the name
            # Add the master back
            for i in self.current_client.files:
                i.set_master(self)


    #Close the current file
    def close_file(self):
        #Try go to previous file, else close all
        if len(self.current_client.files)>1:
            # Set to different request
            # Remove this request
            index = self.current_client.files.index(self.current_client.current_file)
            if index==0:
                new_req_index=1
            else:
                new_req_index = index-1
            self.set_file(self.current_client.files[new_req_index])
            #Remove prev and update files
            self.current_client.files.pop(index)
            self.requests_frame.show_clients(self.clients)
            if self.current_client != "":
                self.requests_frame.show_files(self.current_client.files)
            self.requests_frame.show_list(self.reqs)
            self.requests_frame.scroll_to(True)
            self.requests_frame.scroll_to_file()
        else:
            self.close_all()

    #Close all files open in the workspace
    def close_all(self):
        # Attributes
        self.files=[]
        self.current_file = ""
        self.reqs=[]
        self.req_type=""
        self.prev_type=""
        self.current_req=0
        self.doc_details=None
        self.quick_save_file=""
        self.clients=[]
        self.current_client=""
        # Reset Clients
        self.requests_frame.show_clients([])
        # Reset Files
        self.requests_frame.show_files([])
        # Reset Requests
        self.requests_frame.show_list([])
        # Reset Response
        self.response_frame.reset()
        #Reset Objections
        self.objections_frame.reset()



    ### EXPORTING AS DOCX
    ########################################################################################################


    

    # Export a file as DOCX
    def export(self,file,filename):
        reqs=[]
        resps=[]
        numbers=[]
        for r in file.reqs:#Get responses and requests
            #1. ADD REQUESTS
            reqs.append(r.req)
            #2. ADD RESPONSES
            full_text = r.get_full_resp()
            resps.append(full_text)
            #3. ADD NUMBER POINTERS
            numbers.append(r.custom_key)
        cnv.updateDOC(reqs,resps,file.details,self.req_type,str(filename),numbers)

    # Export all as folder of DOCX's
    def export_all(self):
        if len(self.current_client.files)>0:
            # Select Folder
            filename = tk.filedialog.askdirectory(title='Select Export Folder')
            # For each file
            for file in self.current_client.files:
                self.export(file,filename+"/"+str(file.name.split("/")[-1].split(".")[0]))

    # Select a save from files
    def export_current(self):
        #Need to get the correct file location and then save
        if self.current_client!="":
            filename=tk.filedialog.asksaveasfilename(filetypes=(("DOCX","*.docx"),('All files', '*.*')))
            self.export(self.current_client.current_file,filename)



    ### SETTING AND GETTING OBJECTS
    ########################################################################################################

    #Change an objection buttons state, and if request then update this
    def toggle_objection(self,obj):
        if self.current_req!=0:
            # Update current request objection
            for o in self.current_req.opts:
                if o.key == obj:
                    o.toggle()
                    self.current_req.current_objection = o
                    self.objections_frame.update_current(o)
                    #Set the objection input area to this objection

            # Update buttons
            self.objections_frame.toggle_button(obj)#TOGGLE THE COLOUR OF THIS BUTTON!
            # Update objection special menu





    #Allow for custom response when buttons used
    def setRFP(self,value):
        if value=="Custom":
            self.response_frame.response_text.configure(state="normal")
            self.response_frame.response_text.delete("0.0","end")

    def setRFA(self,value):
        if value=="Custom":
            self.response_frame.response_text.configure(state="normal")
            self.response_frame.response_text.delete("0.0","end")

    #Get objections
    def get_auto_objections(self):#Get and set the current objection file
        self.auto_objections = get_auto_objections_JSON()

    #Set objections on sumbit using the current request opts
    def set_auto_objections(self):
        dic = self.auto_objections
        for i in self.current_req.opts:
            if i.key in self.auto_objections:#If in the auto objections
                vals=re.findall("[\"‘][ a-zA-Z1-9]+[\"’]",i.param)
                for v in vals:
                    v2 = v[1:-1]
                    if v2 not in dic[i.key]:
                        dic[i.key].append(v2)#Add new autos to the dict
        set_auto_objections_JSON(dic)
        self.auto_objections = dic#Save JSON and update current autos

    # Set type of request and save previous also
    def set_type(self,req_type):
        if self.prev_type=="":
            self.prev_type = req_type
        else:
            self.prev_type = self.req_type
        self.req_type = req_type 


    # Set the current client
    def set_client(self,client):
        self.current_client = client
        self.requests_frame.show_clients(self.clients)
        self.set_type(self.current_client.current_file.req_type)
        self.doc_details = self.current_client.current_file.details
        self.reqs = self.current_client.current_file.reqs

        self.requests_frame.show_files(self.current_client.files)
        self.requests_frame.show_list(self.current_client.current_file.reqs)
        self.set_request(self.current_client.current_file.current_req)
        #self.requests_frame.scroll_to(True)
        self.response_frame.redraw(self.current_client.current_file.req_type)
        self.title("myDiscoveryResponses   |   "+str(self.current_client.current_file.name.split("/")[-1]))

    # Set the current file
    def set_file(self,file):
        #NEED TO CHANGE THINGS HERE TOO!!!
        self.current_client.current_file = file
        self.doc_details = file.details
        self.reqs = file.reqs
        # Set is built for a single request type, need to change for files
        self.set_type(file.req_type)# Set first so refresher doesn't overwrite
        self.requests_frame.update_files(self.current_client.files)
        self.requests_frame.show_list(self.current_client.current_file.reqs)
        self.set_request(file.current_req)
        #self.requests_frame.scroll_to(True)
        self.response_frame.redraw(file.req_type)
        self.title("myDiscoveryResponses   |   "+str(file.name.split("/")[-1]))

    # Set the request to a different one
    def set_request(self,req):
        # 1. SAVING PREVIOUS RESPONSE
        if self.current_req!=0:
            # Saving
            self.current_req.resp = self.response_frame.response_text.get("0.0","end-1c")#self.get_objections(self.current_req.opts,False)
            #GET RFP data
            if self.prev_type=="RFP":
                self.current_req.RFP_option=self.response_frame.resp_option.get()
                self.current_req.RFP_text=self.response_frame.resp_text.get()
            elif self.prev_type=="RFA":
                self.current_req.RFA_option=self.response_frame.resp_optionRFA.get()
            #COLOR#########################################
            grey=False
            if self.current_req.resp.replace("\n","")!="" and self.req_type!="RFP":
                grey=True
            elif (self.current_req.RFP_option!="Available" or len(self.current_req.RFP_text)>0):
                grey=True

            if self.current_req.color!="#FF0000" and self.current_req.color!="#50C878":
                if grey:
                    self.current_req.color="grey" 
                else:
                    self.current_req.color=("black","white")
            ################################################
            
        # 2. ENTERING NEW RESPONSE INTO FRAME
        if self.current_req==req:#For when I set to itself
            return
        self.current_req=req
        self.current_client.current_file.current_req=req# Set the current req of the file
        #Save,Reset and add text
        self.response_frame.request_text.configure(state="normal")
        self.response_frame.request_text.delete("0.0","end")
        self.response_frame.request_text.insert("0.0",req.req)
        # Make keywords bold
        #bold_keywords(self.response_frame.request_text,req.req)
        self.response_frame.request_text.configure(state="disabled")
        if req.custom_key!="":
            text = req.custom_key
        else:
            text = req.no+1
        self.response_frame.request_label.configure(text=self.req_type+" NO. "+str(text)+":")
        #Response text
        self.response_frame.response_text.configure(state="normal")
        self.response_frame.response_text.delete("0.0","end")
        self.response_frame.response_text.insert("0.0",req.resp)
        #RFP
        if self.req_type=="RFP":
            self.response_frame.resp_option.set(req.RFP_option)
            self.response_frame.resp_text.delete(0,"end")
            self.response_frame.resp_text.insert(0,req.RFP_text)
        elif self.req_type=="RFA":
            self.response_frame.resp_optionRFA.set(req.RFA_option)
        #Change the objections list!
        self.objections_frame.redraw(req)
        self.requests_frame.update_list(self.reqs)#Redraw the buttons
        self.set_type(self.req_type)
        self.update()   

    # Set the objection buttons for the given request
    def set_req_obj(self,req):
        for i in range(len(req.opts)):
            #Set Check
            self.current_req.opts[i].selected=self.objections_frame.opts[i].get()
            #Set Param
            self.current_req.opts[i].param=self.objections_frame.params[i].get() 











    # CREATE THE OBJECTION TEXT
    def get_objections(self,opts,remove_end=False):
        full_text = "Objection. "
        # 1. GET ALL SELECTED OBJECTIONS
        objs=[]
        for obj in opts:
            if obj.selected==1:
                objs.append(obj)

        # 2. ADD ALL SELECTED OBJECTIONS TO THE TEXT
        if len(objs)>0:
            for key in list(self.objections.keys()):# Put in order given
                for obj in objs:# For each objection
                    if key==obj.key:
                        text=self.objections[key][0]
                        if text=="":
                            text=key
                        if obj.param=="":
                            text = text.replace("[VAR]","")# Replace [VAR]
                        else:
                            text = text.replace("[VAR]"," "+obj.param)# Replace [VAR]
                        full_text = full_text+str(text)+". "#Add new text!

            # 3. ADD FINAL OBJECTION IF REQUESTED AND VALID
            if full_text!="" and remove_end==False:#Response and not RFP. Resp and RFP
                #Default values here
                final_text = "Notwithstanding the foregoing objections and subject thereto, Responding Party responds as follows: "
                extra = ""
                #Change these values if certain objections selected
                for obj in objs:
                    #Change Scope
                    if obj.alter_scope:
                        final_text = "Notwithstanding the foregoing objections and subject thereto, and as Responding Party understands the proper scope and/or meaning of this request, Responding Party responds as follows: "
                    
                    #Add Extra Text
                    text=obj.additional_text
                    if text!="":
                        if obj.additional_param=="":
                            text = text.replace("[VAR]","")# Replace [VAR]
                        else:
                            text = text.replace("[VAR]"," "+obj.additional_param)# Replace [VAR]
                        extra = extra+str(text)+". "#Add new text!
                
                
                full_text = full_text + final_text + extra
            return full_text
        return ""















    # Update the theme JSON and set the new theme
    def update_theme(self):
        # Save new theme then use set_theme
        self.win.withdraw()
        self.theme={
            "text_size":self.win.size_entry.get(),
            "text_color":self.win.text_picker.cget("text"),
            "text_bg":self.win.bg_picker.cget("text"),
            "text_font":self.win.font_entry.get(),
            "theme":self.win.theme_button.get(),
            "layout":["Requests","Responses","Objections"]
        }
        with open("assets/theme.json", "w") as outfile:#Save the new theme JSON
            json.dump(self.theme, outfile)
        self.set_theme()
        self.cancel_win()#Destroy Window

    # Open and set the theme
    def set_theme(self,param="both"):# Return API key from file if possible
        if os.path.exists("assets/theme.json"):
            with open('assets/theme.json', 'r') as file:
                self.theme = json.load(file)
            # Set relevant things here
            if param=="theme" or param=="both":
                tk.set_appearance_mode(self.theme["theme"])
            if param=="text" or param=="both":
                # Set all text areas
                font = (self.theme["text_font"],int(self.theme["text_size"]))
                #Request
                self.response_frame.response_text.configure(False,font=font,text_color=self.theme["text_color"],fg_color=self.theme["text_bg"])
                #Objection
                self.response_frame.request_text.configure(False,font=font,text_color=self.theme["text_color"],fg_color=self.theme["text_bg"])
                #Response
                self.response_frame.objection_text.configure(False,font=font,text_color=self.theme["text_color"],fg_color=self.theme["text_bg"])
                #Resp Text
                self.response_frame.resp_text.configure(font=font,text_color=self.theme["text_color"],fg_color=self.theme["text_bg"])
                #Bold tag for request
                self.response_frame.request_text.tag_config("red",font=(self.theme["text_font"],1+int(self.theme["text_size"]), 'bold'))
                self.requests_frame.show_clients(self.clients)
                if self.current_client != "":
                    self.requests_frame.show_files(self.current_client.files)
                self.requests_frame.show_list(self.reqs)
    ### USER ACTIVITY
    ########################################################################################################



    # Set a request to submitted
    def submit(self):
        if self.current_req!=0:
            #Update autos
            self.set_auto_objections()
            if self.current_req.color=="#50C878":
                self.current_req.color="grey"
            else:
                self.current_req.color="#50C878"
            self.requests_frame.update_list(self.reqs)
            
            #Go to next request
            index = self.reqs.index(self.current_req)
            if index<len(self.reqs)-1:
                self.set_request(self.reqs[index+1])

            #Scroll to this request
            self.requests_frame.scroll_to()
            # If all are green set file green!
            for req in self.reqs:
                if req.color!="#50C878":
                    return
            self.current_client.current_file.color="#50C878"
            self.requests_frame.update_files(self.current_client.files)


    # Copy objections from the previous request
    def copy_previous(self):
        #Copy the previous opts list, use copy maybe
        for i in range(len(self.reqs)):
            if self.reqs[i]==self.current_req:
                if i>=1:
                    # Copy the previous objections
                    for o in range(len(self.reqs[i-1].opts)):
                        #Copy selected
                        self.current_req.opts[o].selected = self.reqs[i-1].opts[o].selected
                        #Copy param
                        self.current_req.opts[o].param = self.reqs[i-1].opts[o].param
                        #Set these in the GUI
                        self.objections_frame.redraw(self.current_req)
                else:
                    return

    # Clear a full request
    def clear(self):
        if self.current_req!=0:
            #Reset Color
            self.current_req.color=("black","white")
            self.current_client.current_file.color=("black","white")
            self.requests_frame.update_files(self.current_client.files)
            #Reset Response
            self.current_req.resp=""
            #Reset Checkboxes & Params
            for i in self.current_req.opts:
                i.selected=0
                i.param=""
            #Reset boxes
            self.response_frame.response_text.delete("0.0","end")
            self.objections_frame.redraw(self.current_req)
            self.requests_frame.update_list(self.reqs)
            #Reset RFP
            if self.req_type=="RFP":
                self.response_frame.resp_option.set("Available")
                self.response_frame.resp_text.delete(0,"end")
            elif self.req_type=="RFA":
                self.response_frame.resp_optionRFA.set("Admit")
            self.update()

    # Set as Check with client
    def check(self):
        if self.current_req!=0:
            if self.current_req.color=="#FF0000":
                self.current_req.color="grey"#set grey
            else:
                self.current_req.color="#FF0000"# Set red
            self.requests_frame.update_list(self.reqs)# Update request colours
            self.current_client.current_file.color=("black","white")
            self.requests_frame.update_files(self.current_client.files)# Turn file white if green
            #Go to next request
            index = self.reqs.index(self.current_req)
            if index<len(self.reqs)-1:
                self.set_request(self.reqs[index+1])
            #Scroll to this
            self.requests_frame.scroll_to()


# WINDOW SPECIFIC FUNTIONS (cannot be elsewhere)
############################################################################################################

# Create a new window with root as parent
def create_window(root):
    App(root)

# Load a new window with files
def load_window(root,files,filename):
    # Create new window
    master=App(root)
    for f in files:
        # Set the new master to this window
        f.set_master(master)
        # Add the object to the list of open files
        master.files.append(f)
    master.requests_frame.show_clients(master.clients)
    if master.current_client != "":
        master.requests_frame.show_files(master.current_client.files)# Show files
    master.set_file(master.files[0])# Set first files request
    master.requests_frame.show_list(master.reqs)# Show requests
    master.requests_frame.scroll_to()
    master.requests_frame.scroll_to_file()
    master.quick_save_file = filename.replace(".discovery","")


# MAIN LOOP
############################################################################################################

if __name__ == "__main__":
    #CONSTANTS    
    RFP_responses={"Available":"Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
                    "Not Exist":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist.",
                    "Not Possessed":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party.",
                    "Lost":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen."}
    
    RFA_responses={"Admit":"Admit. ",
                    "Deny":"Deny. ",
                    "Lack Info":"A reasonable inquiry concerning the matter in this particular request has been made, and the information known or readily obtainable is insufficient to enable Responding Party to admit the matter."}

    AUTOFILLS={" rp ":" Responding Party ",
                " rpib ":" Responding Party is informed and believes ",
                " dic ":" Discovery continues and Responding Party reserves the right to supplement this response with later acquired information. "}
    
    RFP_EXTRA = " Any responsive documents are believed to be in the possession, custody, or control of [VAR]."

    FROGS = {"1.1":"State the name, ADDRESS, telephone number, and relationship to you of each PERSON who prepared or assisted in the preparation of the responses to these interrogatories. (Do not identify anyone who simply typed or reproduced the responses.)",
            "2.1":"State:\n(a) your name;\n(b) every name you have used in the past; and\n(c) the dates you used each name.",
            "2.2":"State the date and place of your birth.",
            "2.3":" At the time of the INCIDENT, did you have a driver's license? If so state: \n(a) the state or other issuing entity; \n(b) the license number and type; \n(c) the date of issuance; and \n(d) all restrictions.",
            "2.4":"At the time of the INCIDENT, did you have any other permit or license for the operation of a motor vehicle? If so, state:\n(a) the state or other issuing entity; \n(b) the license number and type; \n(c) the date of issuance; and \n(d) all restrictions.",
            "2.5":"State:\n(a) your present residence ADDRESS;\n(b) your residence ADDRESSES for the past five years; and\n(c) the dates you lived at each ADDRESS.",
            "2.6":"State:\n(a) the name, ADDRESS, and telephone number of your present employer or place of self-employment; and\n(b) the name, ADDRESS, dates of employment, job title, and nature of work for each employer, or self-employment you have had from five years before the INCIDENT until today.",
            "2.7":"State:\n(a) the name and ADDRESS of each school or other academic or vocational institution you have attended, beginning with high school;\n(b) the dates you attended;\n(c) the highest-grade level you have completed; and\n(d) the degrees received.",
            "2.8":"Have you ever been convicted of a felony? If so, for each conviction state:\n(a) the city and state where you were convicted;\n(b) the date of conviction;\n(c) the offense; and\n(d) the court and case number.",
            "2.9":"Can you speak English with ease?  If not, what language and dialect do you normally use?",
            "2.10":"Can you read and write English with ease?  If not, what language and dialect do you normally use?",
            "2.11":"At the time of the INCIDENT were you acting as an agent or employee for any PERSON? If so, state:\n(a) the name, ADDRESS, and telephone number of that PERSON; and\n(b) a description of your duties.",
            "2.12":"At the time of the INCIDENT did you or any other person have any physical, emotional, or mental disability or condition that may have contributed to the occurrence of the INCIDENT? If so, for each person state: \n(a) the name, ADDRESS, and telephone number;\n(b) the nature of the disability or condition; and\n(c) the manner in which the disability or condition contributed to the occurrence of the INCIDENT.",
            "2.13":"Within 24 hours before the INCIDENT did you or any person involved in the INCIDENT use or take any of the following substances: alcoholic beverage, marijuana, or other drug or medication of any kind (prescription or not)? If so, for each person state:\n(a) the name, ADDRESS, and telephone number;\n(b) the nature or description of each substance;\n(c) the quantity of each substance used or taken;\n(d) the date and time of day when each substance was used or taken;\n(e) the ADDRESS where each substance was used or taken;\n(f) the name, ADDRESS, and telephone number of each person who was present when each substance was used or taken; and\n(g) the name, ADDRESS, and telephone number of any HEALTH CARE PROVIDER who prescribed or furnished the substance and the condition for which it was prescribed or furnished.",
            "3.1":"Are you a corporation? If so, state:\n(a) the name stated in the current articles of incorporation;\n(b) all other names used by the corporation during the past 10 years and the dates each was used;\n(c) the date and place of incorporation; named insured;\n(d) the ADDRESS of the principal place of business; and \n(e) whether you are qualified to do business in California.",
            "3.2":"",
            "3.3":"",
            "3.4":"",
            "3.5":"",
            "3.6":"",
            "3.7":"",
            "4.1":"At the time of the INCIDENT, was there in effect any policy of insurance through which you were or might be insured in any manner (for example, primary, pro-rata, or excess liability coverage or medical expense coverage) for the damages, claims, or actions that have arisen out of the INCIDENT? If so, for each policy state: \n(a) the kind of coverage;\n(b) the name and ADDRESS of the insurance company;\n(c) the name, ADDRESS, and telephone number of each named insured;\n(d) the policy number;\n(e) the limits of coverage for each type of coverage contained in the policy;\n(f) whether any reservation of rights or controversy or coverage dispute exists between you and the insurance company; and\n(g) the name, ADDRESS, and telephone number of the custodian of the policy.",
            "4.2":"Are you self-insured under any statute for the damages, claims, or actions, that have arisen out of the INCIDENT? If so, specific the statute.",
            "6.1":"Do you attribute any physical, mental, or emotional injuries to the INCIDENT? (If your answer is \"no,\" do not answer interrogatories 6.2 through 6.7).",
            "6.2":"Identify each injury you attribute to the INCIDENT and the area of your body affected.",
            "6.3":"Do you still have any complaints that you attribute to the INCIDENT? If so, for each complaint state:\n(a) a description;  \n(b) whether the complaint is subsiding, remaining the same, or becoming worse; and\n(c) the frequency and duration.",
            "6.4":"Did you receive any consultation or examination (except from expert witnesses covered by Code of Civil Procedure sections 2034.210-2034.310) or treatment from a HEALTH CARE PROVIDER for any injury you attribute to the INCIDENT? If so, for each HEALTH CARE PROVIDER state:\n(a) the name, ADDRESS, and telephone number;\n(b) the type of consultation, examination, or treatment provided;\n(c) the dates you received consultation, examination, or treatment; and\n(d) the charges to date.",
            "6.5":"Have you taken any medication, prescribed or not, as a result of injuries that you attribute to the INCIDENT? If so, for each medication state:\n(a) the name;\n(b) the PERSON who prescribed or furnished it;\n(c) the date it was prescribed or furnished;\n(d) the dates you began and stopped taking it; and\n(e) the cost to date.",
            "6.6":"Are there any other medical services necessitated by the injuries that you attribute to the INCIDENT that were not previously listed (for example, ambulance, nursing, prosthetics)?  If so, for each service state:\n(a) the nature;\n(b) the date;\n(c) the cost; and\n(d) the name, ADDRESS, and telephone number of each provider.",
            "6.7":"Has any HEALTH CARE PROVIDER advised that you may require future or additional treatment for any injuries that you attribute to the INCIDENT? If so, for each injury state:\n(a) the name and ADDRESS of each HEALTH CARE PROVIDER;\n(b) the complaints for which the treatment was advised; and\n(c) the nature, duration, and estimated cost of the treatment.",
            "7.1":"Do you attribute any loss of or damage to a vehicle or other property to the INCIDENT? If so, for each item of property:\n(a) describe the property;\n(b) describe the nature and location of the damage to the property;\n(c) state the amount of damage you are claiming for each item of property and how the amount was calculated; and\n(d) if the property was sold, state the name, ADDRESS, and telephone number of the seller, the date of sale, and the sale price.",
            "7.2":"Has a written estimate or evaluation been made for any item of property referred to in your answer to the preceding interrogatory? If so, for each estimate or evaluation state:\n(a) the name, ADDRESS, and telephone number of the PERSON who prepared it and the date prepared;\n(b) the name, ADDRESS, and telephone number of each PERSON who has a copy of it; and\n(c) the amount of damage stated.",
            "7.3":"Has any item of property referred to in your answer to interrogatory 7.1 been repaired? If so, for each item state:\n(a) the date repaired;\n(b) a description of the repair;\n(c) the repair cost;\n(d) the name, ADDRESS, and telephone number of the PERSON who repaired it;\n(e) the name, ADDRESS, and telephone number of the PERSON who paid for the repair.",
            "8.1":"Do you attribute any loss of income or earning capacity to the INCIDENT? (If your answer is \"no,\" do not answer interrogatories 8.2 through 8.8).",
            "8.2":"State:\n(a) the nature of your work;\n(b) your job title at the time of the INCIDENT; and\n(c) the date your employment began.",
            "8.3":"State the last date before the INCIDENT that you worked for compensation.",
            "8.4":"State your monthly income at the time of the INCIDENT and how the amount was calculated.",
            "8.5":"State the date you returned to work at each place of employment following the INCIDENT.",
            "8.6":"State the dates you did not work and for which you lost income as a result of the INCIDENT.",
            "8.7":"State the total income you have lost to date as a result of the INCIDENT and how the amount was calculated.",
            "8.8":"Will you lose income in the future as a result of the INCIDENT? If so, state:\n(a) the facts upon which you base this contention;\n(b) an estimate of the amount;\n(c) an estimate of how long you will be unable to work; and\n(d) how the claim for future income is calculated.",
            "9.1":"Are there any other damages that you attribute to the INCIDENT? If so, for each item of damage state:\n(a) the nature;\n(b) the date it occurred;\n(c) the amount; and\n(d) the name, ADDRESS, and telephone number of each PERSON to whom an obligation was incurred.",
            "9.2":"Do any DOCUMENTS support the existence or amount of any item of damages claimed in interrogatory 9.1?  If so, describe each document and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT.",
            "10.1":"At any time before the INCIDENT did you have complaints or injuries that involved the same part of your body claimed to have been injured in the INCIDENT?  If so, for each state:\n(a) a description of the complaint or injury;\n(b) the dates it began and ended; and,\n(c) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER whom you consulted or who examined or treated you.",
            "10.2":"List all physical, mental, and emotional disabilities you had immediately before the INCIDENT. (You may omit mental or emotional disabilities unless you attribute any mental or emotional injury to the INCIDENT.)",
            "10.3":"At any time after the INCIDENT, did you sustain injuries of the kind for which you are now claiming damages? If so, for each incident giving rise to an injury state:\n(a) the date and the place it occurred;\n(b) the name, ADDRESS, and telephone number of any other PERSON involved;\n(c) the nature of any injuries you sustained;\n(d) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER who you consulted or who examined or treated you; and\n(e) the nature of the treatment and its duration.",
            "11.1":"Except for this action, in the past 10 years have you filed an action or made a written claim or demand for compensation for your personal injuries? If so, for each action, claim, or demand state:\n(a) the date, time, and place and location (closest street ADDRESS or intersection) of the INCIDENT giving rise to the action, claim, or demand;\n(b) the name, ADDRESS, and telephone number of each PERSON against whom the claim or demand was made or the action filed;\n(c) the court, names of the parties, and case number of any action filed;\n(d) the name, ADDRESS, and telephone number of any attorney representing you;\n(e) whether the claim or action has been resolved or is pending; and\n(f) a description of the injury.",
            "11.2":"In the past 10 years have you made a written claim or demand for workers' compensation benefits? If so, for each claim or demand state:\n(a) the date, time, and place of the INCIDENT giving rise to the claim;\n(b) the name, ADDRESS, and telephone number of your employer at the time of the injury;\n(c) the name, ADDRESS, and telephone number of the workers' compensation insurer and the claim number;\n(d) the period of time during which you received workers' compensation benefits;\n(e) a description of the injury;\n(f) the name, ADDRESS, and telephone number of any HEALTH CARE PROVIDER who provided services; and\n(g) the case number at the Workers' Compensation Appeals Board.",
            "12.1":"State the name, ADDRESS, and telephone number of each individual:\n(a) who witnessed the INCIDENT or the events occurring immediately before or after the INCIDENT;\n(b) who made any statement at the scene of the INCIDENT;\n(c) who heard any statements made about the INCIDENT by any individual at the scene; and\n(d) who YOU OR ANYONE ACTING ON YOUR BEHALF claim has knowledge of the INCIDENT (except for expert witnesses covered by Code of Civil Procedure section 2034).",
            "12.2":"Have YOU OR ANYONE ACTING ON YOUR BEHALF interviewed any individual concerning the INCIDENT? If so, for each individual state: \n(a) the name, ADDRESS, and telephone number of the individual interviewed;\n(b) the date of the interview; and\n(c) the name, ADDRESS, and telephone number of the PERSON who conducted the interview.",
            "12.3":"Have YOU OR ANYONE ACTING ON YOUR BEHALF obtained a written or recorded statement from any individual concerning the INCIDENT? If so, for each statement state:\n(a) the name, ADDRESS, and telephone number of the individual from whom the statement was obtained;\n(b) the name, ADDRESS, and telephone number of the individual who obtained the statement;\n(c) the date the statement was obtained; and\n(d) the name, ADDRESS, and telephone number of each PERSON who has the original statement or a copy.",
            "12.4":"Do YOU OR ANYONE ACTING ON YOUR BEHALF know of any photographs, films, or videotapes depicting any place, object, or individual concerning the INCIDENT or plaintiffs’ injuries? If so, state:\n(a) the number of photographs or feet of film or videotape;\n(b) the places, objects, or persons photographed, filmed, or videotaped;\n(c) the date the photographs, films, or videotapes were taken;\n(d) the name, ADDRESS, and telephone number of the individual taking the photographs, films, or videotapes; and\n(e) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of the photographs, films, or videotapes.",
            "12.5":"Do YOU OR ANYONE ACTING ON YOUR BEHALF know of any diagram, reproduction, or model of any place or thing (except for items developed by expert witnesses covered by Code of Civil Procedure sections 2034.2102034.310) concerning the INCIDENT? If so, for each item state:\n(a) the type (i.e., diagram, reproduction, or model);\n(b) the subject matter; and\n(c) the name, ADDRESS, and telephone number of each PERSON who has it.",
            "12.6":"Was a report made by any PERSON concerning the INCIDENT? If so, state:\n(a) the name, title, identification number, and employer of the PERSON who made the report;\n(b) the date and type of report made;\n(c) the name, ADDRESS, and telephone number of the PERSON for whom the report was made; and\n(d) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of the report.",
            "12.7":"Have YOU OR ANYONE ACTING ON YOUR BEHALF inspected the scene of the INCIDENT? If so, for each inspection state:\n(a) the name, ADDRESS, and telephone number of the individual making the inspection (except for expert witnesses covered by Code of Civil Procedure sections 2034.210-2034.310); and\n(b) the date of the inspection.",
            "13.1":"Have YOU OR ANYONE ACTING ON YOUR BEHALF conducted surveillance of any individual involved in the INCIDENT or any party to this action? If so, for each surveillance state: \n(a) The name, ADDRESS, and telephone number of the individual or party; \n(b) The time, date, and place of the surveillance; \n(c) The name, ADDRESS, and telephone number of the individual who conducted the surveillance; and \n(d) The name, ADDRESS, and telephone number of each PERSON who has the original or a copy of any surveillance photograph, film, or videotape. ",
            "13.2":"Has a written report prepared on the surveillance? If so, for each written report state: \n(a) The title;\n(b) The date; \n(c) The name, ADDRESS, and telephone number of the individual who prepared the report; and \n(d) The name, ADDRESS, and telephone number of each PERSON who has the original or a copy. ",
            "14.1":"Do YOU OR ANYONE ACTING ON YOUR BEHALF contend that any PERSON involved in the INCIDENT violated any statute, ordinance, or regulation and that the violation was a legal (proximate) cause of the INCIDENT? If so, identify the name, ADDRESS, and telephone number of each PERSON and the statute, ordinance, or regulation that was violated.",
            "14.2":"Was any PERSON cited or charged with a violation of any statute, ordinance, or regulation as a result of this INCIDENT? If so, for each PERSON state:\n(a) the name, ADDRESS, and telephone number of the PERSON;\n(b) the statute, ordinance, or regulation allegedly violated;\n(c) whether the PERSON entered a plea in response to the citation or charge and, if so, the plea entered; and\n(d) the name and ADDRESS of the court or administrative agency, names of the parties, and case number.",
            "17.1":"Is your response to each request for admission served with these interrogatories an unqualified admission? If not, for each response that is not an unqualified admission: \n(a) State the number of the request; \n(b) State all facts upon which you base your response;\n(c) State the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of these facts; and \n(d) Identify all DOCUMENTS and other tangible things that support your response and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
            "20.1":"State the date, time, and place of the INCIDENT (closest street ADDRESS or intersection).",
            "20.2":"For each vehicle involved in the INCIDENT, state: \n(a) the year, make, model, and license number;\n(b) the name, ADDRESS, and telephone number of the driver;\n(c) the name, ADDRESS, and telephone number of each occupant other than the driver;\n(d) the name, ADDRESS, and telephone number of each registered owner;\n(e) the name, ADDRESS, and telephone number of each lessee;\n(f) the name, ADDRESS, and telephone number of each owner other than the registered owner or lien holder; and\n(g) the name of each owner who gave permission or consent to the driver to operate the vehicle.",
            "20.3":"State the ADDRESS and location where your trip began and the ADDRESS and location of your destination.",
            "20.4":"Describe the route that you followed from the beginning of your trip to the location of the INCIDENT, and state the location of each stop, other than routine traffic stops, during the trip leading up to the INCIDENT.",
            "20.5":"State the name of the street or roadway, the lane of travel, and the direction of travel of each vehicle involved in the INCIDENT for the 500 feet of travel before the INCIDENT.",
            "20.6":"Did the INCIDENT occur at an intersection? If so, describe all traffic control devices, signals, or signs at the intersection.",
            "20.7":"Was there a traffic signal facing you at the time of the INCIDENT? If so, state:\n(a) your location when you first saw it;\n(b) the color;\n(c) the number of seconds it had been that color; and\n(d) whether the color changed between the time you first saw it and the INCIDENT.",
            "20.8":"State how the INCIDENT occurred, giving the speed, direction, and location of each vehicle involved:\n(a) just before the INCIDENT;\n(b) at the time of the INCIDENT; and\n(c) just after the INCIDENT.",
            "20.9":"Do you have information that a malfunction or defect in a vehicle caused the INCIDENT? If so:\n(a) identify the vehicle;\n(b) identify each malfunction or defect;\n(c) state the name, ADDRESS, and telephone number of each PERSON who is a witness to or has information about each malfunction or defect; and\n(d) state the name, ADDRESS, and telephone number of each PERSON who has custody of each defective part.",
            "20.10":"Do you have information that any malfunction or defect in a vehicle contributed to the injuries sustained in the INCIDENT? If so:\n(a) identify the vehicle;\n(b) identify each malfunction or defect;\n(c) state the name, ADDRESS, and telephone number of each PERSON who is a witness to or has information about each malfunction or defect; and\n(d) state the name, ADDRESS, and telephone number of each PERSON who has custody of each defective part.",
            "20.11":"State the name, ADDRESS, and telephone number of each owner and each PERSON who has had possession since the INCIDENT of each vehicle involved in the INCIDENT."
            }
   
    #APPLICATION UTILITY SETUP
    initial_theme()
    root=tk.CTk()
    root.withdraw()
    create_window(root)
    root.mainloop()







# CHANGES
############################################################################################################




#Make autofill system work

#Check all works
#Handle error of objection being removed!
#Remove scroll to file