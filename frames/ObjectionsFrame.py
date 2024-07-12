# Main Imports
from frames.__modules__ import *

# OBJECTIONS FRAME 
############################################################################################################
# Contains list of all possible objections
class Objections_Frame(tk.CTkFrame):
    #Constructor
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #Frame Setup
        self.master=master

        self.opts=[]
        #List Frame
        self.list_frame = tk.CTkScrollableFrame(master=self,corner_radius=0,fg_color="transparent")
        self.list_frame.place(relheight=0.85,relwidth=1)
        #Info Frame
        self.info_frame = tk.CTkFrame(master=self,corner_radius=0)
        self.info_frame.place(relheight=0.14,rely=0.86,relwidth=1)

        #Draw Info box at bottom of objection frame
        self.current_objection_label = tk.CTkLabel(master=self.info_frame,text="OBJECTION NAME")
        self.current_objection_label.pack(padx=5)
        #Objection Input
        self.objection_input = tk.CTkEntry(master=self.info_frame,placeholder_text="Objection Input",text_color="black")
        self.objection_input.pack(padx=15,fill="x")
        #Additional Text Input
        self.additional_input = tk.CTkEntry(master=self.info_frame,placeholder_text="Additional Input",text_color="black")
        self.additional_input.pack(padx=15,fill="x",pady=(5,0))

        self.redraw_all()#Draw all of the objection buttons

    #ORDER and redraw all of the objection buttons
    def redraw_all(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        
        #Cancel if there are no objections
        if len(list(self.master.objections.keys()))<1:
            return
        l=[]
        for i in range(len(list(self.master.objections.keys()))):
            l.append(i)
        self.list_frame.grid_rowconfigure(l,weight=1)
        self.list_frame.columnconfigure((0,1),weight=1)
        # Objections (from file)
        self.options = list(self.master.objections.keys())

        #Move ones with entries to the front
        c=0
        for opt in self.options:
            #For each key
            if "[VAR]" in self.master.objections[opt]:
                #Remove
                temp = opt
                self.options.remove(opt)
                #Insert at the start
                self.options.insert(c,temp)
                c+=1

        # Draw
        c=0
        self.opts=[]
        self.params=[]
        for opt in self.options:
            optbox = tk.CTkButton(master=self.list_frame,text_color=("black","white"),text=opt,corner_radius=0,anchor="w",fg_color="transparent",hover=False,command=partial(self.master.toggle_objection,str(opt)))
            optbox.grid(row=c,column=0,sticky="ew",padx=(10,10),pady=2,columnspan=2)

            #Get theme background
            #SET THIS TO THE COLOUR OF THEME
            if self.master.CONFIG["general"]["hover_tooltips"]:
                SmartToolTip(anchor_widget=optbox, text=opt+". "+self.master.objections[opt][0])
            
            
            #Set Right Click Command
            optbox.bind("<Button-3>",partial(self.master.toggle_selected_objection,str(opt)))
            self.opts.append(optbox)
            c+=1
        
    #Update the colours of the objection buttons
    def redraw(self,req):
        #HIGHLIGHT SELECTED ETC
        for opt in self.opts:
            opt.configure(fg_color="transparent")
        for opt in req.opts:#For each button
            if opt.selected:
                self.toggle_button(opt.key)

    #Change the colour of a single objection button when needed
    def toggle_button(self,obj):
        for opt in self.opts:#For each button
            if opt.cget("text")==obj:
                if opt.cget("fg_color")=="green":
                    opt.configure(fg_color="transparent")
                else:
                    opt.configure(fg_color="green")
                return

    #Reset the colour of all the objection buttons
    def reset(self):
        for opt in self.opts:#For each button
            opt.configure(fg_color="transparent")

    #Set the info box to the currently selected objection
    def update_current(self,obj):
        if obj!="":
            #Set name
            self.current_objection_label.configure(text=obj.key.upper())
            #Set Objection Param
            self.objection_input.delete(0,"end")
            if obj.need_param:
                self.objection_input.configure(state="normal",fg_color="white")
                self.objection_input.insert(0,obj.param)
                self.objection_input._activate_placeholder()
            else:
                self.objection_input._activate_placeholder()
                self.objection_input.configure(state="disabled",fg_color=self.info_frame._fg_color)
            

            #Set additional Param
            self.additional_input.delete(0,"end")
            if obj.need_additional_param:
                self.additional_input.configure(state="normal",fg_color="white")
                self.additional_input.insert(0,obj.additional_param)
                self.additional_input._activate_placeholder()
            else:
                self.additional_input._activate_placeholder()
                self.additional_input.configure(state="disabled",fg_color=self.info_frame._fg_color)

        else:
            self.current_objection_label.configure(text="OBJECTION NAME")
            #Set Objection Param
            self.objection_input.delete(0,"end")
            self.objection_input._activate_placeholder()
            #Set additional Param
            self.additional_input.delete(0,"end")
            self.additional_input._activate_placeholder()