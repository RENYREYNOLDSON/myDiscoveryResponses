# Main Imports
from frames.__modules__ import *

# OBJECTIONS FRAME 
############################################################################################################
# Contains list of all possible objections
class File_Details_Frame(tk.CTkFrame):
    #Constructor
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #Frame Setup
        self.master=master

        self.title_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.title_frame.pack(fill="x")

        label_font = tk.CTkFont("Arial",16,underline=True,weight="bold")

        #Have a back arrow
        self.back_button = tk.CTkButton(master=self.title_frame,width=50,text="←",font=("Segoe UI",30),fg_color="transparent",hover=False,command=self.master.close_details)
        self.back_button.pack(side="left",padx=(10,0))
        #Have a title
        self.title_label = tk.CTkLabel(master=self.title_frame,text="FILE DETAILS",font=label_font,fg_color="transparent",anchor="w")
        self.title_label.pack(side="left",pady=(5,0))


        #Have a scrollable frame of options


        font = (master.CONFIG["appearance"]["text_font"],16)
        details = self.master.current_client.current_file.details
        
        text_col = self.master.CONFIG["appearance"]["text_color"]
        bg_col = self.master.CONFIG["appearance"]["text_bg"]
        r=3
        
        #File Name
        self.file_name_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.file_name_frame.pack(fill="both",pady=5,expand=True)
        name = tk.CTkLabel(master=self.file_name_frame,text="File Name:",anchor="nw",width=120)
        name.pack(side="left",padx=20)
        self.name = tk.CTkTextbox(master=self.file_name_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.name.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.name.insert("0.0",self.master.current_client.current_file.name)

        #Document
        self.document_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.document_frame.pack(fill="both",pady=5,expand=True)
        document = tk.CTkLabel(master=self.document_frame,text="Document Name:",anchor="nw",width=120)
        document.pack(side="left",padx=20)
        self.document = tk.CTkTextbox(master=self.document_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.document.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.document.insert("0.0",details["document"])



        #County
        self.county_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.county_frame.pack(fill="both",pady=5,expand=True)
        county = tk.CTkLabel(master=self.county_frame,text="County:",anchor="nw",width=120)
        county.pack(side="left",padx=20)
        self.county = tk.CTkTextbox(master=self.county_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.county.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.county.insert("0.0",details["county"])





        #Plaintiff
        self.plaintiff_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.plaintiff_frame.pack(fill="both",pady=5,expand=True)
        plaintiff = tk.CTkLabel(master=self.plaintiff_frame,text="Plaintiff(s):",anchor="nw",width=120)
        plaintiff.pack(side="left",padx=20)
        self.plaintiff = tk.CTkTextbox(master=self.plaintiff_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.plaintiff.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.plaintiff.insert("0.0",details["plaintiff"])

        #Defendant
        self.defendant_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.defendant_frame.pack(fill="both",pady=5,expand=True)
        defendant = tk.CTkLabel(master=self.defendant_frame,text="Defendant(s):",anchor="nw",width=120)
        defendant.pack(side="left",padx=20)
        self.defendant = tk.CTkTextbox(master=self.defendant_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.defendant.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.defendant.insert("0.0",details["defendant"])

        #Propounding Party
        self.propounding_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.propounding_frame.pack(fill="both",pady=5,expand=True)
        propounding_party = tk.CTkLabel(master=self.propounding_frame,text="Propounding Party:",anchor="nw",width=120)
        propounding_party.pack(side="left",padx=20)
        self.propounding_party = tk.CTkTextbox(master=self.propounding_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.propounding_party.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.propounding_party.insert("0.0",details["propounding_party"])

        #Responding Party
        self.responding_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.responding_frame.pack(fill="both",pady=5,expand=True)
        responding_party = tk.CTkLabel(master=self.responding_frame,text="Responding Party:",anchor="nw",width=120)
        responding_party.pack(side="left",padx=20)
        self.responding_party = tk.CTkTextbox(master=self.responding_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.responding_party.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.responding_party.insert("0.0",details["responding_party"])

        #Case Number
        self.case_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.case_frame.pack(fill="both",pady=5,expand=True)
        case = tk.CTkLabel(master=self.case_frame,text="Case Number:",anchor="nw",width=120)
        case.pack(side="left",padx=20)
        self.case = tk.CTkTextbox(master=self.case_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.case.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.case.insert("0.0",details["case_number"])

        #Date
        self.date_frame =tk.CTkFrame(master=self,fg_color="transparent")
        self.date_frame.pack(fill="both",pady=5,expand=True)
        date = tk.CTkLabel(master=self.date_frame,text="Date:",anchor="nw",width=120)
        date.pack(side="left",padx=20)
        self.date = tk.CTkTextbox(master=self.date_frame,height=40,wrap="word",font=font,text_color=text_col,fg_color=bg_col,corner_radius=r)
        self.date.pack(side="left",fill="both",expand=True,padx=(0,20))
        self.date.insert("0.0",details["date"])

        self.save_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.save_frame.pack(fill="x",expand=True)
        self.save_button = tk.CTkButton(master=self.save_frame,text="Save",command=master.save_detail_win)
        self.save_button.pack(side="right",pady=(5,10),padx=20)

