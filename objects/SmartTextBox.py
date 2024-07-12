# Main Imports
from objects.__modules__ import *
from objects.Action import *
from functions import *

# CUSTOM SMART TEXT BOX CLASS, BUILT IN SPELL CHECKER
class SmartTextbox(tk.CTkTextbox):
    #Constructor 
    def __init__(self,master,main_master,undo=True,**kwargs):
        #FRAME SETUP
        super().__init__(master,undo=undo,maxundo=100,autoseparators=False, **kwargs)

        self.main_master = main_master
        self.undo_enabled = undo#Name undo taken
        #This is the previous text in the box
        self.previous_text=""
        self.issues=[]
        self.istart,self.iend=0,0#Start and end of selected spellings
        self.pop = DropdownMenu(self,values=["init"])
        self.bind("<Button-3>",self.popup)
        self.after(int(self.main_master.CONFIG["spelling"]["spellcheck_interval"]),self.spellcheck)

        if self.undo_enabled:
            #Bind a function for when this is modified
            autoseparator_bindings = ["<BackSpace>","<Delete>","<Return>","<<Cut>>","<<Paste>>","<<Clear>>",
                                    "<<PasteSelection>>","<space>"]
            for bind in autoseparator_bindings:
                self.bind(bind,self.modified)

            self.bind("<KeyPress>",self.check_if_start)

            #THIS UNBINDS THE UNDO AND REDO!
            self._textbox.event_delete("<<Undo>>")
            self._textbox.event_delete("<<Redo>>")

    #Runs when text is inserted or deleted
    def modified(self,e):
        if self.undo_enabled:
            #ADD AN AUTOSEPERATOR:
            self.edit_separator()
            #Add this onto undo stack -> Then access the box when an undo is needed
            self.main_master.add_action_to_stack(ActionTextBox(self.main_master,self))

    #If the text is empty then add a separator
    def check_if_start(self,e):
        if self.get(0.0,"end-1c") == "":
            self.modified(None)

    def spellcheck(self):
        if self.winfo_manager()!=None:#Only check if text box placed
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
            self.modified(None)

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

    def undo(self):#THIS FUNCTION IS NOT USED!
        self._textbox.edit_undo()

    def redo(self):#THIS FUNCTION IS NOT USED!
        self._textbox.edit_redo()

    def insert(self, index, text, tags=None):
        #self.modified(None)#Modify the autoseparators when inserted to
        return super().insert(index, text, tags)
        