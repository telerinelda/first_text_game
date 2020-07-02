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
console_output = ""

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


#--------------------------------------------------------------------------------
#
#          The Game Function
#
#--------------------------------------------------------------------------------
def game_func(command_input):
    # this function receives the input and returns a text output to display.
    global player_location
    global object_dictionary
    global pathways_dictionary
    global command_counter
    global sound_toggle
    global command_list
    global console_output

    def tot_fail():
        global console_output
        nonlocal output_type
        #couldn't understand the command at all
        console_output += "I'm sorry, I didn't understand the command."
        output_type = "unsuccessful"

    if len(command_input): #hoping that skipping this on an errant entry key will reprint the same message as previous
        command_counter += 1 #gets reversed later if the command is invalid.
        console_output = "" #everything below adds to this and then it gets returned.
        output_type = "neutral" #default response.
        command_list = command_input.upper().replace(".", "").replace(",", "").split()
        command_list[:] = [x for x in command_list if x not in ["A", "THE"]]  # remove fluff
        loop_again = True
        while loop_again:
            loop_again = False #sometimes we'll set this to True below if we need to retranslate the command.

            #
            #       LOOK AT
            #
            if strip_off(["LOOK", "AT"]) or strip_off(["WATCH"]):
                if find_obj():
                    if not object_dictionary[command_list[0]].is_location:
                        # the thing we're looking at is an object, not a location.
                        # if it is a pathway we modulate the description based on which location we're in
                        if command_list[0] in pathways_dictionary:
                            console_output += pathways_dictionary[command_list[0]].look_text[player_location]
                        else:
                            # otherwise we just print the default description:
                            console_output += object_dictionary[command_list[0]].look_text["default"])
                    else:
                        # we're looking at a location
                        console_output += object_dictionary[command_list[0]].look_text["default"]
                        for obj in object_dictionary:
                            if object_dictionary[obj].location == player_location:  # this excludes the inventory
                                console_output += "\n"
                                console_output += object_dictionary[obj].room_look_text["default"]
                            elif command_list[0] == "INVENTORY":
                                console_output += "Here's a list of the things in your inventory:\n"
                                for obj in object_dictionary:
                                    if object_dictionary[obj].location == "INVENTORY":
                                        console_output += obj.lower()
                                        console_output += "\n"
                elif find_location():
                    #we're looking at a location that is not the player location.
                    for obj in pathways_dictionary:
                        if pathways_dictionary[obj].location == player_location and pathways_dictionary[obj].location2 == command_list[0]:
                            #found a pathway to that place so we can in fact look at it.
                            console_output += pathways_dictionary[obj].look_thru_text[player_location]
                            break #stop looking for a path since we found one.
                    else:
                        #tried to look at a location we don't have a direct pathway to
                        tot_fail()
                else:
                    console_output += "I didn't recognize the name of what you're trying to look at.")

            #
            #       PICK UP
            #
            elif strip_off(["PICK", "UP"]) or strip_off(["GET"]) or strip_off(["TAKE"]):
                if find_obj():
                    if object_dictionary[command_list[0]].location != "INVENTORY":
                        if object_dictionary[command_list[0]].can_pick_up:
                            object_dictionary[command_list[0]].location = "INVENTORY"
                        else:
                            pass
                        # either way there should be something here:
                        console_output += object_dictionary[command_list[0]].pick_up_text["default"]
                    else:
                        #tried to pick up something in the inventory.
                        console_output += "You already have that."
                else:
                    console_output += "I don't recognize the name of what you're trying to obtain.")

            #
            #       DROP
            #
            elif strip_off(["PUT", "DOWN"]) or strip_off(["DROP"]) or strip_off(["THROW", "AWAY"]):
                if find_obj():
                    if object_dictionary[command_list[0]].location == "INVENTORY":
                        object_dictionary[command_list[0]].location = player_location
                        console_output += object_dictionary[command_list[0]].drop_text["default"]
                    else:
                        # tried to drop something not in inventory
                        console_output += "That object is not in your inventory so you can't put it down."
                else:
                    console_output += "I don't recognize the name of what you're trying to get rid of.")

            #
            #       TRAVEL!
            #
            elif strip_off(["GO", "TO"]) or strip_off(["WALK", "TO"]) or strip_off(["ENTER"]) or strip_off(["GO", "INTO"]) or strip_off(["APPROACH"]):
                if find_obj():  # this only searches the current location and the inventory
                    if not object_dictionary[command_list[0]].is_location:
                       # user said go to an object rather than a location
                       console_output += object_dictionary[command_list[0]].go_to_text["default"]
                    else:
                        # since location matches, you tried to go to where you are!
                        console_output += "You are already there.")
                elif find_location():  # next check outside the current location for other locations
                    for obj in pathways_dictionary:
                        if pathways_dictionary[obj].location == player_location and pathways_dictionary[obj].location2 == command_list[0] and pathways_dictionary[obj].pathway_open:
                            # found a way in so
                            # put player in new location
                            player_location = command_list[0]
                            console_output += object_dictionary[command_list[0]].go_to_text["default"]
                            # switch locations on pathway objects with location2 = new location
                            for pathway in pathways_dictionary:
                                if pathways_dictionary[pathway].location2 == player_location:
                                    pathways_dictionary[pathway].switch()
                            break
                    else:
                        # this is skipped if we found a way in through any pathway.
                        console_output += "I recognize the place you mentioned but you can't get there from here."

                else:
                    console_output += "I'm sorry, I don't recognize the name of where you're trying to go.")

            #
            #       USE AN OBJECT!
            #
            elif strip_off(["USE"]):
                if find_obj():  # and object_dictionary[command_list[0]].location == "INVENTORY":
                    object1 = command_list[0]
                    # if object_dictionary[object1].can_pick_up:
                        # object_dictionary[object1].location = "INVENTORY" #the silent pick up
                    del command_list[0]
                    if object_dictionary[object1].is_transitive:
                        if object_dictionary[object1].location == "INVENTORY":
                            if strip_off(["ON"]) or strip_off(["WITH"]):
                                if find_obj():
                                    object2 = command_list[0]
                                    if object2 in object_dictionary[object1].use_text:
                                        console_output += object_dictionary[object1].use_text[object2]
                                    else:
                                        #no designated use text for the target
                                        console_output += object_dictionary[object1].use_text["default"]
                                else:
                                    console_output += "I don't recognize the target of that action."
                            else:
                                console_output += "That object needs a target (a direct object) to be used.  Try using it 'on' or 'with' something else that is present."
                        else:
                            console_output += "You need to pick up that object to use it."
                    else:
                        # object doesn't need a target to be used, so we just print the use text
                        if object1 in pathways_dictionary:
                            # we're going to retranslate "use door" as "go to door's second location:
                            command_list = ["GO", "TO", pathways_dictionary[object1].location2]
                            loop_again = True
                        else:
                            console_output += object_dictionary[object1].use_text["default"]
                else:
                    console_output += "I don't recognize what object you're trying to use.")










            #LEFT OFF HERE








            #
            #   SPECIAL VERBS
            #
            elif len(command_list) and command_list[0] in special_verbs:
                object1 = special_verbs[command_list[0]]
                del command_list[0]
                if find_obj():
                    object2 = command_list[0]
                command_list = ["USE", object1, "WITH", object2]
                loop_again = True
                else:
                if object_dictionary[object1].location == "INVENTORY":
                    console_output += "That command needs a target (a direct object).  Try again with one of the objects that is present.")

                else:
                # I'm not totally happy with this error message because it could be used as a clue... Hmm...
                console_output += "You cannot use that command because you don't have the appropriate object in your inventory.")

                #
                #   MISC
                #
                elif strip_off(["LOOK", "AROUND"]):
                command_list = ["LOOK", "AT", "ROOM"]
                loop_again = True
                elif strip_off(["LOOK", "THROUGH"]) or strip_off(["PEER", "THROUGH"]):
                if find_obj() and command_list[0] in pathways_dictionary:
                    console_output += pathways_dictionary[command_list[0]].look_thru_text[player_location])
                else:
                console_output += "You can generally only look through pathways that lead to other locations (such as doorways.)")

                elif strip_off(["GO", "THROUGH"]) or strip_off(["PASS", "THROUGH"]):
                if find_obj():
                    if
                command_list[0] in pathways_dictionary:
                command_list = ["USE", command_list[0]]
                loop_again = True
                else:
                tot_fail()
                else:
                tot_fail()
                elif strip_off(["HELP"]):
                press("   Help   ")
                command_counter -= 1  # cancel out timer increment
                elif strip_off(["ABOUT"]):
                press("   About   ")
                command_counter -= 1  # cancel out timer increment
                elif strip_off(["MUTE"]) or strip_off(["TURN", "SOUND", "OFF"]) or strip_off(["TURN", "SOUNDS", "OFF"]):
                sound_toggle = False
                console_output += "Game sounds have been turned off."
                command_counter -= 1  # cancel out timer increment
                elif strip_off(["UNMUTE"]) or strip_off(["TURN", "SOUND", "ON"]) or strip_off(["TURN", "SOUNDS", "ON"]):
                sound_toggle = True
                console_output += "Game sounds have been turned on."
                command_counter -= 1  # cancel out timer increment

                #
                #   TOTAL FAIL
                #
                elif len(command_list):  # We check this so that an accidental enter key doesn't erase what's on the screen.
                tot_fail()
                else:
                # only executes if there's no text on the command line:
                command_counter -= 1  # cancel out timer increment

                if output_type == "unsuccessful":
            command_counter -= 1 #back out the increment since we didn't understand it.

        #play sound based on output type:
        if sound_toggle:
            tg_gui.play_sound(tg, output_type)

    #some debugging stuff
    print(command_input)
    print(command_list)
    print("count: ", command_counter)
    print(console_output)

    #finally send the output text to the GUI
    return console_output
#
#
#
# This stuff goes last:
tg = tg_gui.setup_gui(game_name,game_func)
tg.go()
