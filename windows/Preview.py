# IMPORTS
from functions import *
import customtkinter as tk
from tkinter import *
from docx2pdf import convert
import fitz,io,sys
from PIL import Image

# PREVIEW DOCX WINDOW
############################################################################################################
class Preview(tk.CTkToplevel):
    #Constructor
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Output DOCX Preview")
        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico")))
        self.minsize(600,750)
        self.prevw,self.prevh=600,750

        #GET WINDOW FOCUS
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()


        self.preview_frame=tk.CTkScrollableFrame(master=self)
        self.preview_frame.place(relx=0.5,rely=0.5,relwidth=0.8,relheight=0.9,anchor="center")

        # Convert this docx to PDF
        sys.stderr = open(os.path.join(os.path.dirname(__file__),"../assets/console.log"), "w")
        convert(os.path.join(os.path.dirname(__file__),"../assets/temp.docx"), os.path.join(os.path.dirname(__file__),"../assets/temp.pdf"))
        sys.stderr.close()
        #Show PDF
        pdf_location=os.path.join(os.path.dirname(__file__),"../assets/temp.pdf")
        self.pages=[]

        open_pdf = fitz.open(pdf_location)

        for page in open_pdf:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix,0) if pix.alpha else pix
            img = pix1.tobytes("ppm")
            img = Image.open(io.BytesIO(img))
            self.pages.append(img)
        for i in self.pages:
            w = int(self._current_width*0.8)
            timg = tk.CTkImage(light_image=i,size=(w,w*1.41))
            label = tk.CTkLabel(master=self.preview_frame, image = timg,text=None)
            label.pack()

        #self.bind("<Configure>",self.redraw)
        self.count=0

    def redraw(self,e):
        if e.height!=self.prevh or e.width!=self.prevw:
            self.prevh=e.height
            self.prevw=e.width
            self.count+=1
            if self.count>=50:
                for w in self.preview_frame.winfo_children():
                    w.destroy()
                for i in self.pages:
                    w = int(e.width*0.8)
                    timg = tk.CTkImage(light_image=i,size=(w,w*1.41))
                    label = tk.CTkLabel(master=self.preview_frame, image = timg,text=None)
                    label.pack()
                self.count=0