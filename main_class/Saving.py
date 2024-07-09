# Main Imports
import converter as cnv
from CTkMessagebox import CTkMessagebox
import json,os,copy,sys,time,subprocess
import pickle
from threading import Thread
import re
import os
from enchant import list_languages
# Main Class Inheritance Imports
from main_class.Saving import *
# Frame Imports
from frames.BarFrame import *
from frames.LandingFrame import *
from frames.ObjectionsFrame import *
from frames.RequestsFrame import *
from frames.ResponseFrame import *
from frames.FileDetails import *
from frames.FirmDetails import *
# Window Imports
from windows.EditObjections import *
from windows.Hotkeys import *
from windows.Preview import *
from windows.PreviewText import *
from windows.Settings import Settings
# Object Imports
from objects.Client import *
from objects.File import *
from objects.Objection import *
from objects.Request import *
from objects.Save import *
from objects.SmartToolTip import *
from objects.Action import *

class Saving:
  ### SAVING AND LOADING OF FILES & FOLDERS
    ########################################################################################################
    # Open a folder containing files
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
            title='Open file',
            filetypes=filetypes)

        for filename in filenames:
            if os.path.exists(filename):
                if filename[-4:].lower()==".pdf":#PDF
                    if self.current_client=="":# If no client selected
                        CTkMessagebox(title="Error",
                                       message="Must create a client to open Discovery Requests", 
                                       icon="cancel",
                                       corner_radius=0,
                                       sound=True,
                                       master=self)
                        return
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
                    self.load(filename)

    # Opens a PDF file specifically
    def open_file(self,filename):
        if os.path.exists(filename):
            self.close_landing_frame()
            try:
                reqs,req_type,doc_details,custom_keys = cnv.getRequests(filename)
            except Exception as e:
                msg = CTkMessagebox(title="Loading Issue", 
                                    message="The selected file: "+str(filename)+" could not be loaded!\nError Message: "+str(e),
                                    icon="warning", 
                                    option_1="Okay",
                                    corner_radius=0,
                                    width=800,
                                    sound=True,
                                    master=self)
                return
            self.set_type(req_type)# Sets the current type
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
                    key = ""
                    if custom_keys!=[]:
                        key = custom_keys[c]
                    self.reqs.append(Request(i,"",c,self,req_type,key))
                    c+=1

            ### ADD NEW FILE TO CLIENT, IF NONE THEN CREATE NEW CLIENT!
            new_file = File(filename,doc_details,self.req_type,self.reqs,self)
            if self.current_client!="":
                self.current_client.files.append(new_file)
            else:
                self.clients.append(Client(doc_details["defendant"],[new_file],self))
                self.set_client(self.clients[-1])



    #SAVING AND LOADING WITH PICKLE

    #Load File whether it be a file or a client
    def load(self,filename):
        # Create file obj
        file = open(filename,"rb")
        # Load the file object
        try:
            save_obj = pickle.load(file)
        except:
            file.close()
            msg = CTkMessagebox(title="File Corrupted", 
                                message="An error has caused this file to become corrupted!",
                                icon="warning", 
                                option_1="Okay",
                                corner_radius=0,
                                sound=True,
                                master=self)
            return
        file.close()
        # Get files array
        if save_obj.save_type == "file":
            self.load_file(save_obj.files[0])
        else:
            self.load_client(save_obj.files[0],filename)
    
    #Load a single file into the current client
    def load_file(self,new_file):
        if self.current_client=="":
            return
        #Set new master
        new_file.set_master(self)
        # Add file
        self.current_client.files.append(new_file)
        self.requests_frame.show_files(self.current_client.files)
        self.set_file(self.current_client.files[-1])
        self.requests_frame.show_clients(self.clients)
        
    #Load Client
    def load_client(self,new_client,filename):
        if self.client_already_open(new_client.name):
            return
        #Set new master
        new_client.set_master(self)
        # Add file
        self.clients.append(new_client)
        self.set_client(self.clients[-1])
        self.requests_frame.show_clients(self.clients)
        self.close_landing_frame()
        #SET THE QUICKSAVE!
        self.current_client.save=filename
        self.set_recents(filename)
        self.reload_objections()


    #Select the save file
    def select_save_file(self):
        # Select a folder and save name
        filename=tk.filedialog.asksaveasfilename(title="Save Current File",filetypes=(("Discovery Save File","*.discovery"),('All files', '*.*'))).replace(".discovery","")
        if filename=="":
            return
        self.save_file(filename)

    #Actually do the file saving
    def save_file(self,filename):
        file = open(filename+".discovery","wb")
        # Remove master from the save
        self.current_client.current_file.set_master(None)
        # Create save object
        save_obj = Save([self.current_client.current_file],"file")
        # Pickle the current File
        pickle.dump(save_obj,file)#Need to fix saving with the name
        # Add the master back
        self.current_client.current_file.set_master(self)
        file.close()

    #Select a save to save the client file as
    def select_save_client(self):
        # Select a folder and save name
        filename=tk.filedialog.asksaveasfilename(title="Save Current Client",filetypes=(("Discovery Save File","*.discovery"),('All files', '*.*'))).replace(".discovery","")
        if filename=="":
            return
        self.save_client(filename)

    """
    #Actually save the client file
    def save_client_OLD(self,filename):
        # Remove master from the save
        self.current_client.set_master(None)
        # Create save object
        save_obj = Save([self.current_client],"client")
        # Pickle the current File
        file = open(filename+".discovery","wb")
        pickle.dump(save_obj,file)#Need to fix saving with the name
        file.close()
        # Add the master back
        self.current_client.set_master(self)
        # Set the quicksave
        self.current_client.save = filename+".discovery"
        self.current_client.saved = True
        #Update clients to show saved
        self.requests_frame.update_clients(self.clients)
        self.set_recents(self.current_client.save)
    """

    #Actually save the client file
    def save_client(self,filename):
        # Remove master from the save
        self.current_client.set_master(None)
        # Create save object
        save_obj = Save([self.current_client],"client")

        #STORE AS A TEMPORARY FILE!
        # Pickle the current File
        file = open(filename+"TEMPORARY"+".discovery","wb")
        try:
            pickle.dump(save_obj,file)#Need to fix saving with the name
        except:
            file.close()
            self.current_client.set_master(self)
            msg = CTkMessagebox(title="Saving Issue", 
                                message="The selected file: "+str(filename)+" could not be saved [1]!",
                                icon="warning", 
                                option_1="Okay",
                                corner_radius=0,
                                sound=True,master=self)
            return 
        file.close()

        try:
            #DELETE ORIGINAL
            if os.path.exists(filename+".discovery"):
                os.remove(filename+".discovery")

            #REPLACE ORIGINAL FILE WITH TEMPORARY FILE!
            os.rename(filename+"TEMPORARY"+".discovery",filename+".discovery")
        except:
            self.current_client.set_master(self)
            msg = CTkMessagebox(title="Saving Issue", 
                                message="The selected file: "+str(filename)+" could not be saved [2]! SAVE UNDER A NEW NAME!",
                                icon="warning", 
                                option_1="Okay",
                                corner_radius=0,
                                sound=True,
                                master=self)
            return 
           
        # Add the master back
        self.current_client.set_master(self)
        # Set the quicksave
        self.current_client.save = filename+".discovery"
        self.current_client.saved = True
        #Update clients to show saved
        self.requests_frame.update_clients(self.clients)
        self.set_recents(self.current_client.save)


    #QUICKSAVE: Only saves CLIENT!
    def quick_save(self):
        if self.current_client!="":
            if valid_file_path(self.current_client.save):#If client has a save
                self.save_client(self.current_client.save.replace(".discovery",""))#Remove file type
                self.bar_frame.update_autosave_time()
                return
            else:
                self.select_save_client()#Save client if nothing else!
                self.bar_frame.update_autosave_time()

    def autosave(self):
        #Change to save all valid clients
        if self.CONFIG["general"]["autosaving"]:
            if self.current_client!="":#ONLY DO IF THERE IS A VALID SAVE FILE!!!
                if valid_file_path(self.current_client.save):#If client has a save
                    self.quick_save()
        self.after(int(self.CONFIG["general"]["autosave_interval"]),self.autosave)


    #Close the current file
    def close_file(self):
        if self.file_open():#We know a valid file is open
            msg = CTkMessagebox(title="Close File?", 
                                message="Are you sure you want to permanently close this file?",
                                icon="question", 
                                option_1="Cancel", 
                                option_3="Yes",
                                corner_radius=0,
                                sound=True,
                                master=self)
            
            if msg.get()=="Yes":
                #Get the index of the current file
                index = self.current_client.files.index(self.current_client.current_file)
                if index==0:
                    new_index=1
                else:
                    new_index = index-1

                #Set the new file
                if new_index<len(self.current_client.files):
                    self.set_file(self.current_client.files[new_index])
                    self.requests_frame.scroll_to_file()
                    self.current_client.files.pop(index)
                else:
                    self.current_client.current_file=""
                    self.current_client.files=[]
                self.set_client(self.current_client)
                #self.requests_frame.show_files(self.current_client.files)

    #Close the current open client
    def close_client(self):
        if self.current_client!="":
            #Close details menu if open!
            self.close_details()
            if self.current_client.saved==False:
                msg = CTkMessagebox(title="Close Client?", 
                                    message="Are you sure you want to close the client without saving?",
                                    icon="question", 
                                    option_1="Cancel", 
                                    option_3="Yes",
                                    corner_radius=0,
                                    sound=True,
                                    master=self)
                
                if msg.get()!="Yes":
                    return
            #Get new index for new selected client
            index = self.clients.index(self.current_client)
            if index==0:
                new_index=1
            else:
                new_index = index-1
            
            if new_index<len(self.clients):
                self.set_client(self.clients[new_index])
            else:
                self.close_all()
                return
            #REMOVE the client
            self.clients.pop(index)
            #Redraw Things
            self.requests_frame.show_clients(self.clients)

    #Close all files open in the workspace
    def close_all(self):
        # Attributes
        self.files=[]
        self.reqs=[]
        self.req_type=""
        self.prev_type=""
        self.current_req=0
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
        #Reset display save time
        self.bar_frame.reset_autosave_time()
        #Reopen landing page
        self.open_landing_frame()
        #Set window title
        self.title("myDiscoveryResponses")#Window title



    def load_client_feedback(self):
        if self.file_open():
            filename = tk.filedialog.askopenfilename(title='Load Client Feedback', filetypes=(('Word Docx', '.docx'),('All files', '*.*')))
            if filename!="":
                feedback = cnv.read_client_feedback(filename)
                #KEY,RESP,TYPE
                for f in feedback:
                    for file in self.current_client.files:
                        if file.req_type == f["type"]:
                            for req in file.reqs:
                                if str(req.custom_key)==f["key"]:
                                    if req.req_type=="RFA" and req.RFA_option!="Custom":#If RFA then set this to custom
                                        req.RFA_option="Custom"
                                        req.resp=""
                                    elif req.req_type=="RFP" and req.RFP_option!="Custom":#If RFP then set this to custom
                                        req.RFP_option="Custom"
                                        req.resp=""
                                    req.resp = req.resp + f["response"]#Add client feedback to end of the response text
                                    if req==self.current_req:#If this is the current request then update screen
                                        self.response_frame.set_RFP("Custom")
                                        self.response_frame.set_RFA("Custom")
                                        self.response_frame.set_response(req.resp)