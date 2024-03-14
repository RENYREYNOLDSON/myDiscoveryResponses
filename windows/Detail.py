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
        self.geometry("600x680")
        self.title("File Details")
        #self.wm_iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico"))#Icon
        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico")))

        #GET WINDOW FOCUS
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()
        self.resizable(False,False)
        self.grid_columnconfigure((0,1),weight=1)
        font = (master.theme["text_font"],16)
        details = self.master.current_client.current_file.details
        r=5
        
        #File Name
        name = tk.CTkLabel(master=self,text="File Name")
        name.grid(row=0,column=0,padx=20,sticky="w")
        self.name = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.name.grid(row=1,column=0,padx=30,columnspan=2,sticky="ew")
        self.name.insert("0.0",self.master.current_client.current_file.name)
        #County
        county = tk.CTkLabel(master=self,text="County")
        county.grid(row=2,column=0,padx=20,sticky="w")
        self.county = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.county.grid(row=3,column=0,padx=30,columnspan=2,sticky="ew")
        self.county.insert("0.0",details["county"])
        #Case Number
        case = tk.CTkLabel(master=self,text="Case Number")
        case.grid(row=4,column=0,padx=20,sticky="w")
        self.case = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.case.grid(row=5,column=0,padx=30,columnspan=2,sticky="ew")
        self.case.insert("0.0",details["case_number"])
        #Document
        document = tk.CTkLabel(master=self,text="Document Name")
        document.grid(row=6,column=0,padx=20,sticky="w")
        self.document = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.document.grid(row=7,column=0,padx=30,columnspan=2,sticky="ew")
        self.document.insert("0.0",details["document"])

        #Plaintiff
        plaintiff = tk.CTkLabel(master=self,text="Plaintiff(s)")
        plaintiff.grid(row=8,column=0,padx=20,sticky="w")
        self.plaintiff = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.plaintiff.grid(row=9,column=0,padx=30,columnspan=2,sticky="ew")
        self.plaintiff.insert("0.0",details["plaintiff"])
        #Defendant
        defendant = tk.CTkLabel(master=self,text="Defendant(s)")
        defendant.grid(row=10,column=0,padx=20,sticky="w")
        self.defendant = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.defendant.grid(row=11,column=0,padx=30,columnspan=2,sticky="ew")
        self.defendant.insert("0.0",details["defendant"])
        #Propounding Party
        propounding_party = tk.CTkLabel(master=self,text="Propounding Party")
        propounding_party.grid(row=12,column=0,padx=20,sticky="w")
        self.propounding_party = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.propounding_party.grid(row=13,column=0,padx=30,columnspan=2,sticky="ew")
        self.propounding_party.insert("0.0",details["propounding_party"])
        #Responding Party
        responding_party = tk.CTkLabel(master=self,text="Responding Party")
        responding_party.grid(row=14,column=0,padx=20,sticky="w")
        self.responding_party = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.responding_party.grid(row=15,column=0,padx=30,columnspan=2,sticky="ew")
        self.responding_party.insert("0.0",details["responding_party"])
        #Date
        date = tk.CTkLabel(master=self,text="Date")
        date.grid(row=16,column=0,padx=20,sticky="w")
        self.date = tk.CTkTextbox(master=self,height=40,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"],corner_radius=r)
        self.date.grid(row=17,column=0,padx=30,columnspan=2,sticky="ew")
        self.date.insert("0.0",details["date"])

        #Cancel Button
        self.cancel_button = tk.CTkButton(master=self,text="Cancel",command=self.master.cancel_win)#Just simply close
        self.cancel_button.grid(row=18,column=0,pady=20)
        #Submit Button
        self.submit_button = tk.CTkButton(master=self,text="Save",command=self.master.save_detail_win)#Save and close
        self.submit_button.grid(row=18,column=1,pady=20)