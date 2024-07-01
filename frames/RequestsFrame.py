# IMPORTS
from functions import *
import customtkinter as tk
from PIL import Image
from functools import partial
import tkinter

#os.path.join(os.path.dirname(__file__),"../assets/icon.ico")
# ICON IMAGES
PDF_ICON=tk.CTkImage(Image.open(os.path.join(os.path.dirname(__file__),"../assets/pdf.png")),size=(16,16))
CLIENT_ICON=tk.CTkImage(Image.open(os.path.join(os.path.dirname(__file__),"../assets/client.png")),size=(16,16))

# REQUESTS FRAME 
############################################################################################################
# Contains list of all the requests in file
class Requests_Frame(tk.CTkFrame):
    #Constructor
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #FRAME SETUP
        self.file_buttons=[]
        self.request_buttons=[]

        # Clients Frame
        client_title_frame = tk.CTkFrame(master=self,fg_color="transparent")
        client_title_frame.pack(fill="both")
        text = tk.CTkLabel(master=client_title_frame,text="CLIENTS",anchor="w")
        text.pack(side="left",fill="both",padx=10)
        #Client Button
        add_button = tk.CTkButton(master=client_title_frame,width=20,height=10,font=("arial",20),text="+",fg_color="transparent",text_color=("black","white"),hover=False,command=master.new_client)
        add_button.pack(side="left")
        add_tooltip(add_button,"Create a blank client document")
        self.unsaved_text = tk.CTkLabel(master=client_title_frame,text="",anchor="w")
        self.unsaved_text.pack(side="left",fill="both",padx=10)
        self.clients_frame = tk.CTkScrollableFrame(master=self,corner_radius=0,fg_color="transparent")
        self.clients_frame.pack(padx=0,pady=0,fill="x")


        # Files Frame
        file_title_frame = tk.CTkFrame(master=self,fg_color="transparent")
        file_title_frame.pack(fill="both")
        text = tk.CTkLabel(master=file_title_frame,text="FILES",anchor="w")
        text.pack(side="left",fill="both",padx=10)
        add_button = tk.CTkButton(master=file_title_frame,width=20,height=10,font=("arial",20),text="+",fg_color="transparent",text_color=("black","white"),hover=False,command=master.select_file)
        add_button.pack(side="left")
        add_tooltip(add_button,"Load a PDF file")
        self.file_frame = tk.CTkScrollableFrame(master=self,corner_radius=0,fg_color="transparent")
        self.file_frame.pack(padx=0,pady=0,fill="x")

        # Requests Frame
        text = tk.CTkLabel(master=self,text="REQUESTS",anchor="w")
        text.pack(fill="both",padx=10)
        self.list_frame = tk.CTkScrollableFrame(master=self,corner_radius=0,fg_color="transparent")
        self.list_frame.pack(padx=0,pady=0,expand=True,fill="both")
        
    #Show all of the open client buttons
    def show_clients(self,clients):
        for w in self.clients_frame.winfo_children():
            w.destroy()
        self.client_buttons=[]
        c=1
        unsaved=0
        for i in clients:
            fg_color="transparent"
            if i==self.master.current_client:
                fg_color='#144870'

            saved_bit=""
            if i.saved==False:
                saved_bit="⦁ "
                unsaved+=1
            button = tk.CTkButton(master=self.clients_frame,image=CLIENT_ICON,anchor="w",text=saved_bit+get_name(i.name,22),hover=False,corner_radius=0,fg_color=fg_color,command=i.set,text_color=i.color)
            button.pack(fill="x",side="top")
            self.client_buttons.append(button)
            c+=1

        self.set_unsaved_text(unsaved)
        

    #Update the client button colours
    def update_clients(self,clients):
        c=0
        unsaved = 0
        for i in clients:
            saved_bit=""
            if i.saved==False:
                saved_bit="• "
                unsaved+=1
            if i==self.master.current_client:
                self.client_buttons[c].configure(fg_color='#144870',text_color=i.color,text=saved_bit+get_name(i.name,22))
            else:
                self.client_buttons[c].configure(fg_color="transparent",text_color=i.color,text=saved_bit+get_name(i.name,22))
            c+=1

        self.set_unsaved_text(unsaved)

    def set_unsaved_text(self,unsaved):
        #Update the unsaved text
        if unsaved==0:
            self.unsaved_text.configure(text="")
        else:
            #Show the number of unsaved clients
            self.unsaved_text.configure(text=str(unsaved)+" unsaved")


    #Show all of the open file buttons
    def show_files(self,files):
        for w in self.file_frame.winfo_children():
            w.destroy()
        self.file_buttons=[]
        c=1
        for i in files:
            fg_color="transparent"
            if i==self.master.current_client.current_file:
                fg_color='#144870'
            button = tk.CTkButton(master=self.file_frame,image=PDF_ICON,anchor="w",text=get_name(i.name,22),hover=False,corner_radius=0,fg_color=fg_color,command=i.set,text_color=i.color)
            button.pack(fill="x",side="top")
            if self.master.CONFIG["general"]["hover_tooltips"]:
                add_tooltip(button,i.name,wraplength=2000)
            button.bind("<ButtonRelease-1>", i.on_drop)
            #button.bind("<B1-Motion>",i.on_drag)
            self.file_buttons.append(button)
            c+=1

    #Update the file button colours
    def update_files(self,files):
        c=0
        for i in files:
            if i==self.master.current_client.current_file:
                self.file_buttons[c].configure(fg_color='#144870',text_color=i.color)
            else:
                self.file_buttons[c].configure(fg_color="transparent",text_color=i.color)
            c+=1

    #Scroll to the current file
    def scroll_to_file(self,reset=False):
        if self.master.current_client!="":
            if reset:
                self.file_frame._parent_canvas.yview_moveto(0)
                #CHANGE THIS TO A CALCULATION OF THE NEW POSITION
                self.update()
            #If new not in the fraction the current move
            current_y = self.file_frame._parent_canvas.yview()#Tuple of start & end
            current_index = self.master.current_client.files.index(self.master.current_client.current_file)#Index of current request
            compare = current_index/len(self.master.current_client.files)#Exact position of current req
            gap=(current_y[1]-current_y[0])
            if compare>current_y[1]-1/len(self.master.current_client.files):#If after box
                new = compare-gap+1/len(self.master.current_client.files)
                self.file_frame._parent_canvas.yview_moveto(new)
            elif compare<current_y[0]:#If before box
                new = compare
                self.file_frame._parent_canvas.yview_moveto(new)
    
    #Scroll to a request
    def scroll_to(self,reset=False):
        if self.master.current_req!=0:
            if reset:
                self.list_frame._parent_canvas.yview_moveto(0)
                #CHANGE THIS TO A CALCULATION OF THE NEW POSITION
                self.update()
            #If new not in the fraction the current move
            current_y = self.list_frame._parent_canvas.yview()#Tuple of start & end
            current_index = self.master.reqs.index(self.master.current_req)#Index of current request
            compare = current_index/len(self.master.reqs)#Exact position of current req
            
            gap=(current_y[1]-current_y[0])
    
            if compare>current_y[1]-1/len(self.master.reqs):#If after box
                new = compare-gap+1/len(self.master.reqs)
                self.list_frame._parent_canvas.yview_moveto(new)
            elif compare<current_y[0]:#If before box
                new = compare
                self.list_frame._parent_canvas.yview_moveto(new)

    #Show all the open request buttons
    def show_list(self,reqs):
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.request_buttons=[]
        c=1
        for i in reqs:
            fg_color="transparent"
            if i==self.master.current_req:
                fg_color='#144870'
            color=i.color
            req_type=self.master.req_type
            if i.custom_key=="":
                text = c
            else:
                text = i.custom_key
            button = tk.CTkButton(master=self.list_frame,text=req_type+" NO. "+str(text),corner_radius=0,text_color=color,fg_color=fg_color,hover=False,command=i.set)
            button.pack(fill="x",side="top")
            self.request_buttons.append(button)
            c+=1

    #Update the request button colours
    def update_list(self,reqs):
        c=0
        for i in reqs:
            color=i.color
            if i==self.master.current_req:
                self.request_buttons[c].configure(fg_color='#144870',text_color=color)
            else:
                self.request_buttons[c].configure(fg_color="transparent",text_color=color)
            c+=1
