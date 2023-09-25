# IMPORTS
from functions import *
import customtkinter as tk
from tkinter import *
from functools import partial

# EDIT OBJECTIONS WINDOW
############################################################################################################
# Window to edit the current objections! 
class EditObjections(tk.CTkToplevel):
    #Constructor
    def __init__(self,master):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.title("Objections Editor")
        self.wm_iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico"))#Icon
        self.master=master
        self.minsize(1100,700)

        #GET WINDOW FOCUS
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()

        self.objections = open_objections()
        # Turn list of autofills into string
        for i in self.objections:
            auto_fill_text = ""
            for auto in self.objections[i][4]:
                auto_fill_text = auto_fill_text + auto + ","
            auto_fill_text=auto_fill_text[:-1]#Remove final comma
            self.objections[i][4] = auto_fill_text


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
        self.edit_frame.pack(ipadx=240,padx=20,pady=20,expand=True,side="right",fill="both")
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
        c=0
        for obj in self.objections:
            button_frame = tk.CTkFrame(master=self.list_frame)
            self.objection_buttons.append(tk.CTkButton(master=button_frame,text_color=("black","white"),fg_color="transparent",text=obj,anchor="w",command=partial(self.load_objection,obj)))
            self.objection_buttons[-1].pack(anchor="w",fill="x",padx=(5,0),side="left",expand=True)

            up_arrow = tk.CTkButton(master=button_frame,text_color=("black","white"),fg_color="transparent",text="▲",anchor="w",command=partial(self.up_button,c),width=20)
            up_arrow.pack(side="right")
            down_arrow = tk.CTkButton(master=button_frame,text_color=("black","white"),fg_color="transparent",text="▼",anchor="w",command=partial(self.down_button,c),width=20)
            down_arrow.pack(side="right")

            button_frame.pack(anchor="w",fill="x",expand=True)
            c+=1

    def swap_buttons(self,i1,i2,name1,name2):
        #Swap obj1 and obj2 buttons
        self.objection_buttons[i1].configure(text=name2,command=partial(self.load_objection,self.objections[name2]))
        self.objection_buttons[i2].configure(text=name1,command=partial(self.load_objection,self.objections[name1]))


    def up_button(self,button):
        #Swap button with previous one
        if button==0:
            return
        prev = get_nth_key(self.objections,button-1)
        current = get_nth_key(self.objections,button)
        #Create a new dict and swap
        new = {}
        c=0
        for obj in self.objections:
            if c==button-1:#If previous objection, add current
                new.update({current:self.objections[current]})
            elif c==button:
                new.update({prev:self.objections[prev]})
            else:
                new.update({obj:self.objections[obj]})
            c+=1
        self.objections = new
        self.swap_buttons(button,button-1,current,prev)

    def down_button(self,button):
        #Swap button with previous one
        if button==len(self.objections):
            return
        prev = get_nth_key(self.objections,button+1)
        current = get_nth_key(self.objections,button)
        #Create a new dict and swap
        new = {}
        c=0
        for obj in self.objections:
            if c==button+1:#If previous objection, add current
                new.update({current:self.objections[current]})
            elif c==button:
                new.update({prev:self.objections[prev]})
            else:
                new.update({obj:self.objections[obj]})
            c+=1
        self.objections = new
        self.swap_buttons(button,button+1,current,prev)

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

        for i in self.objections:
            if "," in self.objections[i][4]:
                self.objections[i][4]=self.objections[i][4].split(",")
            else:
                self.objections[i][4]=[]
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
        self.objections["New"] = ["","",False,False,""]
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