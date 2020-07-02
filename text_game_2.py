import tg_gui
from game import Thing, Place, Pathway


# some initial values
game_name = "test game name"
sound_toggle = False
progress = set()  # you can add values here to keep track of the player's progress through the game. might change how game progress works later when I tackle that.
object_dictionary = dict()
pathways_dictionary = dict()
player_location = "ROOM1"  # name of the starting location
help_text = "HELP:\n\nThis is a text-based game. You can play by entering commands in the command line.  Common " \
            "commands are phrases like 'look at', 'pick up', or 'use'. Most commands need an object. Try typing 'Look" \
            " at room'.  \n\n'mute' or 'unmute' will turn the game sounds on or off."
about_text = "The About button prints this."
command_list = [] #each command entered by the player goes here and then we analyze it.
special_verbs = dict()
command_counter = 0 #this increments with each semi-successful command.

#this can be used to set up events that occur after a certain number of commands.  The wait command will advance the
#command counter until the next event in the scheduled events dictionary.
scheduled_events = dict()

# this is a function that returns a boolean value if a certain object is present
def is_present(obj_name):
    if object_dictionary[obj_name].location == player_location or object_dictionary[obj_name].location == "INVENTORY":
        return True
    else:
        return False

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



# ---------------------------------------------------------------------------------------------
#  Game Objects and Locations
# ---------------------------------------------------------------------------------------------
#  Sample Location 1:
room1 = Place("ROOM1")
#the object room1 will rarely be used by that handle.  instead we call it with object_dictionary("ROOM1")
room1.look_text = {"default": "You look at room number 1.  It's pretty simple."}
#room1.room_look_text = {"default": ""}  # Not needed for locations
room1.pick_up_text = {"default": "You would like to pick up the room but it's kinda too big."}
room1.use_text = {"default": "You are using the room as a room to stand in I guess."}
#room1.drop_text = {"default": ""}  # This is only needed if you can put it in your inventory.
room1.go_to_text = {"default": "You enter room # 1."}
object_dictionary[room1.name] = room1

#  Sample Location 2:
room2 = Place("ROOM2")
room2.look_text = {"default": "You look at room number 2.  It's pretty simple."}
#room2.room_look_text = {"default": ""}  # Not needed for locations
room2.pick_up_text = {"default": "You would like to pick up the room but it's kinda too big."}
room2.use_text = {"default": "You are using the room as a room to stand in I guess."}
#room2.drop_text = {"default": ""}  # This is only needed if you can put it in your inventory.
room2.go_to_text = {"default": "You enter room # 2."}
object_dictionary[room2.name] = room2

# list connections between locations here. (DNU! old way)
#connections = [{"ROOM1", "ROOM2"}]

#sample doorway:
door = Pathway("DOOR")
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
object_dictionary[door.name] = door
pathways_dictionary[door.name] = door


#  Sample Object: a rock you can pick up:
rock = Thing("ROCK")
rock.location = "ROOM1"
rock.can_pick_up = True
rock.look_text = {"default": "You look at the rock.  It is grey and hard, about the size of a baseball."}
rock.room_look_text = {"default": "There is a rock."}
rock.pick_up_text = {"default": "You pick up the rock."}
rock.use_text = {"default": "You can't think of anything to use the rock for at the moment."}
rock.drop_text = {"default": "You drop the rock.  It makes a sound like PLERK as it hits the ground."}
rock.go_to_text = {"default": "You approach the rock.  It does not respond."}
object_dictionary[rock.name] = rock


#  Sample Object: a table that remains stationary
table = Thing("TABLE")
table.location = "ROOM2"
table.can_pick_up = False #this isn't needed because by default you can't pick up objects
table.look_text = {"default": "You are looking at a medium size table made of dark brown wood.  It is old and heavy."}
table.room_look_text = {"default": "There is a table."}
table.pick_up_text = {"default": "The table is too heavy to pick up."}
table.use_text = {"default": "You lean against the table and ponder your life choices."}
#table.drop_text = {} #not needed since you can't pick it up in the first place.
table.go_to_text = {"default": "You approach the table.  It does not react."}
object_dictionary[table.name] = table

#  Sublocation example:  We make "on the table" a place you can put things.
table.sublocation_hidden.append(False) #True if the user must look there before he's aware of ojects there
table.sublocation_preposition.append("ON") #this is what we look for in the user commands
table.sublocation_text.append("on the table") #this is what we parse into the output language
table.num_sublocations = len(table.sublocation_hidden) #always run this after adding a sublocation


#  Sample Transitive Object: a hammer is a transitive object.  to use it you must use it ON something.
hammer = Thing("HAMMER")
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
object_dictionary[hammer.name] = hammer

#add special verbs that can only be used if you have a certain object.  The dictionary returns the object name.
# The user must provide the target.
special_verbs["HAMMER"] = "HAMMER" #Now "Hammer door" is translated as "Use hammer on door"
special_verbs["SMASH"] = "HAMMER"
special_verbs["HIT"] = "HAMMER"

#other examples
special_verbs["LIGHT"] = "MATCHES"
special_verbs["ATTACK"] = "SWORD"


def game_func(command_input):
    # this function receives the input and returns a text output to display.
    global player_location
    global object_dictionary
    global pathways_dictionary
    global command_counter
    global sound_toggle

    def tot_fail():
        nonlocal console_output
        nonlocal output_type
        #couldn't understand the command at all
        console_output += "I'm sorry, I didn't understand the command."
        output_type = "unsuccessful"

    previous_output = console_output #not sure if this works yet
    command_counter += 1 #gets reversed later if the command is invalid.
    console_output = "" #everything below adds to this and then it gets returned.
    output_type = "neutral" #default response.
    command_list = command_input.upper().replace(".", "").replace(",", "").split()
    command_list[:] = [x for x in command_list if x not in ["A", "THE"]]  # remove fluff
    loop_again = True
    while loop_again:
        loop_again = False



    if output_type == "unsuccessful":
        command_counter -= 1 #back out the increment since we didn't understand it.

    #play sound based on output type:
    if sound_toggle:
        tg_gui.play_sound(tg, output_type)

    #finally send the output text to the GUI
    return console_output




#
#
#
# This stuff goes last:
tg = tg_gui.setup_gui(game_name,help_text,about_text,game_func)
tg.go()
