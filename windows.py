import customtkinter as tk
from tkinter.colorchooser import askcolor
import fitz
from PIL import Image
import io
from docx2pdf import convert

# CUSTOM TKINTER WINDOW CLASSES
############################################################################################################

class Preview(tk.CTkToplevel):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Output DOCX Preview")
        self.minsize(600,750)
        self.preview_frame=tk.CTkScrollableFrame(master=self)
        self.preview_frame.place(relx=0.5,rely=0.5,relwidth=0.8,relheight=0.9,anchor="center")
        self.prevw,self.prevh=600,750
        # Convert this docx to PDF
        convert("assets/temp.docx", "assets/temp.pdf")
        #Show PDF
        pdf_location="assets/temp.pdf"
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
            print(self.count)
            if self.count>=50:
                for w in self.preview_frame.winfo_children():
                    w.destroy()
                for i in self.pages:
                    w = int(e.width*0.8)
                    timg = tk.CTkImage(light_image=i,size=(w,w*1.41))
                    label = tk.CTkLabel(master=self.preview_frame, image = timg,text=None)
                    label.pack()
                self.count=0









# Contains details data
class Detail(tk.CTk):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master
        self.geometry("400x500")
        self.title("Document Details")
        self.resizable(False,False)
        self.grid_columnconfigure((0,1),weight=1)
        #County
        county = tk.CTkLabel(master=self,text="County")
        county.grid(row=0,column=0,padx=20,sticky="w")
        self.county = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.county.grid(row=1,column=0,padx=30,columnspan=2,sticky="ew")
        self.county.insert("0.0",self.master.doc_details["county"])
        #Case Number
        case = tk.CTkLabel(master=self,text="Case Number")
        case.grid(row=2,column=0,padx=20,sticky="w")
        self.case = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.case.grid(row=3,column=0,padx=30,columnspan=2,sticky="ew")
        self.case.insert("0.0",self.master.doc_details["case_number"])
        #Document
        document = tk.CTkLabel(master=self,text="Document Name")
        document.grid(row=4,column=0,padx=20,sticky="w")
        self.document = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.document.grid(row=5,column=0,padx=30,columnspan=2,sticky="ew")
        self.document.insert("0.0",self.master.doc_details["document"])
        #Plaintiff
        plaintiff = tk.CTkLabel(master=self,text="Propounding Party")
        plaintiff.grid(row=6,column=0,padx=20,sticky="w")
        self.plaintiff = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.plaintiff.grid(row=7,column=0,padx=30,columnspan=2,sticky="ew")
        self.plaintiff.insert("0.0",self.master.doc_details["plaintiff"])
        #Defendant
        defendant = tk.CTkLabel(master=self,text="Responding Party")
        defendant.grid(row=8,column=0,padx=20,sticky="w")
        self.defendant = tk.CTkTextbox(master=self,height=60,wrap="word")
        self.defendant.grid(row=9,column=0,padx=30,columnspan=2,sticky="ew")
        self.defendant.insert("0.0",self.master.doc_details["defendant"])

        #Cancel Button
        self.cancel_button = tk.CTkButton(master=self,text="Cancel",command=self.master.cancel_win)#Just simply close
        self.cancel_button.grid(row=10,column=0,pady=20)

        #Submit Button
        self.submit_button = tk.CTkButton(master=self,text="Save",command=self.master.save_win)#Save and close
        self.submit_button.grid(row=10,column=1,pady=20)









# Window to edit and browse autofills
class Autofill(tk.CTk):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()

        # Have a column for each valid objection
        # In a text box have all of the options
        # These can be edited and will be saved after with validation


# Window to see a text preview of the response
class PreviewText(tk.CTk):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        #Window showing the end objections and response combined!
        self.title("Response Preview")
        self.geometry("600x400")
        #SET THE TEXT HERE!!!
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








# Contains theme data
class Theme(tk.CTk):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master
        self.geometry("400x345")
        self.title("Theme Options")
        self.resizable(False,False)
        #self.grid_columnconfigure((0,1),weight=1)


        # Window Frame
        self.window_frame = tk.CTkFrame(master=self,width=380)
        self.window_frame.grid_columnconfigure((0,1),weight=2)
        # Main Theme
        self.window_text=tk.CTkLabel(master=self.window_frame,text="Window")
        self.window_text.grid(row=0,column=0,sticky="ew",padx=20,pady=0,columnspan=2)

        self.theme_text=tk.CTkLabel(master=self.window_frame,text="Theme")
        self.theme_text.grid(row=1,column=0,sticky="w",padx=20,pady=0)
        self.theme_button=tk.CTkSegmentedButton(master=self.window_frame,values=["Dark","Light"])
        self.theme_button.set(self.master.theme["theme"])
        self.theme_button.grid(row=2,column=0,sticky="ew",padx=30,pady=(0,20),columnspan=2)


        # Text Frame
        self.text_frame = tk.CTkFrame(master=self,width=380)
        self.text_frame.grid_columnconfigure((0,1),weight=2)
        cols=["#000000","#FFFFFF","#964B00","#89CFF0","#808080"]
        self.text_text=tk.CTkLabel(master=self.text_frame,text="Text")
        self.text_text.grid(row=0,column=0,sticky="ew",padx=20,pady=0,columnspan=2)
        # Text Colour
        # #Have ~6 buttons of different colour to chose from
        self.window_text=tk.CTkLabel(master=self.text_frame,text="Text Color")
        self.window_text.grid(row=1,column=0,sticky="w",padx=20,pady=0)

        self.text_picker = tk.CTkButton(master=self.text_frame,text=self.master.theme["text_color"],fg_color=self.master.theme["text_color"],command=self.change_text_color)
        self.text_picker.grid(row=2,column=0,padx=40)
        #self.text_picker = ColorPicker(master=self.text_frame,colors=cols)
        #self.text_picker.grid(row=2,column=0,padx=40)

        
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


    def change_text_color(self):
        colors = askcolor(title="Text Color Chooser")
        if colors!=None:
            self.text_picker.configure(fg_color=colors[1],text=str(colors[1]))

    def change_bg_color(self):
        colors = askcolor(title="Text Background Color Chooser")
        if colors!=None:
            self.bg_picker.configure(fg_color=colors[1],text=str(colors[1]))






