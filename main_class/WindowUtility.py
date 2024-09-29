# Main Imports
from main_class.__modules__ import *

RFP_responses = {
    "Available": "Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
    "Not Exist": "After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist.",
    "Not Possessed": "After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party.",
    "Lost": "After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen."}

RFA_responses = {"Admit": "Admit. ",
                 "Deny": "Deny. ",
                 "Lack Info": "A reasonable inquiry concerning the matter in this particular request has been made, and the information known or readily obtainable is insufficient to enable Responding Party to admit the matter."}

RFP_EXTRA = " Any responsive documents are believed to be in the possession, custody, or control of [VAR]."


class WindowUtility:
    ### WINDOW UTILITY
    ########################################################################################################

    # Setup key and exit bindings for the main windows
    def setup_bindings(self):
        self.bind("<Up>", self.up_pressed)
        self.bind("<Down>", self.down_pressed)
        self.bind("<Return>", self.enter_pressed)
        self.bind("<Escape>", self.escape_pressed)
        self.bind("<Button-1>", self.mouse_pressed)
        self.protocol("WM_DELETE_WINDOW", self.exit_window)
        self.bind("<Control-n>", self.cntrl_n)
        self.bind("<Control-o>", self.cntrl_o)
        self.bind("<Control-f>", self.cntrl_f)
        self.bind("<Control-s>", self.cntrl_s)
        self.bind("<Control-e>", self.cntrl_e)
        # Undo and Redo
        self.bind("<Control-z>", self.cntrl_z)
        self.bind("<Control-y>", self.cntrl_y)

    # Add Frames to the window
    def populate_window(self):
        # Navigation Bar Frame
        self.bar_frame = Bar_Frame(master=self, corner_radius=0, fg_color="#161616")
        self.bar_frame.pack(padx=0, pady=0, fill="both")
        # Requests Frame
        self.requests_frame = Requests_Frame(master=self, corner_radius=0, width=100)
        self.requests_frame.pack(padx=0, pady=0, expand=False, side="left", fill="both")
        # Landing Frame
        self.landing_frame = Landing_Frame(master=self, corner_radius=15)
        self.landing_frame.pack(padx=100, pady=100, expand=True, side="left", fill="both")
        # Objections Frame
        self.objections_frame = Objections_Frame(master=self, corner_radius=0, width=250)
        # Response Frame
        self.response_frame = Response_Frame(master=self)
        self.set_theme("text")  # Set theme just for text, as main theme loaded at start
        # Additional frame used for editing file and firm details
        self.details_frame = None

    # Toggles whether the program is in fullscreen or not
    def toggle_fullscreen(self):
        self.state("zoomed")  # Ensure that we are maximized first!
        state = not self.attributes('-fullscreen')
        self.attributes("-fullscreen", state)
        self.set_theme("theme")
        self.win

    # Reload the objections for each request! Stops errors when objections changed
    def reload_objections(self):
        for client in self.clients:
            client.reload_objections()

    # Destroy this windows sub window
    def cancel_win(self):
        if self.win != None:
            self.win.destroy()
            self.win = None

    # Save details from the details window
    def save_detail_win(self):
        self.current_client.current_file.details["county"] = self.details_frame.county.get("0.0", "end").replace("\n",
                                                                                                                 "")
        self.current_client.current_file.details["case_number"] = self.details_frame.case.get("0.0", "end").replace(
            "\n", "")
        self.current_client.current_file.details["document"] = self.details_frame.document.get("0.0", "end").replace(
            "\n", "")
        self.current_client.current_file.details["plaintiff"] = self.details_frame.plaintiff.get("0.0", "end").replace(
            "\n", "")
        self.current_client.current_file.details["defendant"] = self.details_frame.defendant.get("0.0", "end").replace(
            "\n", "")
        self.current_client.current_file.details["propounding_party"] = self.details_frame.propounding_party.get("0.0",
                                                                                                                 "end").replace(
            "\n", "")
        self.current_client.current_file.details["responding_party"] = self.details_frame.responding_party.get("0.0",
                                                                                                               "end").replace(
            "\n", "")
        # Date
        self.current_client.current_file.details["date"] = self.details_frame.date.get("0.0", "end").replace("\n", "")
        # Name
        self.current_client.current_file.name = self.details_frame.name.get("0.0", "end").replace("\n", "")

        self.requests_frame.show_files(self.current_client.files)
        self.title("myDiscoveryResponses   |   " + str(self.current_client.current_file.name))
        self.set_client_unsaved(self.current_client)
        self.close_details()

    def save_firm_detail_win(self):
        new_details = {"firm_name": self.details_frame.name.get("0.0", "end-1c"),
                       "address_line_1": self.details_frame.address_line_1.get("0.0", "end-1c"),
                       "address_line_2": self.details_frame.address_line_2.get("0.0", "end-1c"),
                       "telephone": self.details_frame.telephone.get("0.0", "end-1c"),
                       "facsimile": self.details_frame.facsimile.get("0.0", "end-1c"),
                       "email": self.details_frame.email.get("0.0", "end-1c"),
                       "attorneys": self.details_frame.attorneys.get("0.0", "end-1c")}

        if self.current_client != "":
            self.set_client_unsaved(self.current_client)
            self.current_client.firm_details = new_details
        else:
            set_firm_details(new_details)
        self.close_details()

    def client_already_open(self, client_name):
        for client in self.clients:
            if client.name == client_name:
                # Show a warning
                CTkMessagebox(title="Error",
                              message="Already have a client open with the name '" + str(client_name) + "' !",
                              icon="cancel",
                              corner_radius=0,
                              sound=True,
                              wraplength=400,
                              master=self)
                # Return
                return True
        return False

    # validates wether a valid file is open
    def file_open(self):
        if self.current_client != "":
            if self.current_client.current_file != "":
                return True
        return False

    # View and edit the details of the document
    def view_details(self):
        if self.file_open() and self.details_frame == None:
            self.details_frame = File_Details_Frame(master=self)
            # Remove (visibly) response and objection frames
            self.response_frame.pack_forget()
            self.objections_frame.pack_forget()
            self.details_frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.reset_undo_stacks()

    def close_details(self):
        if self.details_frame != None:
            self.details_frame.destroy()
            self.details_frame = None
            if self.clients == []:
                self.landing_frame.pack(padx=100, pady=100, expand=True, side="left", fill="both")
            else:
                self.objections_frame.pack(padx=0, pady=0, expand=False, side="right", fill="both")
                self.response_frame.pack(padx=20, pady=20, expand=True, side="left", fill="both")
            # Reset the undos
            self.reset_undo_stacks()

    def view_firm_details(self):
        if self.details_frame == None:
            # Remove (visibly) response and objection frames
            self.response_frame.pack_forget()
            self.objections_frame.pack_forget()
            self.landing_frame.pack_forget()

            self.details_frame = Firm_Details_Frame(master=self)
            self.details_frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.reset_undo_stacks()

    def view_updater(self):
        self.cancel_win()
        self.win = Update(self)
        self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
        self.win.mainloop()

    # The update failed so we show the issue and close it
    def update_failed(self, error):
        # Set error if closed by user
        if "ctkcanvas" in str(error):
            error = "Updater closed by user"
        self.cancel_win()
        msg = CTkMessagebox(title="Error Updating",
                            message="Error Downloading Update: " + str(error),
                            icon="warning",
                            option_1="Okay",
                            corner_radius=0,
                            sound=True,
                            wraplength=600,
                            master=self)

    # View and edit the OBJECTIONS JSON
    def view_objections(self):
        self.cancel_win()
        self.win = EditObjections(self)
        self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
        self.win.mainloop()

    # View and edit the theme of the software
    def view_hotkeys(self):
        self.cancel_win()
        self.win = Hotkeys(self)
        self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
        self.win.mainloop()

    # View and edit the theme of the software
    def view_settings(self):
        self.cancel_win()
        self.win = Settings(self)
        self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
        self.win.mainloop()

    # View a text preview of the objections+response
    def view_preview(self):
        if self.file_open():
            self.cancel_win()
            # Create a temporary docx
            self.export(self.current_client.current_file, get_temp_path(), preview_mode=True)
            self.win = Preview(self)
            self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
            self.win.mainloop()

    # View a DOCX preview of the output file
    def preview_text(self):
        if self.file_open():
            self.cancel_win()
            self.win = PreviewText(self)
            self.win.protocol("WM_DELETE_WINDOW", self.cancel_win)
            self.win.mainloop()

    def close_landing_frame(self):
        self.landing_frame.pack_forget()
        if not self.objections_frame.winfo_ismapped():
            self.objections_frame.pack(padx=0, pady=0, expand=False, side="right", fill="both")
            self.response_frame.pack(padx=20, pady=20, expand=True, side="left", fill="both")

    def open_landing_frame(self):
        self.objections_frame.pack_forget()
        self.response_frame.pack_forget()
        self.landing_frame.pack(padx=100, pady=100, expand=True, side="left", fill="both")

    # Exit this window and delete
    def exit_window(self):
        unsaved = False
        for client in self.clients:
            if client.saved == False:
                unsaved = True
        if unsaved:  # Check if the user wants to save without closing!!
            msg = CTkMessagebox(title="Exit?",
                                message="Are you sure you want to close without saving?",
                                icon="question",
                                option_1="Cancel",
                                option_3="Yes",
                                corner_radius=0,
                                sound=True,
                                wraplength=400,
                                master=self)
            if msg.get() != "Yes":
                return
        self.destroy()
        c = 0
        for w in self.root.winfo_children():
            c += 1
        if c == 0:  # Destroy root if no windows left open
            self.root.destroy()

    ### KEY PRESSES
    ########################################################################################################
    # HOTKEYS
    # CNTRL-N New Client
    def cntrl_n(self, e):
        self.new_client()

    # CNTRL-
    def cntrl_o(self, e):
        self.select_file()

    def cntrl_f(self, e):
        self.select_folder()

    def cntrl_s(self, e):
        self.quick_save()

    def cntrl_e(self, e):
        self.export_current()

    def cntrl_z(self, e):
        self.undo_action()

    def cntrl_y(self, e):
        self.redo_action()

    # If up arrow
    def up_pressed(self, e):
        # If focus is app
        if self.current_req != 0 and self.focus_get() == self:
            index = self.reqs.index(self.current_req)
            index = max(0, index - 1)
            self.set_request(self.reqs[index])
            self.requests_frame.scroll_to()

    # If down arrow
    def down_pressed(self, e):
        # If focus is app
        if self.current_req != 0 and self.focus_get() == self:
            index = self.reqs.index(self.current_req)
            index = min(len(self.reqs) - 1, index + 1)
            self.set_request(self.reqs[index])
            self.requests_frame.scroll_to()

    # If enter
    def enter_pressed(self, e):
        # If focus is app
        if self.current_req != 0 and self.focus_get() == self:
            self.submit()

    # If escape
    def escape_pressed(self, e):
        self.focus_set()

    # Get mouse press and set focus!
    def mouse_pressed(self, e):
        if "textbox" not in str(e.widget) and "ctkentry" not in str(e.widget):
            self.focus_set()
