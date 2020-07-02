
    #
    #       LOOK AT
    #
    if strip_off(["LOOK", "AT"]) or strip_off(["WATCH"]):
        if find_obj():
            if not object_dictionary[command_list[0]].is_location:
                # the thing we're looking at is an object, not a location.
                # if it is a pathway we modulate the description based on which location we're in
                if command_list[0] in pathways_dictionary:
                    console_output +=pathways_dictionary[command_list[0]].look_text[player_location]
                else:
                    #otherwise we just print the default description:
                    console_output +=object_dictionary[command_list[0]].look_text["default"])
            else:
                # look at the whole room.
                room_text = object_dictionary[command_list[0]].look_text["default"]
                for obj in object_dictionary:
                    if object_dictionary[obj].location == player_location: #this excludes the inventory
                        room_text += "\n" + object_dictionary[obj].room_look_text["default"]
                console_output +=room_text)
        elif command_list[0] == "INVENTORY":
            inv_text = "Here's a list of the things in your inventory:\n"
            for obj in object_dictionary:
                if object_dictionary[obj].location == "INVENTORY":
                    inv_text += obj.lower() + "\n"
            console_output +=inv_text)
        elif find_location():
            for obj in pathways_dictionary:
                if pathways_dictionary[obj].location == player_location and pathways_dictionary[obj].location2 == command_list[0]:
                    console_output +=pathways_dictionary[obj].look_thru_text[player_location])
                    tg_play_sound("neutral")
                    break
            else:
                tot_fail()
        else:
            console_output +="I didn't recognize the name of what you're trying to look at.")

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
                console_output +=object_dictionary[command_list[0]].pick_up_text["default"])

            else:
                console_output +="You already have that.")
        else:
            console_output +="I don't recognize the name of what you're trying to obtain.")

    elif strip_off(["PUT", "DOWN"]) or strip_off(["DROP"]) or strip_off(["THROW", "AWAY"]):
        if find_obj():
            if object_dictionary[command_list[0]].location == "INVENTORY":
                object_dictionary[command_list[0]].location = player_location
                console_output +=object_dictionary[command_list[0]].drop_text["default"])
                tg_play_sound("neutral")
            else:
                # tried to drop something not in inventory
                console_output +="That object is not in your inventory so you can't put it down.")
        else:
            console_output +="I don't recognize the name of what you're trying to get rid of.")
 

    #
    #       TRAVEL!
    #
    elif strip_off(["GO", "TO"]) or strip_off(["WALK", "TO"]) or strip_off(["ENTER"]) or strip_off(["GO","INTO"]):
        if find_obj(): #this only searches the current location and the inventory
            if not object_dictionary[command_list[0]].is_location:
                # user said go to an object rather than a location
                console_output +=object_dictionary[command_list[0]].go_to_text["default"])
            else:
                # since location matches, you tried to go to where you are!
                console_output +="You are already there.")
        elif find_location(): #next check outside the current location for other locations
            for obj in pathways_dictionary:
                if pathways_dictionary[obj].location == player_location and pathways_dictionary[obj].location2 == command_list[0] and pathways_dictionary[obj].pathway_open:
                    #found a way in so
                    #put player in new location
                    player_location = command_list[0]
                    console_output +=object_dictionary[command_list[0]].go_to_text["default"])
                    #switch locations on pathway objects with location2 = new location
                    for pathway in pathways_dictionary:
                        if pathways_dictionary[pathway].location2 == player_location:
                            pathways_dictionary[pathway].switch()
                    break
            else:
                #this is skipped if we found a way in through any pathway.
                console_output += "I recognize the place you mentioned but you can't get there from here."

        else:
            console_output +="I'm sorry, I don't recognize the name of where you're trying to go.")


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
                                console_output +=object_dictionary[object1].use_text[object2])

                            else:
                                console_output +=object_dictionary[object1].use_text["default"])

                        else:
                            console_output +="I don't recognize the target of that action.")

                    else:
                        console_output +="That object needs a target (a direct object) to be used.  Try using it 'on' or 'with' something else that is present.")

                else:
                    console_output +="You need to pick up that object to use it.")

            else:
                #object doesn't need a target to be used, so we just print the use text
                if object1 in pathways_dictionary:
                    #we're going to retranslate "use door" as "go to door's second location:
                    command_list = ["GO","TO",pathways_dictionary[object1].location2]
                    loop_again = True
                else:
                    console_output += object_dictionary[object1].use_text["default"]

        else:
            console_output +="I don't recognize what object you're trying to use.")


    #
    #   SPECIAL VERBS
    #
    elif len(command_list) and command_list[0] in special_verbs:
        object1 = special_verbs[command_list[0]]
        del command_list[0]
        if find_obj():
            object2 = command_list[0]
            command_list = ["USE",object1,"WITH",object2]
            loop_again = True
        else:
            if object_dictionary[object1].location == "INVENTORY":
                console_output +="That command needs a target (a direct object).  Try again with one of the objects that is present.")

            else:
                #I'm not totally happy with this error message because it could be used as a clue... Hmm...
                console_output +="You cannot use that command because you don't have the appropriate object in your inventory.")


    #
    #   MISC
    #
    elif strip_off(["LOOK","AROUND"]):
        command_list = ["LOOK","AT","ROOM"]
        loop_again = True
    elif strip_off(["LOOK","THROUGH"]) or strip_off(["PEER","THROUGH"]):
        if find_obj() and command_list[0] in pathways_dictionary:
            console_output +=pathways_dictionary[command_list[0]].look_thru_text[player_location])
        else:
            console_output +="You can generally only look through pathways that lead to other locations (such as doorways.)")

    elif strip_off(["GO","THROUGH"]) or strip_off(["PASS","THROUGH"]):
        if find_obj():
            if command_list[0] in pathways_dictionary:
                command_list = ["USE",command_list[0]]
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
    elif strip_off(["MUTE"]) or strip_off(["TURN","SOUND","OFF"]) or strip_off(["TURN","SOUNDS","OFF"]):
        sound_toggle = False
        console_output +="Game sounds have been turned off."
        command_counter -= 1  # cancel out timer increment
    elif strip_off(["UNMUTE"])or strip_off(["TURN","SOUND","ON"]) or strip_off(["TURN","SOUNDS","ON"]):
        sound_toggle = True
        console_output +="Game sounds have been turned on."
        command_counter -= 1  # cancel out timer increment

#
#   TOTAL FAIL
#
    elif len(command_list): #We check this so that an accidental enter key doesn't erase what's on the screen.
            tot_fail()
    else:
        #only executes if there's no text on the command line:
        command_counter -= 1 #cancel out timer increment

