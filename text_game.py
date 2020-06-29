from appJar import gui
from random import choice

# Generic Text Game Engine by Kevin Hughes

# some initial values
progress = set()  # you can add values here to keep track of the player's progress through the game. might change how game progress works later when I tackle that.
object_dictionary = dict()
pathways_dictionary = dict()
game_name = "Put the name of the game here"
player_location = "ROOM1"  # name of the starting location
help_text = "HELP:\nThis is a text-based game. You can play by entering commands in the command line.  Common " \
            "commands are phrases like 'look at', 'pick up', or 'use'. Most commands need an object. Try typing 'Look" \
            " at room'. "
about_text = "The About button prints this."
command_list = [] #each command entered by the player goes here and then we analyze it.
special_verbs = dict()
command_counter = 0 #this increments with each semi-successful command.

#this can be used to set up events that occur after a certain number of commands.  The wait command will advance the
#command counter until the next event in the scheduled events dictionary.
scheduled_events = dict()

# this class is the generic data structure of an object or location in the game.
class tgThing:
    location = "nowhere"
    sublocation = ""
    can_pick_up = False
    is_transitive = False  # does it need a direct object to be used?
    is_location = False  # is this thing the room itself?

    def __init__(self, obj_name):
        self.name = obj_name
        object_dictionary[obj_name] = self  # this allows access to the object through the dictionary.
        # it does NOT create a copy of the object.  It's like a pointer.

    # a thing needs response texts for when it is addressed by a command.  This is a dictionary where there
    # is a "default" text and other texts can be stored for use according the progress indicator.
    look_text = {"default": "Default Look Text."}
    room_look_text = {"default": "Default object in room text."}
    pick_up_text = {"default": "default pick up text."}
    use_text = {"default": "default use text."}
    dropa_text = {"default": "default drop text."}
    go_to_text = {"default": "default go to"}

    #other objects may be able to be located in, on, or under this object.  So we can set up a sublocation: (sublocation programming is incomplete)
    num_sublocations = 0 #should always equal len of the two below strings
    sublocation_preposition = [] #values like "UNDER" or "ON" that the user can use
    sublocation_text = [] #values like "under the bed" for building phrases about the place.
    sublocation_hidden = [] #booleans True if you can't see the sublocation just by gazing on the object itself.


# here's a subclass that is for locations (ie rooms).
class tgPlace(tgThing):
    def __init__(self, obj_name):
        self.name = obj_name
        self.location = self.name
        self.is_location = True
        self.room_look_text = {"default":""}
        object_dictionary[obj_name] = self  # this allows access to the object through the dictionary.
        # it does NOT create a copy of the object.  It's like a pointer.

# here's a subclass that is for pathways connecting rooms: doorways, hallways that don't need to be locations.
class tgPathway(tgThing):
    def __init__(self, obj_name):
        self.name = obj_name
        object_dictionary[obj_name] = self
        pathways_dictionary[obj_name] = self
    location2 = "NOWHERE" #this variable will always be the room the player is NOT in (they swap when he moves)
    pathway_open = True #can you pass through?
    def switch(self):
        #this is a method for reversing the locations when you enter the room.  location2 is always the "other" location.
        self.location, self.location2 = self.location2, self.location
    look_thru_text = dict() #If the player tries to peer through the pathway to the next room or location.
    

# this is a function that returns a boolean value if a certain object is present
def is_present(obj_name):
    if object_dictionary[obj_name].location == player_location or object_dictionary[obj_name].location == "INVENTORY":
        return True
    else:
        return False


# Here we are setting up the GUI window using Appjar
tg = gui(game_name, "1000x600")
tg.setPadding([20,20])
tg.setStretch("both")
tg.setSticky("ewns")
tg.setBg("burlywood4")
tg.addMessage("console", "This game is powered By Generic Text Game Engine, by Kevin Hughes")
tg.setMessageBg("console","PaleGreen1")
tg.setMessageWidth("console",960)
#tg.setStretch("none")
tg.setSticky("ew")
tg.addLabelEntry("input")
tg.setLabel("input", "Enter Command: ")
tg.setSticky("ns")

