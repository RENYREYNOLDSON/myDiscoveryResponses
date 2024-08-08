######
###### MYDISCOVERYRESPONSES
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023-2024
###### Uses converter.py to open discovery request PDF's in order to respond
###### Provides a Windows GUI tool for opening files and saving as DOCX
###### myDiscoveryResponses.com
###### Version 1.1.0 | 09/07/2024
######

# IMPORTS
############################################################################################################

import customtkinter as tk
import json,os,pickle,webbrowser,re,subprocess
from objects.SmartToolTip import *
import urllib.request
from tkinter import PhotoImage
from dotenv import load_dotenv

# CONSTANTS 
############################################################################################################

HIGHLIGHT_WORDS=["photograph","videotape","document","evidence","property damage","lost wages","injury","injuries"]

# FILE READING AND WRITING 
############################################################################################################

def get_openai_key():
    load_dotenv()
    print(os.getenv("AI_KEY"))
    return os.getenv("AI_KEY")


def get_main_path():
    return os.path.dirname(__file__)

#GETTERS AND SETTERS FOR RECENT FILES
def get_recents():
    #Open the recent files list
    with open(os.path.join(os.path.dirname(__file__),"config/recents"), "rb") as fp:   # Unpickling
        lst = pickle.load(fp)
    new=[]
    for file in lst:
        if valid_file_path(file):
            new.append(file)
    return new

def set_recents(lst):
    with open(os.path.join(os.path.dirname(__file__),"config/recents"), "wb") as fp:   #Pickling
        pickle.dump(lst, fp)

#Get the path for temp
def get_temp_path():
    return os.path.join(os.path.dirname(__file__),"assets/temp")

#GETTERS AND SETTERS FOR FIRM DETAILS
def get_firm_details():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/firm_details.json")):
        with open(os.path.join(os.path.dirname(__file__),"config/firm_details.json"),"r") as file:
            data = json.load(file)
        return data
    return None

def set_firm_details(data):
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/firm_details.json")):
        with open(os.path.join(os.path.dirname(__file__),'config/firm_details.json'), 'w') as file:
            json.dump(data,file)
    
# Open the hotkeys
def open_hotkeys():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/hotkeys.json")):
        with open(os.path.join(os.path.dirname(__file__),"config/hotkeys.json"),"r") as file:
            data = json.load(file)
        return data
    return None

# Save the new hotkeys file
def save_hotkeys(data):
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/hotkeys.json")):
        with open(os.path.join(os.path.dirname(__file__),'config/hotkeys.json'), 'w') as file:
            json.dump(data,file)

# Opens the objections file
def open_objections():# Return API key from file if possible
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/objections.json")):
        with open(os.path.join(os.path.dirname(__file__),'config/objections.json'), 'r') as file:
            data = json.load(file)
        return data
    return None

# Opens the objections file
def open_objections_backup():# Return API key from file if possible
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/objections_backup.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/objections_backup.json'), 'r') as file:
            data = json.load(file)
        return data
    return None

# Opens the hotkeys backup file
def open_hotkeys_backup():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/hotkeys_backup.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/hotkeys_backup.json'), 'r') as file:
            data = json.load(file)
        return data
    return None

# Opens the config backup file
def open_config_backup():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/config_backup.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/config_backup.json'), 'r') as file:
            data = json.load(file)
        return data
    return None

# Opens the config backup file
def open_config():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/config.json")):
        with open(os.path.join(os.path.dirname(__file__),'config/config.json'), 'r') as file:
            data = json.load(file)
        return data
    return None

# Save the new hotkeys file
def save_config(data):
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/config.json")):
        with open(os.path.join(os.path.dirname(__file__),'config/config.json'), 'w') as file:
            json.dump(data,file)


# Opens the firm details backup file
def open_firm_details_backup():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/firm_details_backup.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/firm_details_backup.json'), 'r') as file:
            data = json.load(file)
        return data
    return None

# Save the new objections file
def save_objections(data):
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/objections.json")):
        with open(os.path.join(os.path.dirname(__file__),'config/objections.json'), 'w') as file:
            json.dump(data,file)

# Validate the integrity of the config file, if there are any details missing then add them from the backup
def validate_integrity_of_config_file():#Run this function on start
    #Get backup config
    backup = open_config_backup()

    #Get current config
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/config.json")):
        with open(os.path.join(os.path.dirname(__file__),'config/config.json'), 'r') as file:
            config = json.load(file)

    #Compare the backup and the config
    fixed = False
    for i in backup:
        if i not in config:
            config[i] = backup[i]
            print(backup[i])
            fixed = True
        else:
            if backup[i]!=1:
                #Check all inside
                for i2 in backup[i]:
                    if i2 not in config[i]:
                        #Add the new dictionary item here
                        config[i][i2] = backup[i][i2]
                        print(i2)
                        fixed = True

    #If fixed then save config file
    if fixed:
        with open(os.path.join(os.path.dirname(__file__),"config/config.json"), "w") as outfile:
            json.dump(config, outfile)

    return

