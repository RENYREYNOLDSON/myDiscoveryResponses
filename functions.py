###### FUNCTIONS
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023
######
###### General functions usable by any program
######


# IMPORTS
############################################################################################################

import customtkinter as tk
import json,os

# CONSTANTS 
############################################################################################################

HIGHLIGHT_WORDS=["photograph","videotape","document","evidence","property damage","lost wages","injury","injuries"]

# FUNCTIONS 
############################################################################################################

#Get the JSON dict of auto objections
def get_auto_objections_JSON():
    if os.path.exists("assets/auto_objections.json"):
        with open('assets/auto_objections.json', 'r') as file:
            data = json.load(file)
        return data
    return None

#Set the JSON dict of auto objections
def set_auto_objections_JSON(dic):
    with open("assets/auto_objections.json", "w") as outfile:#Save the new theme JSON
        json.dump(dic, outfile)


# Opens the objections file
def open_objections():# Return API key from file if possible
    if os.path.exists("assets/objections.json"):
        with open('assets/objections.json', 'r') as file:
            data = json.load(file)
        return data
    return None

# Opens the objections file
def open_objections_backup():# Return API key from file if possible
    if os.path.exists("assets/objections_backup.json"):
        with open('assets/objections_backup.json', 'r') as file:
            data = json.load(file)
        return data
    return None

# Save the new objections file
def save_objections(data):
    if os.path.exists("assets/objections.json"):
        with open('assets/objections.json', 'w') as file:
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
    if os.path.exists("assets/theme.json"):
        with open('assets/theme.json', 'r') as file:
            data= json.load(file)
        # Set relevant things here
        tk.set_appearance_mode(data["theme"])
