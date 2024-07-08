###### APP
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023
###### Uses converter.py to open discovery request PDF's in order to respond
###### Provides a Windows GUI tool for opening files and saving as DOCX
###### Version 4.0 | 05/09/2023

# Rules for clean code space
# 1. Use snake_case unless a class name (then camel case)
# 2. Comment everything!
# 3. If possible make something a simple & standard function
# 4. Break everything down into small components and files
# 5. ROOT->Main Windows->Each can have 1 sub window


# IMPORTS
############################################################################################################

#Import minimum things here
import customtkinter as tk
from windows.splash import *
# Functions
from functions import *

# Open splash window here!
if __name__=="__main__":
    initial_theme()
    #PROGRAM SPLASH SCREEN
    splash_screen = Splash()
    splash_screen.update()

# Main Imports
import converter as cnv
from CTkMessagebox import CTkMessagebox
import json,os,copy,sys,time,subprocess
import pickle
from threading import Thread
import re
import os
from enchant import list_languages

# Frame Imports
from frames.BarFrame import *
from frames.LandingFrame import *
from frames.ObjectionsFrame import *
from frames.RequestsFrame import *
from frames.ResponseFrame import *
from frames.FileDetails import *
from frames.FirmDetails import *
# Window Imports
from windows.EditObjections import *
from windows.Hotkeys import *
from windows.Preview import *
from windows.PreviewText import *
from windows.Settings import Settings
# Object Imports
from objects.Client import *
from objects.File import *
from objects.Objection import *
from objects.Request import *
from objects.Save import *
from objects.SmartToolTip import *
from objects.Action import *


# CONSTANTS
############################################################################################################

#CONSTANTS    
RFP_responses={"Available":"Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
                "Not Exist":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist.",
                "Not Possessed":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party.",
                "Lost":"After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen."}

RFA_responses={"Admit":"Admit. ",
                "Deny":"Deny. ",
                "Lack Info":"A reasonable inquiry concerning the matter in this particular request has been made, and the information known or readily obtainable is insufficient to enable Responding Party to admit the matter."}


RFP_EXTRA = " Any responsive documents are believed to be in the possession, custody, or control of [VAR]."

