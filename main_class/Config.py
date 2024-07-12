# Main Imports
from main_class.__modules__ import *

class Config:
    #Check for updates of software
    def check_for_update(self):
        #Use test function for now
        #urllib.request.urlretrieve("https://mydiscoveryresponses.com/myDiscoveryResponsesInstaller.zip","myDiscoveryResponsesInstaller.zip")
        update_available = True
        if update_available:
            #Check that they are sure
            update_check = CTkMessagebox(title="Update myDiscoveryResponses?",
                                       message="A new version is available! Would you like to update now?", 
                                       icon="info",
                                       option_1="No", 
                                       option_3="Yes",
                                       corner_radius=0,
                                       sound=True,
                                       master=self)
            
            if update_check.get()=="Yes":
                #Download new file
                #Ask if they want to update and show version number

                #THIS SHOULD BE A PATH TO DOWNLOADED FILE!!!
                
                #
                #
                #
                dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"myDiscoveryResponses_Installer.exe")
                #
                #
                #

                #Open installer
                subprocess.Popen(["cmd","/c","start","",dir_path],
                                        stdout=subprocess.DEVNULL,  # Redirect output to avoid hanging on pipes
                                        stderr=subprocess.DEVNULL,
                                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_BREAKAWAY_FROM_JOB,
                                        close_fds=True)

                #Destroy this application
                self.destroy()
                self.root.destroy()

    #RESET COMMANDS
    #Reset the config.json
    def reset_config(self):
        request = CTkMessagebox(title="Reset Settings", 
                                message="Are you sure you want to reset the settings?",
                                icon="warning", 
                                option_1="Cancel", 
                                option_3="Yes",
                                corner_radius=0,
                                sound=True,
                                master=self)
        if request.get()=="Yes":
            #Reset Settings
            #Load backup
            backup = open_config_backup()
            self.CONFIG = backup
            self.update_config(read_settings=False)


    #Reset all of software to defaults
    def reset_all(self):
        request = CTkMessagebox(title="Reset myDiscoveryResponses", 
                                message="Are you sure you want to reset to defaults?",
                                icon="warning", 
                                option_1="Cancel", 
                                option_3="Yes",
                                corner_radius=0,
                                sound=True,
                                master=self)
        
        if request.get()=="Yes":
            #Settings
            config_backup = open_config_backup()
            self.CONFIG = config_backup
            self.update_config(read_settings=False)

            #Hotkeys
            hotkeys_backup = open_hotkeys_backup()
            save_hotkeys(hotkeys_backup)
            self.HOTKEYS = open_hotkeys()

            #Objections
            objections_backup = open_objections_backup()
            save_objections(objections_backup)
            #Update main window objections
            self.objections = open_objections()
            #Reload objections into files
            self.reload_objections()

            #Firm Details
            firm_backup = open_firm_details_backup()
            set_firm_details(firm_backup)
    
            #Recents
            self.RECENTS = []
            set_recents(self.RECENTS)
            self.RECENTS = get_recents()
            # Update menu
            self.bar_frame.update_recents(self.RECENTS)
            # Update landing frame
            self.landing_frame.update_recents(self.RECENTS)

            #Destroy Window
            self.cancel_win()


    #Update the config JSON and set the new config
    def update_config(self,read_settings=True):
        if read_settings:
            self.win.withdraw()
            general = self.win.get_general()
            appearance = self.win.get_appearance()
            spelling = self.win.get_spelling()
            details = 1
            hotkeys = 1
            other = {"last_updated":"18/06/24"}

            self.CONFIG = {"general":general,
                        "appearance":appearance,
                        "spelling":spelling,
                        "details":details,
                        "hotkeys":hotkeys,
                        "other":other}
            
        #Save the new config JSON
        save_config(self.CONFIG)
        self.set_config()
        self.set_theme()
        self.set_tooltips()
        self.bar_frame.update_language_text()
        self.objections_frame.redraw_all()
        if self.file_open():
            self.requests_frame.show_files(self.current_client.files)
        if self.file_open():
            self.objections_frame.redraw(self.current_req)
        #Update spell check language
        self.SPELL_CHECKER = SpellChecker(self.CONFIG["spelling"]["language"])
        #Destroy Window
        self.cancel_win()
        #Reset the undo stack
        self.reset_undo_stacks()

    #Open and update the config
    def set_config(self):
        self.CONFIG = open_config()

    def add_ignore_word(self,word):
        self.CONFIG["spelling"]["ignore"] = self.CONFIG["spelling"]["ignore"]+","+word
        #Save the new config JSON
        save_config(self.CONFIG)

    # Open and set the theme
    def set_theme(self,param="both"):
        theme = self.CONFIG["appearance"]
        # Set relevant things here
        if param=="theme" or param=="both":
            tk.set_appearance_mode(theme["theme"])
        if param=="text" or param=="both":
            # Set all text areas
            font = (theme["text_font"],int(theme["text_size"]))
            self.response_frame.set_theme(font,theme["text_color"],theme["text_bg"])
            self.requests_frame.show_clients(self.clients)
            if self.current_client != "":
                self.requests_frame.show_files(self.current_client.files)
            self.requests_frame.show_list(self.reqs)

    def set_tooltips(self):
        #RESET THE landing frame AND bar frame
        self.landing_frame.set_tooltips()
        self.bar_frame.set_tooltips()
        self.requests_frame.set_tooltips()