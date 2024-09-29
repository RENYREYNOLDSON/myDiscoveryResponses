# Main Imports
import openai

from main_class.__modules__ import *

FROGS = {
    "1.1": "State the name, ADDRESS, telephone number, and relationship to you of each PERSON who prepared or assisted in the preparation of the responses to these interrogatories. (Do not identify anyone who simply typed or reproduced the responses.)",
    "2.1": "State:\n(a) your name;\n(b) every name you have used in the past; and\n(c) the dates you used each name.",
    "2.2": "State the date and place of your birth.",
    "2.3": " At the time of the INCIDENT, did you have a driver's license? If so state: \n(a) the state or other issuing entity; \n(b) the license number and type; \n(c) the date of issuance; and \n(d) all restrictions.",
    "2.4": "At the time of the INCIDENT, did you have any other permit or license for the operation of a motor vehicle? If so, state:\n(a) the state or other issuing entity; \n(b) the license number and type; \n(c) the date of issuance; and \n(d) all restrictions.",
    "2.5": "State:\n(a) your present residence ADDRESS;\n(b) your residence ADDRESSES for the past five years; and\n(c) the dates you lived at each ADDRESS.",
    "2.6": "State:\n(a) the name, ADDRESS, and telephone number of your present employer or place of self-employment; and\n(b) the name, ADDRESS, dates of employment, job title, and nature of work for each employer, or self-employment you have had from five years before the INCIDENT until today.",
    "2.7": "State:\n(a) the name and ADDRESS of each school or other academic or vocational institution you have attended, beginning with high school;\n(b) the dates you attended;\n(c) the highest-grade level you have completed; and\n(d) the degrees received.",
    "2.8": "Have you ever been convicted of a felony? If so, for each conviction state:\n(a) the city and state where you were convicted;\n(b) the date of conviction;\n(c) the offense; and\n(d) the court and case number.",
    "2.9": "Can you speak English with ease?  If not, what language and dialect do you normally use?",
    "2.10": "Can you read and write English with ease?  If not, what language and dialect do you normally use?",
    "2.11": "At the time of the INCIDENT were you acting as an agent or employee for any PERSON? If so, state:\n(a) the name, ADDRESS, and telephone number of that PERSON; and\n(b) a description of your duties.",
    "2.12": "At the time of the INCIDENT did you or any other person have any physical, emotional, or mental disability or condition that may have contributed to the occurrence of the INCIDENT? If so, for each person state: \n(a) the name, ADDRESS, and telephone number;\n(b) the nature of the disability or condition; and\n(c) the manner in which the disability or condition contributed to the occurrence of the INCIDENT.",
    "2.13": "Within 24 hours before the INCIDENT did you or any person involved in the INCIDENT use or take any of the following substances: alcoholic beverage, marijuana, or other drug or medication of any kind (prescription or not)? If so, for each person state:\n(a) the name, ADDRESS, and telephone number;\n(b) the nature or description of each substance;\n(c) the quantity of each substance used or taken;\n(d) the date and time of day when each substance was used or taken;\n(e) the ADDRESS where each substance was used or taken;\n(f) the name, ADDRESS, and telephone number of each person who was present when each substance was used or taken; and\n(g) the name, ADDRESS, and telephone number of any HEALTH CARE PROVIDER who prescribed or furnished the substance and the condition for which it was prescribed or furnished.",
    "3.1": "Are you a corporation? If so, state:\n(a) the name stated in the current articles of incorporation;\n(b) all other names used by the corporation during the past 10 years and the dates each was used;\n(c) the date and place of incorporation; named insured;\n(d) the ADDRESS of the principal place of business; and \n(e) whether you are qualified to do business in California.",
    "3.2": "",
    "3.3": "",
    "3.4": "",
    "3.5": "",
    "3.6": "",
    "3.7": "",
    "4.1": "At the time of the INCIDENT, was there in effect any policy of insurance through which you were or might be insured in any manner (for example, primary, pro-rata, or excess liability coverage or medical expense coverage) for the damages, claims, or actions that have arisen out of the INCIDENT? If so, for each policy state: \n(a) the kind of coverage;\n(b) the name and ADDRESS of the insurance company;\n(c) the name, ADDRESS, and telephone number of each named insured;\n(d) the policy number;\n(e) the limits of coverage for each type of coverage contained in the policy;\n(f) whether any reservation of rights or controversy or coverage dispute exists between you and the insurance company; and\n(g) the name, ADDRESS, and telephone number of the custodian of the policy.",
    "4.2": "Are you self-insured under any statute for the damages, claims, or actions, that have arisen out of the INCIDENT? If so, specific the statute.",
    "6.1": "Do you attribute any physical, mental, or emotional injuries to the INCIDENT? (If your answer is \"no,\" do not answer interrogatories 6.2 through 6.7).",
    "6.2": "Identify each injury you attribute to the INCIDENT and the area of your body affected.",
    "6.3": "Do you still have any complaints that you attribute to the INCIDENT? If so, for each complaint state:\n(a) a description;  \n(b) whether the complaint is subsiding, remaining the same, or becoming worse; and\n(c) the frequency and duration.",
    "6.4": "Did you receive any consultation or examination (except from expert witnesses covered by Code of Civil Procedure sections 2034.210-2034.310) or treatment from a HEALTH CARE PROVIDER for any injury you attribute to the INCIDENT? If so, for each HEALTH CARE PROVIDER state:\n(a) the name, ADDRESS, and telephone number;\n(b) the type of consultation, examination, or treatment provided;\n(c) the dates you received consultation, examination, or treatment; and\n(d) the charges to date.",
    "6.5": "Have you taken any medication, prescribed or not, as a result of injuries that you attribute to the INCIDENT? If so, for each medication state:\n(a) the name;\n(b) the PERSON who prescribed or furnished it;\n(c) the date it was prescribed or furnished;\n(d) the dates you began and stopped taking it; and\n(e) the cost to date.",
    "6.6": "Are there any other medical services necessitated by the injuries that you attribute to the INCIDENT that were not previously listed (for example, ambulance, nursing, prosthetics)?  If so, for each service state:\n(a) the nature;\n(b) the date;\n(c) the cost; and\n(d) the name, ADDRESS, and telephone number of each provider.",
    "6.7": "Has any HEALTH CARE PROVIDER advised that you may require future or additional treatment for any injuries that you attribute to the INCIDENT? If so, for each injury state:\n(a) the name and ADDRESS of each HEALTH CARE PROVIDER;\n(b) the complaints for which the treatment was advised; and\n(c) the nature, duration, and estimated cost of the treatment.",
    "7.1": "Do you attribute any loss of or damage to a vehicle or other property to the INCIDENT? If so, for each item of property:\n(a) describe the property;\n(b) describe the nature and location of the damage to the property;\n(c) state the amount of damage you are claiming for each item of property and how the amount was calculated; and\n(d) if the property was sold, state the name, ADDRESS, and telephone number of the seller, the date of sale, and the sale price.",
    "7.2": "Has a written estimate or evaluation been made for any item of property referred to in your answer to the preceding interrogatory? If so, for each estimate or evaluation state:\n(a) the name, ADDRESS, and telephone number of the PERSON who prepared it and the date prepared;\n(b) the name, ADDRESS, and telephone number of each PERSON who has a copy of it; and\n(c) the amount of damage stated.",
    "7.3": "Has any item of property referred to in your answer to interrogatory 7.1 been repaired? If so, for each item state:\n(a) the date repaired;\n(b) a description of the repair;\n(c) the repair cost;\n(d) the name, ADDRESS, and telephone number of the PERSON who repaired it;\n(e) the name, ADDRESS, and telephone number of the PERSON who paid for the repair.",
    "8.1": "Do you attribute any loss of income or earning capacity to the INCIDENT? (If your answer is \"no,\" do not answer interrogatories 8.2 through 8.8).",
    "8.2": "State:\n(a) the nature of your work;\n(b) your job title at the time of the INCIDENT; and\n(c) the date your employment began.",
    "8.3": "State the last date before the INCIDENT that you worked for compensation.",
    "8.4": "State your monthly income at the time of the INCIDENT and how the amount was calculated.",
    "8.5": "State the date you returned to work at each place of employment following the INCIDENT.",
    "8.6": "State the dates you did not work and for which you lost income as a result of the INCIDENT.",
    "8.7": "State the total income you have lost to date as a result of the INCIDENT and how the amount was calculated.",
    "8.8": "Will you lose income in the future as a result of the INCIDENT? If so, state:\n(a) the facts upon which you base this contention;\n(b) an estimate of the amount;\n(c) an estimate of how long you will be unable to work; and\n(d) how the claim for future income is calculated.",
    "9.1": "Are there any other damages that you attribute to the INCIDENT? If so, for each item of damage state:\n(a) the nature;\n(b) the date it occurred;\n(c) the amount; and\n(d) the name, ADDRESS, and telephone number of each PERSON to whom an obligation was incurred.",
    "9.2": "Do any DOCUMENTS support the existence or amount of any item of damages claimed in interrogatory 9.1?  If so, describe each document and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT.",
    "10.1": "At any time before the INCIDENT did you have complaints or injuries that involved the same part of your body claimed to have been injured in the INCIDENT?  If so, for each state:\n(a) a description of the complaint or injury;\n(b) the dates it began and ended; and,\n(c) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER whom you consulted or who examined or treated you.",
    "10.2": "List all physical, mental, and emotional disabilities you had immediately before the INCIDENT. (You may omit mental or emotional disabilities unless you attribute any mental or emotional injury to the INCIDENT.)",
    "10.3": "At any time after the INCIDENT, did you sustain injuries of the kind for which you are now claiming damages? If so, for each incident giving rise to an injury state:\n(a) the date and the place it occurred;\n(b) the name, ADDRESS, and telephone number of any other PERSON involved;\n(c) the nature of any injuries you sustained;\n(d) the name, ADDRESS, and telephone number of each HEALTH CARE PROVIDER who you consulted or who examined or treated you; and\n(e) the nature of the treatment and its duration.",
    "11.1": "Except for this action, in the past 10 years have you filed an action or made a written claim or demand for compensation for your personal injuries? If so, for each action, claim, or demand state:\n(a) the date, time, and place and location (closest street ADDRESS or intersection) of the INCIDENT giving rise to the action, claim, or demand;\n(b) the name, ADDRESS, and telephone number of each PERSON against whom the claim or demand was made or the action filed;\n(c) the court, names of the parties, and case number of any action filed;\n(d) the name, ADDRESS, and telephone number of any attorney representing you;\n(e) whether the claim or action has been resolved or is pending; and\n(f) a description of the injury.",
    "11.2": "In the past 10 years have you made a written claim or demand for workers' compensation benefits? If so, for each claim or demand state:\n(a) the date, time, and place of the INCIDENT giving rise to the claim;\n(b) the name, ADDRESS, and telephone number of your employer at the time of the injury;\n(c) the name, ADDRESS, and telephone number of the workers' compensation insurer and the claim number;\n(d) the period of time during which you received workers' compensation benefits;\n(e) a description of the injury;\n(f) the name, ADDRESS, and telephone number of any HEALTH CARE PROVIDER who provided services; and\n(g) the case number at the Workers' Compensation Appeals Board.",
    "12.1": "State the name, ADDRESS, and telephone number of each individual:\n(a) who witnessed the INCIDENT or the events occurring immediately before or after the INCIDENT;\n(b) who made any statement at the scene of the INCIDENT;\n(c) who heard any statements made about the INCIDENT by any individual at the scene; and\n(d) who YOU OR ANYONE ACTING ON YOUR BEHALF claim has knowledge of the INCIDENT (except for expert witnesses covered by Code of Civil Procedure section 2034).",
    "12.2": "Have YOU OR ANYONE ACTING ON YOUR BEHALF interviewed any individual concerning the INCIDENT? If so, for each individual state: \n(a) the name, ADDRESS, and telephone number of the individual interviewed;\n(b) the date of the interview; and\n(c) the name, ADDRESS, and telephone number of the PERSON who conducted the interview.",
    "12.3": "Have YOU OR ANYONE ACTING ON YOUR BEHALF obtained a written or recorded statement from any individual concerning the INCIDENT? If so, for each statement state:\n(a) the name, ADDRESS, and telephone number of the individual from whom the statement was obtained;\n(b) the name, ADDRESS, and telephone number of the individual who obtained the statement;\n(c) the date the statement was obtained; and\n(d) the name, ADDRESS, and telephone number of each PERSON who has the original statement or a copy.",
    "12.4": "Do YOU OR ANYONE ACTING ON YOUR BEHALF know of any photographs, films, or videotapes depicting any place, object, or individual concerning the INCIDENT or plaintiffs’ injuries? If so, state:\n(a) the number of photographs or feet of film or videotape;\n(b) the places, objects, or persons photographed, filmed, or videotaped;\n(c) the date the photographs, films, or videotapes were taken;\n(d) the name, ADDRESS, and telephone number of the individual taking the photographs, films, or videotapes; and\n(e) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of the photographs, films, or videotapes.",
    "12.5": "Do YOU OR ANYONE ACTING ON YOUR BEHALF know of any diagram, reproduction, or model of any place or thing (except for items developed by expert witnesses covered by Code of Civil Procedure sections 2034.2102034.310) concerning the INCIDENT? If so, for each item state:\n(a) the type (i.e., diagram, reproduction, or model);\n(b) the subject matter; and\n(c) the name, ADDRESS, and telephone number of each PERSON who has it.",
    "12.6": "Was a report made by any PERSON concerning the INCIDENT? If so, state:\n(a) the name, title, identification number, and employer of the PERSON who made the report;\n(b) the date and type of report made;\n(c) the name, ADDRESS, and telephone number of the PERSON for whom the report was made; and\n(d) the name, ADDRESS, and telephone number of each PERSON who has the original or a copy of the report.",
    "12.7": "Have YOU OR ANYONE ACTING ON YOUR BEHALF inspected the scene of the INCIDENT? If so, for each inspection state:\n(a) the name, ADDRESS, and telephone number of the individual making the inspection (except for expert witnesses covered by Code of Civil Procedure sections 2034.210-2034.310); and\n(b) the date of the inspection.",
    "13.1": "Have YOU OR ANYONE ACTING ON YOUR BEHALF conducted surveillance of any individual involved in the INCIDENT or any party to this action? If so, for each surveillance state: \n(a) The name, ADDRESS, and telephone number of the individual or party; \n(b) The time, date, and place of the surveillance; \n(c) The name, ADDRESS, and telephone number of the individual who conducted the surveillance; and \n(d) The name, ADDRESS, and telephone number of each PERSON who has the original or a copy of any surveillance photograph, film, or videotape. ",
    "13.2": "Has a written report prepared on the surveillance? If so, for each written report state: \n(a) The title;\n(b) The date; \n(c) The name, ADDRESS, and telephone number of the individual who prepared the report; and \n(d) The name, ADDRESS, and telephone number of each PERSON who has the original or a copy. ",
    "14.1": "Do YOU OR ANYONE ACTING ON YOUR BEHALF contend that any PERSON involved in the INCIDENT violated any statute, ordinance, or regulation and that the violation was a legal (proximate) cause of the INCIDENT? If so, identify the name, ADDRESS, and telephone number of each PERSON and the statute, ordinance, or regulation that was violated.",
    "14.2": "Was any PERSON cited or charged with a violation of any statute, ordinance, or regulation as a result of this INCIDENT? If so, for each PERSON state:\n(a) the name, ADDRESS, and telephone number of the PERSON;\n(b) the statute, ordinance, or regulation allegedly violated;\n(c) whether the PERSON entered a plea in response to the citation or charge and, if so, the plea entered; and\n(d) the name and ADDRESS of the court or administrative agency, names of the parties, and case number.",
    "17.1": "Is your response to each request for admission served with these interrogatories an unqualified admission? If not, for each response that is not an unqualified admission: \n(a) State the number of the request; \n(b) State all facts upon which you base your response;\n(c) State the names, ADDRESSES, and telephone numbers of all PERSONS who have knowledge of these facts; and \n(d) Identify all DOCUMENTS and other tangible things that support your response and state the name, ADDRESS, and telephone number of the PERSON who has each DOCUMENT or thing.",
    "20.1": "State the date, time, and place of the INCIDENT (closest street ADDRESS or intersection).",
    "20.2": "For each vehicle involved in the INCIDENT, state: \n(a) the year, make, model, and license number;\n(b) the name, ADDRESS, and telephone number of the driver;\n(c) the name, ADDRESS, and telephone number of each occupant other than the driver;\n(d) the name, ADDRESS, and telephone number of each registered owner;\n(e) the name, ADDRESS, and telephone number of each lessee;\n(f) the name, ADDRESS, and telephone number of each owner other than the registered owner or lien holder; and\n(g) the name of each owner who gave permission or consent to the driver to operate the vehicle.",
    "20.3": "State the ADDRESS and location where your trip began and the ADDRESS and location of your destination.",
    "20.4": "Describe the route that you followed from the beginning of your trip to the location of the INCIDENT, and state the location of each stop, other than routine traffic stops, during the trip leading up to the INCIDENT.",
    "20.5": "State the name of the street or roadway, the lane of travel, and the direction of travel of each vehicle involved in the INCIDENT for the 500 feet of travel before the INCIDENT.",
    "20.6": "Did the INCIDENT occur at an intersection? If so, describe all traffic control devices, signals, or signs at the intersection.",
    "20.7": "Was there a traffic signal facing you at the time of the INCIDENT? If so, state:\n(a) your location when you first saw it;\n(b) the color;\n(c) the number of seconds it had been that color; and\n(d) whether the color changed between the time you first saw it and the INCIDENT.",
    "20.8": "State how the INCIDENT occurred, giving the speed, direction, and location of each vehicle involved:\n(a) just before the INCIDENT;\n(b) at the time of the INCIDENT; and\n(c) just after the INCIDENT.",
    "20.9": "Do you have information that a malfunction or defect in a vehicle caused the INCIDENT? If so:\n(a) identify the vehicle;\n(b) identify each malfunction or defect;\n(c) state the name, ADDRESS, and telephone number of each PERSON who is a witness to or has information about each malfunction or defect; and\n(d) state the name, ADDRESS, and telephone number of each PERSON who has custody of each defective part.",
    "20.10": "Do you have information that any malfunction or defect in a vehicle contributed to the injuries sustained in the INCIDENT? If so:\n(a) identify the vehicle;\n(b) identify each malfunction or defect;\n(c) state the name, ADDRESS, and telephone number of each PERSON who is a witness to or has information about each malfunction or defect; and\n(d) state the name, ADDRESS, and telephone number of each PERSON who has custody of each defective part.",
    "20.11": "State the name, ADDRESS, and telephone number of each owner and each PERSON who has had possession since the INCIDENT of each vehicle involved in the INCIDENT."
    }

