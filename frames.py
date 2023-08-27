import customtkinter as tk
from PIL import Image

PDF_ICON=tk.CTkImage(Image.open("assets/pdf.png"),size=(16,16))

# Contains request and response data
class Response_Frame(tk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #Frame Setup
        self.grid_columnconfigure((0,1),weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12),weight=1)
        self.prev=None

        #Label Font
        label_font = tk.CTkFont("Arial",16,underline=True,weight="bold")
        # Request Body
        self.request_label=tk.CTkLabel(master=self,text="REQUEST:",font=label_font)
        self.request_label.grid(row=0,column=0,sticky="w",columnspan=2,padx=20)
        self.request_text=tk.CTkTextbox(master=self,wrap="word",state="disabled",height=20)
        self.request_text.grid(row=1,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3)
        

        # Objections Body
        self.objection_label=tk.CTkLabel(master=self,text="OBJECTIONS:",font=label_font)
        self.objection_label.grid(row=4,column=0,sticky="w",columnspan=2,padx=20)
        self.objection_text=tk.CTkTextbox(master=self,wrap="word",state="disabled",height=20)
        self.objection_text.grid(row=5,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3)

        #Response body
        self.response_label=tk.CTkLabel(master=self,text="RESPONSE:",font=label_font)
        self.response_label.grid(row=8,column=0,sticky="w",columnspan=2,padx=20)
        self.response_text=tk.CTkTextbox(master=self,wrap="word",state="normal")
        self.response_text.grid(row=9,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3)

        #Clear
        self.clear_button = tk.CTkButton(master=self,text="Check With Client",command=self.master.check)
        self.clear_button.grid(row=12,column=0)

        #Next
        self.next_button = tk.CTkButton(master=self,text="Submit",command=self.master.submit)
        self.next_button.grid(row=12,column=1)

        #RFP menu
        self.resp_label = tk.CTkLabel(master=self,text="Documents Location:")
        self.resp_text = tk.CTkEntry(master=self,state="normal")
        self.resp_option = tk.CTkSegmentedButton(master=self,values=["Available","Not Exist","Not Possessed","Lost","Custom"])
        self.resp_option.set("Available")

    def redraw(self,req_type):
        if req_type=="RFP":
            if self.prev!="RFP":
                self.response_text.grid_forget()
                #Selector for option
                self.resp_option.grid(row=9,column=0,padx=30,sticky="ew",columnspan=2)
                #Text box for file etc
                self.resp_label.grid(row=10,column=0,sticky="w",padx=(30,0),columnspan=2)
                self.resp_text.grid(row=10,column=0,sticky="ew",padx=(160,30),columnspan=2)
                self.response_text.grid(row=11,column=0,padx=30,stick="nsew",columnspan=2,rowspan=1)
                self.response_text.configure(state="disabled") 
        else:
            self.resp_label.grid_forget()
            self.resp_text.grid_forget()
            self.resp_option.grid_forget()
            #Just change text if it exists
            if self.prev=="RFP":
                self.response_text.grid_forget()
                self.response_text.grid(row=9,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3) 
            self.response_text.configure(state="normal") 
        self.prev = req_type

    def reset(self):
        #Reset Request Number
        self.request_label.configure(text="REQUEST:")
        #Reset RFP Button
        self.resp_option.set("Available")
        #Reset RFP text
        self.resp_text.delete(0,"end")
        #Reset Respnse
        self.response_text.configure(state="normal") 
        self.response_text.delete("0.0","end")
        #Reset Objection
        self.objection_text.configure(state="normal") 
        self.objection_text.delete("0.0","end")
        self.objection_text.configure(state="disabled") 
        #Reset Request
        self.request_text.configure(state="normal") 
        self.request_text.delete("0.0","end")
        self.request_text.configure(state="disabled") 
       














