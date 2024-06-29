# IMPORTS
from functions import *
import customtkinter as tk
from PIL import Image
from functools import partial
import tkinter

# LANDING FRAME 
############################################################################################################
class Landing_Frame(tk.CTkFrame):
    #Constructor 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.master=master

        title_frame = tk.CTkFrame(master=self,fg_color="transparent")
        title_frame.place(relx=0.05,rely=0.05,anchor="nw")
        # Title
        font = ("Segoe UI",50,"bold")
        title = tk.CTkLabel(master=title_frame,text="myDiscoveryResponses",font=font,anchor="w")
        title.pack(fill="x")
        # Sub Title
        font = ("Segoe UI",20,"bold")
        title = tk.CTkLabel(master=title_frame,text="  Software for the creation of Discovery Responses",font=font,anchor="w")
        title.pack(fill="x")

        footer = tk.CTkLabel(master=self,text="Version "+str(master.version))
        footer.place(relx=0.5,rely=0.99,anchor="s")

        font=("Segoe UI",20)

        button_frame = tk.CTkFrame(master=self,fg_color="transparent")
        button_frame.place(relx=0.3,rely=0.3,anchor="n",relwidth=0.3)
        #Button List
        #New Client
        self.new_client_button = tk.CTkButton(master=button_frame,font=font,hover=False,text="➕ New Client",anchor="w",fg_color="transparent",text_color=("black","white"),command=master.new_client)
        self.new_client_button.pack(pady=2,fill="x")
        self.client_tooltip = add_tooltip(self.new_client_button,"Create a blank client document")
        #Load File
        self.load_file_button = tk.CTkButton(master=button_frame,font=font,hover=False,text="📂 Load File",anchor="w",fg_color="transparent",text_color=("black","white"),command=master.select_file)
        self.load_file_button.pack(pady=2,fill="x")
        self.load_tooltip = add_tooltip(self.load_file_button,"Load a discovery save file")

        #User Guide
        self.user_guide_button = tk.CTkButton(master=button_frame,font=font,hover=False,text="📖 User Guide",anchor="w",fg_color="transparent",text_color=("black","white"),command=open_user_guide)
        self.user_guide_button.pack(pady=2,fill="x")
        self.guide_tooltip = add_tooltip(self.user_guide_button,"Open the GitHub guide")
        #Settings
        self.settings_button = tk.CTkButton(master=button_frame,font=font,hover=False,text="⚙️ Settings",anchor="w",fg_color="transparent",text_color=("black","white"),command=master.view_settings)
        self.settings_button.pack(pady=2,fill="x")
        self.settings_tooltip = add_tooltip(self.settings_button,"Open software settings")
        #Exit
        self.exit_button = tk.CTkButton(master=button_frame,font=font,hover=False,text="❌ Exit",anchor="w",fg_color="transparent",text_color=("black","white"),command=master.exit_window)
        self.exit_button.pack(pady=2,fill="x")

        self.recent_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.recent_frame.place(relx=0.7,rely=0.3,anchor="n",relwidth=0.4)
        #Recent List
        #Recent Label
        i=0
        while i<min(8,len(master.RECENTS)):
            self.new_client_button = tk.CTkButton(master=self.recent_frame,hover=False,font=font,text=master.RECENTS[i].split("/")[-1],anchor="w",fg_color="transparent",text_color=("black","white"),command=partial(master.load,master.RECENTS[i]))
            self.new_client_button.pack(pady=2,fill="x")
            i+=1

        #Change if the tooltips are enabled
        self.set_tooltips()

    def update_recents(self,recents):
        font=("Segoe UI",20)
        for w in self.recent_frame.winfo_children():
            w.destroy()
        i=0
        while i<min(8,len(recents)):
            self.new_client_button = tk.CTkButton(master=self.recent_frame,hover=False,font=font,text=recents[i].split("/")[-1],anchor="w",fg_color="transparent",text_color=("black","white"),command=partial(self.master.load,recents[i]))
            self.new_client_button.pack(pady=2,fill="x")
            i+=1

    def set_tooltips(self):
        if self.master.CONFIG["general"]["hover_tooltips"]:
            self.client_tooltip.enable()
            self.load_tooltip.enable()
            self.guide_tooltip.enable()
            self.settings_tooltip.enable()
        else:
            self.client_tooltip.disable()
            self.load_tooltip.disable()
            self.guide_tooltip.disable()
            self.settings_tooltip.disable()