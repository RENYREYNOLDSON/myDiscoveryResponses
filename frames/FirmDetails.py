# Main Imports
from frames.__modules__ import *

# OBJECTIONS FRAME 
############################################################################################################
# Contains list of all possible objections
class Firm_Details_Frame(tk.CTkFrame):
    #Constructor
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #Frame Setup
        self.master=master

        self.title_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.title_frame.pack(fill="x")

        label_font = tk.CTkFont("Arial",16,underline=True,weight="bold")
        warn_font = tk.CTkFont("Arial",16,underline=False)

        #Have a back arrow
        self.back_button = tk.CTkButton(master=self.title_frame,width=50,text="←",font=("Segoe UI",30),fg_color="transparent",hover=False,command=self.master.close_details)
        self.back_button.pack(side="left",padx=(10,0))
        #Have a title
        self.title_label = tk.CTkLabel(master=self.title_frame,text="FIRM/COMPANY DETAILS",font=label_font,fg_color="transparent",anchor="w")
        self.title_label.pack(side="left",pady=(5,0))


        #Have a scrollable frame of options


        font = (master.CONFIG["appearance"]["text_font"],16)
        
        text_col = self.master.CONFIG["appearance"]["text_color"]
        bg_col = self.master.CONFIG["appearance"]["text_bg"]
        r=3

        #Change firm details for just one client!
        if self.master.current_client!="":
            firm_details = self.master.current_client.firm_details#Each client loads default details and then they can be edited
            self.title_label = tk.CTkLabel(master=self.title_frame,text="Changing for current client only! Close clients to edit global firm details.",font=warn_font,fg_color="transparent",anchor="w",text_color="red")
            self.title_label.pack(side="left",pady=(5,0),padx=20)
        else:
            firm_details = get_firm_details()

        #ADD TEXT ABOUT THIS!!

        #File Name
        self.name_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.name_frame.pack(fill="both",pady=5,expand=True)
        name = tk.CTkLabel(master=self.name_frame ,text="Firm Name:",anchor="nw",width=120)
        name.pack(side="left",padx=20)
        self.name = tk.CTkTextbox(master=self.name_frame ,height=60,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.name.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.name.insert("0.0",firm_details["firm_name"])

        #Address 1
        self.address_1 =tk.CTkFrame(master=self,fg_color="transparent")
        self.address_1.pack(fill="both",pady=5,expand=True)
        address_line_1 = tk.CTkLabel(master=self.address_1 ,text="Address Line 1:",anchor="nw",width=120)
        address_line_1.pack(side="left",padx=20)
        self.address_line_1 = tk.CTkTextbox(master=self.address_1 ,height=60,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.address_line_1.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.address_line_1.insert("0.0",firm_details["address_line_1"])

        #Address 2
        self.address_2 =tk.CTkFrame(master=self,fg_color="transparent")
        self.address_2.pack(fill="both",pady=5,expand=True)
        address_line_2 = tk.CTkLabel(master=self.address_2,text="Address Line 2:",anchor="nw",width=120)
        address_line_2.pack(side="left",padx=20)
        self.address_line_2 = tk.CTkTextbox(master=self.address_2,height=60,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.address_line_2.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.address_line_2.insert("0.0",firm_details["address_line_2"])

        #Telephone
        self.telephone_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.telephone_frame.pack(fill="both",pady=5,expand=True)
        telephone = tk.CTkLabel(master=self.telephone_frame,text="Telephone:",anchor="nw",width=120)
        telephone.pack(side="left",padx=20)
        self.telephone = tk.CTkTextbox(master=self.telephone_frame,height=60,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.telephone.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.telephone.insert("0.0",firm_details["telephone"])

        #Facsimile
        self.facsimile_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.facsimile_frame.pack(fill="both",pady=5,expand=True)
        facsimile = tk.CTkLabel(master=self.facsimile_frame,text="Facsimile:",anchor="nw",width=120)
        facsimile.pack(side="left",padx=20)
        self.facsimile = tk.CTkTextbox(master=self.facsimile_frame,height=60,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.facsimile.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.facsimile.insert("0.0",firm_details["facsimile"])

        #email
        self.email_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.email_frame.pack(fill="both",pady=5,expand=True)
        email = tk.CTkLabel(master=self.email_frame,text="Email:",anchor="nw",width=120)
        email.pack(side="left",padx=20)
        self.email = tk.CTkTextbox(master=self.email_frame,height=60,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.email.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.email.insert("0.0",firm_details["email"])

        #attorneys
        self.attorneys_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.attorneys_frame.pack(fill="both",pady=5,expand=True)
        attorneys = tk.CTkLabel(master=self.attorneys_frame ,text="Attorneys:",anchor="nw",width=120)
        attorneys.pack(side="left",padx=20)
        self.attorneys = tk.CTkTextbox(master=self.attorneys_frame ,height=60,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.attorneys.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.attorneys.insert("0.0",firm_details["attorneys"])


        self.save_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.save_frame.pack(fill="x",expand=True)
        self.save_button = tk.CTkButton(master=self.save_frame,text="Save",command=self.master.save_firm_detail_win)
        self.save_button.pack(side="right",pady=(5,10),padx=20)