def press(button):
    global command_list
    global command_counter
    if button == "   Exit   ":
        tg.stop()
    elif button == "   Help   ":
        # help stuff here.
        tg.setMessage("console", help_text)
        tg_play_sound("neutral")
        tg.setFocus("input")
    elif button == "   About   ":
        tg.setMessage("console", about_text)
        tg_play_sound("neutral")
    elif button == "   Submit   ":
        user_input = tg.getEntry("input")
        command_counter += 1
        command_list = user_input.upper().replace(".","").replace(",","").split()
        command_list[:] = [x for x in command_list if x not in ["A","THE"]] #remove fluff
        game()  # this function call evaluates the input and reacts to it.
        tg.setEntry("input", "")
        tg.setFocus("input")
    else:
        print("this shouldn't happen")

tg.addButtons(["   Submit   ", "   Help   ", "   About   ", "   Exit   "], press)
tg.setFocus("input")


# this bit makes the Submit button get activated if you press the enter key
def ent():
    press("   Submit   ")
tg.enableEnter(ent)


# Here's a function that makes it slightly easier to display text in the main message location
def tgprint(print_text):
    #prev = tg.getMessage("console")
    #tg.setMessage("console", prev + "\n\n" + print_text)
    tg.setMessage("console", print_text)


# this function is used to parse the user command a word or phrase at a time If it finds what it's looking for it
# returns True and strips the identified words off of the front of the command list.
def strip_off(checklist):
    global command_list
    if command_list[:len(checklist)] == checklist:
        command_list = command_list[len(checklist):]
        return True
    else:
        return False


# this function returns true if the command list begins with an object that is present
def find_obj():
    global command_list
    if len(command_list):
        if command_list[0] in ["ROOM", "SURROUNDINGS",
                               "AREA"]:  # room is a generic name for where the player is currently.
            command_list[0] = player_location
        if command_list[0] in object_dictionary and is_present(command_list[0]):
            return True
        else:
            return False
    else:
        return False


def find_location():
    global command_list
    if command_list[0] in object_dictionary and object_dictionary[command_list[0]].is_location:
        return True
    else:
        return False


def tg_play_sound(sound_type = "neutral"):
    sound_file = ""
    if sound_type == "neutral":
        sound_file = "neutral" + choice(["1","2","3"]) + ".Wav"
    elif sound_type == "unsuccessful":
        sound_file = "unsuccessful" + choice(["1","2","3"]) + ".Wav"
    elif sound_type == "success":
        sound_file = "success1.Wav"
    elif sound_type == "zelda":
        sound_file = "Zeldasound.Wav"
    elif sound_type == "death":
        sound_file = "death.Wav"
    elif sound_type == "victory":
        sound_file = "victory.Wav"
    if sound_file != "":
        tg.playSound(sound_file)
#tg_play_sound("zelda")


# ---------------------------------------------------------------------------------------------
#  Game Objects and Locations
# ---------------------------------------------------------------------------------------------
#  Sample Location 1:
room1 = tgPlace("ROOM1")
room1.look_text = {"default": "You look at room number 1.  It's pretty simple."}
#room1.room_look_text = {"default": ""}  # Not needed for locations
room1.pick_up_text = {"default": "You would like to pick up the room but it's kinda too big."}
room1.use_text = {"default": "You are using the room as a room to stand in I guess."}
#room1.drop_text = {"default": ""}  # This is only needed if you can put it in your inventory.
room1.go_to_text = {"default": "You enter room # 1."}

#  Sample Location 2:
room2 = tgPlace("ROOM2")
room2.look_text = {"default": "You look at room number 2.  It's pretty simple."}
#room2.room_look_text = {"default": ""}  # Not needed for locations
room2.pick_up_text = {"default": "You would like to pick up the room but it's kinda too big."}
room2.use_text = {"default": "You are using the room as a room to stand in I guess."}
#room2.drop_text = {"default": ""}  # This is only needed if you can put it in your inventory.
room2.go_to_text = {"default": "You enter room # 2."}

# list connections between locations here. (DNU! old way)
#connections = [{"ROOM1", "ROOM2"}]

