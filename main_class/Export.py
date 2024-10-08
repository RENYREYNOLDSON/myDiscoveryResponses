# Main Imports
from main_class.__modules__ import *


class Export:
    ### EXPORTING AS DOCX
    ########################################################################################################

    # Export a file as DOCX
    def export(self, file, filename, preview_mode=False):
        reqs = []
        resps = []
        numbers = []
        for r in file.reqs:  # Get responses and requests
            # Export ALL for FROGS, and submitted for others depending on setting
            if file.req_type == "FROG" or (file.req_type != "FROG" and r.color == "#50C878") or self.CONFIG["general"][
                "submitted_only"] == 0:
                # 1. ADD REQUESTS
                reqs.append(r.req)
                # 2. ADD RESPONSES
                full_text = r.get_full_resp()
                resps.append(full_text)
                # 3. ADD NUMBER POINTERS
                numbers.append(r.custom_key)
        cnv.updateDOC(reqs, resps, file.details, self.current_client.firm_details, file.req_type, str(filename),
                      numbers)

        # Open the word document if setting is selected
        if self.CONFIG["general"]["open_export"] and preview_mode == False:
            filename = str(filename) + ".docx"
            os.system(f'start "" "{filename}"')

    # Export all as a folder of DOCX's
    def export_all(self):
        if len(self.current_client.files) > 0:
            # Select Folder
            filename = tk.filedialog.askdirectory(title='Select Export Folder')
            # For each file
            for file in self.current_client.files:
                self.export(file, filename + "/" + str(file.name.split("/")[-1].split(".")[0]))

    # Select a save then use export function
    def export_current(self):
        # Need to get the correct file location and then save
        if self.current_client != "":
            filename = tk.filedialog.asksaveasfilename(title="Export Current File as DOCX",
                                                       filetypes=(("DOCX", "*.docx"), ('All files', '*.*')))
            self.export(self.current_client.current_file, filename)

    # This outputs all of the check with clients WITHIN the file!
    def export_check_with_clients(self):
        if self.file_open():
            # Get all check with clients / red
            filename = tk.filedialog.asksaveasfilename(title="Export Check with Client",
                                                       filetypes=(("DOCX", "*.docx"), ('All files', '*.*')))
            if filename != "":
                reqs = []
                resps = []
                numbers = []
                req_types = []
                for file in self.current_client.files:
                    for r in file.reqs:  # Get responses and requests
                        if r.color == "#FF0000":
                            # 1. ADD REQUESTS
                            reqs.append(r.req)
                            # 2. ADD RESPONSES
                            full_text = r.get_full_resp()
                            resps.append(full_text)
                            # 3. ADD NUMBER POINTERS
                            numbers.append(r.custom_key)
                            # 4. ADD REQUEST TYPE
                            req_types.append(r.req_type)
                if len(reqs) > 0:
                    cnv.updateDOC(reqs, resps, file.details, self.current_client.firm_details, req_types, str(filename),
                                  numbers)
                    if self.CONFIG["general"]["open_export"]:
                        os.system("start " + str(filename) + ".docx")
