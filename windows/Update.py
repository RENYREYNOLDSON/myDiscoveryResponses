# Main Imports
import requests

from windows.__modules__ import *


# UPDATER WINDOW
############################################################################################################
# Contains theme data
class Update(tk.CTkToplevel):
    # Constructor
    def __init__(self, master):
        # CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master = master
        self.geometry("400x60")
        self.title("Update myDiscoveryResponses")
        self.lift()
        self.attributes("-topmost", True)
        self.grab_set()
        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__), "../assets/icon.ico")))
        self.resizable(False, False)

        heading_font = ("Segoe UI", 20)

        # Add title
        self.title = tk.CTkLabel(master=self, text="Downloading Update", anchor="w")
        self.title.pack(fill="x", padx=10, pady=(5, 5))

        # Add progress bar
        self.progress_bar = tk.CTkProgressBar(master=self, height=14)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=5)

        self.after(1000, self.download_update)

    def download_update(self):
        try:
            # Download new file
            url = "https://www.myDiscoveryResponses.com/myDiscoveryResponses Installer.exe"

            filename = "myDiscoveryResponses Installer.exe"

            try:
                response = requests.get(url, stream=True)
            except:
                update_check = CTkMessagebox(title="No Connection",
                                             message="Could not establish a connection with the server!",
                                             icon="warning",
                                             corner_radius=0,
                                             sound=True,
                                             wraplength=400,
                                             master=self)
                return
            total_size = int(response.headers.get('content-length', 0))

            block_size = 1024  # 1 Kilobyte
            total = 0
            with open(filename, 'wb') as file:
                for data in response.iter_content(block_size):
                    self.progress_bar.set(total / total_size)
                    self.update()
                    file.write(data)
                    total += block_size
                    if total % 1024000 == 0:  # At each MB
                        self.title.configure(text="Downloading Update " + str(int(total / 1024000)) + "/" + str(
                            int(total_size / 1024000)) + "MB")

            exe_path = os.path.join(get_main_path(), filename)

            """
            #Need to extract exe file
            with zipfile.ZipFile(dir_path, 'r') as zip_ref:
                zip_ref.extractall(get_main_path())
            """

            # exe_path = os.path.join(get_main_path(),"myDiscoveryResponsesInstaller.exe")

            # Open installer
            subprocess.Popen(["cmd", "/c", "start", "", exe_path],
                             stdout=subprocess.DEVNULL,  # Redirect output to avoid hanging on pipes
                             stderr=subprocess.DEVNULL,
                             creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_BREAKAWAY_FROM_JOB,
                             close_fds=True)
            # Destroy this application
            self.master.destroy()
            self.master.root.destroy()

        except Exception as e:
            self.master.update_failed(e)
