# Main Imports
from frames.__modules__ import *


# OBJECTIONS FRAME
############################################################################################################
# Contains list of all possible objections
class File_Details_Frame(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Frame Setup
        self.master = master

        self.title_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.title_frame.pack(fill="x")

        label_font = tk.CTkFont("Arial", 16, underline=True, weight="bold")

        # Have a back arrow
        self.back_button = tk.CTkButton(master=self.title_frame, width=50, text="←", font=("Segoe UI", 30),
                                        fg_color="transparent", hover=False, command=self.master.close_details)
        self.back_button.pack(side="left", padx=(10, 0))
        # Have a title
        self.title_label = tk.CTkLabel(master=self.title_frame, text="FILE DETAILS", font=label_font,
                                       fg_color="transparent", anchor="w")
        self.title_label.pack(side="left", pady=(5, 0))

        # Have a scrollable frame of options

        font = (master.CONFIG["appearance"]["text_font"], 16)
        details = self.master.current_client.current_file.details

        text_col = self.master.CONFIG["appearance"]["text_color"]
        bg_col = self.master.CONFIG["appearance"]["text_bg"]
        r = 3

        # File Name
        self.file_name_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.file_name_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(self.master.current_client.current_file.name)
        if warning != False:
            name = tk.CTkLabel(master=self.file_name_frame, text="File Name:", anchor="nw", width=110)
            name.pack(side="left", padx=(20, 10))
            self.name_warning = tk.CTkButton(master=self.file_name_frame, text="!", width=10, hover=False,
                                             fg_color="red")
            self.name_warning.pack(side="left", padx=(0, 5))
            self.name_tooltip = add_warning_tooltip(self.name_warning, warning)
        else:
            name = tk.CTkLabel(master=self.file_name_frame, text="File Name:", anchor="nw", width=110)
            name.pack(side="left", padx=(20, 31))

        self.name = SmartTextbox(main_master=self.master, master=self.file_name_frame, height=40, wrap="word",
                                 font=font, text_color=text_col, fg_color=bg_col, corner_radius=r)
        self.name.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.name.insert("0.0", self.master.current_client.current_file.name)

        # Document
        self.document_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.document_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(details["document"])
        if warning != False:
            document = tk.CTkLabel(master=self.document_frame, text="Document Name:", anchor="nw", width=110)
            document.pack(side="left", padx=(20, 10))
            self.document_warning = tk.CTkButton(master=self.document_frame, text="!", width=10, hover=False,
                                                 fg_color="red")
            self.document_warning.pack(side="left", padx=(0, 5))
            self.document_tooltip = add_warning_tooltip(self.document_warning, warning)
        else:
            document = tk.CTkLabel(master=self.document_frame, text="Document Name:", anchor="nw", width=110)
            document.pack(side="left", padx=(20, 31))

        self.document = SmartTextbox(main_master=self.master, master=self.document_frame, height=40, wrap="word",
                                     font=font, text_color=text_col, fg_color=bg_col, corner_radius=r)
        self.document.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.document.insert("0.0", details["document"])

        # County
        self.county_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.county_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(details["county"])
        if warning != False:
            county = tk.CTkLabel(master=self.county_frame, text="County:", anchor="nw", width=110)
            county.pack(side="left", padx=(20, 10))
            self.county_warning = tk.CTkButton(master=self.county_frame, text="!", width=10, hover=False,
                                               fg_color="red")
            self.county_warning.pack(side="left", padx=(0, 5))
            self.county_toolip = add_warning_tooltip(self.county_warning, warning)
        else:
            county = tk.CTkLabel(master=self.county_frame, text="County:", anchor="nw", width=110)
            county.pack(side="left", padx=(20, 31))

        self.county = SmartTextbox(main_master=self.master, master=self.county_frame, height=40, wrap="word", font=font,
                                   text_color=text_col, fg_color=bg_col, corner_radius=r)
        self.county.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.county.insert("0.0", details["county"])

        # Plaintiff
        self.plaintiff_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.plaintiff_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(details["plaintiff"])
        if warning != False:
            plaintiff = tk.CTkLabel(master=self.plaintiff_frame, text="Plaintiff(s):", anchor="nw", width=110)
            plaintiff.pack(side="left", padx=(20, 10))
            self.plaintiff_warning = tk.CTkButton(master=self.plaintiff_frame, text="!", width=10, hover=False,
                                                  fg_color="red")
            self.plaintiff_warning.pack(side="left", padx=(0, 5))
            self.plaintiff_tooltip = add_warning_tooltip(self.plaintiff_warning, warning)
        else:
            plaintiff = tk.CTkLabel(master=self.plaintiff_frame, text="Plaintiff(s):", anchor="nw", width=110)
            plaintiff.pack(side="left", padx=(20, 31))

        self.plaintiff = SmartTextbox(main_master=self.master, master=self.plaintiff_frame, height=40, wrap="word",
                                      font=font, text_color=text_col, fg_color=bg_col, corner_radius=r)
        self.plaintiff.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.plaintiff.insert("0.0", details["plaintiff"])

        # Defendant
        self.defendant_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.defendant_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(details["defendant"])
        if warning != False:
            defendant = tk.CTkLabel(master=self.defendant_frame, text="Defendant(s):", anchor="nw", width=110)
            defendant.pack(side="left", padx=(20, 10))
            self.defendant_warning = tk.CTkButton(master=self.defendant_frame, text="!", width=10, hover=False,
                                                  fg_color="red")
            self.defendant_warning.pack(side="left", padx=(0, 5))
            self.defendant_tooltip = add_warning_tooltip(self.defendant_warning, warning)
        else:
            defendant = tk.CTkLabel(master=self.defendant_frame, text="Defendant(s):", anchor="nw", width=110)
            defendant.pack(side="left", padx=(20, 31))

        self.defendant = SmartTextbox(main_master=self.master, master=self.defendant_frame, height=40, wrap="word",
                                      font=font, text_color=text_col, fg_color=bg_col, corner_radius=r)
        self.defendant.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.defendant.insert("0.0", details["defendant"])

        # Propounding Party
        self.propounding_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.propounding_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(details["propounding_party"])
        if warning != False:
            propounding_party = tk.CTkLabel(master=self.propounding_frame, text="Propounding Party:", anchor="nw",
                                            width=110)
            propounding_party.pack(side="left", padx=(20, 10))
            self.propounding_warning = tk.CTkButton(master=self.propounding_frame, text="!", width=10, hover=False,
                                                    fg_color="red")
            self.propounding_warning.pack(side="left", padx=(0, 5))
            self.propounding_tooltip = add_warning_tooltip(self.propounding_warning, warning)
        else:
            propounding_party = tk.CTkLabel(master=self.propounding_frame, text="Propounding Party:", anchor="nw",
                                            width=110)
            propounding_party.pack(side="left", padx=(20, 31))

        self.propounding_party = SmartTextbox(main_master=self.master, master=self.propounding_frame, height=40,
                                              wrap="word", font=font, text_color=text_col, fg_color=bg_col,
                                              corner_radius=r)
        self.propounding_party.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.propounding_party.insert("0.0", details["propounding_party"])

        # Responding Party
        self.responding_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.responding_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(details["responding_party"])
        if warning != False:
            responding_party = tk.CTkLabel(master=self.responding_frame, text="Responding Party:", anchor="nw",
                                           width=110)
            responding_party.pack(side="left", padx=(20, 10))
            self.responding_warning = tk.CTkButton(master=self.responding_frame, text="!", width=10, hover=False,
                                                   fg_color="red")
            self.responding_warning.pack(side="left", padx=(0, 5))
            self.responding_tooltip = add_warning_tooltip(self.responding_warning, warning)
        else:
            responding_party = tk.CTkLabel(master=self.responding_frame, text="Responding Party:", anchor="nw",
                                           width=110)
            responding_party.pack(side="left", padx=(20, 31))

        self.responding_party = SmartTextbox(main_master=self.master, master=self.responding_frame, height=40,
                                             wrap="word", font=font, text_color=text_col, fg_color=bg_col,
                                             corner_radius=r)
        self.responding_party.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.responding_party.insert("0.0", details["responding_party"])

        # Case Number
        self.case_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.case_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(details["case_number"])
        if warning != False:
            case = tk.CTkLabel(master=self.case_frame, text="Case Number:", anchor="nw", width=110)
            case.pack(side="left", padx=(20, 10))
            self.case_warning = tk.CTkButton(master=self.case_frame, text="!", width=10, hover=False, fg_color="red")
            self.case_warning.pack(side="left", padx=(0, 5))
            self.case_tooltip = add_warning_tooltip(self.case_warning, warning)
        else:
            case = tk.CTkLabel(master=self.case_frame, text="Case Number:", anchor="nw", width=110)
            case.pack(side="left", padx=(20, 31))

        self.case = SmartTextbox(main_master=self.master, master=self.case_frame, height=40, wrap="word", font=font,
                                 text_color=text_col, fg_color=bg_col, corner_radius=r)
        self.case.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.case.insert("0.0", details["case_number"])

        # Date
        self.date_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.date_frame.pack(fill="both", pady=5, expand=True)

        warning = get_file_details_warning(details["date"])
        if warning != False:
            date = tk.CTkLabel(master=self.date_frame, text="Date:", anchor="nw", width=110)
            date.pack(side="left", padx=(20, 10))
            self.date_warning = tk.CTkButton(master=self.date_frame, text="!", width=10, hover=False, fg_color="red")
            self.date_warning.pack(side="left", padx=(0, 5))
            self.date_tooltip = add_warning_tooltip(self.date_warning, warning)
        else:
            date = tk.CTkLabel(master=self.date_frame, text="Date:", anchor="nw", width=110)
            date.pack(side="left", padx=(20, 31))

        self.date = SmartTextbox(main_master=self.master, master=self.date_frame, height=40, wrap="word", font=font,
                                 text_color=text_col, fg_color=bg_col, corner_radius=r)
        self.date.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.date.insert("0.0", details["date"])

        self.save_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.save_frame.pack(fill="x", expand=True)
        self.save_button = tk.CTkButton(master=self.save_frame, text="Save", command=master.save_detail_win)
        self.save_button.pack(side="right", pady=(5, 10), padx=20)