#sample doorway:
door = tgPathway("DOOR")
door.location = "ROOM1"
door.location2 = "ROOM2"
door.look_text = {"ROOM1":"You inspect the door.  It is a heavy wooden door with no keyhole. The door leads to room2.",
                  "ROOM2":"You inspect the door.  It is a heavy wooden door with no keyhole. The door leads to room1."}
door.room_look_text = {"default":"There is a door."}
door.pick_up_text = {"default":"Sigh.... No you can't pick up a door."}
door.go_to_text = {"default":"You approach the door..."}
door.look_thru_text = {"ROOM1":"Beyond the door is room2.  You can make out a wooden table.",
                       "ROOM2":"Beyond the door is room1.  You don't see any people or large objects."}
#door.use_text = {} #not needed for pathways.


#  Sample Object: a rock you can pick up:
rock = tgThing("ROCK")
rock.location = "ROOM1"
rock.can_pick_up = True
rock.look_text = {"default": "You look at the rock.  It is grey and hard, about the size of a baseball."}
rock.room_look_text = {"default": "There is a rock."}
rock.pick_up_text = {"default": "You pick up the rock."}
rock.use_text = {"default": "You can't think of anything to use the rock for at the moment."}
rock.drop_text = {"default": "You drop the rock.  It makes a sound like PLERK as it hits the ground."}
rock.go_to_text = {"default": "You approach the rock.  It does not respond."}

#  Sample Object: a table that remains stationary
table = tgThing("TABLE")
table.location = "ROOM2"
table.can_pick_up = False #this isn't needed because by default you can't pick up objects
table.look_text = {"default": "You are looking at a medium size table made of dark brown wood.  It is old and heavy."}
table.room_look_text = {"default": "There is a table."}
table.pick_up_text = {"default": "The table is too heavy to pick up."}
table.use_text = {"default": "You lean against the table and ponder your life choices."}
#table.drop_text = {} #not needed since you can't pick it up in the first place.
table.go_to_text = {"default": "You approach the table.  It does not react."}

#  Sublocation example:  We make "on the table" a place you can put things.
table.sublocation_hidden.append(False) #True if the user must look there before he's aware of ojects there
table.sublocation_preposition.append("ON") #this is what we look for in the user commands
table.sublocation_text.append("on the table") #this is what we parse into the output language
table.num_sublocations = len(table.sublocation_hidden) #always run this after adding a sublocation


#  Sample Transitive Object: a hammer is a transitive object.  to use it you must use it ON something.
hammer = tgThing("HAMMER")
hammer.is_transitive = True
hammer.location = "ROOM1"
hammer.can_pick_up = True
hammer.look_text = {"default": "You look at the hammer.  It is made of metal with a wooden handle."}
hammer.room_look_text = {"default": "There is a hammer."}
hammer.pick_up_text = {"default": "You pick up the hammer."}
hammer.use_text = {"default": "Thunk!",
                   "ROCK": "You carefully aim the hammer and strike the rock.  Crack!  The rock does not break."}
hammer.drop_text = {"default": "You place the hammer down."}
hammer.go_to_text = {"default": "You approach the hammer.  It does not respond."}

#add special verbs that can only be used if you have a certain object.  The dictionary returns the object name.
# The user must provide the target.
special_verbs["HAMMER"] = "HAMMER" #Now "Hammer door" is translated as "Use hammer on door"
special_verbs["SMASH"] = "HAMMER"
special_verbs["HIT"] = "HAMMER"

#other examples
special_verbs["LIGHT"] = "MATCHES"
special_verbs["ATTACK"] = "SWORD"





# ---------------------------------------------------------------------------------------------
#   Finally, this is the part where we interpret what the player typed in the command line
# ---------------------------------------------------------------------------------------------
def command_fail():
    global command_counter
    tgprint("I'm sorry. I don't understand the command you entered.")
    tg_play_sound("unsuccessful")
    command_counter -= 1 #this command didn't increment the counter.

