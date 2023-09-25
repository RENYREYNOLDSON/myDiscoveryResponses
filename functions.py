###### FUNCTIONS
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023
######
###### General functions usable by any program
######


# IMPORTS
############################################################################################################

import customtkinter as tk
import json,os,pickle

# CONSTANTS 
############################################################################################################

HIGHLIGHT_WORDS=["photograph","videotape","document","evidence","property damage","lost wages","injury","injuries"]

# FUNCTIONS 
############################################################################################################

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 

def valid_file_path(filename):
    if filename=="":
        return False
    if os.path.exists(filename):
        return True
    return False

# Open the user guide pdf
def open_user_guide():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    file = "assets/user_guide.pdf"
    file = os.path.join(script_dir, file)
    os.startfile(file)




# Get a name with ... if needed
def get_name(name,length):
    text = name[:length]#Only get first n-3 chars
    if len(name)>length:
        text = text[:-3] +"..."
    return text

#GETTERS AND SETTERS FOR RECENT FILES
def get_recents():
    #Open the recent files list
    with open(os.path.join(os.path.dirname(__file__),"assets/recents"), "rb") as fp:   # Unpickling
        lst = pickle.load(fp)
    new=[]
    for file in lst:
        if valid_file_path(file):
            new.append(file)
    return new
def set_recents(lst):
    with open(os.path.join(os.path.dirname(__file__),"assets/recents"), "wb") as fp:   #Pickling
        pickle.dump(lst, fp)

#GETTERS AND SETTERS FOR FIRM DETAILS
def get_firm_details():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/firm_details.json")):
        with open(os.path.join(os.path.dirname(__file__),"assets/firm_details.json"),"r") as file:
            data = json.load(file)
        return data
    return None

def set_firm_details(data):
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/firm_details.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/firm_details.json'), 'w') as file:
            json.dump(data,file)
    

# Open the hotkeys
def open_hotkeys():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/hotkeys.json")):
        with open(os.path.join(os.path.dirname(__file__),"assets/hotkeys.json"),"r") as file:
            data = json.load(file)
        return data
    return None

# Save the new hotkeys file
def save_hotkeys(data):
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/hotkeys.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/hotkeys.json'), 'w') as file:
            json.dump(data,file)


# Opens the objections file
def open_objections():# Return API key from file if possible
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/objections.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/objections.json'), 'r') as file:
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

# Save the new objections file
def save_objections(data):
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/objections.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/objections.json'), 'w') as file:
            json.dump(data,file)

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

# Set the initial tkinter theme
def initial_theme():
    if os.path.exists(os.path.join(os.path.dirname(__file__),"assets/theme.json")):
        with open(os.path.join(os.path.dirname(__file__),'assets/theme.json'), 'r') as file:
            data= json.load(file)
        # Set relevant things here
        tk.set_appearance_mode(data["theme"])


# Form the objection text using the selected objections
def get_objection_text(opts,objections,remove_end=False):
    full_text = "Objection. "
    # 1. GET ALL SELECTED OBJECTIONS
    objs=[]
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
                        text = text.replace("[VAR]"," "+obj.param)# Replace [VAR]
                    full_text = full_text+str(text)+". "#Add new text!

        # 3. ADD FINAL OBJECTION IF REQUESTED AND VALID
        if full_text!="" and remove_end==False:#Response and not RFP. Resp and RFP
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
    return ""