def valid_file_path(filename):
    if filename=="":
        return False
    if os.path.exists(filename):
        return True
    return False

def open_splash_image():
    return PhotoImage(file=os.path.join(os.path.dirname(__file__),"assets/splash_image.png"))



# SOFTWARE LOCAL FILES
############################################################################################################

def remove_installers():
    #Remove any zips
    zip_path = os.path.join(os.path.dirname(__file__),"myDiscoveryResponses Installer.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    #Remove any exe's
    exe_path = os.path.join(os.path.dirname(__file__),"myDiscoveryResponses Installer.exe")
    if os.path.exists(exe_path):
        os.remove(exe_path)

    return


    
#Open the software install location
def open_install_location():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.startfile(dir_path)


# TEXTBOX FUNCTIONS
############################################################################################################

# Find all instances of keywords [start,end]
def find_all(string,sub):
    indices=[]
    for i in range(len(string)):
        if i+len(sub)<len(string):
            if string[i:i+len(sub)].upper()==sub.upper():
                #Add indices to list
                #Add extra if s
                extra=0
                if string[i+len(sub)].lower()=="s":
                    extra=1
                #If space of punc after
                if string[i+len(sub)+extra] in [" ",".",",","'","!",";"]:
                    indices.append([i,i+len(sub)+extra])#Add to indices
    return indices

# Bold certain key words in given text
def bold_keywords(obj,text):
    # Define tag
    indices=[]
    #Find Indexes of the keywords
    #Set each to the tag
    for word in HIGHLIGHT_WORDS:
        for i in find_all(text,word):
            indices.append(i)
    #Set them to the tag!
    for i in indices:
        obj.tag_add("red", "0.0 + "+str(i[0])+" chars","0.0 + "+str(i[1])+" chars",)

# Checks spelling in a textbox, highlights and returns
def spellcheck(obj,text):
    #Load the spelling config
    chkr = obj.main_master.SPELL_CHECKER
    spell_config = obj.main_master.CONFIG["spelling"]
    chkr.set_text(text)
    #Ignores
    ignores = obj.main_master.CONFIG["spelling"]["ignore"].split(",")
    #List of issues
    issues=[]
    #CLEAR ISSUES
    obj.tag_delete("spelling")

    for err in chkr:#Checks all of the matches and adds them to issues
        if err.word not in ignores:
            suggestions = chkr.suggest(err.word)
            obj.tag_add("spelling", "0.0 + "+str(err.wordpos-1)+" chars","0.0 + "+str(len(err.word)+err.wordpos-1)+" chars",)
            new_issue = ["Spelling Issue","Always Ignore",err.word,err.wordpos,len(err.word),suggestions[:5]]#Only get 1st five
            issues.append(new_issue)

    #Get font size and adjust squiggle XBM
    squiggles = {"8":"squiggle_small",
                 "10":"squiggle_small",
                 "12":"squiggle_small",
                 "14":"squiggle_mid",
                 "16":"squiggle_mid",
                 "18":"squiggle_midsmall",
                 "20":"squiggle_midsmall",
                 "22":"squiggle_midsmall",
                 "24":"squiggle_big",
                 "26":"squiggle_big",}

    font_size = str(obj.cget("font")[1])#This is font size

    squiggle_file = "@"+os.path.join(os.path.dirname(__file__),"assets/"+squiggles[font_size]+".xbm")

    obj.tag_config("spelling",bgstipple=squiggle_file,background=spell_config["underline"])
    
    return issues

    #DONT INCLUDE LAST ONE IF USER STILL TYPING
    #UNHIGHLIGHT WHEN WORDS ARE FIXED
    #SEPERATE OUT GRAMMAR AND SPELLING?


# OTHER FUNCTIONS
############################################################################################################

#Get warnings from a file detail
def get_file_details_warning(text):
    warning = False
    if len(text)>150:
        warning = "Text longer than expected"
    elif len(text)==0:
        warning = "No text found"

    return warning



#Add a tooltip to an object
def add_tooltip(obj,text,wraplength=400):
    return SmartToolTip(anchor_widget = obj,text = text,wraplength=wraplength)

#Add a warning tooltip to an object
def add_warning_tooltip(obj,text,wraplength=400):
    return SmartToolTipWarning(anchor_widget = obj,text = text,wraplength=wraplength)

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 


# Open the user guide pdf
def open_user_guide():
    webbrowser.open("https://mydiscoveryresponses.com/documentation.html")


# Get a name with ... if needed
def get_name(name,length):
    text = name[:length]#Only get first n-3 chars
    if len(name)>length:
        text = text[:-3] +"..."
    return text


# Set the initial tkinter theme
def initial_theme():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"config/config.json")):
        with open(os.path.join(os.path.dirname(__file__),'config/config.json'), 'r') as file:
            data= json.load(file)
        # Set relevant things here
        tk.set_appearance_mode(data["appearance"]["theme"])

