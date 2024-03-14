# IMPORTS
from functions import *
import customtkinter as tk
from tkinter import *

# PREVIEW TEXT WINDOW
############################################################################################################
# Window to see a text preview of the full response
class PreviewText(tk.CTkToplevel):
    #Constructor
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Response Preview")
        #self.wm_iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico"))#Icon
        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico")))
        self.geometry("600x400")
        
        #GET WINDOW FOCUS
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()

        #SET THE TEXT HERE
        master.set_request(master.current_req)

        #Box formatted like other text
        label_font = tk.CTkFont("Arial",16,underline=True,weight="bold")
        self.response_label=tk.CTkLabel(master=self,text="RESPONSE:",font=label_font,anchor="w")
        self.response_label.pack(padx=10,pady=(10,0),fill="both")
        #Get style here from main program
        font = (master.theme["text_font"],int(master.theme["text_size"]))
        self.text = tk.CTkTextbox(master=self,wrap="word",font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.text.pack(fill="both",expand=True,padx=20,pady=10)
        self.text.insert("0.0",master.current_req.get_full_resp())
        self.text.configure(state="disabled")
        #OK button
        self.ok_button = tk.CTkButton(master=self,text="Ok",command=master.cancel_win)
        self.ok_button.pack(side="right",padx=10,pady=(0,10))