RFP_responses = {
    "Available": "Responding Party will comply with this demand. Please see “[VAR]” produced concurrently herewith.",
    "Not Exist": "After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents are known to exist.",
    "Not Possessed": "After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, because no such documents have ever been in the possession, custody, or control of Responding Party.",
    "Lost": "After a diligent search and reasonable inquiry, Responding Party finds no responsive documents in their possession, custody, or control, any such documents have been destroyed, lost, misplaced or stolen."}

RFA_responses = {"Admit": "Admit. ",
                 "Deny": "Deny. ",
                 "Lack Info": "A reasonable inquiry concerning the matter in this particular request has been made, and the information known or readily obtainable is insufficient to enable Responding Party to admit the matter."}

RFP_EXTRA = " Any responsive documents are believed to be in the possession, custody, or control of [VAR]."


class Requests:

    ### SETTING AND GETTING OBJECTS
    ########################################################################################################

    def set_client_unsaved(self, client):
        if client.saved == False:
            return
        client.saved = False
        self.requests_frame.update_clients(self.clients)

    # Add a new file to recents and save!
    def set_recents(self, new):
        if new in self.RECENTS:
            # Swap with the first one
            index = self.RECENTS.index(new)
            temp = self.RECENTS[0]
            self.RECENTS[0] = new
            self.RECENTS[index] = temp
        else:
            # Add to front and push
            self.RECENTS.insert(0, new)
            if len(self.RECENTS) > 10:
                self.RECENTS.pop(-1)
        # Update recents file
        set_recents(self.RECENTS)
        # Update menu
        self.bar_frame.update_recents(self.RECENTS)
        # Update landing frame
        self.landing_frame.update_recents(self.RECENTS)

    # Move a file to a different client using drag and drop
    def move_file(self, file, client_name):
        if get_name(self.current_client.name, 22) == client_name:
            return
        for i in self.clients:
            if get_name(i.name, 22) == client_name:
                # Do the moving here
                # Add to client
                i.files.append(file)
                if i.current_file == "":  # If no current file then set this
                    i.current_file = i.files[0]
                # Remove from current
                self.close_file()
                # Close current req
                return

    # Box to add a new client!
    def new_client(self):
        dialog = tk.CTkInputDialog(text="Enter new client name:", title="New Client")
        text = dialog.get_input()  # waits for input
        if self.client_already_open(text):
            return
        if text != None and text != "":
            # Check if text in clients if it is then return
            for client in self.clients:
                if client.name == get_name(text, 22):
                    return
            self.close_landing_frame()
            self.clients.append(Client(text, [], self))
            self.set_client(self.clients[-1])

    # Change an objection buttons state, and if request then update this
    def toggle_objection(self, obj, undo_command=False):
        if self.current_req != 0:
            # Update current request objection
            for o in self.current_req.opts:
                if o.key == obj:
                    o.toggle()
                    self.current_req.current_objection = o
                    # Set the objection input area to this objection
                    self.objections_frame.update_current(o)
                    # UNDO functionality
                    if not undo_command:
                        self.add_action_to_stack(ActionToggleObjection(self, o.key))

            # Update buttons
            self.objections_frame.toggle_button(obj)  # TOGGLE THE COLOUR OF THIS BUTTON!
            # Update objection special menu
            self.update_objection_textbox()

    # Change the currently selected objection
    def toggle_selected_objection(self, obj, event):
        if self.current_req != 0:
            for o in self.current_req.opts:
                if o.key == obj:
                    self.current_req.current_objection = o
                    self.objections_frame.update_current(o)
                    # Set the objection input area to this objection

    # Allow for custom response when 'Custom' selected RFP
    def setRFP(self, value, undo_command=False):
        # Add an undo option here!
        if not undo_command:
            self.add_action_to_stack(ActionRFPEntry(master=self, obj=(
            self.response_frame.previous_option, value)))  # Pass current and new
        self.response_frame.set_previous_option(value)
        self.response_frame.set_textbox_state(value)
        self.response_frame.set_response("")
        self.update_response_textbox()

    # Allow for custom response when 'Custom' selected RFA
    def setRFA(self, value, undo_command=False):
        # Add an undo option here!
        if not undo_command:
            self.add_action_to_stack(
                ActionRFAEntry(master=self, obj=(self.response_frame.previous_option, value)))  # Pass current and new
        self.response_frame.set_previous_option(value)
        self.response_frame.set_textbox_state(value)
        self.response_frame.set_response("")
        self.update_response_textbox()

    # UPDATE THIS FOR NEW METHOD!
    # Set objections on sumbit using the current request opts
    def set_auto_objections(self):
        for i in self.current_req.opts:
            if i.key in self.objections:  # If in the auto objections
                vals = i.param.split(",")
                for v in vals:
                    if v.strip() not in self.objections[i.key][4] and len(v) > 1:
                        self.objections[i.key][4].append(v.strip())  # Add new autos to the dict
        save_objections(self.objections)  # Save the file!

    # Set type of request and save previous also
    def set_type(self, req_type):
        if self.prev_type == "":
            self.prev_type = req_type
        else:
            self.prev_type = self.req_type
        self.req_type = req_type

        # Set the current client

    # Triggers: Clicking a client, creating a client, undo action, loading a client
    def set_client(self, client, skip_set_request=False):
        # 1.Reset the autosave time
        self.bar_frame.reset_autosave_time()
        # 2. Close the file details window if needed
        self.close_details()
        # 3. Set the current client
        self.current_client = client
        # 4. Update the clients list
        self.requests_frame.show_clients(self.clients)
        # 5. If the client is not empty then set the file and request, otherwise blank
        if self.current_client.current_file != "":
            # 5.1. Set the file
            self.requests_frame.show_files(self.current_client.files)
            self.set_file(self.current_client.current_file)
        else:
            if self.current_req != 0:
                self.save_request()
            # Reset Files
            self.requests_frame.show_files([])
            # Reset Requests
            self.requests_frame.show_list([])
            # Reset Response
            self.response_frame.reset()
            # Reset Objections
            self.objections_frame.reset()

            self.reqs = []
            self.current_req = 0

    # Set the current file
    # Triggers: Clicking a file, undo, Loading a file/client
    def set_file(self, file, skip_set_request=False):
        # 1. Set the current file
        self.current_client.current_file = file
        # 2. Get the current requests
        self.reqs = file.reqs
        # 3. Close the details window if needed
        # self.close_details()

        # 5. Update the files list
        self.requests_frame.update_files(self.current_client.files)
        # 6. Show the requests list
        self.requests_frame.show_list(self.current_client.current_file.reqs, self.current_client.current_file.req_type)
        # 7. Set the current request
        self.set_request(file.current_req)
        # 8. Scroll to the current request
        self.requests_frame.scroll_to(True)
        # 9. Set the window title
        self.title("myDiscoveryResponses   |   " + str(file.name.split("/")[-1]))

    # Save request and open a different one
    # Triggers: Set client, set file, clicking on req, arrows, submit, check, undo,
    def set_request(self, req, save_current=True):
        # 1. Close the details window if needed
        self.close_details()
        # 2. Save current request
        if self.current_req != 0:
            if save_current:
                self.save_request()

        # 4. Set the request type
        self.set_type(req.req_type)

        # 3. Format response frame for new response type
        self.response_frame.redraw(req.req_type)

        # 5. Set the current request
        self.current_req = req
        # 6. Set the files current request
        self.current_client.current_file.current_req = req
        # 8. Set the request number label
        text = req.get_number()
        self.response_frame.request_label.configure(text=self.req_type + " NO. " + str(text) + ":")

        # Update the request
        self.update_request()

        return

    def update_request(self):
        # 7. Set the request in the textbox
        self.response_frame.set_request(self.current_req.req)

        # 9. Set the current response textbox
        self.response_frame.set_response(self.current_req.resp, remove_separator=True)

        # Set the current objection textbox
        self.response_frame.set_objection(self.current_req.custom_objection_text)

        # 10. Set RFP & RFA Options and labels
        if self.req_type == "RFP":
            self.response_frame.set_RFP(self.current_req.RFP_option)
            self.response_frame.set_textbox_state(self.current_req.RFP_option)
            self.response_frame.set_RFP_text(self.current_req.RFP_text)
        elif self.req_type == "RFA":
            self.response_frame.set_RFA(self.current_req.RFA_option)
            self.response_frame.set_textbox_state(self.current_req.RFA_option)
            self.response_frame.set_RFA_text(self.current_req.RFA_text)

        # 11. Set the objection textbox
        # self.update_objection_textbox()
        # 12. Set the response textbox
        self.update_response_textbox()
        # 14. Redraw the objections list
        self.objections_frame.redraw(self.current_req)
        # 15. Redraw the requests list
        self.requests_frame.update_list(self.reqs)
        # 16. Set the objection [VAR] inputs
        self.objections_frame.update_current(self.current_req.current_objection)
        # Done
        print("Updated")
        return

    # Save the current request
    # Triggers: submit, check, previews
    def save_request(self):
        # 2.1. Save current response
        self.current_req.resp = self.response_frame.get_response()

        # 2.2. Save current request
        self.current_req.req = self.response_frame.get_request()

        # 2.3 Save the current objection text
        self.current_req.custom_objection_text = self.response_frame.get_objection()

        # 2.3. Save the RFP and RFA options
        if self.req_type == "RFP":
            self.current_req.RFP_option = self.response_frame.get_RFP()
            self.current_req.RFP_text = self.response_frame.get_RFP_text()
        elif self.req_type == "RFA":
            self.current_req.RFA_option = self.response_frame.get_RFA()
            self.current_req.RFA_text = self.response_frame.get_RFA_text()

        # 2.4. Set the colour of the request
        grey = False
        if self.current_req.resp.replace("\n", "") != "" and self.req_type != "RFP":
            grey = True
        elif (self.current_req.RFP_option != "Available" or len(self.current_req.RFP_text) > 0):
            grey = True
        if self.current_req.color != "#FF0000" and self.current_req.color != "#50C878":
            if grey:
                self.current_req.color = "grey"
            else:
                self.current_req.color = ("black", "white")

        self.requests_frame.update_list(self.reqs)
        return

    # UPDATE OBJECTION TEXTBOX ON CHANGE
    # Triggers: Changing request, toggle obj, change objections, edit [VAR] text
    def update_objection_textbox(self, event=None):
        if self.current_req != 0:
            # 1. Set the current objection parameters from inputs
            if self.current_req.current_objection != "":
                self.current_req.current_objection.param = self.objections_frame.objection_input.get()
                self.current_req.current_objection.additional_param = self.objections_frame.additional_input.get()

            # 2. Set the custom text to the current box contents
            self.current_req.custom_objection_text = self.response_frame.get_objection()  # Get prev text from box

            # 3. Get the objection text - just from objections
            remove_end = False
            if not ((self.req_type != "RFP" and len(self.response_frame.get_response()) > 0) or (
                    self.req_type == "RFP" and len(self.response_frame.get_RFP()) > 0)):
                remove_end = True
            text = get_objection_text(self.current_req, self.objections,
                                      remove_end)  # Get objections with no end if text in response

            # 4. If new objections or params then set the objection textbox to this
            if text != self.previous_objection_text:  # If the text has changed REDRAW
                self.response_frame.set_objection(text)
                self.set_client_unsaved(self.current_client)

            self.previous_objection_text = text  # Save for next time

    # UPDATE RESPONSE TEXTBOX ON CHANGE
    # Triggers: Changing option, changing request, typing into RFP
    def update_response_textbox(self, event=None):
        if self.current_req != 0:
            # 1. Get current selected RFA/RFP option
            if self.req_type == "RFA":
                option = self.response_frame.get_RFA()
            else:
                option = self.response_frame.get_RFP()

            # 2. Set the response depending on current option chosen
            # RFP
            if self.req_type == "RFP" and option != "Custom":
                temp = self.response_frame.get_response()  # Get prev text from box
                resp = self.response_frame.get_RFP_text()
                text = RFP_responses[option].replace("[VAR]", resp)
                if option != "Available" and resp != "":
                    text = (text + RFP_EXTRA).replace("[VAR]", resp)
                if text != temp.replace("\n", ""):  # If the text has changed REDRAW
                    self.set_client_unsaved(self.current_client)
                    # Change response text
                    self.response_frame.set_response(text)
                    # Change color of request
                    self.current_req.color = "grey"
                    self.current_client.current_file.color = ("black", "white")
                    self.requests_frame.update_files(self.current_client.files)
            # RFA
            elif self.req_type == "RFA" and option != "Custom":
                resp = " " + self.response_frame.get_RFA_text()  # Current response text
                temp = self.response_frame.get_response()  # Get prev text from box
                text = RFA_responses[option]
                if text != temp.replace("\n", ""):  # If the text has changed REDRAW
                    self.set_client_unsaved(self.current_client)
                    # Change response text
                    self.response_frame.set_response(text)
                    # Change color of request
                    self.current_req.color = "grey"
                    self.current_client.current_file.color = ("black", "white")
                    self.requests_frame.update_files(self.current_client.files)
            # NORMAL
            else:  # If NOT RFP or RFA custom
                resp = self.response_frame.get_response()  # Current response text
                if resp[1:].replace("\n", "") != self.current_req.resp.replace("\n",
                                                                               ""):  # Change colour back if edited
                    self.current_req.color = "grey"
                    self.current_req.resp = resp[1:]
                    self.current_client.current_file.color = ("black", "white")
                    self.requests_frame.update_files(self.current_client.files)
                    self.set_client_unsaved(self.current_client)

    def add_blank_frog(self):
        if self.current_client != "":
            self.close_landing_frame()

            reqs, req_type, doc_details, custom_keys = cnv.getRequests("BLANK FROG")
            self.reqs = []
            c = 0
            for i in FROGS:
                if i in reqs and "(" not in i:
                    new = Request(FROGS[i], "", c, self, "FROG", i)
                    self.reqs.append(new)
                c += 1

            ### ADD NEW FILE TO CLIENT, IF NONE THEN CREATE NEW CLIENT!
            new_file = File("FROGFROG", doc_details, "FROG", self.reqs, self)
            self.current_client.files.append(new_file)
            self.requests_frame.show_files(self.current_client.files)
            self.set_file(new_file)

            # self.add_action_to_stack(ActionReadFile(master=self,obj=new_file))

    ### USER ACTIVITY
    ########################################################################################################

    # Set a request to submitted
    def submit(self, undo_command=False):
        if self.current_req != 0:
            if not undo_command:
                self.add_action_to_stack(ActionSubmit(self, "Submit"))
            self.set_client_unsaved(self.current_client)
            # Update autos
            self.set_auto_objections()
            if self.current_req.color == "#50C878":
                self.current_req.color = "grey"
            else:
                self.current_req.color = "#50C878"

            prev_req = self.current_req
            # Go to next request
            index = self.reqs.index(self.current_req)
            if index < len(self.reqs) - 1:
                self.set_request(self.reqs[index + 1])
            else:
                self.save_request()

            # If an RFA request then update 17.1 response if needed
            if prev_req.RFA_option != "Admit" and self.CONFIG["general"][
                "auto_FROGS"] == 1:  # If ADMIT and ADD17.1 CHECKED
                # If not admit then add the 17.1 response
                # Find the 17.1
                self.current_client.add_special_response([prev_req.custom_key, prev_req.RFA_text])
                for file in self.current_client.files:
                    if file.req_type == "FROG":
                        for frog in file.reqs:
                            if frog.custom_key == "17.1":
                                # Add strings
                                frog.resp = ""
                                for texts in self.current_client.special_responses:
                                    frog.resp += (str(texts[1]) + "\n")  # Add new text to 17.1

            # Scroll to this request
            if not undo_command:
                self.requests_frame.scroll_to()
            # If all are green set file green!
            for req in self.reqs:
                if req.color != "#50C878":
                    self.current_client.current_file.color = "white"  # SET FILE TO WHITE if still requests not done
                    self.requests_frame.update_files(self.current_client.files)
                    return
            self.current_client.current_file.color = "#50C878"  # Set file to green if all done!
            self.requests_frame.update_files(self.current_client.files)

            if undo_command:
                self.requests_frame.scroll_to()

    # Set as Check with client
    def check(self, undo_command=False):
        if self.current_req != 0:
            if not undo_command:
                self.add_action_to_stack(ActionCheck(self, "Check"))
            if self.current_req.color == "#FF0000":
                self.current_req.color = "grey"  # set grey
            else:
                self.current_req.color = "#FF0000"  # Set red
            self.current_client.current_file.color = ("black", "white")
            self.requests_frame.update_files(self.current_client.files)  # Turn file white if green
            # Go to next request
            index = self.reqs.index(self.current_req)
            if index < len(self.reqs) - 1:
                self.set_request(self.reqs[index + 1])
            else:
                self.save_request()
            # Scroll to this
            if undo_command:  # This line makes run better
                self.requests_frame.scroll_to()

    # Copy objections from the previous request
    def copy_previous(self, undo_command=False):
        if self.file_open():
            if not undo_command:  # Add the undo action
                self.add_action_to_stack(ActionCopyPrevious(master=self, obj="Copy"))
            # Copy the previous opts list, use copy maybe
            for i in range(len(self.reqs)):
                if self.reqs[i] == self.current_req:
                    if i >= 1:
                        # Copy the previous objections
                        for o in range(len(self.reqs[i - 1].opts)):
                            # Copy selected
                            self.current_req.opts[o].selected = self.reqs[i - 1].opts[o].selected
                            # Copy param
                            self.current_req.opts[o].param = self.reqs[i - 1].opts[o].param
                            self.current_req.opts[o].additional_param = self.reqs[i - 1].opts[o].additional_param
                            # Set these in the GUI
                            self.objections_frame.redraw(self.current_req)
                    else:
                        return
            self.update_response_textbox()
            self.update_objection_textbox()

    # Clear a full request#
    def clear(self, undo_command=False):
        if self.current_req != 0:
            if not undo_command:
                # Add to undo queue
                self.add_action_to_stack(ActionClear(self, "Clear"))

            # Reset Color
            self.current_req.color = ("black", "white")
            self.current_client.current_file.color = ("black", "white")
            self.requests_frame.update_files(self.current_client.files)
            # Reset Response
            self.current_req.resp = ""
            # Reset Checkboxes & Params
            for i in self.current_req.opts:
                i.selected = 0
                i.param = ""
            # Reset boxes
            self.response_frame.set_response("", remove_separator=True)

            self.objections_frame.redraw(self.current_req)
            self.requests_frame.update_list(self.reqs)
            # Reset RFP
            if self.req_type == "RFP":
                self.response_frame.set_RFP("Available")
                self.response_frame.set_RFP_text("")
            elif self.req_type == "RFA":
                self.response_frame.set_RFA("Admit")

            if not undo_command:  # fix undo stack
                # self.revert_undo_stack(undo_action)
                pass

            self.update_response_textbox()
            self.update_objection_textbox()

    def generate_AI_response(self):
        # Generate AI text and then use it here
        openai.api_key = get_openai_key()
        failed = 0
        while failed < 3:
            chat = None
            messages = [{"role": "user",
                         "content": "You are a lawyer in LA california. You need to write a response to a discovery request of the type " + str(
                             self.req_type) + ".\n The request is: " + str(
                             self.current_req.req) + "\n The objections are: " + str(
                             self.current_req.custom_objection_text) + "\n Now give a response: "}]
            try:
                chat = openai.chat.completions.create(
                    model="gpt-3.5-turbo", messages=messages
                )
            except Exception as e:
                failed += 1
                print(e)
            if chat != None:
                reply = chat.model_dump_json(indent=2)
                reply = chat.choices[0].message.content
                failed = 5

        self.response_frame.current_frame.response_text.animate_typing(reply)
