######
###### MYDISCOVERYRESPONSES
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023-2024
###### Uses converter.py to open discovery request PDF's in order to respond
###### Provides a Windows GUI tool for opening files and saving as DOCX
###### myDiscoveryResponses.com
###### Version 1.1.0 | 09/07/2024
######

###### Rules for clean code space
###### 1. Use snake_case unless a class name (then camel case)
###### 2. Comment everything!
###### 3. If possible make something a simple & standard function
###### 4. Break everything down into small components and files
###### 5. ROOT->Main Windows->Each can have 1 sub window

# IMPORTS
############################################################################################################
import customtkinter as tk
from windows.splash import *
from functions import *
##### Open splash screen before large module imports
if __name__=="__main__":
    initial_theme()
    splash_screen = Splash()
    splash_screen.update()
##### Run the script to import modules
from __modules__ import *

# MAIN WINDOW CLASS
############################################################################################################
class App(tk.CTkToplevel,Saving,WindowUtility,Config,Undo,Export,Requests):
    #CONSTRUCTOR 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)

        ##### VERSION NUMBER
        self.version="1.1.0"
        #####

        ##### CLASS ATTRIBUTES
        self.root=root#Master is root of the program (Top level tk)
        root.call()
        #A list of all the open client objects
        self.clients=[]
        #Holds all requests in the currently selected file
        self.reqs=[]
        #Denotes the current client object
        self.current_client = ""
        #Current selected file object
        self.current_file = ""
        #Pointer to the currently selected request
        self.current_req=0
        #Request type of the current file
        self.req_type=""
        #Previous request type, using for managing window
        self.prev_type=""
        #The previous objection text
        self.previous_objection_text=""
        #Same container for all of the pop out windows, only one open at once!
        self.win=None
        #Contains a stack of all of the previous actions, maximum size can be defined in settings
        #Default maximum size of 100
        self.ACTION_STACK = []
        self.REDO_ACTION_STACK = []

        ##### LOAD ATTRIBUTES FROM METHODS
        #Opens the shortcuts
        self.HOTKEYS=open_hotkeys()
        #Opens the recent files json
        self.RECENTS=get_recents()
        #Repairs the config file if new items have been added
        #Loads the config file (software settings)
        validate_integrity_of_config_file()
        self.set_config()
        #Initialises the spell checker with the current language
        self.SPELL_CHECKER = SpellChecker(self.CONFIG["spelling"]["language"])
        #Get the list of objections
        self.objections = open_objections()

        ##### WINDOW SETUP
        #Set the icon after a delay (otherwise overwritten by ctk)
        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__),"assets/icon.ico")))
        #Set minimum size of window
        self.minsize(1050,720)
        #Set to be fullscreened
        self.state("zoomed")
        #Set the title of the main window
        self.title("myDiscoveryResponses")

        ##### BEGIN REGULAR INTERVAL FUNCTIONS
        #Refresher updates text and software as the user interacts
        self.after(100, self.refresher)
        #Autosave will trigger the save function at regular intervals
        self.after(int(self.CONFIG["general"]["autosave_interval"]),self.autosave)
        
        ##### KEY BINDINGS
        self.setup_bindings()

        ##### POPULATE WINDOW WITH OBJECTS
        self.populate_window()
        
    # Create a new MAIN window, must be here
    def create_window(self):
        create_window(self.master)


# ROOT FUNCTIONS
############################################################################################################
# Create a new window with root as parent
def create_window(root,from_file="file which will not exist on anybody's file path"):
    if os.path.exists(from_file.replace("\\","/")):
        App(root).load(from_file.replace("\\","/"))#Create a window with the selected client open
    else:
        App(root)

#ROOT UTILITY FUNCTION
def check_windows_open():
    if len(root.winfo_children())==0:#Destroy root if no windows left open
        print("ROOT CLOSED AS NO WINDOWS DETECTED")
        root.destroy()
    root.after(10000,check_windows_open)

# MAIN LOOP
############################################################################################################

if __name__ == "__main__":
    splash_screen.destroy()
    root=tk.CTk()
    root.withdraw()
    #CHECK if file has been opened from a saved client
    #sys.argv are the arguments such as opening a file!
    if len(sys.argv)>1:
        create_window(root,sys.argv[-1])
    else:
        create_window(root)
    root.after(10000,check_windows_open)
    #Run program mainloop
    root.mainloop()











