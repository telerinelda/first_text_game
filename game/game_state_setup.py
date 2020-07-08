#set up game state and define some methods used by the game engine.

class gameState:
    def __init__(self):
        self.game_name = "game name here"
        self.game_opening_text = "The game has begun!  You are in a room."
        self.sound_toggle = False
        self.progress = set()
        self.object_dictionary = dict()
        self.pathways_dictionary = dict()
        self.player_location = "ROOM 2" #starting point
        self.help_text = "HELP:\n\nThis is a text-based game. You can play by entering commands in the command line.  Common " \
            "commands are phrases like 'look at', 'pick up', or 'use'. Most commands need an object. Try typing 'Look" \
            " at room'.  \n\n'mute' or 'unmute' will turn the game sounds on or off."
        self.about_text = "The about text"
        self.command_list = []
        self.special_verbs = dict()
        self.command_counter = 0
        self.multiword = []
        self.console_output = ""
        self.scheduled_events = dict()
        self.wait_text = "You wait silently.  Time passes."
        #here's two example events
        self.scheduled_events[5] = "RUMBLE"
        self.scheduled_events[10] = "RUMBLE"

        #populate the multiword dictionary with some generic things
        self.multiword.append([["DOOR", "WAY"],"DOOR"])
        self.multiword.append([["DOORWAY"],"DOOR"])


    # this is a function that returns a boolean value if a certain object is present
    def is_present(self,obj_name):
        if self.object_dictionary[obj_name].location == self.player_location or self.object_dictionary[
            obj_name].location == "INVENTORY":
            return True
        else:
            return False

    # this function is used to parse the user command a word or phrase at a time If it finds what it's looking for it
    # returns True and strips the identified words off of the front of the command list.
    def strip_off(self,checklist):
        # global self.command_list
        if self.command_list[:len(checklist)] == checklist:
            self.command_list = self.command_list[len(checklist):]
            return True
        else:
            return False

    # this function returns true if the command list begins with an object that is present
    def find_obj(self):
        if len(self.command_list):
            if self.command_list[0] in ["ROOM", "SURROUNDINGS",
                                      "AREA"]:  # room is a generic name for where the player is currently.
                self.command_list[0] = self.player_location
            if self.command_list[0] in self.object_dictionary and self.is_present(self.command_list[0]):
                return True
            else:
                return False
        else:
            return False

    # return true if the command list begins with a valid location
    def find_location(self):
        if len(self.command_list):
            if self.command_list[0] in self.object_dictionary and self.object_dictionary[self.command_list[0]].is_location:
                return True
            else:
                return False
        else:
            return False

    def subseq_replace(self,comlist, find, replace):
        for i in range(len(comlist)):
            if comlist[i:i + len(find)] == find:
                del comlist[i:i + len(find)]
                comlist.insert(i,replace)
                break
        return comlist

    def replacements(self,comlist):
        for repl in self.multiword:
            comlist = self.subseq_replace(comlist,repl[0],repl[1])
        return comlist