#Adds the additiol text to an objection text if needed
def add_extra_objection_text(full_text,objs):
    #Default values here
    final_text = "Notwithstanding the foregoing objections and subject thereto, Responding Party responds as follows: "
    extra = ""
    #Change these values if certain objections selected
    for obj in objs:
        #Change Scope
        if obj.alter_scope:
            final_text = "Notwithstanding the foregoing objections and subject thereto, and as Responding Party understands the proper scope and/or meaning of this request, Responding Party responds as follows: "
        #Add Extra Text
        text=obj.additional_text
        if text!="":
            if obj.additional_param=="":
                text = text.replace("[VAR]","")# Replace [VAR]
            else:
                text = text.replace("[VAR]"," "+obj.additional_param)# Replace [VAR]
            extra = extra+str(text)+". "#Add new text!
            
    full_text = full_text + final_text + extra
    return full_text

# Form the objection text using the selected objections
def get_objection_text(req,objections,remove_end=False):
    full_text = "Objection. "
    # 1. GET ALL SELECTED OBJECTIONS
    objs=[]
    opts = req.opts

    for obj in opts:
        if obj.selected==1:
            objs.append(obj)

    # 2. ADD ALL SELECTED OBJECTIONS TO THE TEXT
    if len(objs)>0:
        for key in list(objections.keys()):# Put in order given
            for obj in objs:# For each objection
                if key==obj.key:
                    text=objections[key][0]
                    if text=="":
                        text=key
                    if obj.param=="":
                        text = text.replace("[VAR]","")# Replace [VAR]
                    else:
                        #Format this nicely if using autofills
                        if obj.autofill:
                            #Add these formatted nicely
                            words = obj.param.split(",")
                            fill=""
                            c=0
                            for w in words:
                                if fill=="":#If the first autofill word
                                    fill = "as to “"+w+"”"
                                elif c==len(words)-1:
                                    fill = fill + " and “"+w+"”"
                                else:
                                    fill = fill[:-2] + ",” “"+w+"”"

                                c+=1

                            text = text.replace("[VAR]"," "+str(fill))# Replace [VAR]
                        else:
                            #Add basic parameter
                            text = text.replace("[VAR]"," "+obj.param)# Replace [VAR]
                    full_text = full_text+str(text)+". "#Add new text!

        """
        # 3. ADD FINAL OBJECTION IF REQUESTED AND VALID
        if full_text!="" and remove_end==False:#Response and not RFP. Resp and RFP
            add_extra_objection_text(full_text,objs)
        """
        
        return full_text
    return ""



def get_objection_text2(req,remove_end=False):
    # 1. GET ALL SELECTED OBJECTIONS
    objs=[]
    opts = req.opts
    for obj in opts:
        if obj.selected==1:
            objs.append(obj)

    # 2. USE CURRENT TEXT ATTRIBUTE
    if len(req.custom_objection_text)>0:
        full_text = req.custom_objection_text+" "
        # 3. ADD FINAL OBJECTION IF REQUESTED AND VALID
        if full_text!="" and remove_end==False:#Response and not RFP. Resp and RFP
            full_text=add_extra_objection_text(full_text,objs)
        return full_text
    return ""



#Convert text with " and ' to curly
def curly_convert(text):
    double_state="closed"
    doubles={"closed":"“","open":"”"}
    single_state="closed"
    singles={"closed":"‘","open":"’"}
    #First replace singles with text either side!
    pattern = r"'"
    # Define the replacement string
    replacement = r'’'
    # Perform the substitution
    text = re.sub(pattern, replacement, text)

    for i in range(len(text)):
        if text[i]=="“":
            double_state="open"
        elif text[i]=="”":
            double_state="closed"
        elif text[i]=='"':
            text = text[:i] + doubles[double_state] + text[i+1:]
            if double_state=="open":
                double_state="closed"
            else:
                double_state="open"

    return text


if __name__=="__main__":
    validate_integrity_of_config_file()