FROGS = {"1.1":"State the name, ADDRESS, telephone number, and relationship to you of each PERSON who prepared or assisted in the preparation of the responses to these interrogatories. (Do not identify anyone who simply typed or reproduced the responses.)",
        "2.1":"State:\n(a) your name;\n(b) every name you have used in the past; and\n(c) the dates you used each name.",
        "2.2":"State the date and place of your birth.",
        "2.3":" At the time of the INCIDENT, did you have a driver's license? If so state: \n(a) the state or other issuing entity; \n(b) the license number and type; \n(c) the date of issuance; and \n(d) all restrictions.",
        "2.4":"At the time of the INCIDENT, did you have any other permit or license for the operation of a motor vehicle? If so, state:\n(a) the state or other issuing entity; \n(b) the license number and type; \n(c) the date of issuance; and \n(d) all restrictions.",
        "2.5":"State:\n(a) your present residence ADDRESS;\n(b) your residence ADDRESSES for the past five years; and\n(c) the dates you lived at each ADDRESS.",
        "2.6":"State:\n(a) the name, ADDRESS, and telephone number of your present employer or place of self-employment; and\n(b) the name, ADDRESS, dates of employment, job title, and nature of work for each employer, or self-employment you have had from five years before the INCIDENT until today.",
        "2.7":"State:\n(a) the name and ADDRESS of each school or other academic or vocational institution you have attended, beginning with high school;\n(b) the dates you attended;\n(c) the highest-grade level you have completed; and\n(d) the degrees received.",
        "2.8":"Have you ever been convicted of a felony? If so, for each conviction state:\n(a) the city and state where you were convicted;\n(b) the date of conviction;\n(c) the offense; and\n(d) the court and case number.",
        "2.9":"Can you speak English with ease?  If not, what language and dialect do you normally use?",
        "2.10":"Can you read and write English with ease?  If not, what language and dialect do you normally use?",
        "2.11":"At the time of the INCIDENT were you acting as an agent or employee for any PERSON? If so, state:\n(a) the name, ADDRESS, and telephone number of that PERSON; and\n(b) a description of your duties.",
        "2.12":"At the time of the INCIDENT did you or any other person have any physical, emotional, or mental disability or condition that may have contributed to the occurrence of the INCIDENT? If so, for each person state: \n(a) the name, ADDRESS, and telephone number;\n(b) the nature of the disability or condition; and\n(c) the manner in which the disability or condition contributed to the occurrence of the INCIDENT.",
        "2.13":"Within 24 hours before the INCIDENT did you or any person involved in the INCIDENT use or take any of the following substances: alcoholic beverage, marijuana, or other drug or medication of any kind (prescription or not)? If so, for each person state:\n(a) the name, ADDRESS, and telephone number;\n(b) the nature or description of each substance;\n(c) the quantity of each substance used or taken;\n(d) the date and time of day when each substance was used or taken;\n(e) the ADDRESS where each substance was used or taken;\n(f) the name, ADDRESS, and telephone number of each person who was present when each substance was used or taken; and\n(g) the name, ADDRESS, and telephone number of any HEALTH CARE PROVIDER who prescribed or furnished the substance and the condition for which it was prescribed or furnished.",
        "3.1":"Are you a corporation? If so, state:\n(a) the name stated in the current articles of incorporation;\n(b) all other names used by the corporation during the past 10 years and the dates each was used;\n(c) the date and place of incorporation; named insured;\n(d) the ADDRESS of the principal place of business; and \n(e) whether you are qualified to do business in California.",
        "3.2":"",
        "3.3":"",
        "3.4":"",
        "3.5":"",
        "3.6":"",
        "3.7":"",
        "4.1":"At the time of the INCIDENT, was there in effect any policy of insurance through which you were or might be insured in any manner (for example, primary, pro-rata, or excess liability coverage or medical expense coverage) for the damages, claims, or actions that have arisen out of the INCIDENT? If so, for each policy state: \n(a) the kind of coverage;\n(b) the name and ADDRESS of the insurance company;\n(c) the name, ADDRESS, and telephone number of each named insured;\n(d) the policy number;\n(e) the limits of coverage for each type of coverage contained in the policy;\n(f) whether any reservation of rights or controversy or coverage dispute exists between you and the insurance company; and\n(g) the name, ADDRESS, and telephone number of the custodian of the policy.",
        "4.2":"Are you self-insured under any statute for the damages, claims, or actions, that have arisen out of the INCIDENT? If so, specific the statute.",
        "6.1":"Do you attribute any physical, mental, or emotional injuries to the INCIDENT? (If your answer is \"no,\" do not answer interrogatories 6.2 through 6.7).",
        "6.2":"Identify each injury you attribute to the INCIDENT and the area of your body affected.",
        "6.3":"Do you still have any complaints that you attribute to the INCIDENT? If so, for each complaint state:\n(a) a description;  \n(b) whether the complaint is subsiding, remaining the same, or becoming worse; and\n(c) the frequency and duration.",
        "6.4":"Did you receive any consultation or examination (except from expert witnesses covered by Code of Civil Procedure sections 2034.210-2034.310) or treatment from a HEALTH CARE PROVIDER for any injury you attribute to the INCIDENT? If so, for each HEALTH CARE PROVIDER state:\n(a) the name, ADDRESS, and telephone number;\n(b) the type of consultation, examination, or treatment provided;\n(c) the dates you received consultation, examination, or treatment; and\n(d) the charges to date.",
        "6.5":"Have you taken any medication, prescribed or not, as a result of injuries that you attribute to the INCIDENT? If so, for each medication state:\n(a) the name;\n(b) the PERSON who prescribed or furnished it;\n(c) the date it was prescribed or furnished;\n(d) the dates you began and stopped taking it; and\n(e) the cost to date.",
        "6.6":"Are there any other medical services necessitated by the injuries that you attribute to the INCIDENT that were not previously listed (for example, ambulance, nursing, prosthetics)?  If so, for each service state:\n(a) the nature;\n(b) the date;\n(c) the cost; and\n(d) the name, ADDRESS, and telephone number of each provider.",
        "6.7":"Has any HEALTH CARE PROVIDER advised that you may require future or additional treatment for any injuries that you attribute to the INCIDENT? If so, for each injury state:\n(a) the name and ADDRESS of each HEALTH CARE PROVIDER;\n(b) the complaints for which the treatment was advised; and\n(c) the nature, duration, and estimated cost of the treatment.",
        "7.1":"Do you attribute any loss of or damage to a vehicle or other property to the INCIDENT? If so, for each item of property:\n(a) describe the property;\n(b) describe the nature and location of the damage to the property;\n(c) state the amount of damage you are claiming for each item of property and how the amount was calculated; and\n(d) if the property was sold, state the name, ADDRESS, and telephone number of the seller, the date of sale, and the sale price.",
        "7.2":"Has a written estimate or evaluation been made for any item of property referred to in your answer to the preceding interrogatory? If so, for each estimate or evaluation state:\n(a) the name, ADDRESS, and telephone number of the PERSON who prepared it and the date prepared;\n(b) the name, ADDRESS, and telephone number of each PERSON who has a copy of it; and\n(c) the amount of damage stated.",
        "7.3":"Has any item of property referred to in your answer to interrogatory 7.1 been repaired? If so, for each item state:\n(a) the date repaired;\n(b) a description of the repair;\n(c) the repair cost;\n(d) the name, ADDRESS, and telephone number of the PERSON who repaired it;\n(e) the name, ADDRESS, and telephone number of the PERSON who paid for the repair.",
        "8.1":"Do you attribute any loss of income or earning capacity to the INCIDENT? (If your answer is \"no,\" do not answer interrogatories 8.2 through 8.8).",
        "8.2":"State:\n(a) the nature of your work;\n(b) your job title at the time of the INCIDENT; and\n(c) the date your employment began.",
        "8.3":"State the last date before the INCIDENT that you worked for compensation.",
        "8.4":"State your monthly income at the time of the INCIDENT and how the amount was calculated.",
        "8.5":"State the date you returned to work at each place of employment following the INCIDENT.",
        "8.6":"State the dates you did not work and for which you lost income as a result of the INCIDENT.",
        "8.7":"State the total income you have lost to date as a result of the INCIDENT and how the amount was calculated.",
        "8.8":"Will you lose income in the future as a result of the INCIDENT? If so, state:\n(a) the facts upon which you base this contention;\n(b) an estimate of the amount;\n(c) an estimate of how long you will be unable to work; and\n(d) how the claim for future income is calculated.",
        "9.1":"Are there any other damages that you attribute to the INCIDENT? If so, for each item of damage state:\n(a) the nature;\n(b) the date it occurred;\n(c) the amount; and\n(d) the name, ADDRESS, and telephone number of each PERSON to whom an obligation was incurred.",
        "9.2":"Do any DOCUMENTS support the existence or amount of any item of damages claimed in interrogatory 9.1?  If so, describe each document and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT.",
        "10.1":"At any time before the INCIDENT did you have complaints or injuries that involved the same part of your body claimed to have been injured in the INCIDENT?  If so, for each state:\n(a) a description of the complaint or injury;\n(b) the dates it began and ended; and,\n(c) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER whom you consulted or who examined or treated you.",
        "10.2":"List all physical, mental, and emotional disabilities you had immediately before the INCIDENT. (You may omit mental or emotional disabilities unless you attribute any mental or emotional injury to the INCIDENT.)",
        "10.3":"At any time after the INCIDENT, did you sustain injuries of the kind for which you are now claiming damages? If so, for each incident giving rise to an injury state:\n(a) the date and the place it occurred;\n(b) the name, ADDRESS, and telephone number of any other PERSON involved;\n(c) the nature of any injuries you sustained;\n(d) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER who you consulted or who examined or treated you; and\n(e) the nature of the treatment and its duration.",
        "11.1":"Except for this action, in the past 10 years have you filed an action or made a written claim or demand for compensation for your personal injuries? If so, for each action, claim, or demand state:\n(a) the date, time, and place and location (closest street ADDRESS or intersection) of the INCIDENT giving rise to the action, claim, or demand;\n(b) the name, ADDRESS, and telephone number of each PERSON against whom the claim or demand was made or the action filed;\n(c) the court, names of the parties, and case number of any action filed;\n(d) the name, ADDRESS, and telephone number of any attorney representing you;\n(e) whether the claim or action has been resolved or is pending; and\n(f) a description of the injury.",
        "11.2":"In the past 10 years have you made a written claim or demand for workers' compensation benefits? If so, for each claim or demand state:\n(a) the date, time, and place of the INCIDENT giving rise to the claim;\n(b) the name, ADDRESS, and telephone number of your employer at the time of the injury;\n(c) the name, ADDRESS, and telephone number of the workers' compensation insurer and the claim number;\n(d) the period of time during which you received workers' compensation benefits;\n(e) a description of the injury;\n(f) the name, ADDRESS, and telephone number of any HEALTH CARE PROVIDER who provided services; and\n(g) the case number at the Workers' Compensation Appeals Board.",
        "12.1":"State the name, ADDRESS, and telephone number of each individual:\n(a) who witnessed the INCIDENT or the events occurring immediately before or after the INCIDENT;\n(b) who made any statement at the scene of the INCIDENT;\n(c) who heard any statements made about the INCIDENT by any individual at the scene; and\n(d) who YOU OR ANYONE ACTING ON YOUR BEHALF claim has knowledge of the INCIDENT (except for expert witnesses covered by Code of Civil Procedure section 2034).",
        "12.2":"Have YOU OR ANYONE ACTING ON YOUR BEHALF interviewed any individual concerning the INCIDENT? If so, for each individual state: \n(a) the name, ADDRESS, and telephone number of the individual interviewed;\n(b) the date of the interview; and\n(c) the name, ADDRESS, and telephone number of the PERSON who conducted the interview.",
        "12.3":"Have YOU OR ANYONE ACTING ON YOUR BEHALF obtained a written or recorded statement from any individual concerning the INCIDENT? If so, for each statement state:\n(a) the name, ADDRESS, and telephone number of the individual from whom the statement was obtained;\n(b) the name, ADDRESS, and telephone number of the individual who obtained the statement;\n(c) the date the statement was obtained; and\n(d) the name, ADDRESS, and telephone number of each PERSON who has the original statement or a copy.",
        "12.4":"Do YOU OR ANYONE ACTING ON YOUR BEHALF know of any photographs, films, or videotapes depicting any place, object, or individual concerning the INCIDENT or plaintiffs’ injuries? If so, state:\n(a) the number of photographs or feet of film or videotape;\n(b) the places, objects, or persons photographed, filmed, or videotaped;\n(c) the date the photographs, films, or videotapes were taken;\n(d) the name, ADDRESS, and telephone number of the individual taking the photographs, films, or videotapes; and\n(e) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of the photographs, films, or videotapes.",
        "12.5":"Do YOU OR ANYONE ACTING ON YOUR BEHALF know of any diagram, reproduction, or model of any place or thing (except for items developed by expert witnesses covered by Code of Civil Procedure sections 2034.2102034.310) concerning the INCIDENT? If so, for each item state:\n(a) the type (i.e., diagram, reproduction, or model);\n(b) the subject matter; and\n(c) the name, ADDRESS, and telephone number of each PERSON who has it.",
        "12.6":"Was a report made by any PERSON concerning the INCIDENT? If so, state:\n(a) the name, title, identification number, and employer of the PERSON who made the report;\n(b) the date and type of report made;\n(c) the name, ADDRESS, and telephone number of the PERSON for whom the report was made; and\n(d) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of the report.",
        "12.7":"Have YOU OR ANYONE ACTING ON YOUR BEHALF inspected the scene of the INCIDENT? If so, for each inspection state:\n(a) the name, ADDRESS, and telephone number of the individual making the inspection (except for expert witnesses covered by Code of Civil Procedure sections 2034.210-2034.310); and\n(b) the date of the inspection.",
        "13.1":"Have YOU OR ANYONE ACTING ON YOUR BEHALF conducted surveillance of any individual involved in the INCIDENT or any party to this action? If so, for each surveillance state: \n(a) The name, ADDRESS, and telephone number of the individual or party; \n(b) The time, date, and place of the surveillance; \n(c) The name, ADDRESS, and telephone number of the individual who conducted the surveillance; and \n(d) The name, ADDRESS, and telephone number of each PERSON who has the original or a copy of any surveillance photograph, film, or videotape. ",
        "13.2":"Has a written report prepared on the surveillance? If so, for each written report state: \n(a) The title;\n(b) The date; \n(c) The name, ADDRESS, and telephone number of the individual who prepared the report; and \n(d) The name, ADDRESS, and telephone number of each PERSON who has the original or a copy. ",
        "14.1":"Do YOU OR ANYONE ACTING ON YOUR BEHALF contend that any PERSON involved in the INCIDENT violated any statute, ordinance, or regulation and that the violation was a legal (proximate) cause of the INCIDENT? If so, identify the name, ADDRESS, and telephone number of each PERSON and the statute, ordinance, or regulation that was violated.",
        "14.2":"Was any PERSON cited or charged with a violation of any statute, ordinance, or regulation as a result of this INCIDENT? If so, for each PERSON state:\n(a) the name, ADDRESS, and telephone number of the PERSON;\n(b) the statute, ordinance, or regulation allegedly violated;\n(c) whether the PERSON entered a plea in response to the citation or charge and, if so, the plea entered; and\n(d) the name and ADDRESS of the court or administrative agency, names of the parties, and case number.",
        "17.1":"Is your response to each request for admission served with these interrogatories an unqualified admission? If not, for each response that is not an unqualified admission: \n(a) State the number of the request; \n(b) State all facts upon which you base your response;\n(c) State the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of these facts; and \n(d) Identify all DOCUMENTS and other tangible things that support your response and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
        "20.1":"State the date, time, and place of the INCIDENT (closest street ADDRESS or intersection).",
        "20.2":"For each vehicle involved in the INCIDENT, state: \n(a) the year, make, model, and license number;\n(b) the name, ADDRESS, and telephone number of the driver;\n(c) the name, ADDRESS, and telephone number of each occupant other than the driver;\n(d) the name, ADDRESS, and telephone number of each registered owner;\n(e) the name, ADDRESS, and telephone number of each lessee;\n(f) the name, ADDRESS, and telephone number of each owner other than the registered owner or lien holder; and\n(g) the name of each owner who gave permission or consent to the driver to operate the vehicle.",
        "20.3":"State the ADDRESS and location where your trip began and the ADDRESS and location of your destination.",
        "20.4":"Describe the route that you followed from the beginning of your trip to the location of the INCIDENT, and state the location of each stop, other than routine traffic stops, during the trip leading up to the INCIDENT.",
        "20.5":"State the name of the street or roadway, the lane of travel, and the direction of travel of each vehicle involved in the INCIDENT for the 500 feet of travel before the INCIDENT.",
        "20.6":"Did the INCIDENT occur at an intersection? If so, describe all traffic control devices, signals, or signs at the intersection.",
        "20.7":"Was there a traffic signal facing you at the time of the INCIDENT? If so, state:\n(a) your location when you first saw it;\n(b) the color;\n(c) the number of seconds it had been that color; and\n(d) whether the color changed between the time you first saw it and the INCIDENT.",
        "20.8":"State how the INCIDENT occurred, giving the speed, direction, and location of each vehicle involved:\n(a) just before the INCIDENT;\n(b) at the time of the INCIDENT; and\n(c) just after the INCIDENT.",
        "20.9":"Do you have information that a malfunction or defect in a vehicle caused the INCIDENT? If so:\n(a) identify the vehicle;\n(b) identify each malfunction or defect;\n(c) state the name, ADDRESS, and telephone number of each PERSON who is a witness to or has information about each malfunction or defect; and\n(d) state the name, ADDRESS, and telephone number of each PERSON who has custody of each defective part.",
        "20.10":"Do you have information that any malfunction or defect in a vehicle contributed to the injuries sustained in the INCIDENT? If so:\n(a) identify the vehicle;\n(b) identify each malfunction or defect;\n(c) state the name, ADDRESS, and telephone number of each PERSON who is a witness to or has information about each malfunction or defect; and\n(d) state the name, ADDRESS, and telephone number of each PERSON who has custody of each defective part.",
        "20.11":"State the name, ADDRESS, and telephone number of each owner and each PERSON who has had possession since the INCIDENT of each vehicle involved in the INCIDENT."
        }


