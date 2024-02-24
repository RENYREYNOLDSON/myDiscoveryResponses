# IMPORTS
from functions import *
import customtkinter as tk
from PIL import Image
from functools import partial
import tkinter
from customtkinter.windows.widgets.core_widget_classes.dropdown_menu import DropdownMenu

# BAR FRAME 
############################################################################################################
class Bar_Frame(tk.CTkFrame):
    #Constructor 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #FRAME SETUP

        # File
        var = tk.StringVar(value="File")
        self.file=tk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["New Window"],width=100,corner_radius=0,bg_color="transparent",command=self.call_file)
        self.file.configure(button_color="#161616",fg_color="#161616")
        #Add the open recent menu
        values=[]
        for f in master.RECENTS:
            values.append(f)
        menu_recent = DropdownMenu(self.file,values=values,command=self.call_recent)
        self.file._dropdown_menu.add_command(label="New Client", command=self.master.new_client, accelerator="Ctrl+N")
        self.file._dropdown_menu.insert_cascade(3,menu=menu_recent, label='Open Recent')
        self.file._dropdown_menu.add_command(label="Open File", command=self.master.select_file, accelerator="Ctrl+O")
        self.file._dropdown_menu.add_command(label="Open Folder", command=self.master.select_folder, accelerator="Ctrl+F")
        self.file._dropdown_menu.add_command(label="Add Blank FROG", command=self.master.add_blank_frog)
        self.file._dropdown_menu.add_command(label="Load Client Feedback", command=self.master.load_client_feedback)
        self.file._dropdown_menu.add_command(label="Save Client", command=self.master.quick_save, accelerator="Ctrl+S")
        self.file._dropdown_menu.add_command(label="Save Client As", command=self.master.select_save_client)
        self.file._dropdown_menu.add_command(label="Export File as DOCX", command=self.master.export_current)
        self.file._dropdown_menu.add_command(label="Export Client as DOCX", command=self.master.export_all)
        self.file._dropdown_menu.add_command(label="Export Check With Client", command=self.master.export_check_with_clients)
        self.file._dropdown_menu.add_command(label="Preview DOCX", command=self.master.view_preview)
        self.file._dropdown_menu.add_command(label="Close File", command=self.master.close_file)
        self.file._dropdown_menu.add_command(label="Close Client", command=self.master.close_client)
        self.file._dropdown_menu.add_command(label="Exit", command=self.master.exit_window)



        self.file._dropdown_menu.insert_separator(1)
        self.file._dropdown_menu.insert_separator(8)
        self.file._dropdown_menu.insert_separator(11)
        self.file._dropdown_menu.insert_separator(16)
        self.file.pack(side="left")


        # View
        var = tk.StringVar(value="Options")
        self.options=tk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["Firm Details","Theme","Objections","Hotkeys","User Guide"],width=100,corner_radius=0,bg_color="transparent",command=self.call_options)
        self.options.configure(button_color="#161616",fg_color="#161616")
        self.options.pack(side="left")
        self.options._dropdown_menu.insert_separator(1)

        # Details
        self.details = tk.CTkButton(master=self,text="File Details",fg_color="transparent",width=100,command=self.master.view_details,corner_radius=0)
        self.details.pack(side="left")

        # Clear
        self.clear = tk.CTkButton(master=self,text="Clear",fg_color="transparent",width=100,corner_radius=0,command=self.master.clear)
        self.clear.pack(side="right")

        # Copy Previous
        self.copy = tk.CTkButton(master=self,text="Copy Previous",fg_color="transparent",width=100,command=self.master.copy_previous,corner_radius=0)
        self.copy.pack(side="right")

        # Preview
        self.copy = tk.CTkButton(master=self,text="Preview",fg_color="transparent",width=100,corner_radius=0,command=self.master.preview_text)
        self.copy.pack(side="right")

        # Save
        self.copy = tk.CTkButton(master=self,text="Save",fg_color="transparent",width=100,corner_radius=0,command=self.master.quick_save)
        self.copy.pack(side="right")

    def update_recents(self,recents):
        menu_recent = DropdownMenu(self.file,values=recents,command=self.call_recent)
        self.file._dropdown_menu.entryconfigure(3,menu=menu_recent)

    #Trigger a file load when a 'recent' clicked
    def call_recent(self,val):
        if valid_file_path(val):
            self.master.load(val)

    #Trigger a command when a 'File' button clicked
    def call_file(self,val):# All of file manu options
        self.file.set("File")
        if val=="New Window":
            self.master.create_window()

    #Trigger a command when an 'Options' button clicked
    def call_options(self,val):
        self.options.set("Options")
        if val=="Theme":
            self.master.view_theme()
        elif val=="Objections":
            self.master.view_objections()
        elif val=="Hotkeys":
            self.master.view_hotkeys()
        elif val=="User Guide":
            open_user_guide()
        elif val=="Firm Details":
            self.master.view_firm_details()