def game():

    global command_list
    global player_location
    global object_dictionary
    global pathways_dictionary
    global command_counter

    #tg.tg_play_sound("neutral1.wav")

    #
    #       LOOK AT
    #
    if strip_off(["LOOK", "AT"]) or strip_off(["WATCH"]):
        if find_obj():
            if not object_dictionary[command_list[0]].is_location:
                # the thing we're looking at is an object, not a location.
                # if it is a pathway we modulate the description based on which location we're in
                if command_list[0] in pathways_dictionary:
                    tgprint(pathways_dictionary[command_list[0]].look_text[player_location])
                    tg_play_sound("neutral")
                else:
                    #otherwise we just print the default description:
                    tgprint(object_dictionary[command_list[0]].look_text["default"])
                    tg_play_sound("neutral")
            else:
                # look at the whole room.
                room_text = object_dictionary[command_list[0]].look_text["default"]
                for obj in object_dictionary:
                    if object_dictionary[obj].location == player_location: #this excludes the inventory
                        room_text += "\n" + object_dictionary[obj].room_look_text["default"]
                tgprint(room_text)
                tg_play_sound("neutral")
        elif command_list[0] == "INVENTORY":
            inv_text = "Here's a list of the things in your inventory:\n"
            for obj in object_dictionary:
                if object_dictionary[obj].location == "INVENTORY":
                    inv_text += obj.lower() + "\n"
            tgprint(inv_text)
            tg_play_sound("neutral")
        elif find_location():
            for obj in pathways_dictionary:
                if pathways_dictionary[obj].location == player_location and pathways_dictionary[obj].location2 == command_list[0]:
                    tgprint(pathways_dictionary[obj].look_thru_text[player_location])
                    tg_play_sound("neutral")
                    break
            else:
                command_fail()
        else:
            tgprint("I didn't recognize the name of what you're trying to look at.")
            tg_play_sound("unsuccessful")

    #
    #       PICK UP
    #
    elif strip_off(["PICK", "UP"]) or strip_off(["GET"]) or strip_off(["TAKE"]):
        if find_obj():
            if object_dictionary[command_list[0]].location != "INVENTORY":
                if object_dictionary[command_list[0]].can_pick_up:
                    object_dictionary[command_list[0]].location = "INVENTORY"
                    tg_play_sound("success")
                else:
                    tg_play_sound("unsuccessful")  # can't pick up item
                # either way there should be something here:
                tgprint(object_dictionary[command_list[0]].pick_up_text["default"])

            else:
                tgprint("You already have that.")
                tg_play_sound("unsuccessful")
        else:
            tgprint("I don't recognize the name of what you're trying to obtain.")
            tg_play_sound("unsuccessful")

    elif strip_off(["PUT", "DOWN"]) or strip_off(["DROP"]) or strip_off(["THROW", "AWAY"]):
        if find_obj():
            if object_dictionary[command_list[0]].location == "INVENTORY":
                object_dictionary[command_list[0]].location = player_location
                tgprint(object_dictionary[command_list[0]].drop_text["default"])
                tg_play_sound("neutral")
            else:
                # tried to drop something not in inventory
                tgprint("That object is not in your inventory so you can't put it down.")
                tg_play_sound("unsuccessful")
        else:
            tgprint("I don't recognize the name of what you're trying to get rid of.")
            tg_play_sound("unsuccessful")

    #
    #       TRAVEL!
    #
    elif strip_off(["GO", "TO"]) or strip_off(["WALK", "TO"]) or strip_off(["ENTER"]) or strip_off(["GO","INTO"]):
        if find_obj(): #this only searches the current location and the inventory
            if not object_dictionary[command_list[0]].is_location:
                # user said go to an object rather than a location
                tgprint(object_dictionary[command_list[0]].go_to_text["default"])
                tg_play_sound("neutral")
            else:
                # since location matches, you tried to go to where you are!
                tgprint("You are already there.")
                tg_play_sound("unsuccessful")
        elif find_location(): #next check outside the current location for other locations
            for obj in pathways_dictionary:
                if pathways_dictionary[obj].location == player_location and pathways_dictionary[obj].location2 == command_list[0] and pathways_dictionary[obj].pathway_open:
                    #found a way in so
                    #put player in new location
                    player_location = command_list[0]
                    tgprint(object_dictionary[command_list[0]].go_to_text["default"])
                    tg_play_sound("success")
                    #switch locations on pathway objects with location2 = new location
                    for pathway in pathways_dictionary:
                        if pathways_dictionary[pathway].location2 == player_location:
                            pathways_dictionary[pathway].switch()
                    break
            else:
                #this is skipped if we found a way in through any pathway.
                tgprint("I recognize the place you mentioned but you can't get there from here.")
                tg_play_sound("unsuccessful")
        else:
            tgprint("I'm sorry, I don't recognize the name of where you're trying to go.")
            tg_play_sound("unsuccessful")

