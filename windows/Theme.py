# IMPORTS
from functions import *
import customtkinter as tk
from tkinter import *
from tkinter.colorchooser import askcolor

# THEME WINDOW
############################################################################################################
# Contains theme data
class Theme(tk.CTkToplevel):
    #Constructor
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master
        self.geometry("400x440")
        self.title("Theme Options")
        #self.wm_iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico"))#Icon
        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico")))
        self.resizable(False,False)

        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()


        # Window Frame
        self.window_frame = tk.CTkFrame(master=self,width=380)
        self.window_frame.grid_columnconfigure((0,1),weight=2)

        heading_font=("Segoe UI",20)
        # Main Theme
        self.theme = self.master.theme["theme"]
        self.window_text=tk.CTkLabel(master=self.window_frame,text="Window",font=heading_font)
        self.window_text.grid(row=0,column=0,sticky="ew",padx=20,pady=0,columnspan=2)

        # Theme Buttons
        dark_mode_image = PhotoImage(master=self.window_frame,file=os.path.join(os.path.dirname(__file__),"../assets/dark_mode.png"))
        self.dark_mode_button = tk.CTkButton(master=self.window_frame,image=dark_mode_image,text="",hover=False,fg_color="transparent",command=self.set_dark)
        self.dark_mode_button.grid(row=1,column=0,sticky="ew",padx=10,pady=(10,0))
        
        light_mode_image = PhotoImage(master=self.window_frame,file=os.path.join(os.path.dirname(__file__),"../assets/light_mode.png"))
        self.light_mode_button = tk.CTkButton(master=self.window_frame,image=light_mode_image,text="",hover=False,fg_color="transparent",command=self.set_light)
        self.light_mode_button.grid(row=1,column=1,sticky="ew",padx=10,pady=(10,0))

        self.theme_text=tk.CTkLabel(master=self.window_frame,text="Dark Mode",anchor="center")
        self.theme_text.grid(row=2,column=0,sticky="ew",padx=20,pady=(0,10))
        self.theme_text=tk.CTkLabel(master=self.window_frame,text="Light Mode",anchor="center")
        self.theme_text.grid(row=2,column=1,sticky="ew",padx=20,pady=(0,10))


        if self.theme=="Light":
            self.light_mode_button.configure(fg_color=['#3B8ED0', '#1F6AA5'])
        else:
            self.dark_mode_button.configure(fg_color=['#3B8ED0', '#1F6AA5'])

        # Text Frame
        self.text_frame = tk.CTkFrame(master=self,width=380)
        self.text_frame.grid_columnconfigure((0,1),weight=2)
        cols=["#000000","#FFFFFF","#964B00","#89CFF0","#808080"]
        self.text_text=tk.CTkLabel(master=self.text_frame,text="Text Options",font=heading_font)
        self.text_text.grid(row=0,column=0,sticky="ew",padx=20,pady=0,columnspan=2)
        # Text Colour
        self.window_text=tk.CTkLabel(master=self.text_frame,text="Text Color")
        self.window_text.grid(row=1,column=0,sticky="w",padx=20,pady=0)
        self.text_picker = tk.CTkButton(master=self.text_frame,text=self.master.theme["text_color"],fg_color=self.master.theme["text_color"],command=self.change_text_color)
        self.text_picker.grid(row=2,column=0,padx=40)
        
        # Text Background
        self.window_text=tk.CTkLabel(master=self.text_frame,text="Background Color")
        self.window_text.grid(row=1,column=1,sticky="w",padx=20,pady=0)
        self.bg_picker = tk.CTkButton(master=self.text_frame,text=self.master.theme["text_bg"],fg_color=self.master.theme["text_bg"],command=self.change_bg_color)
        self.bg_picker.grid(row=2,column=1,padx=40)

        # Text Font
        self.font_text=tk.CTkLabel(master=self.text_frame,text="Font")
        self.font_text.grid(row=3,column=0,sticky="w",padx=20,pady=(10,0))
        self.font_entry=tk.CTkOptionMenu(master=self.text_frame,values=["Arial","Times","Courier","Calibri","Cambria"])
        self.font_entry.set(self.master.theme["text_font"])
        self.font_entry.grid(row=4,column=0,padx=40,pady=(0,20))

        # Text Size
        self.size_text=tk.CTkLabel(master=self.text_frame,text="Size")
        self.size_text.grid(row=3,column=1,sticky="w",padx=20,pady=(10,0))
        self.size_entry=tk.CTkOptionMenu(master=self.text_frame,values=["8","10","12","14","16","18","20","22","24","26"])
        self.size_entry.set(self.master.theme["text_size"])
        self.size_entry.grid(row=4,column=1,padx=40,pady=(0,20))
        self.buttons_frame=tk.CTkLabel(master=self,fg_color="transparent")
        self.buttons_frame.grid_columnconfigure((0,1),weight=1)

        #Cancel Button
        self.cancel_button = tk.CTkButton(master=self.buttons_frame,text="Cancel",command=self.master.cancel_win)#Just simply close
        self.cancel_button.grid(row=0,column=0)

        #Submit Button
        self.submit_button = tk.CTkButton(master=self.buttons_frame,text="Save",command=self.master.update_theme)#Save and close
        self.submit_button.grid(row=0,column=1)

        #PACK FRAMES
        self.window_frame.pack(fill="x",padx=10,pady=10)
        self.text_frame.pack(fill="x",padx=10,pady=(0,10))
        self.buttons_frame.pack(fill="x",padx=10,pady=(0,10))

    #Open the text colour picker
    def change_text_color(self):
        colors = askcolor(title="Text Color Chooser")
        if colors!=None:
            self.text_picker.configure(fg_color=colors[1],text=str(colors[1]))

    #Open the background colour picker
    def change_bg_color(self):
        colors = askcolor(title="Text Background Color Chooser")
        if colors!=None:
            self.bg_picker.configure(fg_color=colors[1],text=str(colors[1]))


    def set_dark(self):
        self.theme="Dark"
        self.dark_mode_button.configure(fg_color=['#3B8ED0', '#1F6AA5'])
        self.light_mode_button.configure(fg_color="transparent")

    def set_light(self):
        self.theme="Light"
        self.light_mode_button.configure(fg_color=['#3B8ED0', '#1F6AA5'])
        self.dark_mode_button.configure(fg_color="transparent")
