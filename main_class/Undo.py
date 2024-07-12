# Main Imports
from main_class.__modules__ import *

class Undo:
    #Reset both of the undo stacks
    def reset_undo_stacks(self):
        #Reset both undo stacks
        self.ACTION_STACK = []
        self.REDO_ACTION_STACK = []
        self.bar_frame.disable_undo()
        self.bar_frame.disable_redo()

    #Reverts the stack back to a particular action! Usefuly for clear etc
    def revert_undo_stack(self,action):
        self.ACTION_STACK = self.ACTION_STACK[:self.ACTION_STACK.index(action)+1]


    #Ensure both stacks are below the config undo length
    def validate_action_stacks(self):
        maximum = int(self.CONFIG["general"]["undo_stack"])
        if len(self.ACTION_STACK)>maximum:
            self.ACTION_STACK = self.ACTION_STACK[-maximum:]
        if len(self.REDO_ACTION_STACK)>maximum:
            self.REDO_ACTION_STACK = self.REDO_ACTION_STACK[-maximum:]

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

        #Ensure both stacks are below the config undo length
        self.validate_action_stacks()

    #Undo the previous action and remove it from the stack (put on redo stack)
    def undo_action(self):
        if len(self.ACTION_STACK)>0:
            action = self.ACTION_STACK.pop()
            ## UNDO ACTION HERE
            action.undo()
            ## 

            self.REDO_ACTION_STACK.append(action)
            #IF EMPTY then disable the undo button
            if len(self.ACTION_STACK)==0:
                self.bar_frame.disable_undo()

            #If redo now has one then enable
            if len(self.REDO_ACTION_STACK)==1:
                self.bar_frame.enable_redo()

            self.print_stacks()

            #Ensure both stacks are below the config undo length
            self.validate_action_stacks()

    #Redo an action which was undone, when action stack added to then the redo stack will clear
    def redo_action(self):
        if len(self.REDO_ACTION_STACK)>0:
            action = self.REDO_ACTION_STACK.pop()

            ## REDO ACTION HERE
            action.redo()
            ## 
            
            self.ACTION_STACK.append(action)
            #IF EMPTY then disable the redo button
            if len(self.REDO_ACTION_STACK)==0:
                self.bar_frame.disable_redo()

            #If only one item then enable the undo button again
            if len(self.ACTION_STACK)==1:
                self.bar_frame.enable_undo()

            self.print_stacks()

            #Ensure both stacks are below the config undo length
            self.validate_action_stacks()

    def print_stacks(self):
        print("ACTION STACK: "+str(len(self.ACTION_STACK))+"  REDO STACK: "+str(len(self.REDO_ACTION_STACK)))
