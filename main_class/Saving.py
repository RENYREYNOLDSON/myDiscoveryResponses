# Main Imports
from main_class.__modules__ import *

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

class Saving:
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
            #Add this file to undo queue
            self.add_action_to_stack(ActionReadFile(master=self,obj=new_file))
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
                self.delete_file()

    #Actually remove the file
    def delete_file(self,undo_command=False):
        index = self.current_client.files.index(self.current_client.current_file)
        if not undo_command:
            self.add_action_to_stack(ActionDeleteFile(master=self,obj=index))
        #Get the index of the current file
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

    #Bring a file back using undo/redo
    def revive_file(self,file,index):
        self.current_client.files.insert(index,file)
        #May need to set to the original index?
        #Else if a obj
        self.current_client.current_file =self.current_client.files[-1]
        # Add file
        self.requests_frame.show_clients(self.clients)
        self.requests_frame.show_files(self.current_client.files)
        self.requests_frame.show_list(self.reqs)
        self.set_request(file.current_req)
        self.requests_frame.scroll_to(True)

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
        # Reset Undo and Redo stacks
        self.reset_undo_stacks()
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