# MAIN WINDOW FRAME
############################################################################################################

# MAIN WINDOW CLASS
class App(tk.CTkToplevel):
    #CONSTRUCTOR 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)

        ##### VERSION NUMBER
        self.version="1.1.0"

        ##### CLASS ATTRIBUTES
        self.master=master#Master is root of the program (Top level tk)
        master.call()
        #A list of all the open client objects
        self.clients=[]
        #Holds all requests in the currently selected file
        self.reqs=[]
        #Denotes the current client object
        self.current_client = ""
        #Current selected file object
        self.current_file = ""
        #The currently selected request
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
        validate_integrity_of_config_file()
        #Loads the config file (software settings)
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
        #Set the starting size of the window, but then set to zoomed
        self.geometry("1050x720")
        self.state("zoomed")
        #Set the title of the main window
        self.title("myDiscoveryResponses")#Window title

        ##### BEGIN REGULAR INTERVAL FUNCTIONS
        #Refresher updates text and software as the user interacts
        self.after(100, self.refresher)
        #Autosave will trigger the save function at regular intervals
        self.after(int(self.CONFIG["general"]["autosave_interval"]),self.autosave)
        
        ##### KEY BINDINGS
        self.bind("<Up>",self.up_pressed)
        self.bind("<Down>",self.down_pressed)
        self.bind("<Return>",self.enter_pressed)
        self.bind("<Escape>",self.escape_pressed)
        self.bind("<Button-1>",self.mouse_pressed)
        self.protocol("WM_DELETE_WINDOW", self.exit_window)
        self.bind("<Control-n>",self.cntrl_n)
        self.bind("<Control-o>",self.cntrl_o)
        self.bind("<Control-f>",self.cntrl_f)
        self.bind("<Control-s>",self.cntrl_s)
        self.bind("<Control-e>",self.cntrl_e)

        ##### POPULATE WINDOW WITH OBJECTS
        self.populate_window()

        return


        

    ### WINDOW UTILITY
    ########################################################################################################

    #Add Frames to the window
    def populate_window(self):
        # Navigation Bar Frame
        self.bar_frame = Bar_Frame(master=self,corner_radius=0,fg_color="#161616")
        self.bar_frame.pack(padx=0,pady=0,fill="both")
        # Requests Frame
        self.requests_frame = Requests_Frame(master=self,corner_radius=0,width=100)
        self.requests_frame.pack(padx=0,pady=0,expand=False,side="left",fill="both")
        #Landing Frame
        self.landing_frame = Landing_Frame(master=self,corner_radius=15)
        self.landing_frame.pack(padx=100,pady=100,expand=True,side="left",fill="both")
        # Objections Frame
        self.objections_frame = Objections_Frame(master=self,corner_radius=0,width=250)
        # Response Frame
        self.response_frame = Response_Frame(master=self)
        self.set_theme("text")#Set theme just for text, as main theme loaded at start
        #Additional frame used for editing file and firm details
        self.details_frame = None
        
    # Create a new MAIN window
    def create_window(self):
        create_window(self.master)

    # REFRESH WINDOW PERIODICALLY, (MUST BE EFFICIENT FOR PERFORMANCE)
    def refresher(self):
        if self.current_req!=0:
            # 1. UPDATE OBJECTION TEXTBOX
            #Set the current objection parameters
            if self.current_req.current_objection!="":
                self.current_req.current_objection.param = self.objections_frame.objection_input.get()
                self.current_req.current_objection.additional_param = self.objections_frame.additional_input.get()

            #The custom text is the text typed into the box
            self.current_req.custom_objection_text = self.response_frame.get_objection()#Get prev text from box

            remove_end=False
            if not ((self.req_type!="RFP" and len(self.response_frame.get_response())>0) or (self.req_type=="RFP" and len(self.response_frame.get_RFP())>0)):
                remove_end = True
            text = get_objection_text(self.current_req.opts,self.objections,remove_end)#Get objections with no end if text in response
            #Check if any of the objections or params have changed
            if text!=self.previous_objection_text:#If the text has changed REDRAW
                self.response_frame.set_objection(text)
                self.set_client_unsaved(self.current_client)


            self.previous_objection_text = text # Save for next time

            # 2. UPDATE RESPONSE TEXTBOX
            if self.req_type=="RFA":
                option = self.response_frame.get_RFA()

                #Do Hotkeys for the 17.1 Response

                ###COPIED FROM BELOW: REPLACE!!! CREATE A FUNCTION FOR THIS

                #Do HOTKEYS HERE
                insert_index = self.response_frame.current_frame.RFA_text.index(tk.INSERT)#Current index
                resp = " "+self.response_frame.get_RFA_text()#Current response text
                use_fill=None
                use_pos=0
                start=0
                for fill in self.HOTKEYS:# Replace all autofill phrases
                    position = -1
                    trigger = " "+fill+" "
                    position = resp.find(trigger)#Pos of index
                    if position<0:
                        position = resp.find("\n"+trigger[1:])# Try new line instances
                        if position>=0:
                            start=1
                    if position>=0:
                        use_fill = fill# Set this to fill
                        use_pos = position
                if use_fill!=None:# IF AN AUTOFILL USED
                    text = resp[1:]#Remove space
                    # Update index if grown in length, must add suffic n + chars
                    text_index="0.0 + "+str(use_pos)+" chars"
                    text_end_index="0.0 + "+str(use_pos+len(use_fill+" "))+" chars"
                    # Put the text here 
                    self.response_frame.current_frame.RFA_text.delete(text_index,text_end_index)
                    self.response_frame.current_frame.RFA_text.insert(text_index,(self.HOTKEYS[use_fill]+" "))
                    # Reset index
                    insert_index+=" + "+str(len(self.HOTKEYS[use_fill]+" ")-len(use_fill)-1)+" chars"
                    self.response_frame.current_frame.RFA_text.mark_set("insert",insert_index)



            else:
                option = self.response_frame.get_RFP()
            
            # RFP
            if self.req_type=="RFP" and option!="Custom":
                temp = self.response_frame.get_response()#Get prev text from box
                resp = self.response_frame.get_RFP_text()
                text = RFP_responses[option].replace("[VAR]",resp)
                if option!="Available" and resp!="":
                    text = (text+RFP_EXTRA).replace("[VAR]",resp)
                if text!=temp.replace("\n",""):#If the text has changed REDRAW
                    self.set_client_unsaved(self.current_client)
                    #Change response text
                    self.response_frame.set_response(text)
                    #Change color of request
                    self.current_req.color="grey"
                    self.current_client.current_file.color=("black","white")
                    self.requests_frame.update_files(self.current_client.files)
            # RFA
            elif self.req_type=="RFA" and option!="Custom":
                temp = self.response_frame.get_response()#Get prev text from box
                text = RFA_responses[option]
                if text!=temp.replace("\n",""):#If the text has changed REDRAW
                    self.set_client_unsaved(self.current_client)
                    #Change response text
                    self.response_frame.set_response(text)
                    #Change color of request
                    self.current_req.color="grey"
                    self.current_client.current_file.color=("black","white")
                    self.requests_frame.update_files(self.current_client.files)

            # NORMAL
            else:#If NOT RFP

                
                insert_index = self.response_frame.current_frame.response_text.index(tk.INSERT)#Current index
                resp = " "+self.response_frame.get_response()#Current response text

                #DO CURCLY QUOTES HERE!
                if '"' in resp or "'" in resp:
                    resp = curly_convert(resp)
                    # Put the text here 
                    self.response_frame.current_frame.response_text.delete("0.0","end-1c")
                    self.response_frame.current_frame.response_text.insert("0.0",resp[1:])
                    self.response_frame.current_frame.response_text.mark_set("insert",insert_index)

                #DO HOTKEYS HERE
                use_fill=None
                use_pos=0
                start=0
                for fill in self.HOTKEYS:# Replace all autofill phrases
                    position = -1
                    trigger = " "+fill+" "
                    position = resp.find(trigger)#Pos of index
                    if position<0:
                        position = resp.find("\n"+trigger[1:])# Try new line instances
                        if position>=0:
                            start=1
                    if position>=0:
                        use_fill = fill# Set this to fill
                        use_pos = position
                if use_fill!=None:# IF AN AUTOFILL USED
                    text = resp[1:]#Remove space
                    # Update index if grown in length, must add suffic n + chars
                    text_index="0.0 + "+str(use_pos)+" chars"
                    text_end_index="0.0 + "+str(use_pos+len(use_fill+" "))+" chars"
                    # Put the text here 
                    self.response_frame.current_frame.response_text.delete(text_index,text_end_index)
                    self.response_frame.current_frame.response_text.insert(text_index,(self.HOTKEYS[use_fill]+" "))
                    # Reset index
                    insert_index+=" + "+str(len(self.HOTKEYS[use_fill]+" ")-len(use_fill)-1)+" chars"
                    self.response_frame.current_frame.response_text.mark_set("insert",insert_index)

                if resp[1:].replace("\n","")!=self.current_req.resp.replace("\n",""):# Change colour back if edited
                    self.current_req.color="grey"
                    self.current_req.resp=resp[1:]
                    self.current_client.current_file.color=("black","white")
                    self.requests_frame.update_files(self.current_client.files)
                    self.set_client_unsaved(self.current_client)


        self.after(100, self.refresher)#REFRESH AGAIN

    #Toggles whether the program is in fullscreen or not
    def toggle_fullscreen(self):
        state = not self.attributes('-fullscreen')
        self.attributes("-fullscreen",state)
        self.set_theme("theme")
        self.win

    #Reload the objections for each request! Stops errors when objections changed
    def reload_objections(self):
        for client in self.clients:
            client.reload_objections()

    #Destroy this windows sub window
    def cancel_win(self):
        if self.win!=None:
            self.win.destroy()
            self.win=None

    # Save details from the details window
    def save_detail_win(self):
        self.current_client.current_file.details["county"] = self.details_frame.county.get("0.0","end").replace("\n","")
        self.current_client.current_file.details["case_number"] = self.details_frame.case.get("0.0","end").replace("\n","")
        self.current_client.current_file.details["document"] = self.details_frame.document.get("0.0","end").replace("\n","")
        self.current_client.current_file.details["plaintiff"] = self.details_frame.plaintiff.get("0.0","end").replace("\n","")
        self.current_client.current_file.details["defendant"] = self.details_frame.defendant.get("0.0","end").replace("\n","")
        self.current_client.current_file.details["propounding_party"] = self.details_frame.propounding_party.get("0.0","end").replace("\n","")
        self.current_client.current_file.details["responding_party"] = self.details_frame.responding_party.get("0.0","end").replace("\n","")
        #Date
        self.current_client.current_file.details["date"] = self.details_frame.date.get("0.0","end").replace("\n","")
        #Name
        self.current_client.current_file.name = self.details_frame.name.get("0.0","end").replace("\n","")

        self.requests_frame.show_files(self.current_client.files)
        self.title("myDiscoveryResponses   |   "+str(self.current_client.current_file.name))
        self.set_client_unsaved(self.current_client)
        self.close_details()
        
    def save_firm_detail_win(self):
        new_details={"firm_name":self.details_frame.name.get("0.0","end-1c"),
                    "address_line_1":self.details_frame.address_line_1.get("0.0","end-1c"),
                    "address_line_2":self.details_frame.address_line_2.get("0.0","end-1c"),
                    "telephone":self.details_frame.telephone.get("0.0","end-1c"),
                    "facsimile":self.details_frame.facsimile.get("0.0","end-1c"),
                    "email":self.details_frame.email.get("0.0","end-1c"),
                    "attorneys":self.details_frame.attorneys.get("0.0","end-1c")}
        
        if self.current_client!="":
            self.set_client_unsaved(self.current_client)
            self.current_client.firm_details = new_details
        else:
            set_firm_details(new_details)
        self.close_details()


    def client_already_open(self,client_name):
        for client in self.clients:
            if client.name == client_name:
                #Show a warning
                CTkMessagebox(title="Error",
                               message="Already have a client open with the name '"+str(client_name)+"' !", 
                               icon="cancel",
                               corner_radius=0,
                               sound=True,
                               master=self)
                #Return 
                return True
        return False
        

    # validates wether a valid file is open
    def file_open(self):
        if self.current_client!="":
            if self.current_client.current_file!="":
                return True
        return False

    # View and edit the details of the document
    def view_details(self):
        if self.file_open() and self.details_frame==None:
            #Remove (visibly) response and objection frames
            self.response_frame.pack_forget()
            self.objections_frame.pack_forget()

            self.details_frame = File_Details_Frame(master=self)
            self.details_frame.pack(fill="both",expand=True,padx=20,pady=20)

    def close_details(self):
        if self.details_frame!=None:
            self.details_frame.destroy()
            self.details_frame = None
            if self.clients==[]:
                self.landing_frame.pack(padx=100,pady=100,expand=True,side="left",fill="both")
            else:
                self.objections_frame.pack(padx=0,pady=0,expand=False,side="right",fill="both")
                self.response_frame.pack(padx=20,pady=20,expand=True,side="left",fill="both")


    def view_firm_details(self):
        if self.details_frame==None:
            #Remove (visibly) response and objection frames
            self.response_frame.pack_forget()
            self.objections_frame.pack_forget()
            self.landing_frame.pack_forget()

            self.details_frame = Firm_Details_Frame(master=self)
            self.details_frame.pack(fill="both",expand=True,padx=20,pady=20)


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
            self.export(self.current_client.current_file,os.path.join(os.path.dirname(__file__),"assets/temp"))
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
            self.objections_frame.pack(padx=0,pady=0,expand=False,side="right",fill="both")
            self.response_frame.pack(padx=20,pady=20,expand=True,side="left",fill="both")

    def open_landing_frame(self):
        self.objections_frame.pack_forget()
        self.response_frame.pack_forget()
        self.landing_frame.pack(padx=100,pady=100,expand=True,side="left",fill="both")

    # Exit this window and delete
    def exit_window(self):
        unsaved=False
        for client in self.clients:
            if client.saved==False:
                unsaved=True
        if unsaved:#Check if the user wants to save without closing!!
            msg = CTkMessagebox(title="Exit?", 
                                message="Are you sure you want to close without saving?",
                                icon="question",
                                option_1="Cancel", 
                                option_3="Yes",
                                corner_radius=0,
                                sound=True,
                                master=self)
            if msg.get()!="Yes":
                return
        self.destroy()
        c=0
        for w in root.winfo_children():
            c+=1
        if c==0:#Destroy root if no windows left open
            root.destroy()

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
                dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"myDiscoveryResponses_Installer.exe")

                #Open installer
                subprocess.Popen(["cmd","/c","start","",dir_path],
                                        stdout=subprocess.DEVNULL,  # Redirect output to avoid hanging on pipes
                                        stderr=subprocess.DEVNULL,
                                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_BREAKAWAY_FROM_JOB,
                                        close_fds=True)

                #Destroy this application
                self.destroy()
                root.destroy()



    ### KEY PRESSES
    ########################################################################################################
    # HOTKEYS
    # CNTRL-N New Client
    def cntrl_n(self,e):
        self.new_client()
    # CNTRL-
    def cntrl_o(self,e):
        self.select_file()
    def cntrl_f(self,e):
        self.select_folder()
    def cntrl_s(self,e):
        self.quick_save()
    def cntrl_e(self,e):
        self.export_current()

    # If up arrow
    def up_pressed(self,e):
        #If focus is app
        if self.current_req!=0 and self.focus_get()==self:
            index = self.reqs.index(self.current_req)
            index = max(0,index-1)
            self.set_request(self.reqs[index])
            self.requests_frame.scroll_to()

    # If down arrow
    def down_pressed(self,e):
        #If focus is app
        if self.current_req!=0 and self.focus_get()==self:
            index = self.reqs.index(self.current_req)
            index = min(len(self.reqs)-1,index+1)
            self.set_request(self.reqs[index])
            self.requests_frame.scroll_to()

    #If enter
    def enter_pressed(self,e):
        #If focus is app
        if self.current_req!=0 and self.focus_get()==self:
            self.submit()

    #If escape
    def escape_pressed(self,e):
        self.focus_set()

    #Get mouse press and set focus!
    def mouse_pressed(self,e):
        if "textbox" not in str(e.widget) and "ctkentry" not in str(e.widget):
            self.focus_set()


    #Add an action to the undo action stack
    def add_action_to_stack(self,new_action):
        #Reset redos as now out of date
        self.REDO_ACTION_STACK = []
        self.bar_frame.disable_redo()
        #Add to the action stack
        self.ACTION_STACK.append(new_action)
        #If only one item then enable the undo button again
        if len(self.ACTION_STACK)==1:
            self.bar_frame.enable_undo()

        self.print_stacks()

    #Undo the previous action and remove it from the stack (put on redo stack)
    def undo_action(self):
        action = self.ACTION_STACK.pop()
        action.undo()
        self.REDO_ACTION_STACK.append(action)
        #IF EMPTY then disable the undo button
        if len(self.ACTION_STACK)==0:
            self.bar_frame.disable_undo()

        #If redo now has one then enable
        if len(self.REDO_ACTION_STACK)==1:
            self.bar_frame.enable_redo()

        self.print_stacks()

    #Redo an action which was undone, when action stack added to then the redo stack will clear
    def redo_action(self):
        action = self.REDO_ACTION_STACK.pop()
        action.redo()
        self.ACTION_STACK.append(action)
        #IF EMPTY then disable the redo button
        if len(self.REDO_ACTION_STACK)==0:
            self.bar_frame.disable_redo()

        #If only one item then enable the undo button again
        if len(self.ACTION_STACK)==1:
            self.bar_frame.enable_undo()

        self.print_stacks()

    def print_stacks(self):
        print("ACTION STACK: "+str(len(self.ACTION_STACK))+"  REDO STACK: "+str(len(self.REDO_ACTION_STACK)))

    ### SAVING AND LOADING OF FILES & FOLDERS
    ########################################################################################################


    # Open a folder containing files
    def select_folder(self):
        filename = tk.filedialog.askdirectory(
            title='Open Folder')
        if filename=="":
            return
        added=False
        for f in os.listdir(filename):
            if len(f)>4:
                if f[-4:]==".pdf":
                    if os.path.exists(filename+"/"+f):
                        self.open_file(filename+"/"+f)
                        added=True
        if added:# Set the file if been added!
            self.title("myDiscoveryResponses   |   "+str(self.current_client.files[-1].name.split("/")[-1]))
            self.current_client.current_file=self.current_client.files[-1]
            # Add file
            self.requests_frame.show_clients(self.clients)
            if self.current_client!="":
                self.requests_frame.show_files(self.current_client.files)
            self.requests_frame.show_list(self.reqs)
            self.set_request(self.reqs[0])
            self.requests_frame.scroll_to(True)
            self.update()

    # Open a single file
    def select_file(self):
        filetypes = (
            ('Files', '*.pdf *.discovery'),
            ('All files', '*.*')
        )
        filenames = tk.filedialog.askopenfilenames(
            title='Open file',
            filetypes=filetypes)

        for filename in filenames:
            if os.path.exists(filename):
                if filename[-4:].lower()==".pdf":#PDF
                    if self.current_client=="":# If no client selected
                        CTkMessagebox(title="Error",
                                       message="Must create a client to open Discovery Requests", 
                                       icon="cancel",
                                       corner_radius=0,
                                       sound=True,
                                       master=self)
                        return
                    self.title("myDiscoveryResponses   |   "+str(filename.split("/")[-1]))
                    self.open_file(filename)
                    #Else if a obj
                    self.current_client.current_file =self.current_client.files[-1]
                    # Add file
                    self.requests_frame.show_clients(self.clients)
                    if self.current_client!="":
                        self.requests_frame.show_files(self.current_client.files)
                    self.requests_frame.show_list(self.reqs)
                    self.set_request(self.reqs[0])
                    self.requests_frame.scroll_to(True)
                    self.update()
                elif filename[-10:]==".discovery":#OBJ
                    self.load(filename)

    # Opens a PDF file specifically
    def open_file(self,filename):
        if os.path.exists(filename):
            self.close_landing_frame()
            try:
                reqs,req_type,doc_details,custom_keys = cnv.getRequests(filename)
            except Exception as e:
                msg = CTkMessagebox(title="Loading Issue", 
                                    message="The selected file: "+str(filename)+" could not be loaded!\nError Message: "+str(e),
                                    icon="warning", 
                                    option_1="Okay",
                                    corner_radius=0,
                                    width=800,
                                    sound=True,
                                    master=self)
                return
            self.set_type(req_type)# Sets the current type
            self.reqs=[]
            #Redraw for production
            self.response_frame.redraw(self.req_type)
            if req_type=="FROG":
                c=0
                for i in FROGS:
                    if i in reqs and "(" not in i:
                        new = Request(FROGS[i],"",c,self,req_type,i)
                        self.reqs.append(new)
                    c+=1
            else:
                c=0
                for i in reqs:
                    key = ""
                    if custom_keys!=[]:
                        key = custom_keys[c]
                    self.reqs.append(Request(i,"",c,self,req_type,key))
                    c+=1

            ### ADD NEW FILE TO CLIENT, IF NONE THEN CREATE NEW CLIENT!
            new_file = File(filename,doc_details,self.req_type,self.reqs,self)
            if self.current_client!="":
                self.current_client.files.append(new_file)
            else:
                self.clients.append(Client(doc_details["defendant"],[new_file],self))
                self.set_client(self.clients[-1])



    #SAVING AND LOADING WITH PICKLE

    #Load File whether it be a file or a client
    def load(self,filename):
        # Create file obj
        file = open(filename,"rb")
        # Load the file object
        try:
            save_obj = pickle.load(file)
        except:
            file.close()
            msg = CTkMessagebox(title="File Corrupted", 
                                message="An error has caused this file to become corrupted!",
                                icon="warning", 
                                option_1="Okay",
                                corner_radius=0,
                                sound=True,
                                master=self)
            return
        file.close()
        # Get files array
        if save_obj.save_type == "file":
            self.load_file(save_obj.files[0])
        else:
            self.load_client(save_obj.files[0],filename)
    
    #Load a single file into the current client
    def load_file(self,new_file):
        if self.current_client=="":
            return
        #Set new master
        new_file.set_master(self)
        # Add file
        self.current_client.files.append(new_file)
        self.requests_frame.show_files(self.current_client.files)
        self.set_file(self.current_client.files[-1])
        self.requests_frame.show_clients(self.clients)
        
    #Load Client
    def load_client(self,new_client,filename):
        if self.client_already_open(new_client.name):
            return
        #Set new master
        new_client.set_master(self)
        # Add file
        self.clients.append(new_client)
        self.set_client(self.clients[-1])
        self.requests_frame.show_clients(self.clients)
        self.close_landing_frame()
        #SET THE QUICKSAVE!
        self.current_client.save=filename
        self.set_recents(filename)
        self.reload_objections()


    #Select the save file
    def select_save_file(self):
        # Select a folder and save name
        filename=tk.filedialog.asksaveasfilename(title="Save Current File",filetypes=(("Discovery Save File","*.discovery"),('All files', '*.*'))).replace(".discovery","")
        if filename=="":
            return
        self.save_file(filename)

    #Actually do the file saving
    def save_file(self,filename):
        file = open(filename+".discovery","wb")
        # Remove master from the save
        self.current_client.current_file.set_master(None)
        # Create save object
        save_obj = Save([self.current_client.current_file],"file")
        # Pickle the current File
        pickle.dump(save_obj,file)#Need to fix saving with the name
        # Add the master back
        self.current_client.current_file.set_master(self)
        file.close()

    #Select a save to save the client file as
    def select_save_client(self):
        # Select a folder and save name
        filename=tk.filedialog.asksaveasfilename(title="Save Current Client",filetypes=(("Discovery Save File","*.discovery"),('All files', '*.*'))).replace(".discovery","")
        if filename=="":
            return
        self.save_client(filename)

    """
    #Actually save the client file
    def save_client_OLD(self,filename):
        # Remove master from the save
        self.current_client.set_master(None)
        # Create save object
        save_obj = Save([self.current_client],"client")
        # Pickle the current File
        file = open(filename+".discovery","wb")
        pickle.dump(save_obj,file)#Need to fix saving with the name
        file.close()
        # Add the master back
        self.current_client.set_master(self)
        # Set the quicksave
        self.current_client.save = filename+".discovery"
        self.current_client.saved = True
        #Update clients to show saved
        self.requests_frame.update_clients(self.clients)
        self.set_recents(self.current_client.save)
    """

    #Actually save the client file
    def save_client(self,filename):
        # Remove master from the save
        self.current_client.set_master(None)
        # Create save object
        save_obj = Save([self.current_client],"client")

        #STORE AS A TEMPORARY FILE!
        # Pickle the current File
        file = open(filename+"TEMPORARY"+".discovery","wb")
        try:
            pickle.dump(save_obj,file)#Need to fix saving with the name
        except:
            file.close()
            self.current_client.set_master(self)
            msg = CTkMessagebox(title="Saving Issue", 
                                message="The selected file: "+str(filename)+" could not be saved [1]!",
                                icon="warning", 
                                option_1="Okay",
                                corner_radius=0,
                                sound=True,master=self)
            return 
        file.close()

        try:
            #DELETE ORIGINAL
            if os.path.exists(filename+".discovery"):
                os.remove(filename+".discovery")

            #REPLACE ORIGINAL FILE WITH TEMPORARY FILE!
            os.rename(filename+"TEMPORARY"+".discovery",filename+".discovery")
        except:
            self.current_client.set_master(self)
            msg = CTkMessagebox(title="Saving Issue", 
                                message="The selected file: "+str(filename)+" could not be saved [2]! SAVE UNDER A NEW NAME!",
                                icon="warning", 
                                option_1="Okay",
                                corner_radius=0,
                                sound=True,
                                master=self)
            return 
           
        # Add the master back
        self.current_client.set_master(self)
        # Set the quicksave
        self.current_client.save = filename+".discovery"
        self.current_client.saved = True
        #Update clients to show saved
        self.requests_frame.update_clients(self.clients)
        self.set_recents(self.current_client.save)


    #QUICKSAVE: Only saves CLIENT!
    def quick_save(self):
        if self.current_client!="":
            if valid_file_path(self.current_client.save):#If client has a save
                self.save_client(self.current_client.save.replace(".discovery",""))#Remove file type
                self.bar_frame.update_autosave_time()
                return
            else:
                self.select_save_client()#Save client if nothing else!
                self.bar_frame.update_autosave_time()

    def autosave(self):
        #Change to save all valid clients
        if self.CONFIG["general"]["autosaving"]:
            if self.current_client!="":#ONLY DO IF THERE IS A VALID SAVE FILE!!!
                if valid_file_path(self.current_client.save):#If client has a save
                    self.quick_save()
        self.after(int(self.CONFIG["general"]["autosave_interval"]),self.autosave)

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

    #Close the current file
    def close_file(self):
        if self.file_open():#We know a valid file is open
            msg = CTkMessagebox(title="Close File?", 
                                message="Are you sure you want to permanently close this file?",
                                icon="question", 
                                option_1="Cancel", 
                                option_3="Yes",
                                corner_radius=0,
                                sound=True,
                                master=self)
            
            if msg.get()=="Yes":
                #Get the index of the current file
                index = self.current_client.files.index(self.current_client.current_file)
                if index==0:
                    new_index=1
                else:
                    new_index = index-1

                #Set the new file
                if new_index<len(self.current_client.files):
                    self.set_file(self.current_client.files[new_index])
                    self.requests_frame.scroll_to_file()
                    self.current_client.files.pop(index)
                else:
                    self.current_client.current_file=""
                    self.current_client.files=[]
                self.set_client(self.current_client)
                #self.requests_frame.show_files(self.current_client.files)

    #Close the current open client
    def close_client(self):
        if self.current_client!="":
            #Close details menu if open!
            self.close_details()
            if self.current_client.saved==False:
                msg = CTkMessagebox(title="Close Client?", 
                                    message="Are you sure you want to close the client without saving?",
                                    icon="question", 
                                    option_1="Cancel", 
                                    option_3="Yes",
                                    corner_radius=0,
                                    sound=True,
                                    master=self)
                
                if msg.get()!="Yes":
                    return
            #Get new index for new selected client
            index = self.clients.index(self.current_client)
            if index==0:
                new_index=1
            else:
                new_index = index-1
            
            if new_index<len(self.clients):
                self.set_client(self.clients[new_index])
            else:
                self.close_all()
                return
            #REMOVE the client
            self.clients.pop(index)
            #Redraw Things
            self.requests_frame.show_clients(self.clients)

    #Close all files open in the workspace
    def close_all(self):
        # Attributes
        self.files=[]
        self.reqs=[]
        self.req_type=""
        self.prev_type=""
        self.current_req=0
        self.clients=[]
        self.current_client=""
        # Reset Clients
        self.requests_frame.show_clients([])
        # Reset Files
        self.requests_frame.show_files([])
        # Reset Requests
        self.requests_frame.show_list([])
        # Reset Response
        self.response_frame.reset()
        #Reset Objections
        self.objections_frame.reset()
        #Reset display save time
        self.bar_frame.reset_autosave_time()
        #Reopen landing page
        self.open_landing_frame()
        #Set window title
        self.title("myDiscoveryResponses")#Window title



    def load_client_feedback(self):
        if self.file_open():
            filename = tk.filedialog.askopenfilename(title='Load Client Feedback', filetypes=(('Word Docx', '.docx'),('All files', '*.*')))
            if filename!="":
                feedback = cnv.read_client_feedback(filename)
                #KEY,RESP,TYPE
                for f in feedback:
                    for file in self.current_client.files:
                        if file.req_type == f["type"]:
                            for req in file.reqs:
                                if str(req.custom_key)==f["key"]:
                                    if req.req_type=="RFA" and req.RFA_option!="Custom":#If RFA then set this to custom
                                        req.RFA_option="Custom"
                                        req.resp=""
                                    elif req.req_type=="RFP" and req.RFP_option!="Custom":#If RFP then set this to custom
                                        req.RFP_option="Custom"
                                        req.resp=""
                                    req.resp = req.resp + f["response"]#Add client feedback to end of the response text
                                    if req==self.current_req:#If this is the current request then update screen
                                        self.response_frame.set_RFP("Custom")
                                        self.response_frame.set_RFA("Custom")
                                        self.response_frame.set_response(req.resp)



    ### EXPORTING AS DOCX
    ########################################################################################################

    
    # Export a file as DOCX
    def export(self,file,filename):
        reqs=[]
        resps=[]
        numbers=[]
        for r in file.reqs:#Get responses and requests
            #Export ALL for FROGS, and submitted for others depending on setting
            if file.req_type=="FROG" or (file.req_type!="FROG" and r.color=="#50C878") or self.CONFIG["general"]["submitted_only"]==0:
                #1. ADD REQUESTS
                reqs.append(r.req)
                #2. ADD RESPONSES
                full_text = r.get_full_resp()
                resps.append(full_text)
                #3. ADD NUMBER POINTERS
                numbers.append(r.custom_key)
        cnv.updateDOC(reqs,resps,file.details,self.current_client.firm_details,file.req_type,str(filename),numbers)

        #Open the word document if setting is selected
        if self.CONFIG["general"]["open_export"]:
            filename = str(filename)+".docx"
            os.system(f'start "" "{filename}"')

    # Export all as a folder of DOCX's
    def export_all(self):
        if len(self.current_client.files)>0:
            # Select Folder
            filename = tk.filedialog.askdirectory(title='Select Export Folder')
            # For each file
            for file in self.current_client.files:
                self.export(file,filename+"/"+str(file.name.split("/")[-1].split(".")[0]))

    # Select a save then use export function
    def export_current(self):
        #Need to get the correct file location and then save
        if self.current_client!="":
            filename=tk.filedialog.asksaveasfilename(title="Export Current File as DOCX",
                                                     filetypes=(("DOCX","*.docx"),('All files', '*.*')))
            self.export(self.current_client.current_file,filename)

    # This outputs all of the check with clients WITHIN the file!
    def export_check_with_clients(self):
        if self.file_open():
            # Get all check with clients / red
            filename=tk.filedialog.asksaveasfilename(title="Export Check with Client",
                                                     filetypes=(("DOCX","*.docx"),('All files', '*.*')))
            if filename!="":
                reqs=[]
                resps=[]
                numbers=[]
                req_types=[]
                for file in self.current_client.files:
                    for r in file.reqs:#Get responses and requests
                        if r.color=="#FF0000":
                            #1. ADD REQUESTS
                            reqs.append(r.req)
                            #2. ADD RESPONSES
                            full_text = r.get_full_resp()
                            resps.append(full_text)
                            #3. ADD NUMBER POINTERS
                            numbers.append(r.custom_key)
                            #4. ADD REQUEST TYPE
                            req_types.append(r.req_type)
                if len(reqs)>0:
                    cnv.updateDOC(reqs,resps,file.details,self.current_client.firm_details,req_types,str(filename),numbers)
                    if self.CONFIG["general"]["open_export"]:
                        os.system("start "+str(filename)+".docx")

    ### SETTING AND GETTING OBJECTS
    ########################################################################################################

    def set_client_unsaved(self,client):
        if client.saved==False:
            return
        client.saved = False
        self.requests_frame.update_clients(self.clients)



    # Add a new file to recents and save!
    def set_recents(self,new):
        if new in self.RECENTS:
            #Swap with the first one
            index = self.RECENTS.index(new)
            temp=self.RECENTS[0]
            self.RECENTS[0]=new
            self.RECENTS[index]=temp
        else:
            #Add to front and push
            self.RECENTS.insert(0,new)
            if len(self.RECENTS)>10:
                self.RECENTS.pop(-1)
        # Update recents file
        set_recents(self.RECENTS)
        # Update menu
        self.bar_frame.update_recents(self.RECENTS)
        # Update landing frame
        self.landing_frame.update_recents(self.RECENTS)



    # Move a file to a different client using drag and drop
    def move_file(self,file,client_name):
        if get_name(self.current_client.name,22)==client_name:
            return
        for i in self.clients:
            if get_name(i.name,22) == client_name:
                #Do the moving here
                #Add to client
                i.files.append(file)
                if i.current_file=="":#If no current file then set this
                    i.current_file=i.files[0]
                #Remove from current 
                self.close_file()
                #Close current req
                return


    #Box to add a new client!
    def new_client(self):
        dialog = tk.CTkInputDialog(text="Enter new client name:", title="New Client")
        text = dialog.get_input()  # waits for input
        if self.client_already_open(text):
            return
        if text!=None and text!="":
            #Check if text in clients if it is then return
            for client in self.clients:
                if client.name==get_name(text,22):
                    return
            self.close_landing_frame()
            self.clients.append(Client(text,[],self))
            self.set_client(self.clients[-1])



    #Change an objection buttons state, and if request then update this
    def toggle_objection(self,obj,undo_command=False):
        if self.current_req!=0:
            # Update current request objection
            for o in self.current_req.opts:
                if o.key == obj:
                    o.toggle()
                    self.current_req.current_objection = o
                    #Set the objection input area to this objection
                    self.objections_frame.update_current(o)
                    #UNDO functionality
                    if not undo_command:
                        self.add_action_to_stack(ActionToggleObjection(self,
                                                                       self.current_client,
                                                                       o.key))

            # Update buttons
            self.objections_frame.toggle_button(obj)#TOGGLE THE COLOUR OF THIS BUTTON!
            # Update objection special menu

    #Change the currently selected objection
    def toggle_selected_objection(self,obj,event):
        if self.current_req!=0:
            for o in self.current_req.opts:
                if o.key == obj:
                    self.current_req.current_objection = o
                    self.objections_frame.update_current(o)

                    #Set the objection input area to this objection


    #Allow for custom response when 'Custom' selected RFP
    def setRFP(self,value):
        if value=="Custom":
            self.response_frame.current_frame.response_text.configure(state="normal")
            self.response_frame.current_frame.response_text.delete("0.0","end")

    #Allow for custom response when 'Custom' selected RFA
    def setRFA(self,value):
        if value=="Custom":
            self.response_frame.current_frame.response_text.configure(state="normal")
            self.response_frame.current_frame.response_text.delete("0.0","end")


    #UPDATE THIS FOR NEW METHOD!
    #Set objections on sumbit using the current request opts
    def set_auto_objections(self):
        for i in self.current_req.opts:
            if i.key in self.objections:#If in the auto objections
                vals=i.param.split(",")
                for v in vals:
                    if v.strip() not in self.objections[i.key][4] and len(v)>1:
                        self.objections[i.key][4].append(v.strip())#Add new autos to the dict
        save_objections(self.objections)#Save the file!

    # Set type of request and save previous also
    def set_type(self,req_type):
        if self.prev_type=="":
            self.prev_type = req_type
        else:
            self.prev_type = self.req_type
        self.req_type = req_type 

    # Set the current client
    def set_client(self,client):
        self.bar_frame.reset_autosave_time()
        self.close_details()
        self.current_client = client
        self.requests_frame.show_clients(self.clients)
        if self.current_client.current_file!="":
            self.set_type(self.current_client.current_file.req_type)
            self.reqs = self.current_client.current_file.reqs

            self.requests_frame.show_files(self.current_client.files)
            self.requests_frame.show_list(self.current_client.current_file.reqs)
            self.set_request(self.current_client.current_file.current_req)
            self.requests_frame.scroll_to(True)
            self.title("myDiscoveryResponses   |   "+str(self.current_client.current_file.name.split("/")[-1]))
        else:
            #RESET THE REQUESTS HERE
            # Reset Files
            self.requests_frame.show_files([])
            # Reset Requests
            self.requests_frame.show_list([])
            # Reset Response
            self.response_frame.reset()
            #Reset Objections
            self.objections_frame.reset()

            self.reqs=[]
            self.current_req=0




    # Set the current file
    def set_file(self,file):
        #NEED TO CHANGE THINGS HERE TOO!!!
        self.current_client.current_file = file
        self.reqs = file.reqs
        #Close the details menu
        self.close_details()
        # Set is built for a single request type, need to change for files
        self.set_type(file.req_type)# Set first so refresher doesn't overwrite
        self.requests_frame.update_files(self.current_client.files)
        self.requests_frame.show_list(self.current_client.current_file.reqs)
        self.set_request(file.current_req)
        self.requests_frame.scroll_to(True)
        self.title("myDiscoveryResponses   |   "+str(file.name.split("/")[-1]))

    # Save request and open a different one
    def set_request(self,req):
        #Close details menu
        self.close_details()
        # 1. SAVING PREVIOUS RESPONSE
        if self.current_req!=0:
            # Saving
            self.current_req.resp = self.response_frame.get_response()
            #GET RFP data
            if self.prev_type=="RFP":
                self.current_req.RFP_option=self.response_frame.get_RFP()
                self.current_req.RFP_text=self.response_frame.get_RFP_text()
            elif self.prev_type=="RFA":
                self.current_req.RFA_option=self.response_frame.get_RFA()
                self.current_req.RFA_text=self.response_frame.get_RFA_text()
            #COLOR#########################################
            grey=False
            if self.current_req.resp.replace("\n","")!="" and self.req_type!="RFP":
                grey=True
            elif (self.current_req.RFP_option!="Available" or len(self.current_req.RFP_text)>0):
                grey=True

            if self.current_req.color!="#FF0000" and self.current_req.color!="#50C878":
                if grey:
                    self.current_req.color="grey" 
                else:
                    self.current_req.color=("black","white")
            ################################################
            
        # 2. ENTERING NEW RESPONSE INTO FRAME
        self.response_frame.redraw(req.req_type)
        #If set to itself then return
        if self.current_req==req:
            return
        #SET THE NEW REQ
        self.current_req=req
        self.current_client.current_file.current_req=req# Set the current req of the file

        #UPDATING THE RESPONSE FRAME
        #Set the request textbox
        self.response_frame.set_request(req.req)
        #Set the response number label
        if req.custom_key!="":
            text = req.custom_key
        else:
            text = req.no+1
        self.response_frame.request_label.configure(text=self.req_type+" NO. "+str(text)+":")
        #Set the response textbox
        self.response_frame.set_response(req.resp)
        #RFP & RFA Options and labels
        if self.req_type=="RFP":
            self.response_frame.set_RFP(req.RFP_option)
            self.response_frame.set_RFP_text(req.RFP_text)
        elif self.req_type=="RFA":
            self.response_frame.set_RFA(req.RFA_option)
            self.response_frame.set_RFA_text(req.RFA_text)

        #Set the request type to itself
        self.set_type(self.req_type)    

        #Update Objections List
        self.objections_frame.redraw(req)
        #Redraw the request buttons
        self.requests_frame.update_list(self.reqs)
        #Update the objection special input
        self.objections_frame.update_current(self.current_req.current_objection)

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
        with open(os.path.join(os.path.dirname(__file__),"config/config.json"), "w") as outfile:
            json.dump(self.CONFIG, outfile)
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

    #Open and update the config
    def set_config(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__),"config/config.json")):
            with open(os.path.join(os.path.dirname(__file__),'config/config.json'), 'r') as file:
                self.CONFIG = json.load(file)


    def add_ignore_word(self,word):
        self.CONFIG["spelling"]["ignore"] = self.CONFIG["spelling"]["ignore"]+","+word
        #Save the new config JSON
        with open(os.path.join(os.path.dirname(__file__),"config/config.json"), "w") as outfile:
            json.dump(self.CONFIG, outfile)

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

    def add_blank_frog(self):
        if self.current_client!="":
            self.close_landing_frame()

            reqs,req_type,doc_details,custom_keys = cnv.getRequests("BLANK FROG")
            self.set_type(req_type)# Sets the current type
            self.reqs=[]
            #Redraw for production
            self.response_frame.redraw(self.req_type)
            c=0
            for i in FROGS:
                if i in reqs and "(" not in i:
                    new = Request(FROGS[i],"",c,self,req_type,i)
                    self.reqs.append(new)
                c+=1

            ### ADD NEW FILE TO CLIENT, IF NONE THEN CREATE NEW CLIENT!
            new_file = File("FROGFROG",doc_details,self.req_type,self.reqs,self)
            if self.current_client!="":
                self.current_client.files.append(new_file)

            self.title("myDiscoveryResponses   |   "+str("FROG"))
            self.open_file("FROG")
            #Else if a obj
            self.current_client.current_file =self.current_client.files[-1]
            # Add file
            self.requests_frame.show_clients(self.clients)
            self.requests_frame.show_files(self.current_client.files)
            self.requests_frame.show_list(self.reqs)
            self.set_request(self.reqs[0])
            self.requests_frame.scroll_to(True)
            self.update()
    ### USER ACTIVITY
    ########################################################################################################

    # Set a request to submitted
    def submit(self):
        if self.current_req!=0:
            self.set_client_unsaved(self.current_client)
            #Update autos
            self.set_auto_objections()
            if self.current_req.color=="#50C878":
                self.current_req.color="grey"
            else:
                self.current_req.color="#50C878"
            self.requests_frame.update_list(self.reqs)
            
            prev_req=self.current_req
            #Go to next request
            index = self.reqs.index(self.current_req)
            if index<len(self.reqs)-1:
                self.set_request(self.reqs[index+1])
            else:
                self.set_request(self.current_req)

            #If an RFA request then update 17.1 response if needed
            
            if prev_req.RFA_option!="Admit" and self.CONFIG["general"]["auto_FROGS"]==1:#If ADMIT and ADD17.1 CHECKED
                #If not admit then add the 17.1 response
                #Find the 17.1
                self.current_client.add_special_response([prev_req.custom_key,prev_req.RFA_text])
                for file in self.current_client.files:
                    if file.req_type=="FROG":
                        for frog in file.reqs:
                            if frog.custom_key=="17.1":
                                #Add strings
                                frog.resp=""
                                for texts in self.current_client.special_responses:
                                    frog.resp+=(str(texts[1])+"\n")#Add new text to 17.1
            
            #Scroll to this request
            self.requests_frame.scroll_to()
            # If all are green set file green!
            for req in self.reqs:
                if req.color!="#50C878":
                    self.current_client.current_file.color="white"#SET FILE TO WHITE if still requests not done
                    self.requests_frame.update_files(self.current_client.files)
                    return
            self.current_client.current_file.color="#50C878"#Set file to green if all done!
            self.requests_frame.update_files(self.current_client.files)


    # Set as Check with client
    def check(self):
        if self.current_req!=0:
            if self.current_req.color=="#FF0000":
                self.current_req.color="grey"#set grey
            else:
                self.current_req.color="#FF0000"# Set red
            self.requests_frame.update_list(self.reqs)# Update request colours
            self.current_client.current_file.color=("black","white")
            self.requests_frame.update_files(self.current_client.files)# Turn file white if green
            #Go to next request
            index = self.reqs.index(self.current_req)
            if index<len(self.reqs)-1:
                self.set_request(self.reqs[index+1])
            #Scroll to this
            self.requests_frame.scroll_to()


    # Copy objections from the previous request
    def copy_previous(self):
        #Copy the previous opts list, use copy maybe
        for i in range(len(self.reqs)):
            if self.reqs[i]==self.current_req:
                if i>=1:
                    # Copy the previous objections
                    for o in range(len(self.reqs[i-1].opts)):
                        #Copy selected
                        self.current_req.opts[o].selected = self.reqs[i-1].opts[o].selected
                        #Copy param
                        self.current_req.opts[o].param = self.reqs[i-1].opts[o].param
                        self.current_req.opts[o].additional_param = self.reqs[i-1].opts[o].additional_param
                        #Set these in the GUI
                        self.objections_frame.redraw(self.current_req)
                else:
                    return

    # Clear a full request
    def clear(self):
        if self.current_req!=0:
            #Reset Color
            self.current_req.color=("black","white")
            self.current_client.current_file.color=("black","white")
            self.requests_frame.update_files(self.current_client.files)
            #Reset Response
            self.current_req.resp=""
            #Reset Checkboxes & Params
            for i in self.current_req.opts:
                i.selected=0
                i.param=""
            #Reset boxes
            self.response_frame.set_response("")
            self.objections_frame.redraw(self.current_req)
            self.requests_frame.update_list(self.reqs)
            #Reset RFP
            if self.req_type=="RFP":
                self.response_frame.set_RFP("Available")
                self.response_frame.set_RFP_text("")
            elif self.req_type=="RFA":
                self.response_frame.set_RFA("Admit")
            self.update()










