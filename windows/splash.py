# IMPORTS
from functions import *
import customtkinter as tk
from tkinter import *

class Splash(tk.CTk):
    #Constructor
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Splash Screen Title")

        width = 600
        height = 200

        x = (self.winfo_screenwidth()//2)+(width//4)
        y = (self.winfo_screenheight()//2)+(height)

        self.geometry("{}x{}+{}+{}".format(width,height,x,y))

        self.overrideredirect(True)

        title_frame = tk.CTkFrame(master=self,fg_color="transparent")
        title_frame.place(relx=0.05,rely=0.25,anchor="nw")
        # Title
        font = ("Segoe UI",50,"bold")
        title = tk.CTkLabel(master=title_frame,text="myDiscoveryResponses",font=font,anchor="w")
        title.pack(fill="x")
        # Sub Title
        font = ("Segoe UI",20,"bold")
        title = tk.CTkLabel(master=title_frame,text="  Software for the creation of Discovery Responses",font=font,anchor="w")
        title.pack(fill="x")

        loading =tk.CTkLabel(master=self,text="Loading...",text_color="grey")
        loading.place(relx=0.02,rely=0.85)