# IMPORTS
from functions import *
import customtkinter as tk
from tkinter import *

# FIRM DETAILS WINDOW
############################################################################################################
class FirmDetail(tk.CTkToplevel):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master
        self.geometry("400x680")
        self.title("Firm Details")

        #GET WINDOW FOCUS
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()

        self.wm_iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico"))#Icon
        self.resizable(False,False)
        self.grid_columnconfigure((0,1),weight=1)
        font = (master.theme["text_font"],int(master.theme["text_size"]))
        
        #Firm Name
        #Address
        #Email
        #Telephone NUmber
        #Facsimile
        #Attorneys - Each has a state bar number
        if self.master.current_client!="":
            firm_details = self.master.current_client.firm_details#Each client loads default details and then they can be edited
        else:
            firm_details = get_firm_details()
        #File Name
        name = tk.CTkLabel(master=self,text="Firm Name")
        name.grid(row=0,column=0,padx=20,sticky="w")
        self.name = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.name.grid(row=1,column=0,padx=30,columnspan=2,sticky="ew")
        self.name.insert("0.0",firm_details["firm_name"])
        #County
        address_line_1 = tk.CTkLabel(master=self,text="Address Line 1")
        address_line_1.grid(row=2,column=0,padx=20,sticky="w")
        self.address_line_1 = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.address_line_1.grid(row=3,column=0,padx=30,columnspan=2,sticky="ew")
        self.address_line_1.insert("0.0",firm_details["address_line_1"])
        #Case Number
        address_line_2 = tk.CTkLabel(master=self,text="Address Line 2")
        address_line_2.grid(row=4,column=0,padx=20,sticky="w")
        self.address_line_2 = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.address_line_2.grid(row=5,column=0,padx=30,columnspan=2,sticky="ew")
        self.address_line_2.insert("0.0",firm_details["address_line_2"])
        #Document
        telephone = tk.CTkLabel(master=self,text="Telephone")
        telephone.grid(row=6,column=0,padx=20,sticky="w")
        self.telephone = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.telephone.grid(row=7,column=0,padx=30,columnspan=2,sticky="ew")
        self.telephone.insert("0.0",firm_details["telephone"])
        #Plaintiff
        facsimile = tk.CTkLabel(master=self,text="Facsimile")
        facsimile.grid(row=8,column=0,padx=20,sticky="w")
        self.facsimile = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.facsimile.grid(row=9,column=0,padx=30,columnspan=2,sticky="ew")
        self.facsimile.insert("0.0",firm_details["facsimile"])
        #Defendant
        email = tk.CTkLabel(master=self,text="Email")
        email.grid(row=10,column=0,padx=20,sticky="w")
        self.email = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.email.grid(row=11,column=0,padx=30,columnspan=2,sticky="ew")
        self.email.insert("0.0",firm_details["email"])
        #Date
        attorneys = tk.CTkLabel(master=self,text="Attorneys")
        attorneys.grid(row=12,column=0,padx=20,sticky="w")
        self.attorneys = tk.CTkTextbox(master=self,height=60,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.attorneys.grid(row=13,column=0,padx=30,columnspan=2,sticky="ew")
        self.attorneys.insert("0.0",firm_details["attorneys"])

        #Cancel Button
        self.cancel_button = tk.CTkButton(master=self,text="Cancel",command=self.master.cancel_win)#Just simply close
        self.cancel_button.grid(row=14,column=0,pady=20)
        #Submit Button
        self.submit_button = tk.CTkButton(master=self,text="Save",command=self.master.save_firm_detail_win)#Save and close
        self.submit_button.grid(row=14,column=1,pady=20)