# WINDOW SPECIFIC FUNTIONS (cannot be elsewhere)
############################################################################################################

# Create a new window with root as parent
def create_window(root,from_file="file which will not exist on anybody's file path"):
    if os.path.exists(from_file.replace("\\","/")):
        App(root).load(from_file.replace("\\","/"))#Create a window with the selected client open
    else:
        App(root)

# MAIN LOOP
############################################################################################################

#ROOT UTILITY FUNCTION
def check_windows_open():
    c=0
    for w in root.winfo_children():
        c+=1
    if c==0:#Destroy root if no windows left open
        print("ROOT CLOSED AS NO WINDOWS DETECTED")
        root.destroy()
    root.after(10000,check_windows_open)



if __name__ == "__main__":
    #APPLICATION UTILITY SETUP
    splash_screen.destroy()
    root=tk.CTk()
    root.iconbitmap(os.path.join(os.path.dirname(__file__),"assets/icon.ico"))
    root.withdraw()
    ##CHECK if file has been opened from a saved client
    print(sys.argv)
    if len(sys.argv)>1:
        create_window(root,sys.argv[-1])
    else:
        create_window(root)
    root.after(10000,check_windows_open)
    root.mainloop()




# CHANGES
############################################################################################################

#DONE:
#Added undo and redo objections
#Added hotkeys


#CURRENT PLAN:
#THIS BRANCH IS ADDING THE UNDO BUTTON!!!!
#each text box keeps it's own undo. Keep action stack

#Create a list of 'actions' that I can go back through and undo
#Possible actions:
#Clear
#Add/remove objection
#Select response option
#Submit
#Check with clients
#Delete file
#Change client, request, file
#Add text to text box (track which box then use that boxes undo)







