###### WINDOWS
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023
######
###### Code containing the 6 sub windows: PREVIEW DOCX, DETAILS, HOTKEYS, EDIT_OBJ, PREVIEW TEXT, THEME
######


# IMPORTS
############################################################################################################

from functions import *
import customtkinter as tk
from tkinter.colorchooser import askcolor
import fitz
from PIL import Image
import io
from docx2pdf import convert
from functools import partial

# PREVIEW DOCX WINDOW
############################################################################################################
class Preview(tk.CTkToplevel):
    #Constructor
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Output DOCX Preview")
        self.minsize(600,750)
        self.prevw,self.prevh=600,750

        self.preview_frame=tk.CTkScrollableFrame(master=self)
        self.preview_frame.place(relx=0.5,rely=0.5,relwidth=0.8,relheight=0.9,anchor="center")
        
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
            if self.count>=50:
                for w in self.preview_frame.winfo_children():
                    w.destroy()
                for i in self.pages:
                    w = int(e.width*0.8)
                    timg = tk.CTkImage(light_image=i,size=(w,w*1.41))
                    label = tk.CTkLabel(master=self.preview_frame, image = timg,text=None)
                    label.pack()
                self.count=0

# DETAIL WINDOW
############################################################################################################
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

# HOTKEYS WINDOW
############################################################################################################
class Hotkeys(tk.CTk):
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master

