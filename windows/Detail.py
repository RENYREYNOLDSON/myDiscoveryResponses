# IMPORTS
from functions import *
import customtkinter as tk
from tkinter import *

# DETAIL WINDOW
############################################################################################################
# Contains details data
class Detail(tk.CTkToplevel):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master
        self.geometry("400x680")
        self.title("File Details")
        self.wm_iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico"))#Icon

        #GET WINDOW FOCUS
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()
        self.resizable(False,False)
        self.grid_columnconfigure((0,1),weight=1)
        font = (master.theme["text_font"],int(master.theme["text_size"]))
        details = self.master.current_client.current_file.details
        
        #File Name
        name = tk.CTkLabel(master=self,text="File Name")
        name.grid(row=0,column=0,padx=20,sticky="w")
        self.name = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.name.grid(row=1,column=0,padx=30,columnspan=2,sticky="ew")
        self.name.insert("0.0",self.master.current_client.current_file.name)
        #County
        county = tk.CTkLabel(master=self,text="County")
        county.grid(row=2,column=0,padx=20,sticky="w")
        self.county = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.county.grid(row=3,column=0,padx=30,columnspan=2,sticky="ew")
        self.county.insert("0.0",details["county"])
        #Case Number
        case = tk.CTkLabel(master=self,text="Case Number")
        case.grid(row=4,column=0,padx=20,sticky="w")
        self.case = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.case.grid(row=5,column=0,padx=30,columnspan=2,sticky="ew")
        self.case.insert("0.0",details["case_number"])
        #Document
        document = tk.CTkLabel(master=self,text="Document Name")
        document.grid(row=6,column=0,padx=20,sticky="w")
        self.document = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.document.grid(row=7,column=0,padx=30,columnspan=2,sticky="ew")
        self.document.insert("0.0",details["document"])
        #Plaintiff
        plaintiff = tk.CTkLabel(master=self,text="Propounding Party")
        plaintiff.grid(row=8,column=0,padx=20,sticky="w")
        self.plaintiff = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.plaintiff.grid(row=9,column=0,padx=30,columnspan=2,sticky="ew")
        self.plaintiff.insert("0.0",details["defendant"])
        #Defendant
        defendant = tk.CTkLabel(master=self,text="Responding Party")
        defendant.grid(row=10,column=0,padx=20,sticky="w")
        self.defendant = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.defendant.grid(row=11,column=0,padx=30,columnspan=2,sticky="ew")
        self.defendant.insert("0.0",details["plaintiff"])
        #Date
        date = tk.CTkLabel(master=self,text="Date")
        date.grid(row=12,column=0,padx=20,sticky="w")
        self.date = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.date.grid(row=13,column=0,padx=30,columnspan=2,sticky="ew")
        self.date.insert("0.0",details["date"])

        #Cancel Button
        self.cancel_button = tk.CTkButton(master=self,text="Cancel",command=self.master.cancel_win)#Just simply close
        self.cancel_button.grid(row=14,column=0,pady=20)
        #Submit Button
        self.submit_button = tk.CTkButton(master=self,text="Save",command=self.master.save_detail_win)#Save and close
        self.submit_button.grid(row=14,column=1,pady=20)