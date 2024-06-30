# IMPORTS
from functions import *
import customtkinter as tk
from customtkinter.windows.widgets.core_widget_classes.dropdown_menu import DropdownMenu

# CUSTOM SMART TEXT BOX CLASS, BUILT IN SPELL CHECKER
class SmartTextbox(tk.CTkTextbox):
    #Constructor 
    def __init__(self,master,main_master,**kwargs):
        #FRAME SETUP
        super().__init__(master,undo=True,maxundo=-1, **kwargs)

        self.main_master = main_master
        #This is the previous text in the box
        self.previous_text=""
        self.issues=[]
        self.istart,self.iend=0,0#Start and end of selected spellings
        self.pop = DropdownMenu(self,values=["init"])
        self.bind("<Button-3>",self.popup)
        self.after(2000,self.spellcheck)

    def spellcheck(self):
        #DO SPELLCHECKING!
        if self.main_master.CONFIG["spelling"]["use_spellcheck"]:
            self.current_text = self.get(0.0,"end-1c")
            #Only spellcheck if text has changed
            if self.current_text!=self.previous_text:
                #Highlight them
                self.issues = spellcheck(self," "+self.get("0.0","end-1c"))# [message,start,width,replacements array]
        else:
            #CLEAR SPELLCHECK HERE!
            pass

        self.previous_text = self.current_text
        self.after(int(self.main_master.CONFIG["spelling"]["spellcheck_interval"]),self.spellcheck)

    def insert_spelling(self,v):
        if v=="Spelling Issue":#Only add if a valid fix, not the title
            return
        elif v=="Always Ignore":
            self.main_master.add_ignore_word(self.iword)
            self.issues = spellcheck(self," "+self.get("0.0","end-1c"))# [message,start,width,replacements array]
            return
        else:
            self.delete(self.istart,self.iend)
            self.insert(self.istart,v)

    def popup(self,event):
        try:
            #Get index position
            index = self.index(f"@{event.x},{event.y}")

            #Check most recent spell check, these should be held by each text box!
            vals=[]
            for i in self.issues:
                #if clicked where the issue is:
                chars = self._textbox.count("0.0", index, "chars")[0]
                if chars>=int(i[3])-1 and chars<=int(i[3]+i[4]) and vals==[]:#If in issue range, only pick 1!
                    added = 0
                    for r in i[5]:
                        if added<int(self.main_master.CONFIG["spelling"]["corrections"]):
                            vals.append(r)#Add issue to correction menu, Only add maximum of settings value!
                            added+=1
                    vals.insert(0,i[0])
                    vals.insert(1,i[1])
                    self.istart = "0.0+"+str(int(i[3])-1)+"c"
                    self.iend = "0.0+"+str(int(i[3]+i[4])-1)+"c"
                    self.iword = str(i[2])

            #If none then ignore
            if vals==[]:
                return
            
            #Create popup spelling window
            self.pop = DropdownMenu(self,values=vals,command=self.insert_spelling)

            if len(vals)>1:
                self.pop.insert_separator(2)
            try:
                self.pop.tk_popup(event.x_root, event.y_root, 0)
            finally:
                #Release the grab
                self.pop.grab_release()

        except:
            print("Popup failed")