# IMPORTS
from functions import *
import customtkinter as tk
from tkinter import *
from functools import partial

# HOTKEYS WINDOW
############################################################################################################
class Hotkeys(tk.CTkToplevel):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master
        self.title("Shortcut Editor")
        #self.wm_iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico"))#Icon
        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico")))
        self.minsize(800,400)
        self.resizable(False,False)
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()

        self.hotkey_array=[]
        #SETUP HOTKEY ARRAY
        for hot in self.master.HOTKEYS:
            self.hotkey_array.append([hot,self.master.HOTKEYS[hot]])

        #FOR THE GUI
        #1. Have list of hotkey and output with a bin button
        #2. Have a + at the bottom to add another!

        #EDIT HOTKEYS
        self.scroll_frame = tk.CTkScrollableFrame(master=self)
        self.scroll_frame.pack(fill="both",expand=True)
        self.redraw_hotkeys()
        
        #SAVE AND CANCEL BUTTONS
        buttons_frame = tk.CTkFrame(master=self)
        buttons_frame.columnconfigure((0,1),weight=1)
        buttons_frame.pack(fill="x")
        #Cancel
        cancel_button = tk.CTkButton(master=buttons_frame,text="Cancel",command=self.master.cancel_win)
        cancel_button.grid(row=0,column=0,padx=10,pady=5)
        #Save
        save_button = tk.CTkButton(master=buttons_frame,text="Save",command=self.save)
        save_button.grid(row=0,column=1,padx=10,pady=5)

    def save(self):
        # go through each hotkey frame and add text form array
        self.hotkey_array={}
        for w in self.scroll_frame.winfo_children():
            #Each frame
            new_hotkey=[]
            for w2 in w.winfo_children():
                if "!ctkentry" in str(w2.winfo_name()):
                    new_hotkey.append(w2.get())
            if len(new_hotkey)==2:
                #Add new hotkey        
                self.hotkey_array[new_hotkey[0]] = new_hotkey[1]
        # Save the hotkeys and close
        save_hotkeys(self.hotkey_array)
        self.master.HOTKEYS=self.hotkey_array#Update apps hotkeys
        self.master.cancel_win()
        

    def redraw_hotkeys(self):
        #Destroy previous hotkey frames
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        #Get font
        font = (self.master.CONFIG["appearance"]["text_font"],int(self.master.CONFIG["appearance"]["text_size"]))
        text_color=self.master.CONFIG["appearance"]["text_color"]
        fg_color=self.master.CONFIG["appearance"]["text_bg"]
        #Create a frame for each
        count=0
        for hot in self.hotkey_array:
            frame = tk.CTkFrame(master=self.scroll_frame)
            frame.pack(fill="x",pady=10)
            #Add Input
            input_text=tk.CTkLabel(master=frame,text="Trigger:")
            input_text.pack(side="left",padx=5)
            input=tk.CTkEntry(master=frame,font=font,text_color=text_color,fg_color=fg_color)
            input.pack(side="left",padx=5)
            input.insert(0,hot[0])
            #Add Output
            output_text=tk.CTkLabel(master=frame,text="Output:")
            output_text.pack(side="left",padx=5)
            output=tk.CTkEntry(master=frame,font=font,text_color=text_color,fg_color=fg_color)
            output.pack(side="left",fill="x",expand=True,padx=5)
            output.insert(0,hot[1])
            #Add Delete Button
            delete=tk.CTkButton(master=frame,text="🗑",text_color=("black","white"),fg_color="transparent",hover=False,font=("Segoe UI",20),width=40,command=partial(self.delete,count))
            delete.pack(side="left",padx=5)
            count+=1
        #Add New Button
        add_button=tk.CTkButton(master=self.scroll_frame,text="➕",width=40,fg_color="transparent",command=self.add,text_color=("black","white"))
        add_button.pack()
    #Delete a hotkey from array
    def delete(self,index):
        self.hotkey_array.pop(index)
        self.redraw_hotkeys()
    #Add a new hotkey frame to window
    def add(self):
        self.hotkey_array.append(["",""])
        self.redraw_hotkeys()