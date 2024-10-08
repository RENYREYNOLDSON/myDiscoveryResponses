# Main Imports
from functions import *
from objects.Action import *


# CUSTOM SMART TEXT BOX CLASS, BUILT IN SPELL CHECKER
class SmartTextbox(tk.CTkTextbox):
    # Constructor
    def __init__(self, master, main_master, undo=True, **kwargs):
        # FRAME SETUP
        super().__init__(master, undo=False, maxundo=100, autoseparators=False, **kwargs)

        self.main_master = main_master
        self.undo_enabled = undo  # Name undo taken
        # This is the previous text in the box
        self.previous_text = ""
        self.previous_modified_text = ""
        self.current_text = ""
        self.issues = []
        self.istart, self.iend = 0, 0  # Start and end of selected spellings
        self.pop = DropdownMenu(self, values=["init"])
        self.bind("<Button-3>", self.popup)
        self.after(int(self.main_master.CONFIG["spelling"]["spellcheck_interval"]), self.spellcheck)

        # When space pressed, check if a shortcut is present
        self.bind("<space>", self.check_shortcuts)
        if self.undo_enabled:
            # Bind a function for when this is modified
            autoseparator_bindings = ["<Delete>", "<Return>", "<<Cut>>", "<<Paste>>", "<<Clear>>",
                                      "<<PasteSelection>>", "<space>"]
            for bind in autoseparator_bindings:
                self.bind(bind, self.modified)

            self.bind("<KeyPress>", self.check_if_start)
            self.bind("<KeyRelease>", self.curly_convert)
            self.bind("<BackSpace>", self.backspace)  # Get's its own function
            # THIS UNBINDS THE UNDO AND REDO!
            self._textbox.event_delete("<<Undo>>")
            self._textbox.event_delete("<<Redo>>")

    def backspace(self, e):
        self.modified(None)

    # Runs when text is inserted or deleted
    def modified(self, e):
        if self.undo_enabled:
            # Add this onto undo stack -> Then access the box when an undo is needed
            # Pass master, textbox, previous_modified_text, new text
            # Only add if actually changed
            print(self.previous_modified_text)
            print(self.get("0.0", "end-1c"))
            new_action = ActionTextBox(self.main_master, self, self.previous_modified_text, self.get("0.0", "end-1c"))
            self.main_master.add_action_to_stack(new_action)
            self.previous_modified_text = self.get("0.0", "end-1c")
            print("Added text undo to stack")

    # If the text is empty then add a separator
    def check_if_start(self, e):
        if self.get(0.0, "end-1c") == "":
            self.modified(None)

    # DO CURLY QUOTES HERE!
    def curly_convert(self, e):
        insert_index = self.index(tk.INSERT)  # Current index
        resp = " " + self.get(0.0, "end-1c")  # Current response text
        if '"' in resp or "'" in resp:
            resp = curly_convert(resp)
            # Put the text here 
            self.delete("0.0", "end-1c")
            self.insert("0.0", resp[1:])
            self.mark_set("insert", insert_index)

    def check_shortcuts(self, e):
        # DO HOTKEYS HERE
        insert_index = self.index(tk.INSERT)  # Current index
        resp = self.get(0.0, "end-1c")
        use_fill = None
        use_pos = 0
        start = False
        for fill in self.main_master.HOTKEYS:  # Replace all autofill phrases
            position = -1
            trigger = " " + fill
            position = resp.find(trigger)  # Pos of index
            if position < 0:
                position = resp.find("\n" + trigger[1:])  # Try new line instances
                if position >= 0:
                    start = 1
            if position >= 0:
                use_fill = fill  # Set this to fill
                use_pos = position
            # If first word
            if resp == fill:
                use_fill = fill
                use_pos = 0
                start = True
        if use_fill != None:  # IF AN AUTOFILL USED
            # Update index if grown in length, must add suffic n + chars
            text_index = "0.0 + " + str(use_pos) + " chars"
            text_end_index = "0.0 + " + str(use_pos + len(use_fill + " ")) + " chars"
            # Put the text here 
            self.delete(text_index, text_end_index)
            if start:
                self.insert(text_index, (self.main_master.HOTKEYS[use_fill]))
            else:
                self.insert(text_index, (" " + self.main_master.HOTKEYS[use_fill]))
            # Reset index
            insert_index += " + " + str(len(self.main_master.HOTKEYS[use_fill] + " ") - len(use_fill) - 1) + " chars"
            self.mark_set("insert", insert_index)

    def spellcheck(self, loop=True):
        if self.winfo_manager() != None:  # Only check if text box placed
            # DO SPELLCHECKING!
            if self.main_master.CONFIG["spelling"]["use_spellcheck"]:
                self.current_text = self.get(0.0, "end-1c")
                # Only spellcheck if text has changed
                if self.current_text != self.previous_text:
                    # Highlight them
                    self.issues = spellcheck(self, " " + self.get("0.0",
                                                                  "end-1c"))  # [message,start,width,replacements array]
            else:
                # CLEAR SPELLCHECK HERE!
                # Remove all spelling tags
                for tag in self.tag_names():
                    self.tag_delete(tag)

            self.previous_text = self.current_text

        if loop:
            self.after(int(self.main_master.CONFIG["spelling"]["spellcheck_interval"]), self.spellcheck)

    def insert_spelling(self, v):
        if v == "Spelling Issue":  # Only add if a valid fix, not the title
            return
        elif v == "Always Ignore":
            self.main_master.add_ignore_word(self.iword)
            self.issues = spellcheck(self, " " + self.get("0.0", "end-1c"))  # [message,start,width,replacements array]
            return
        else:
            # Save the previous text
            temp = self.get("0.0", "end-1c")
            self.delete(self.istart, self.iend)
            self.insert(self.istart, v)
            self.previous_modified_text = temp
            self.modified(None)
            self.issues = spellcheck(self, " " + self.get("0.0", "end-1c"))  # [message,start,width,replacements array]

    def popup(self, event):
        try:
            # Get index position
            index = self.index(f"@{event.x},{event.y}")
            # Check most recent spell check, these should be held by each text box!
            vals = []
            for i in self.issues:
                # if clicked where the issue is:
                if index == "1.0":
                    chars = 0
                else:
                    chars = self._textbox.count("0.0", index, "chars")[0]
                if chars >= int(i[3]) - 1 and chars <= int(
                        i[3] + i[4]) and vals == []:  # If in issue range, only pick 1!
                    added = 0
                    for r in i[5]:
                        if added < int(self.main_master.CONFIG["spelling"]["corrections"]):
                            vals.append(r)  # Add issue to correction menu, Only add maximum of settings value!
                            added += 1
                    vals.insert(0, i[0])
                    vals.insert(1, i[1])
                    self.istart = "0.0+" + str(int(i[3]) - 1) + "c"
                    self.iend = "0.0+" + str(int(i[3] + i[4]) - 1) + "c"
                    self.iword = str(i[2])

            # If none then ignore
            if vals == []:
                return

            # Create popup spelling window
            self.pop = DropdownMenu(self, values=vals, command=self.insert_spelling)

            if len(vals) > 1:
                self.pop.insert_separator(2)
            try:
                self.pop.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # Release the grab
                self.pop.grab_release()

        except:
            print("Popup failed")

    def animate_typing(self, text):
        if text == "":  # Finished
            return
        # Add letter then go
        super().insert("end-1c", text[0], None)

        self.after(30, lambda: self.animate_typing(text[1:]))

    def set_text(self, text):
        self.delete("0.0", "end")
        self.insert("0.0", text)

    def delete(self, index1, index2=None, remove_separator=False):
        super().delete(index1, index2)
        self.previous_modified_text = self.get("0.0", "end-1c")
        return

    def insert(self, index, text, remove_separator=False, tags=None):
        # self.modified(None)#Modify the autoseparators when inserted to
        super().insert(index, text, tags)
        self.previous_modified_text = self.get("0.0", "end-1c")
        self.spellcheck(loop=False)
        return

    def edit_separator(self):
        return super().edit_separator()
