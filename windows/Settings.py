# Main Imports
import os
from tkinter.colorchooser import askcolor

from enchant import list_languages

from windows.__modules__ import *

heading_font = ("Segoe UI", 20)


def set_switch(switch, var):
    if var:
        switch = switch.select()
    return switch


class General(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        # FRAME SETUP
        super().__init__(master, **kwargs)

        self.scroll_frame = tk.CTkScrollableFrame(master=self, fg_color="transparent")
        self.scroll_frame.pack(expand=True, fill="both")
        # Title
        title = tk.CTkLabel(master=self.scroll_frame, text="General", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)

        # Tooltips?
        tooltips = tk.CTkLabel(master=self.scroll_frame, text="Show tooltips on hover", anchor="w")
        tooltips.pack(fill="x", padx=10, pady=(0, 0))
        self.tooltips_switch = tk.CTkSwitch(master=self.scroll_frame, text="")
        set_switch(self.tooltips_switch, self.master.master.CONFIG["general"]["hover_tooltips"])
        self.tooltips_switch.pack(fill="x", padx=10, pady=(0, 0))

        # 17.1 automatically?
        seventeen_label = tk.CTkLabel(master=self.scroll_frame, text="Automatically add FROG 17.1 responses",
                                      anchor="w")
        seventeen_label.pack(fill="x", padx=10, pady=(5, 0))
        self.seventeen_switch = tk.CTkSwitch(master=self.scroll_frame, text="")
        set_switch(self.seventeen_switch, self.master.master.CONFIG["general"]["auto_FROGS"])
        self.seventeen_switch.pack(fill="x", padx=10, pady=(0, 0))

        # Undo Stack
        value = int(self.master.master.CONFIG["general"]["undo_stack"])
        self.undo_label = tk.CTkLabel(master=self.scroll_frame,
                                      text="Maximum actions in the Undo list (" + str(value) + ")", anchor="w")
        self.undo_label.pack(fill="x", padx=10, pady=(5, 0))
        self.undo_stack = tk.CTkSlider(master=self.scroll_frame, from_=5, to=100, command=self.update_undo_stack_label,
                                       number_of_steps=94)
        self.undo_stack.set(self.master.master.CONFIG["general"]["undo_stack"])
        self.undo_stack.pack(fill="x", padx=(10, 300), pady=(0, 5))

        # Objections Order
        order_label = tk.CTkLabel(master=self.scroll_frame, text="Objections display order", anchor="w")
        order_label.pack(fill="x", padx=10, pady=(5, 0))
        self.objections_order = tk.CTkOptionMenu(master=self.scroll_frame, values=["Saved Order", "Alphabetical"])
        self.objections_order.set(self.master.master.CONFIG["general"]["objections_order"])
        self.objections_order.pack(fill="x", padx=(10, 300), pady=(0, 5))

        title = tk.CTkLabel(master=self.scroll_frame, text="Saving", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=(20, 5))

        # Autosaving?
        autosave_label = tk.CTkLabel(master=self.scroll_frame, text="Use autosaving", anchor="w")
        autosave_label.pack(fill="x", padx=10, pady=(0, 0))
        self.autosave_checkbox = tk.CTkSwitch(master=self.scroll_frame, text="")
        set_switch(self.autosave_checkbox, self.master.master.CONFIG["general"]["autosaving"])
        self.autosave_checkbox.pack(fill="x", padx=10, pady=(0, 5))

        # Autosave Interval
        value = int(self.master.master.CONFIG["general"]["autosave_interval"] // 1000)
        self.autosave_label = tk.CTkLabel(master=self.scroll_frame,
                                          text="Autosave interval in seconds (" + str(value) + "s)", anchor="w")
        self.autosave_label.pack(fill="x", padx=10, pady=(5, 0))
        self.autosave_interval = tk.CTkSlider(master=self.scroll_frame, from_=10000, to=500000,
                                              command=self.update_autosave_label, number_of_steps=49)
        self.autosave_interval.set(self.master.master.CONFIG["general"]["autosave_interval"])
        self.autosave_interval.pack(fill="x", padx=(10, 300), pady=(0, 5))

        # Export include
        export_label = tk.CTkLabel(master=self.scroll_frame, text="Only include submitted requests in the export",
                                   anchor="w")
        export_label.pack(fill="x", padx=10, pady=(5, 0))
        self.export_switch = tk.CTkSwitch(master=self.scroll_frame, text="")
        set_switch(self.export_switch, self.master.master.CONFIG["general"]["submitted_only"])
        self.export_switch.pack(fill="x", padx=10, pady=(0, 5))

        # Open Export
        export_label = tk.CTkLabel(master=self.scroll_frame, text="Open exported file", anchor="w")
        export_label.pack(fill="x", padx=10, pady=(5, 0))
        self.open_export_switch = tk.CTkSwitch(master=self.scroll_frame, text="")
        set_switch(self.open_export_switch, self.master.master.CONFIG["general"]["open_export"])
        self.open_export_switch.pack(fill="x", padx=10, pady=(0, 5))

    def update_autosave_label(self, val):
        value = int(val // 1000)
        self.autosave_label.configure(text="Autosave interval in seconds (" + str(value) + "s)")

    def update_undo_stack_label(self, val):
        value = int(val)
        self.undo_label.configure(text="Maximum actions in the Undo list (" + str(value) + ")")


class Theme(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        # FRAME SETUP
        super().__init__(master, **kwargs)
        self.theme = self.master.master.CONFIG["appearance"]["theme"]
        # Title
        title = tk.CTkLabel(master=self, text="Theme", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)

        self.window_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.window_frame.grid_columnconfigure((0, 1), weight=1)
        self.window_frame.pack(anchor="w", fill="both")

        dark_mode_image = PhotoImage(master=self.window_frame,
                                     file=os.path.join(os.path.dirname(__file__), "../assets/dark_mode.png"))
        self.dark_mode_button = tk.CTkButton(master=self.window_frame, image=dark_mode_image, text="", hover=False,
                                             fg_color="transparent", command=self.set_dark)
        self.dark_mode_button.grid(row=1, column=0, padx=10, pady=(0, 0))

        light_mode_image = PhotoImage(master=self.window_frame,
                                      file=os.path.join(os.path.dirname(__file__), "../assets/light_mode.png"))
        self.light_mode_button = tk.CTkButton(master=self.window_frame, image=light_mode_image, text="", hover=False,
                                              fg_color="transparent", command=self.set_light)
        self.light_mode_button.grid(row=1, column=1, padx=10, pady=(0, 0))

        self.theme_text = tk.CTkLabel(master=self.window_frame, text="Dark Mode", anchor="center")
        self.theme_text.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.theme_text = tk.CTkLabel(master=self.window_frame, text="Light Mode", anchor="center")
        self.theme_text.grid(row=2, column=1, sticky="ew", padx=20, pady=(0, 10))

        if self.theme == "Dark":
            self.set_dark()
        else:
            self.set_light()

        # title = tk.CTkLabel(master=self,text="Layout",font=heading_font,anchor="w")
        # title.pack(fill="x",padx=10,pady=5)

        title = tk.CTkLabel(master=self, text="Text Formatting", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)

        # Text Colour
        text_text = tk.CTkLabel(master=self, text="Text color", anchor="w")
        text_text.pack(fill="x", padx=10, pady=(0, 0))
        self.text_picker = tk.CTkButton(master=self, text=self.master.master.CONFIG["appearance"]["text_color"],
                                        fg_color=self.master.master.CONFIG["appearance"]["text_color"],
                                        command=self.change_text_color)
        self.text_picker.pack(anchor="w", padx=10, pady=(0, 0))

        # Text Background
        background_text = tk.CTkLabel(master=self, text="Text background color", anchor="w")
        background_text.pack(fill="x", padx=10, pady=(5, 0))
        self.background_picker = tk.CTkButton(master=self, text=self.master.master.CONFIG["appearance"]["text_bg"],
                                              fg_color=self.master.master.CONFIG["appearance"]["text_bg"],
                                              command=self.change_bg_color)
        self.background_picker.pack(anchor="w", padx=10, pady=(0, 0))

        # Text Font
        font_text = tk.CTkLabel(master=self, text="Text font", anchor="w")
        font_text.pack(fill="x", padx=10, pady=(5, 0))
        self.font_entry = tk.CTkOptionMenu(master=self, values=["Arial", "Times", "Courier", "Calibri", "Cambria"])
        self.font_entry.set(self.master.master.CONFIG["appearance"]["text_font"])
        self.font_entry.pack(fill="x", padx=(10, 300), pady=(5, 0))

        # Text Size
        size_text = tk.CTkLabel(master=self, text="Text font size", anchor="w")
        size_text.pack(fill="x", padx=10, pady=(5, 0))
        self.size_entry = tk.CTkOptionMenu(master=self,
                                           values=["8", "10", "12", "14", "16", "18", "20", "22", "24", "26"])
        self.size_entry.set(self.master.master.CONFIG["appearance"]["text_size"])
        self.size_entry.pack(fill="x", padx=(10, 300), pady=(5, 0))

        # TEXT BOX PREVIEW

    def set_dark(self):
        self.theme = "Dark"
        self.dark_mode_button.configure(fg_color=['#3B8ED0', '#1F6AA5'])
        self.light_mode_button.configure(fg_color="transparent")

    def set_light(self):
        self.theme = "Light"
        self.light_mode_button.configure(fg_color=['#3B8ED0', '#1F6AA5'])
        self.dark_mode_button.configure(fg_color="transparent")

    # Open the text colour picker
    def change_text_color(self):
        colors = askcolor(title="Text Color Chooser")
        if colors != None:
            self.text_picker.configure(fg_color=colors[1], text=str(colors[1]))

    # Open the background colour picker
    def change_bg_color(self):
        colors = askcolor(title="Text Background Color Chooser")
        if colors != None:
            self.background_picker.configure(fg_color=colors[1], text=str(colors[1]))


class Spelling(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        # FRAME SETUP
        super().__init__(master, **kwargs)
        title = tk.CTkLabel(master=self, text="Spelling", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)

        # Spell Check?
        spellcheck_label = tk.CTkLabel(master=self, text="Use spellcheck", anchor="w")
        spellcheck_label.pack(fill="x", padx=10, pady=(0, 0))
        self.spellcheck_switch = tk.CTkSwitch(master=self, text="")
        set_switch(self.spellcheck_switch, self.master.master.CONFIG["spelling"]["use_spellcheck"])
        self.spellcheck_switch.pack(fill="x", padx=10, pady=(0, 0))

        # Spellcheck Interval
        value = int(self.master.master.CONFIG["spelling"]["spellcheck_interval"] // 1000)
        self.interval_label = tk.CTkLabel(master=self, text="Spellcheck interval in seconds (" + str(value) + "s)",
                                          anchor="w")
        self.interval_label.pack(fill="x", padx=10, pady=(5, 0))
        self.spellcheck_interval = tk.CTkSlider(master=self, from_=1000, to=20000, command=self.update_interval_label)
        self.spellcheck_interval.set(self.master.master.CONFIG["spelling"]["spellcheck_interval"])
        self.spellcheck_interval.pack(fill="x", padx=(10, 300), pady=(0, 5))

        language_label = tk.CTkLabel(master=self, text="Language to use for spellchecking", anchor="w")
        language_label.pack(fill="x", padx=10, pady=(5, 0))
        self.language = tk.CTkOptionMenu(master=self, values=sorted(list_languages()))
        self.language.set(self.master.master.CONFIG["spelling"]["language"])
        self.language.pack(fill="x", padx=(10, 300), pady=(0, 5))

        color_label = tk.CTkLabel(master=self, text="Error underline colour", anchor="w")
        color_label.pack(fill="x", padx=10, pady=(5, 0))
        self.color_picker = tk.CTkButton(master=self, text=self.master.master.CONFIG["spelling"]["underline"],
                                         fg_color=self.master.master.CONFIG["spelling"]["underline"],
                                         command=self.change_underline_color)
        self.color_picker.pack(anchor="w", padx=10, pady=(0, 5))

        value = self.master.master.CONFIG["spelling"]["corrections"]
        self.corrections_label = tk.CTkLabel(master=self,
                                             text="Maximum number of corrections shown (" + str(int(value)) + ")",
                                             anchor="w")
        self.corrections_label.pack(fill="x", padx=10, pady=(5, 0))
        self.corrections_interval = tk.CTkSlider(master=self, number_of_steps=19, from_=1, to=20,
                                                 command=self.update_corrections_label)
        self.corrections_interval.set(self.master.master.CONFIG["spelling"]["corrections"])
        self.corrections_interval.pack(fill="x", padx=(10, 300), pady=(0, 5))

        ignore_label = tk.CTkLabel(master=self, text="Words to ignore", anchor="w")
        ignore_label.pack(fill="x", padx=10, pady=(5, 0))
        self.ignore_text = tk.CTkTextbox(master=self, height=100)
        self.ignore_text.insert(0.0, str(self.master.master.CONFIG["spelling"]["ignore"]))
        self.ignore_text.pack(fill="x", padx=(10, 300), pady=(0, 5))

    # Open the background colour picker
    def change_underline_color(self):
        colors = askcolor(title="Underline Color Chooser")
        if colors != None:
            self.color_picker.configure(fg_color=colors[1], text=str(colors[1]))

    def update_interval_label(self, val):
        value = int(val // 1000)
        self.interval_label.configure(text="Spellcheck interval in seconds (" + str(value) + "s)")

    def update_corrections_label(self, val):
        self.corrections_label.configure(text="Maximum number of corrections shown (" + str(int(val)) + ")")

    def get_ignores(self):
        return self.ignore_text.get(0.0, "end-1c")


class Loading(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        # FRAME SETUP
        super().__init__(master, **kwargs)
        # Title

        # Title
        title = tk.CTkLabel(master=self, text="Loading", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)


class Objections(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        # FRAME SETUP
        super().__init__(master, **kwargs)
        # Title
        title = tk.CTkLabel(master=self, text="Objections", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)


class Hotkeys(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        # FRAME SETUP
        super().__init__(master, **kwargs)
        # Title
        title = tk.CTkLabel(master=self, text="Hotkeys", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)

        hotkey_frame = tk.CTkFrame(master=self, fg_color="transparent")
        hotkey_frame.pack(fill="both", expand=True, padx=20)
        hotkey_frame.columnconfigure((0, 1), weight=1)

        hotkeys = {"Up-Arrow": "Move up a request",
                   "Down-Arrow": "Move down a request",
                   "Enter": "Submit a request",
                   "Escape": "Escape a text box",
                   "Ctrl+N": "Create new client",
                   "Ctrl+O": "Open a file",
                   "Ctrl+F": "Open a folder",
                   "Ctrl+S": "Save current client",
                   "Ctrl+E": "Export current file",
                   "Ctrl+Z": "Undo action",
                   "Ctrl+Y": "Redo action"}

        c = 0
        for h in hotkeys.keys():
            hotkey_text = tk.CTkLabel(master=hotkey_frame, text=h)
            hotkey_text.grid(row=c, column=0)
            hotkey_text = tk.CTkLabel(master=hotkey_frame, text=hotkeys[h], text_color="grey")
            hotkey_text.grid(row=c, column=1)
            c += 1


class About(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        # FRAME SETUP
        super().__init__(master, **kwargs)
        # Title
        title = tk.CTkLabel(master=self, text="About", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)

        # Version number
        text = tk.CTkLabel(master=self, text="Current version:  " + str(self.master.master.master.version), anchor="w")
        text.pack(fill="x", padx=10, pady=(5, 0))
        # Report an issue
        text = tk.CTkLabel(master=self, text="Report any issues to:  reynoldson2002@gmail.com", anchor="w")
        text.pack(fill="x", padx=10, pady=(5, 0))

        check_button = tk.CTkButton(master=self, text="Check for Updates",
                                    command=master.master.master.check_for_update)
        check_button.pack(anchor="w", padx=10, pady=(5, 0))

        # Go to file location
        reset_shortcuts_text = tk.CTkLabel(master=self, text="Open myDiscoveryResponses install location", anchor="w")
        reset_shortcuts_text.pack(fill="x", padx=10, pady=(5, 0))
        reset_shortcuts = tk.CTkButton(master=self, text="📂 Open file location", command=open_install_location)
        reset_shortcuts.pack(anchor="w", padx=10, pady=(5, 20))

        title = tk.CTkLabel(master=self, text="Reset", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)

        # Reset objections
        """
        reset_shortcuts_text = tk.CTkLabel(master=self,text="Reset Objections",anchor="w")
        reset_shortcuts_text.pack(fill="x",padx=10,pady=(5,0))
        reset_shortcuts = tk.CTkButton(master=self,text="Reset",fg_color="#404040")
        reset_shortcuts.pack(anchor="w",padx=10,pady=(5,0))
        """
        # Reset all settings
        reset_shortcuts_text = tk.CTkLabel(master=self, text="Reset settings to default", anchor="w")
        reset_shortcuts_text.pack(fill="x", padx=10, pady=(5, 0))
        reset_shortcuts = tk.CTkButton(master=self, text="Reset", fg_color="#404040",
                                       command=master.master.master.reset_config)
        reset_shortcuts.pack(anchor="w", padx=10, pady=(5, 0))
        # Reset all
        reset_shortcuts_text = tk.CTkLabel(master=self, text="Fully reset myDiscoveryResponses to default", anchor="w")
        reset_shortcuts_text.pack(fill="x", padx=10, pady=(5, 0))
        reset_shortcuts = tk.CTkButton(master=self, text="Reset", fg_color="#404040",
                                       command=master.master.master.reset_all)
        reset_shortcuts.pack(anchor="w", padx=10, pady=(5, 0))
        # Uninstall
        reset_shortcuts_text = tk.CTkLabel(master=self, text="Uninstall myDiscoveryResponses", anchor="w")
        reset_shortcuts_text.pack(fill="x", padx=10, pady=(5, 0))
        reset_shortcuts = tk.CTkButton(master=self, text="Uninstall", fg_color="red",
                                       command=master.master.master.uninstall)
        reset_shortcuts.pack(anchor="w", padx=10, pady=(5, 0))


class Update(tk.CTkFrame):
    # Constructor
    def __init__(self, master, **kwargs):
        # FRAME SETUP
        super().__init__(master, **kwargs)
        # Title
        title = tk.CTkLabel(master=self, text="Update", font=heading_font, anchor="w")
        title.pack(fill="x", padx=10, pady=5)

        # Last Updated: x
        check_button = tk.CTkButton(master=self, text="Check for Updates",
                                    command=master.master.master.check_for_update)
        check_button.pack()

        # Last Updated
        # Version Number
        # Check for updates


# THEME WINDOW
############################################################################################################
# Contains theme data
class Settings(tk.CTkToplevel):
    # Constructor
    def __init__(self, master):
        # CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.master = master
        self.geometry("800x600")
        self.title("Settings")
        # self.wm_iconbitmap(os.path.join(os.path.dirname(__file__),"../assets/icon.ico"))#Icon
        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__), "../assets/icon.ico")))
        self.resizable(False, False)

        self.lift()
        # self.attributes("-topmost", True)
        self.grab_set()

        self.after(500, self.grab_release)

        self.CONFIG = self.master.CONFIG

        self.menu_frame = tk.CTkFrame(master=self, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")

        self.main_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # GENERAL
        self.general_button = tk.CTkButton(master=self.menu_frame, text=" ⚙️  General", corner_radius=0, width=200,
                                           fg_color='#144870', hover=False, anchor="w", command=self.set_general,
                                           text_color=("black", "white"))
        self.general_button.pack()
        self.general_frame = General(master=self.main_frame, fg_color="transparent")
        self.general_frame.pack(fill="both", expand=True)

        # THEME/APPEARANCE
        self.theme_button = tk.CTkButton(master=self.menu_frame, text=" 🎨  Appearance", corner_radius=0, width=200,
                                         fg_color="transparent", hover=False, anchor="w", command=self.set_appearance,
                                         text_color=("black", "white"))
        self.theme_button.pack()
        self.theme_frame = Theme(master=self.main_frame, fg_color="transparent")

        # SPELLING
        self.spelling_button = tk.CTkButton(master=self.menu_frame, text=" 🌍  Spelling & Language", corner_radius=0,
                                            width=200, fg_color="transparent", hover=False, anchor="w",
                                            command=self.set_spelling, text_color=("black", "white"))
        self.spelling_button.pack()
        self.spelling_frame = Spelling(master=self.main_frame, fg_color="transparent")

        # SAVING
        # self.saving_button = tk.CTkButton(master=self.menu_frame,text=" 💾  Saving & Loading",corner_radius=0,width=200,fg_color="transparent",hover=False,anchor="w",command=self.set_saving)
        # self.saving_button.pack()
        # self.saving_frame = Saving(master=self.main_frame,fg_color="transparent")

        # OBJECTIONS
        self.objections_button = tk.CTkButton(master=self.menu_frame, state="disabled", text=" 🗸  Objections",
                                              corner_radius=0, width=200, fg_color="transparent", hover=False,
                                              anchor="w", command=self.set_objections, text_color=("black", "white"))
        self.objections_button.pack()
        self.objections_frame = Objections(master=self.main_frame, fg_color="transparent")

        # HOTKEYS
        self.hotkeys_button = tk.CTkButton(master=self.menu_frame, text=" ↔  Hotkeys", corner_radius=0, width=200,
                                           fg_color="transparent", hover=False, anchor="w", command=self.set_hotkeys,
                                           text_color=("black", "white"))
        self.hotkeys_button.pack()
        self.hotkeys_frame = Hotkeys(master=self.main_frame, fg_color="transparent")

        # ABOUT
        self.about_button = tk.CTkButton(master=self.menu_frame, text=" ⓘ  About", corner_radius=0, width=200,
                                         fg_color="transparent", hover=False, anchor="w", command=self.set_about,
                                         text_color=("black", "white"))
        self.about_button.pack()
        self.about_frame = About(master=self.main_frame, fg_color="transparent")

        # UPDATE
        """
        self.update_button = tk.CTkButton(master=self.menu_frame,text=" ⏏  Update",corner_radius=0,width=200,fg_color="transparent",hover=False,anchor="w",command=self.set_update,text_color=("black","white"))
        self.update_button.pack()
        self.update_frame = Update(master=self.main_frame,fg_color="transparent")
        """

        # BUTTONS!
        self.button_frame = tk.CTkFrame(master=self, fg_color="transparent")
        self.button_frame.pack(fill="x")

        apply_button = tk.CTkButton(master=self.button_frame, text="Apply", command=self.master.update_config)
        apply_button.pack(side="right", padx=10, pady=10)

        cancel_button = tk.CTkButton(master=self.button_frame, text="Cancel", command=self.master.cancel_win)
        cancel_button.pack(side="right", padx=10, pady=10)

    def get_settings(self):
        pass

    def set_settings(self):
        pass

    # Clears the main frame
    def set_main_frame(self, frame, but):
        # Set the main frame
        for c in self.main_frame.winfo_children():
            c.pack_forget()
        for button in self.menu_frame.winfo_children():
            button.configure(fg_color="transparent")

        frame.pack(fill="both", expand=True)
        but.configure(fg_color='#144870')

    # Set the current open menu
    def set_general(self):
        self.set_main_frame(self.general_frame, self.general_button)

    def set_appearance(self):
        self.set_main_frame(self.theme_frame, self.theme_button)

    def set_spelling(self):
        self.set_main_frame(self.spelling_frame, self.spelling_button)

    def set_saving(self):
        self.set_main_frame(self.saving_frame, self.saving_button)

    def set_objections(self):
        self.set_main_frame(self.objections_frame, self.objections_button)

    def set_hotkeys(self):
        self.set_main_frame(self.hotkeys_frame, self.hotkeys_button)

    def set_about(self):
        self.set_main_frame(self.about_frame, self.about_button)

    def set_update(self):
        self.set_main_frame(self.update_frame, self.update_button)

    def get_general(self):
        general = {"hover_tooltips": self.general_frame.tooltips_switch.get(),
                   "auto_FROGS": self.general_frame.seventeen_switch.get(),
                   "autosaving": self.general_frame.autosave_checkbox.get(),
                   "autosave_interval": self.general_frame.autosave_interval.get(),
                   "submitted_only": self.general_frame.export_switch.get(),
                   "open_export": self.general_frame.open_export_switch.get(),
                   "undo_stack": self.general_frame.undo_stack.get(),
                   "objections_order": self.general_frame.objections_order.get()}
        return general

    def get_appearance(self):
        appearance = {
            "text_size": self.theme_frame.size_entry.get(),
            "text_color": self.theme_frame.text_picker.cget("text"),
            "text_bg": self.theme_frame.background_picker.cget("text"),
            "text_font": self.theme_frame.font_entry.get(),
            "theme": self.theme_frame.theme,
            "layout": ["Requests", "Responses", "Objections"]
        }
        return appearance

    def get_spelling(self):
        spelling = {
            "use_spellcheck": self.spelling_frame.spellcheck_switch.get(),
            "spellcheck_interval": self.spelling_frame.spellcheck_interval.get(),
            "language": self.spelling_frame.language.get(),
            "underline": self.spelling_frame.color_picker.cget("text"),
            "corrections": self.spelling_frame.corrections_interval.get(),
            "ignore": self.spelling_frame.get_ignores()
        }
        return spelling


if __name__ == "__main__":
    root = Settings()
    root.mainloop()

# GENERAL:
# Hotkeys enabled?
# show hover tooltips?
# Auto add to 17.1s?
# Bold keywords?
# Undo Options:


# THEME:
# Layout options!


# SPELLING:
# Spell Check?
# Language (there are loads in this new library!)
# Check Interval
# Underline colour
# Ignore rules
# Number of corrections shown

# SAVING:
# Autosave?
# Autosaving interval
# Only include submitted requests in the export?
# Open file after export?


# OBJECTIONS:

# HOTKEYS:
# Remap keys for different tasks

# ABOUT:
# Text about the software
# Reset
# Reset Recently Saved

# UPDATE:
# Update