# EDIT OBJECTIONS WINDOW
############################################################################################################
# Window to edit the current objections! 
class EditObjections(tk.CTkToplevel):
    #Constructor
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Objections Editor")
        self.master=master
        self.minsize(1100,700)
        self.objections = open_objections()
        self.current_objection=""
        font = (master.theme["text_font"],int(master.theme["text_size"]))
        label_font = tk.CTkFont("Arial",16,underline=True,weight="bold")

        #LAYOUT OF OBJECTIONS DICT FOR REFERENCE
        #Name,Objection,Additional,Modify?,Autofill?,Autofills
        
        #BAR FRAME
        self.bar_frame = tk.CTkFrame(master=self,fg_color="#161616",corner_radius=0)
        self.bar_frame.pack(padx=0,pady=0,fill="x")
        #Save
        save_btn = tk.CTkButton(master=self.bar_frame,fg_color="transparent",corner_radius=0,text="Save All",width=100,command=self.save_all)
        save_btn.pack(side="left")
        #Add
        new_btn = tk.CTkButton(master=self.bar_frame,fg_color="transparent",corner_radius=0,text="New",width=100,command=self.new)
        new_btn.pack(side="left")
        #Delete
        del_btn = tk.CTkButton(master=self.bar_frame,fg_color="transparent",corner_radius=0,text="Delete",width=100,command=self.delete)
        del_btn.pack(side="left")
        #Reset all
        reset_btn = tk.CTkButton(master=self.bar_frame,fg_color="transparent",corner_radius=0,text="Reset All",width=100,command=self.reset_all)
        reset_btn.pack(side="right")

        #OBJECTION LIST FRAME
        self.list_frame = tk.CTkScrollableFrame(master=self,corner_radius=0)
        self.list_frame.pack(padx=0,pady=0,expand=True,side="left",fill="both")
        #Add each objection as a button
        self.objection_buttons = []#List holds the buttons
        self.redraw_buttons()

        #OBJECTION EDIT FRAME
        self.edit_frame = tk.CTkFrame(master=self)
        self.edit_frame.pack(ipadx=300,padx=20,pady=20,expand=True,side="right",fill="both")
        #Name
        name_label=tk.CTkLabel(master=self.edit_frame,text="OBJECTION NAME:",font=label_font,anchor="w")
        name_label.pack(fill="x",padx=10,pady=(5,5))
        self.name_entry = tk.CTkEntry(master=self.edit_frame,font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.name_entry.pack(padx=20,fill="x")
        #Objection
        objection_label=tk.CTkLabel(master=self.edit_frame,text="OBJECTION BODY:",font=label_font,anchor="w")
        objection_label.pack(fill="x",padx=10,pady=(5,5))
        self.objection_entry = tk.CTkTextbox(master=self.edit_frame,wrap="word",height=100,font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.objection_entry.pack(padx=20,fill="both",expand=True)
        #End Text
        additional_label=tk.CTkLabel(master=self.edit_frame,text="ADDITIONAL TEXT:",font=label_font,anchor="w")
        additional_label.pack(fill="x",padx=10,pady=(5,5))
        self.additional_entry = tk.CTkTextbox(master=self.edit_frame,wrap="word",height=50,font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.additional_entry.pack(padx=20,pady=(0,10),fill="both",expand=True)
        #Autofill Text
        autofill_label=tk.CTkLabel(master=self.edit_frame,text="AUTO FILLS:",font=label_font,anchor="w")
        autofill_label.pack(fill="x",padx=10,pady=(5,5))
        self.autofill_entry = tk.CTkTextbox(master=self.edit_frame,wrap="word",height=50,font=font,text_color=master.theme["text_color"],fg_color=master.theme["text_bg"])
        self.autofill_entry.pack(padx=20,pady=(0,10),fill="both",expand=True)
        #Checkboxes
        self.modify_box = tk.CTkCheckBox(master=self.edit_frame,text="Alter 'Notwithstanding' Text")
        self.modify_box.pack(padx=20,pady=(0,10),anchor="w")
        self.autofill_box = tk.CTkCheckBox(master=self.edit_frame,text="Use Autofills")
        self.autofill_box.pack(padx=20,pady=(0,10),anchor="w")
        # Save objections
        """
        dic={}
        for o in self.objections:
            dic.update({o:[self.objections[o],"",False,False,[]]})
        save_objections(dic)
        """
    #Redraw all of the objection buttons to the window
    def redraw_buttons(self):
        for o in self.objection_buttons:
            o.destroy()
        self.objection_buttons = []
        for w in self.list_frame.winfo_children():
            w.destroy()
        #Add each objection as a button
        for obj in self.objections:
            self.objection_buttons.append(tk.CTkButton(master=self.list_frame,fg_color="transparent",text=obj,anchor="w",command=partial(self.load_objection,obj)))
            self.objection_buttons[-1].pack(anchor="w",fill="x",padx=10)

    #Update the text of the previous button
    def update_button(self,old,new):
        for o in self.objection_buttons:
            if o.cget("text")==old:
                o.configure(text=new,command=partial(self.load_objection,new))#Reset text and command

    #Save all of the objections and close the window
    def save_all(self):
        if self.current_objection!="":
            #Save current one
            name = self.name_entry.get()
            text = self.objection_entry.get("0.0","end").replace("\n","")
            additional = self.additional_entry.get("0.0","end").replace("\n","")
            autofills = self.autofill_entry.get("0.0","end").replace("\n","")
            modify = self.modify_box.get()
            autofill = self.autofill_box.get()
            update_array = [text,additional,modify,autofill,autofills]
            self.objections = {key if key != self.current_objection else name: value for key, value in self.objections.items()}
            #Remove prev and add new
            self.objections[name] = update_array
        #Save json
        save_objections(self.objections)
        #Update main window objections
        self.master.objections = open_objections()
        #Close window
        self.master.objections_frame.redraw_all()
        if self.master.current_req!=0:#Reset all selected objections
            self.master.objections_frame.redraw(self.master.current_req)
        self.master.cancel_win()

    #Create a blank new objection
    def new(self):
        # Add a new black objection below the current one!
        self.objections["New"] = ["","",False,False,[]]
        self.redraw_buttons()

    #Delete the current objection and deselect
    def delete(self):
        # Delete current objection and deselect
        if self.current_objection in self.objections:
            self.objections.pop(self.current_objection)
        self.current_objection=""
        #RESET BOXES
        self.name_entry.delete(0,"end")
        # Objection entry
        self.objection_entry.delete("0.0","end-1c")
        #Additional Entry
        self.additional_entry.delete("0.0","end-1c")
        #Autofills Entry
        self.autofill_entry.delete("0.0","end-1c")
        #Modfiy?
        self.modify_box.deselect()
        self.autofill_box.deselect()
        self.redraw_buttons()

    #Reset all of the objections using the backup file
    def reset_all(self):
        # Set the current objections to those in the backup file!!
        self.objections = open_objections_backup()
        self.current_objection=""
        self.redraw_buttons()
        
    #Open the selected objection
    def load_objection(self,obj):
        #SAVE THE PREVIOUS ONE
        if self.current_objection!="":
            #Add text
            name = self.name_entry.get()
            text = self.objection_entry.get("0.0","end").replace("\n","")
            additional = self.additional_entry.get("0.0","end").replace("\n","")
            autofills = self.autofill_entry.get("0.0","end").replace("\n","")
            modify = self.modify_box.get()
            autofill = self.autofill_box.get()
            update_array = [text,additional,modify,autofill,autofills]
            self.objections = {key if key != self.current_objection else name: value for key, value in self.objections.items()}
            #Remove prev and add new
            self.objections[name] = update_array

            self.update_button(self.current_objection,name)

        # Add relevant text to each box using the dict
        self.current_objection = obj
        self.name_entry.delete(0,"end")
        self.name_entry.insert(0,obj)

        # Objection entry
        self.objection_entry.delete("0.0","end-1c")
        self.objection_entry.insert("0.0",self.objections[obj][0])
        #Additional Entry
        self.additional_entry.delete("0.0","end-1c")
        self.additional_entry.insert("0.0",self.objections[obj][1])
        #Autofills Entry
        self.autofill_entry.delete("0.0","end-1c")
        self.autofill_entry.insert("0.0",str(self.objections[obj][4]))
        #Modfiy?
        if self.objections[obj][2]:
            self.modify_box.select()
        else:
            self.modify_box.deselect()
        #Autofills?
        if self.objections[obj][3]:
            self.autofill_box.select()
        else:
            self.autofill_box.deselect()

# PREVIEW TEXT WINDOW
############################################################################################################
# Window to see a text preview of the full response
class PreviewText(tk.CTk):
    #Constructor
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Response Preview")
        self.geometry("600x400")
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

# THEME WINDOW
############################################################################################################
# Contains theme data
class Theme(tk.CTk):
    #Constructor
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master=master
        self.geometry("400x345")
        self.title("Theme Options")
        self.resizable(False,False)


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