# Contains list of all the requests in file
class Requests_Frame(tk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_buttons=[]
        self.request_buttons=[]
        # Files Frame
        text = tk.CTkLabel(master=self,text="FILES",anchor="w")
        text.pack(fill="both",padx=10)
        self.file_frame = tk.CTkScrollableFrame(master=self,corner_radius=0,fg_color="transparent")
        self.file_frame.pack(padx=0,pady=0,fill="x")
        # Requests Frame
        text = tk.CTkLabel(master=self,text="REQUESTS",anchor="w")
        text.pack(fill="both",padx=10)
        self.list_frame = tk.CTkScrollableFrame(master=self,corner_radius=0,fg_color="transparent")
        self.list_frame.pack(padx=0,pady=0,expand=True,fill="both")
        

    def show_files(self,files):
        for w in self.file_frame.winfo_children():
            w.destroy()
        self.file_buttons=[]
        c=1
        for i in files:
            fg_color="transparent"
            if i==self.master.current_file:
                fg_color='#144870'
            button = tk.CTkButton(master=self.file_frame,image=PDF_ICON,anchor="w",text=str(i.name).split("/")[-1][:22]+"...",hover=False,corner_radius=0,fg_color=fg_color,command=i.set,text_color=i.color)
            button.pack(fill="x",side="top")
            self.file_buttons.append(button)
            c+=1
        

    def update_files(self,files):
        c=0
        for i in files:
            if i==self.master.current_file:
                self.file_buttons[c].configure(fg_color='#144870',text_color=i.color)
            else:
                self.file_buttons[c].configure(fg_color="transparent",text_color=i.color)
            c+=1

    #Scroll to the current file
    def scroll_to_file(self,reset=False):
        pass
    
    #Scroll to a request
    def scroll_to(self,reset=False):
        if self.master.current_req!=0:
            if reset:
                self.list_frame._parent_canvas.yview_moveto(0)
                #CHANGE THIS TO A CALCULATION OF THE NEW POSITION
                self.update()
            #If new not in the fraction the current move
            current_y = self.list_frame._parent_canvas.yview()#Tuple of start & end
            current_index = self.master.reqs.index(self.master.current_req)#Index of current request
            compare = current_index/len(self.master.reqs)#Exact position of current req
            
            gap=(current_y[1]-current_y[0])
    
            if compare>current_y[1]-1/len(self.master.reqs):#If after box
                new = compare-gap+1/len(self.master.reqs)
                self.list_frame._parent_canvas.yview_moveto(new)
            elif compare<current_y[0]:#If before box
                new = compare
                self.list_frame._parent_canvas.yview_moveto(new)

    def show_list(self,reqs):
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.request_buttons=[]
        c=1
        for i in reqs:
            fg_color="transparent"
            if i==self.master.current_req:
                fg_color='#144870'
            color=i.color
            req_type=self.master.req_type
            if i.custom_key=="":
                text = c
            else:
                text = i.custom_key
            button = tk.CTkButton(master=self.list_frame,text=req_type+" NO. "+str(text),corner_radius=0,text_color=color,fg_color=fg_color,hover=False,command=i.set)
            button.pack(fill="x",side="top")
            self.request_buttons.append(button)
            c+=1


    def update_list(self,reqs):
        c=0
        for i in reqs:
            color=i.color
            if i==self.master.current_req:
                self.request_buttons[c].configure(fg_color='#144870',text_color=color)
            else:
                self.request_buttons[c].configure(fg_color="transparent",text_color=color)
            c+=1

















# Contains list of all possible objections
class Objections_Frame(tk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #Frame Setup
        l=[]
        for i in range(len(list(master.objections.keys()))):
            l.append(i)
        self.grid_rowconfigure(l,weight=1)
        self.columnconfigure((0,1),weight=1)
        # Option (from file)
        self.options = sorted(list(master.objections.keys()))
        #Move ones with entries to the front

        c=0
        for opt in self.options:
            #For each key
            if "[VAR]" in master.objections[opt] or opt=="Compilation":
                #Remove
                temp = opt
                self.options.remove(opt)
                #Insert at the start
                self.options.insert(c,temp)
                c+=1

        c=0
        self.opts=[]
        self.params=[]
        for opt in self.options:
            optbox = tk.CTkCheckBox(master=self,text=opt,corner_radius=0)
            optbox.grid(row=c,column=0,sticky="w",padx=(10,0),pady=2)
            self.opts.append(optbox)

            #Text Input, SET COLOURS
            if "[VAR]" in master.objections[opt] or opt=="Compilation":#Highlight valid inputs
                param = tk.CTkEntry(master=self,state="normal",fg_color=("white","#3b3b3b"))
            else:
                param = tk.CTkEntry(master=self,state="disabled",fg_color="transparent")
            param.grid(row=c,column=1,padx=(10,5),sticky="ew")
            self.params.append(param)
            c+=1

    def redraw(self,req):
        for i in range(len(self.opts)):
            #Update checkbox
            if req.opts[i].selected==1:
                self.opts[i].select()#configure(variable=req.opts[i].selected)
            else:
                self.opts[i].deselect()
            #Update Entry
            self.params[i].delete(0,"end")
            self.params[i].insert(0,req.opts[i].param)
    def reset(self):
        for i in range(len(self.opts)):
            self.opts[i].deselect()
            #Update Entry
            self.params[i].delete(0,"end")

















class Bar_Frame(tk.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)

        # File
        var = tk.StringVar(value="File")
        self.file=tk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["New Window","Open File","Open Folder","Save File As","Save Workspace As","Export File as DOCX","Export All as DOCX","Preview DOCX","Close File","Close All","Exit"],width=100,corner_radius=0,bg_color="transparent",command=self.call_file)
        self.file.configure(button_color="#161616",fg_color="#161616")
        self.file.pack(side="left")

        # Discovery
        var = tk.StringVar(value="Discovery")
        self.discovery=tk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["List Here"],width=100,corner_radius=0,bg_color="transparent",command=self.call_discovery)
        self.discovery.configure(button_color="#161616",fg_color="#161616")
        self.discovery.pack(side="left")

        # View
        var = tk.StringVar(value="Options")
        self.options=tk.CTkOptionMenu(master=self,anchor="center",variable=var,values=["Theme","Autofill","Highlights","Hotkeys","Other"],width=100,corner_radius=0,bg_color="transparent",command=self.call_options)
        self.options.configure(button_color="#161616",fg_color="#161616")
        self.options.pack(side="left")

        # Details
        self.details = tk.CTkButton(master=self,text="Details",fg_color="transparent",width=100,command=self.master.view_details,corner_radius=0)
        self.details.pack(side="left")

        # Clear
        self.clear = tk.CTkButton(master=self,text="Clear",fg_color="transparent",width=100,corner_radius=0,command=self.master.clear)
        self.clear.pack(side="right")

        # Copy Previous
        self.copy = tk.CTkButton(master=self,text="Copy Previous",fg_color="transparent",width=100,command=self.master.copy_previous,corner_radius=0)
        self.copy.pack(side="right")

        # Preview
        self.copy = tk.CTkButton(master=self,text="Preview",fg_color="transparent",width=100,corner_radius=0,command=self.master.preview_text)
        self.copy.pack(side="right")

        # Save
        self.copy = tk.CTkButton(master=self,text="Save",fg_color="transparent",width=100,corner_radius=0,command=self.master.quick_save)
        self.copy.pack(side="right")



    def call_file(self,val):# All of file manu options
        self.file.set("File")
        if val=="New Window":
            self.master.create_window()
        elif val=="Open File":
            self.master.select_file()
        elif val=="Open Folder":
            self.master.select_folder()
        elif val=="Save File As":
            self.master.save_file()
        elif val=="Save Workspace As":
            self.master.save_workspace()
        elif val=="Export File as DOCX":
            self.master.export_current()
        elif val=="Export All as DOCX":
            self.master.export_all()
        elif val=="Preview DOCX":
            self.master.view_preview()
        elif val=="Close File":
            self.master.close_file()
        elif val=="Close All":
            self.master.close_all()
        elif val=="Exit":
            self.master.exit_window()

    def call_discovery(self,val):# All of discovery menu options
        self.discovery.set("Discovery")

    def call_options(self,val): # All of options menu options
        self.options.set("Options")
        if val=="Theme":
            self.master.view_theme()
        elif val=="Autofill":
            self.master.view_autofill()