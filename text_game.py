from game import Thing, Place, Pathway
from game import tg_gui
from game import gameState, add_object_data

gs = gameState() #load the initial values for a new game.
gs = add_object_data(gs)

#--------------------------------------------------------------------------------
#
#          The Game Function
#
#--------------------------------------------------------------------------------
def game_func(command_input):
    # this function receives the input and returns a text output to display.

    global gs

    def tot_fail():
        #global gs.console_output
        nonlocal output_type
        #couldn't understand the command at all
        gs.console_output += "I'm sorry, I didn't understand the command."
        output_type = "unsuccessful"

    if len(command_input): #skipping this on an errant entry key will reprint the same message as previous
        gs.command_counter += 1 #gets reversed later if the command is invalid.
        gs.console_output = "" #everything below adds to this and then it gets returned.
        output_type = "neutral" #default response type.
        gs.command_list = gs.replacements(command_input.upper().replace(".", "").replace(",", "").split())
        gs.command_list[:] = [x for x in gs.command_list if x not in ["A", "THE", "MY", "THIS"]]  # remove fluff
        loop_again = True
        while loop_again:
            loop_again = False #sometimes we'll set this to True below if we need to retranslate the command.

            #
            #       LOOK AT
            #
            if gs.strip_off(["LOOK", "AT"]) or gs.strip_off(["WATCH"]):
                if len(gs.command_list) and gs.find_obj():
                    if not gs.object_dictionary[gs.command_list[0]].is_location:
                        # the thing we're looking at is an object, not a location.
                        # if it is a pathway we modulate the description based on which location we're in
                        if gs.command_list[0] in gs.pathways_dictionary:
                            gs.console_output += gs.pathways_dictionary[gs.command_list[0]].look_text[gs.player_location]
                        else:
                            # here we're looking at an object that isn't a location or a pathway.
                            # the final check: is it hidden in a sublocation?
                            if gs.object_dictionary[gs.command_list[0]].is_hidden(gs):
                                #It's important this matches the error message below
                                # for when the object name isn't recognized at all!
                                #the object is present but hidden. we don't want to tip off the user...
                                gs.console_output += "I didn't recognize the name of what you're trying to look at."
                                output_type = "unsuccessful"
                            else:
                                #standard output for looking at an object.
                                gs.console_output += gs.object_dictionary[gs.command_list[0]].look_text["default"]
                    else:
                        # we're looking at a location
                        gs.console_output += gs.object_dictionary[gs.command_list[0]].look_text["default"]
                        look_subs = []
                        gs.console_output += "\n"
                        for obj in gs.object_dictionary:
                            if gs.object_dictionary[obj].location == gs.player_location and gs.object_dictionary[obj].sublocation == []:
                                # this excludes the inventory and objects in sublocations.
                                gs.console_output += "\n"
                                gs.console_output += gs.object_dictionary[obj].room_look_text["default"]
                            #now we're going to build a collection of the sublocations that need to be mentioned.
                            if gs.object_dictionary[obj].location == gs.player_location and gs.object_dictionary[obj].sublocation != [] and not gs.object_dictionary[obj].is_hidden(gs):
                                if gs.object_dictionary[obj].sublocation not in look_subs:
                                    look_subs.append(gs.object_dictionary[obj].sublocation)
                        for sub in look_subs:
                            #now list the sublocated objects by sublocation
                            gs.console_output += "\n\n"
                            sub_owner = sub[0]
                            sub_prep = sub[1]
                            sub_i = gs.object_dictionary[sub_owner].sublocation_index(sub_prep)
                            gs.console_output += gs.object_dictionary[sub_owner].sublocation_text + ":"
                            for obj in gs.object_dictionary:
                                if gs.object_dictionary[obj].sublocation == [sub_owner,sub_prep]:
                                    gs.console_output += "\n"
                                    gs.console_output += gs.object_dictionary[obj].room_look_text["default"]

                elif len(gs.command_list) and gs.command_list[0] == "INVENTORY":
                    gs.console_output += "Here's a list of the things in your inventory:\n"
                    for obj in gs.object_dictionary:
                        if gs.object_dictionary[obj].location == "INVENTORY":
                            gs.console_output += obj.lower()
                            gs.console_output += "\n"
                elif gs.find_location():
                    #we're looking at a location that is not the player location.
                    for obj in gs.pathways_dictionary:
                        if gs.pathways_dictionary[obj].location == gs.player_location and gs.pathways_dictionary[obj].location2 == gs.command_list[0]:
                            #found a pathway to that place so we can in fact look at it.
                            gs.console_output += gs.pathways_dictionary[obj].look_thru_text[gs.player_location]
                            break #stop looking for a path since we found one.
                    else:
                        #tried to look at a location we don't have a direct pathway to
                        tot_fail()
                else:
                    gs.console_output += "I didn't recognize the name of what you're trying to look at."
                    output_type = "unsuccessful"
            elif gs.strip_off(["LOOK"]) or gs.strip_off(["PEER"]):
                if gs.strip_off(["AROUND"]):
                    gs.command_list = ["LOOK", "AT", "ROOM"]
                    loop_again = True
                elif gs.strip_off(["THROUGH"]):
                    if gs.find_obj() and gs.command_list[0] in gs.pathways_dictionary:
                        gs.console_output += gs.pathways_dictionary[gs.command_list[0]].look_thru_text[
                        gs.player_loation]
                    else:
                        gs.console_output += "You can generally only look through pathways that lead to other locations (such as doorways.)"
                        output_type = "unsuccessful"
                elif gs.strip_off(["IN","INVENTORY"]):
                    gs.command_list = ["LOOK","AT","INVENTORY"]
                    loop_again = True
                elif len(gs.command_list):
                    sub_prep = gs.command_list[0]
                    del gs.command_list[0]
                    if gs.find_obj():
                        sub_owner = gs.command_list[0]
                        if sub_prep in gs.object_dictionary[sub_owner].sublocation_preposition:
                            sub_i = gs.object_dictionary[sub_owner].sublocation_index(sub_prep)
                            gs.object_dictionary[sub_owner].sublocation_hidden = False
                            gs.console_output += "You look "
                            gs.console_output += gs.object_dictionary[sub_owner].sublocation_text.lower()
                            gs.console_output += "."
                            find_count = 0
                            for obj in gs.object_dictionary:
                                if gs.object_dictionary[obj].sublocation == [sub_owner,sub_prep]:
                                    find_count += 1
                                    gs.console_output += "\n"
                                    gs.console_output += gs.object_dictionary[obj].room_look_text["default"]
                            if find_count == 0:
                                gs.console_output += "\nThere doesn't seem to be anything there."
                        else:
                            gs.console_output += "I didn't recognize what you're trying to look at."
                            output_type = "unsuccessful"
                    else:
                        gs.console_output += "I didn't recognize what you're trying to look at."
                        output_type = "unsuccessful"
                else:
                    gs.console_output += "I didn't recognize what you're trying to look at."
                    output_type = "unsuccessful"



            #
            #       PICK UP
            #
            elif gs.strip_off(["PICK", "UP"]) or gs.strip_off(["GET"]) or gs.strip_off(["TAKE"]):
                if gs.find_obj() and not gs.object_dictionary[gs.command_list[0]].is_hidden(gs):
                    if gs.object_dictionary[gs.command_list[0]].location != "INVENTORY":
                        if gs.object_dictionary[gs.command_list[0]].can_pick_up:
                            gs.object_dictionary[gs.command_list[0]].location = "INVENTORY"
                            gs.object_dictionary[gs.command_list[0]].sublocation = []
                            output_type = "success"
                        else:
                            output_type = "unsuccessful"
                        # either way there should be something here:
                        gs.console_output += gs.object_dictionary[gs.command_list[0]].pick_up_text["default"]
                    else:
                        #tried to pick up something in the inventory.
                        gs.console_output += "You already have that."
                        output_type = "unsuccessful"
                else:
                    gs.console_output += "I don't recognize the name of what you're trying to obtain."
                    output_type = "unsuccessful"


            #
            #       DROP
            #
            elif gs.strip_off(["PUT", "DOWN"]) or gs.strip_off(["DROP"]) or gs.strip_off(["THROW", "AWAY"]):
                if gs.find_obj():
                    if gs.object_dictionary[gs.command_list[0]].location == "INVENTORY":
                        gs.object_dictionary[gs.command_list[0]].location = gs.player_location
                        gs.console_output += gs.object_dictionary[gs.command_list[0]].drop_text["default"]
                    else:
                        # tried to drop something not in inventory
                        gs.console_output += "That object is not in your inventory so you can't put it down."
                        output_type = "unsuccessful"
                else:
                    gs.console_output += "I don't recognize the name of what you're trying to get rid of."
                    output_type = "unsuccessful"
            elif gs.strip_off(["PUT"]) or gs.strip_off(["PLACE"]):
                if gs.find_obj():
                    if gs.object_dictionary[gs.command_list[0]].location == "INVENTORY":
                        obj = gs.command_list[0]
                        del gs.command_list[0]
                        if gs.strip_off(["DOWN"]):
                            gs.command_list = ["DROP",obj]
                            loop_again = True
                        else:
                            sub_prep = gs.command_list[0]
                            del gs.command_list[0]
                            if gs.find_obj():
                                sub_owner = gs.command_list[0]
                                if sub_prep in gs.object_dictionary[sub_owner].sublocation_preposition:
                                    #we are putting the object down in a sublocation.
                                    sub_i = gs.object_dictionary[sub_owner].sublocation_index(sub_prep)
                                    gs.object_dictionary[obj].location = gs.player_location
                                    gs.object_dictionary[obj].sublocation = [sub_owner,sub_prep]
                                    gs.console_output += "You place the "
                                    gs.console_output += obj.lower()
                                    gs.console_output += " "
                                    gs.console_output += gs.object_dictionary[sub_owner].sublocation_text.lower()
                                    gs.console_output += "."
                                else:
                                    gs.console_output += "I don't recognize where you want to put that."
                                    output_type = "unsuccessful"
                            else:
                                gs.console_output += "I don't recognize where you want to put that."
                                output_type = "unsuccessful"
                    else:
                        gs.console_output += "You don't have that in your inventory so you can't place it somewhere."
                        output_type = "unsuccessful"
                else:
                    tot_fail()



            #
            #       TRAVEL!
            #
            elif gs.strip_off(["GO", "TO"]) or gs.strip_off(["WALK", "TO"]) or gs.strip_off(["ENTER"]) or gs.strip_off(["GO", "INTO"]) or gs.strip_off(["APPROACH"]) or gs.strip_off(["GOTO"]):
                if gs.find_obj():  # this only searches the current location and the inventory
                    if not gs.object_dictionary[gs.command_list[0]].is_location:
                       # user said go to an object rather than a location
                       gs.console_output += gs.object_dictionary[gs.command_list[0]].go_to_text["default"]
                    else:
                        # since location matches, you tried to go to where you are!
                        gs.console_output += "You are already there."
                        output_type = "unsuccessful"
                elif gs.find_location():  # next check outside the current location for other locations
                    for obj in gs.pathways_dictionary:
                        if gs.pathways_dictionary[obj].location == gs.player_location and gs.pathways_dictionary[obj].location2 == gs.command_list[0] and gs.pathways_dictionary[obj].pathway_open:
                            # found a way in so
                            # put player in new location
                            gs.player_location = gs.command_list[0]
                            output_type = "success"
                            gs.console_output += gs.object_dictionary[gs.command_list[0]].go_to_text["default"]
                            # switch locations on pathway objects with location2 = new location
                            for pathway in gs.pathways_dictionary:
                                if gs.pathways_dictionary[pathway].location2 == gs.player_location:
                                    gs.pathways_dictionary[pathway].switch()
                            break #this break causes us to skip the for:else clause immediately following.
                    else:
                        # this is skipped if we found a way in through any pathway.
                        gs.console_output += "I recognize the place you mentioned but you can't get there from here."
                        output_type = "unsuccessful"
                else:
                    gs.console_output += "I'm sorry, I don't recognize the name of where you're trying to go."
                    output_type = "unsuccessful"

            #
            #       USE AN OBJECT!
            #
            elif gs.strip_off(["USE"]):
                if gs.find_obj():  # and gs.object_dictionary[gs.command_list[0]].location == "INVENTORY":
                    object1 = gs.command_list[0]
                    # if gs.object_dictionary[object1].can_pick_up:
                        # gs.object_dictionary[object1].location = "INVENTORY" #the silent pick up
                    del gs.command_list[0]
                    if gs.object_dictionary[object1].is_transitive:
                        if gs.object_dictionary[object1].location == "INVENTORY":
                            if gs.strip_off(["ON"]) or gs.strip_off(["WITH"]):
                                if gs.find_obj():
                                    object2 = gs.command_list[0]
                                    if object2 in gs.object_dictionary[object1].use_text:
                                        gs.console_output += gs.object_dictionary[object1].use_text[object2]
                                        output_type = "success"
                                        #This is a place where it's likely that progress points are established.
                                        #Here's an example:
                                        if object1 == "HAMMER" and object2 == "ROCK":
                                            gs.progress.add("hit rock")
                                            gs.object_dictionary["ROCK"].location = "NOWHERE"
                                            output_type = "zelda"
                                    else:
                                        #no designated use text for the target
                                        gs.console_output += gs.object_dictionary[object1].use_text["default"]
                                else:
                                    gs.console_output += "I don't recognize the target of that action."
                                    output_type = "unsuccessful"
                            else:
                                gs.console_output += "That object needs a target (a direct object) to be used.  Try using it 'on' or 'with' something else that is present."
                                output_type = "unsuccessful"
                        else:
                            gs.console_output += "You need to pick up that object to use it."
                            output_type = "unsuccessful"
                    else:
                        # object doesn't need a target to be used, so we just print the use text
                        if object1 in gs.pathways_dictionary:
                            # we're going to retranslate "use door" as "go to door's second location:
                            gs.command_list = ["GO", "TO", gs.pathways_dictionary[object1].location2]
                            loop_again = True
                        else:
                            gs.console_output += gs.object_dictionary[object1].use_text["default"]
                else:
                    gs.console_output += "I don't recognize what object you're trying to use."
                    output_type = "unsuccessful"

            #
            #   SPECIAL VERBS
            #
            elif len(gs.command_list) and gs.command_list[0] in gs.special_verbs:
                object1 = gs.special_verbs[gs.command_list[0]]
                del gs.command_list[0]
                if gs.find_obj():
                    object2 = gs.command_list[0]
                    gs.command_list = ["USE", object1, "WITH", object2]
                    loop_again = True
                else:
                    #did not find target
                    if gs.object_dictionary[object1].location == "INVENTORY":
                        gs.console_output += "That command needs a target (a direct object).  Try again with one of the objects that is present."
                        output_type = "unsuccessful"
                    else:
                        # Got rid of the below error message because it's potentially a clue to the player.
                        #gs.console_output += "You cannot use that command because you don't have the appropriate object in your inventory.")
                        #instead:
                        tot_fail()

            #
            #   MISC
            #

            elif gs.strip_off(["GO", "THROUGH"]) or gs.strip_off(["PASS", "THROUGH"]):
                if gs.find_obj():
                    if gs.command_list[0] in gs.pathways_dictionary:
                        gs.command_list = ["USE", gs.command_list[0]]
                        loop_again = True
                    else:
                        tot_fail()
                else:
                    tot_fail()

            elif gs.strip_off(["HELP"]):
                gs.console_output += gs.help_text
                gs.command_counter -= 1
            elif gs.strip_off(["ABOUT"]):
                gs.console_output += gs.about_text
                gs.command_counter -= 1
            elif gs.strip_off(["EXIT","GAME"]):
                gs.console_output = "EXIT" #The GUI checks for this and will kill the application.
            elif gs.strip_off(["EXIT"]):
                gs.console_output += "To exit the game itself, you must type 'exit game'."
                output_type = "unsuccessful"
            elif gs.strip_off(["RESTART","GAME"]):
                gs = gameState()  # load the initial values for a new game.
                gs = add_object_data(gs)
                gs.console_output = "Restarting Game....\n\n"
                gs.console_output += gs.game_opening_text
            elif gs.strip_off(["RESTART"]):
                gs.console_output += "To restart the game itself, you must type 'restart game'."
                output_type = "unsuccessful"
            elif gs.strip_off(["MUTE"]) or gs.strip_off(["TURN", "SOUND", "OFF"]) or gs.strip_off(["TURN", "SOUNDS", "OFF"]):
                gs.sound_toggle = False
                gs.console_output += "Game sounds have been turned off."
                gs.command_counter -= 1  # cancel out timer increment
            elif gs.strip_off(["UNMUTE"]) or gs.strip_off(["TURN", "SOUND", "ON"]) or gs.strip_off(["TURN", "SOUNDS", "ON"]):
                gs.sound_toggle = True
                output_type = "success"
                gs.console_output += "Game sounds have been turned on."
                gs.command_counter -= 1  # cancel out timer increment
            elif gs.strip_off(["WAIT"]):
                if len(gs.scheduled_events):
                    gs.command_counter = min(gs.scheduled_events.keys())
                gs.console_output += gs.wait_text

            else:
                tot_fail()

        #just exited while loop
        if output_type == "unsuccessful":
            gs.command_counter -= 1 #back out the increment since we didn't understand it.

        #play sound based on output type:
        if gs.sound_toggle:
            tg_gui.play_sound(tg, output_type)

        if gs.command_counter in gs.scheduled_events:
            #custom code for events here.
            if gs.scheduled_events[gs.command_counter] == "RUMBLE":
                gs.console_output += "\n\nA distant rumble threatens..."
            del gs.scheduled_events[gs.command_counter] #always remove them after they are executed.

    #some debugging stuff
    #print(command_input)
    #print(gs.command_list)
    print("count: ", gs.command_counter)
    #print(gs.console_output)

    #finally send the output text to the GUI
    return gs.console_output
#
#
#
# This stuff goes last:
tg = tg_gui.setup_gui(gs.game_name, game_func,gs.game_opening_text)

tg.go()
