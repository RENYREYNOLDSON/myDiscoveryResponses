# Main Imports
from frames.__modules__ import *

# RESPONSE FRAME 
############################################################################################################
# Contains request and response data
class Response_Frame(tk.CTkFrame):
    #Constructor 
    def __init__(self,master, **kwargs):
        #FRAME SETUP
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1),weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13),weight=1)
        self.prev=None
        #Set Custom Label Font
        label_font = tk.CTkFont("Arial",16,underline=True,weight="bold")

        self.default_frame=tk.CTkFrame(master=self,fg_color="transparent")
        self.RFA_frame=tk.CTkFrame(master=self,fg_color="transparent")
        self.RFP_frame=tk.CTkFrame(master=self,fg_color="transparent")

        self.current_frame=self.default_frame#This keeps track of current open frame

        #Previous option - Used to track RFA and RFP options
        self.previous_option = None

        #1. STANDARD REQUEST AND OBJECTION
        # Request Body
        self.request_label=tk.CTkLabel(master=self,text="REQUEST:",font=label_font)
        self.request_label.grid(row=0,column=0,sticky="w",columnspan=2,padx=20)
        self.request_text=tk.CTkTextbox(master=self,wrap="word",state="disabled",height=40)
        self.request_text.grid(row=1,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3)
        # Objections Body
        self.objection_label=tk.CTkLabel(master=self,text="OBJECTIONS:",font=label_font)
        self.objection_label.grid(row=4,column=0,sticky="w",columnspan=2,padx=20)
        self.objection_text=tk.CTkTextbox(master=self,wrap="word",state="normal",height=40)
        self.objection_text.grid(row=5,column=0,padx=30,stick="nsew",columnspan=2,rowspan=3)


        #2. CUSTOM RESPONSE FRAMES
        #Default Frame
        self.default_frame.response_label = tk.CTkLabel(master=self.default_frame,text="RESPONSE:",font=label_font)
        self.default_frame.response_text = SmartTextbox(master=self.default_frame,main_master=self.master,wrap="word",state="normal")
        #pack
        self.default_frame.response_label.pack(padx=20,anchor="w",pady=10)
        self.default_frame.response_text.pack(padx=30,fill="both",expand=True,anchor="center")

        #FRA Frame
        self.RFA_frame.response_label=tk.CTkLabel(master=self.RFA_frame,text="RESPONSE:",font=label_font)
        self.RFA_frame.response_text=tk.CTkTextbox(master=self.RFA_frame,wrap="word",state="disabled",height=60)
        self.RFA_frame.RFA_option = tk.CTkSegmentedButton(master=self.RFA_frame,values=["Admit","Deny","Lack Info","Custom"],border_width=0,command=master.setRFA)
        self.RFA_frame.RFA_label=tk.CTkLabel(master=self.RFA_frame,text="17.1 RESPONSE:",font=label_font)
        self.RFA_frame.RFA_text=tk.CTkTextbox(master=self.RFA_frame,wrap="word",state="normal",height=60)
        self.RFA_frame.RFA_option.set("Admit")
        #pack
        self.RFA_frame.response_label.pack(padx=20,anchor="w",pady=(10,0))
        self.RFA_frame.RFA_option.pack(fill="x",padx=30,pady=2)
        self.RFA_frame.response_text.pack(padx=30,fill="both",expand=True,anchor="center")
        self.RFA_frame.RFA_label.pack(padx=20,anchor="w",pady=(10,0))
        self.RFA_frame.RFA_text.pack(padx=30,fill="both",expand=True,anchor="center")



        #FRP Frame
        location_frame=tk.CTkFrame(master=self.RFP_frame)
        self.RFP_frame.response_label=tk.CTkLabel(master=self.RFP_frame,text="RESPONSE:",font=label_font)
        self.RFP_frame.response_text=tk.CTkTextbox(master=self.RFP_frame,wrap="word",state="normal")
        self.RFP_frame.RFP_label = tk.CTkLabel(master=location_frame,text="Documents Location: ")
        self.RFP_frame.RFP_text = tk.CTkEntry(master=location_frame,state="normal")
        self.RFP_frame.RFP_option = tk.CTkSegmentedButton(master=self.RFP_frame,values=["Available","Not Exist","Not Possessed","Lost","Custom"],border_width=0,command=master.setRFP)
        self.RFP_frame.RFP_option.set("Available")
        #pack
        self.RFP_frame.response_label.pack(padx=20,anchor="w",pady=(10,0))
        self.RFP_frame.RFP_option.pack(fill="x",padx=30,pady=2)

        self.RFP_frame.RFP_label.pack(side="left",anchor="w")
        self.RFP_frame.RFP_text.pack(side="left",anchor="w",fill="x",expand=True)
        location_frame.pack(pady=2,fill="x",padx=30)

        self.RFP_frame.response_text.pack(padx=30,fill="both",expand=True,anchor="center")


        #PLACE THE RESPONSE FRAME
        self.current_frame.grid(row=8,column=0,sticky="nsew",columnspan=2,rowspan=5)
        #3. NORMAL BUTTONS
        #Clear
        self.clear_button = tk.CTkButton(master=self,text="Check With Client",command=self.master.check)
        self.clear_button.grid(row=13,column=0)
        #Next
        self.next_button = tk.CTkButton(master=self,text="Submit",command=self.master.submit)
        self.next_button.grid(row=13,column=1)

    #Redraws the frame for different discovery types
    def redraw(self,req_type):
        if req_type=="RFP":
            if self.prev!="RFP":
                self.current_frame.grid_forget()
                self.current_frame = self.RFP_frame
                self.current_frame.grid(row=8,column=0,sticky="nsew",columnspan=2,rowspan=5)
        elif req_type=="RFA":
            if self.prev!="RFA":
                self.current_frame.grid_forget()
                self.current_frame = self.RFA_frame
                self.current_frame.grid(row=8,column=0,sticky="nsew",columnspan=2,rowspan=5)
        else:
            self.current_frame.grid_forget()
            self.current_frame = self.default_frame
            self.current_frame.grid(row=8,column=0,sticky="nsew",columnspan=2,rowspan=5)
        self.prev = req_type

    #Resets this frame to being empty
    def reset(self):
        #Reset Request Number
        self.request_label.configure(text="REQUEST:")
        #Reset Respnse
        self.set_response("")
        #Reset Objection
        self.set_objection("")
        #Reset RFP
        self.set_RFP("Available")
        self.set_RFP_text("")
        #Reset RFA
        self.set_RFA("Admit")
        self.set_RFA_text("")
        #Reset Request
        self.set_request("")
        self.redraw("clear")

       
    def set_theme(self,font,text_col,fg_col):
        self.request_text.configure(False,font=font,text_color=text_col,fg_color=fg_col)#OBJECTION
        self.objection_text.configure(False,font=font,text_color=text_col,fg_color=fg_col)#REQUEST

        #DEFAULT FRAME
        self.default_frame.response_text.configure(False,font=font,text_color=text_col,fg_color=fg_col)#RESPONSE

        #RFP FRAME
        self.RFP_frame.response_text.configure(False,font=font,text_color=text_col,fg_color=fg_col)#RESPONSE
        self.RFP_frame.RFP_text.configure(False,font=font,text_color=text_col,fg_color=fg_col)#RESPONSE

        #RFA FRAME
        self.RFA_frame.response_text.configure(False,font=font,text_color=text_col,fg_color=fg_col)#RESPONSE
        self.RFA_frame.RFA_text.configure(False,font=font,text_color=text_col,fg_color=fg_col)#RESPONSE

        #Bold tag for request
        #self.response_frame.request_text.tag_config("red",font=(self.theme["text_font"],1+int(self.theme["text_size"]), 'bold'))
        #Special Request



    # Getters and Setters for all parameters!
    #Request
    def get_request(self):
        return self.request_text.get("0.0","end-1c")
    def set_request(self,text):
        self.request_text.configure(state="normal")
        self.request_text.delete("0.0","end")
        self.request_text.insert("0.0",text)
        self.request_text.configure(state="disabled")
    #Objection
    def get_objection(self):
        return self.objection_text.get("0.0","end-1c")
    def set_objection(self,text):
        self.objection_text.configure(state="normal")
        self.objection_text.delete("0.0","end")
        self.objection_text.insert("0.0",text)
        self.objection_text.configure(state="normal")

    #Response
    def get_response(self):
        return self.current_frame.response_text.get("0.0","end-1c")
    def set_response(self,text):
        state=self.current_frame.response_text._textbox.cget("state")
        self.current_frame.response_text.configure(state="normal")
        self.current_frame.response_text.delete("0.0","end")
        self.current_frame.response_text.insert("0.0",text)
        self.current_frame.response_text.configure(state=state)

    #RFP Text
    def get_RFP_text(self):
        return self.RFP_frame.RFP_text.get()
    def set_RFP_text(self,text):
        self.RFP_frame.RFP_text.delete(0,"end")
        self.RFP_frame.RFP_text.insert(0,text)
    #RFA Text
    def get_RFA_text(self):
        return self.RFA_frame.RFA_text.get("0.0","end-1c")
    def set_RFA_text(self,text):
        self.RFA_frame.RFA_text.delete("0.0","end")
        self.RFA_frame.RFA_text.insert("0.0",text)
    #Buttons
    def set_RFA(self,val):
        self.RFA_frame.RFA_option.set(val)
        self.previous_option = val
    def get_RFA(self):
        return self.RFA_frame.RFA_option.get()
    def set_RFP(self,val):
        self.RFP_frame.RFP_option.set(val)
        self.previous_option = val
    def get_RFP(self):
        return self.RFP_frame.RFP_option.get()
    def get_previous_option(self):
        return self.previous_option
    def set_previous_option(self,val):
        self.previous_option = val