#
#       USE AN OBJECT!
#
    elif strip_off(["USE"]):
        if find_obj():# and object_dictionary[command_list[0]].location == "INVENTORY":
            object1 = command_list[0]
            #if object_dictionary[object1].can_pick_up:
                #object_dictionary[object1].location = "INVENTORY" #the silent pick up
            del command_list[0]
            if object_dictionary[object1].is_transitive:
                if object_dictionary[object1].location == "INVENTORY":
                    if strip_off(["ON"]) or strip_off(["WITH"]):
                        if find_obj():
                            object2 = command_list[0]
                            if object2 in object_dictionary[object1].use_text:
                                tgprint(object_dictionary[object1].use_text[object2])
                                tg_play_sound("neutral")
                            else:
                                tgprint(object_dictionary[object1].use_text["default"])
                                tg_play_sound("neutral")
                        else:
                            tgprint("I don't recognize the target of that action.")
                            tg_play_sound("unsuccessful")
                    else:
                        tgprint("That object needs a target (a direct object) to be used.  Try using it 'on' or 'with' something else that is present.")
                        tg_play_sound("unsuccessful")
                else:
                    tgprint("You need to pick up that object to use it.")
                    tg_play_sound("unsuccessful")
            else:
                #object doesn't need a target to be used, so we just print the use text
                if object1 in pathways_dictionary:
                    #we're going to retranslate "use door" as "go to door's second location:
                    command_list = ["GO","TO",pathways_dictionary[object1].location2]
                    game()
                else:
                    tgprint(object_dictionary[object1].use_text["default"])
                    tg_play_sound("neutral")
        else:
            tgprint("I don't recognize what object you're trying to use.")
            tg_play_sound("unsuccessful")

    #
    #   SPECIAL VERBS
    #
    elif len(command_list) and command_list[0] in special_verbs:
        object1 = special_verbs[command_list[0]]
        del command_list[0]
        if find_obj():
            object2 = command_list[0]
            command_list = ["USE",object1,"WITH",object2]
            game()
        else:
            if object_dictionary[object1].location == "INVENTORY":
                tgprint("That command needs a target (a direct object).  Try again with one of the objects that is present.")
                tg_play_sound("unsuccessful")
            else:
                #I'm not totally happy with this error message because it could be used as a clue... Hmm...
                tgprint("You cannot use that command because you don't have the appropriate object in your inventory.")
                tg_play_sound("unsuccessful")

    #
    #   MISC
    #
    elif strip_off(["LOOK","AROUND"]):
        command_list = ["LOOK","AT","ROOM"]
        game()
    elif strip_off(["LOOK","THROUGH"]) or strip_off(["PEER","THROUGH"]):
        if find_obj() and command_list[0] in pathways_dictionary:
            tgprint(pathways_dictionary[command_list[0]].look_thru_text[player_location])
            tg_play_sound("neutral")
        else:
            tgprint("You can generally only look through pathways that lead to other locations (such as doorways.)")
            tg_play_sound("unsuccessful")

    elif strip_off(["GO","THROUGH"]) or strip_off(["PASS","THROUGH"]):
        if find_obj():
            if command_list[0] in pathways_dictionary:
                command_list = ["USE",command_list[0]]
                game()
            else:
                command_fail()
        else:
            command_fail()

#
#   TOTAL FAIL
#
    elif len(command_list): #We check this so that an accidental enter key doesn't erase what's on the screen.
            command_fail()
    else:
        #only executes if there's no text on the command line:
        command_counter -= 1 #cancel out timer increment





#
#
#
#
# leave this command last:
tg.go()
