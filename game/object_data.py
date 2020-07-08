from game import Thing, Place, Pathway



def add_object_data(gs):
    # ---------------------------------------------------------------------------------------------
    #  Game Objects and Locations
    # ---------------------------------------------------------------------------------------------
    #  Sample Location 1:
    room1 = Place("ROOM 1")
    #the object room1 will rarely be used by that handle.  instead we call it with gs.object_dictionary("ROOM1")
    room1.look_text = {"default": "You look at room number 1.  It's pretty simple."}
    #room1.room_look_text = {"default": ""}  # Not needed for locations
    room1.pick_up_text = {"default": "You would like to pick up the room but it's kinda too big."}
    room1.use_text = {"default": "You are using the room as a room to stand in I guess."}
    #room1.drop_text = {"default": ""}  # This is only needed if you can put it in your inventory.
    room1.go_to_text = {"default": "You enter room # 1."}
    gs.object_dictionary[room1.name] = room1
    #next we set up some alternate names
    gs.multiword.append([["ROOM1"],"ROOM 1"])
    gs.multiword.append([["ROOM","1"],"ROOM 1"])
    gs.multiword.append([["ROOM","ONE"],"ROOM 1"])

    #  Sample Location 2:
    room2 = Place("ROOM 2")
    room2.look_text = {"default": "You look at room number 2.  It's pretty simple."}
    #room2.room_look_text = {"default": ""}  # Not needed for locations
    room2.pick_up_text = {"default": "You would like to pick up the room but it's kinda too big."}
    room2.use_text = {"default": "You are using the room as a room to stand in I guess."}
    #room2.drop_text = {"default": ""}  # This is only needed if you can put it in your inventory.
    room2.go_to_text = {"default": "You enter room # 2."}
    gs.object_dictionary[room2.name] = room2
    gs.multiword.append([["ROOM2"],"ROOM 2"])
    gs.multiword.append([["ROOM","2"],"ROOM 2"])
    gs.multiword.append([["ROOM","TWO"],"ROOM 2"])

    # list connections between locations here. (DNU! old way)
    #connections = [{"ROOM 1", "ROOM 2"}]

    #sample doorway:
    door = Pathway("DOOR")
    door.location = "ROOM 2"
    door.location2 = "ROOM 1"
    door.look_text = {"ROOM 1":"You inspect the door.  It is a heavy wooden door with no keyhole. The door leads to room 2.",
                      "ROOM 2":"You inspect the door.  It is a heavy wooden door with no keyhole. The door leads to room 1."}
    door.room_look_text = {"default":"There is a door."}
    door.pick_up_text = {"default":"Sigh.... No you can't pick up a door."}
    door.go_to_text = {"default":"You approach the door..."}
    door.look_thru_text = {"ROOM 1":"Beyond the door is room 2.  You can make out a wooden table.",
                           "ROOM 2":"Beyond the door is room 1.  You don't see any people or large objects."}
    #door.use_text = {} #not needed for pathways.
    gs.object_dictionary[door.name] = door
    gs.pathways_dictionary[door.name] = door


    #  Sample Object: a rock you can pick up:
    rock = Thing("ROCK")
    rock.location = "ROOM 1"
    rock.can_pick_up = True
    rock.look_text = {"default": "You look at the rock.  It is grey and hard, about the size of a baseball."}
    rock.room_look_text = {"default": "There is a rock."}
    rock.pick_up_text = {"default": "You pick up the rock."}
    rock.use_text = {"default": "You can't think of anything to use the rock for at the moment."}
    rock.drop_text = {"default": "You drop the rock.  It makes a sound like PLERK as it hits the ground."}
    rock.go_to_text = {"default": "You approach the rock.  It does not respond."}
    gs.object_dictionary[rock.name] = rock


    #  Sample Object: a table that remains stationary
    table = Thing("TABLE")
    table.location = "ROOM 2"
    table.can_pick_up = False #this isn't needed because by default you can't pick up objects
    table.look_text = {"default": "You are looking at a medium size table made of dark brown wood.  It is old and heavy."}
    table.room_look_text = {"default": "There is a table."}
    table.pick_up_text = {"default": "The table is too heavy to pick up."}
    table.use_text = {"default": "You lean against the table and ponder your life choices."}
    #table.drop_text = {} #not needed since you can't pick it up in the first place.
    table.go_to_text = {"default": "You approach the table.  It does not react."}
    gs.object_dictionary[table.name] = table

    #  Sublocation example:  We make "on the table" a place you can put things.
    table.add_sublocation(preposition="ON",text="On the table",hidden=True)

    #  Sample Transitive Object: a hammer is a transitive object.  to use it you must use it ON something.
    hammer = Thing("HAMMER")
    hammer.is_transitive = True
    hammer.location = "ROOM 2"
    hammer.sublocation = ["TABLE","ON"]
    hammer.can_pick_up = True
    hammer.look_text = {"default": "You look at the hammer.  It is made of metal with a wooden handle."}
    hammer.room_look_text = {"default": "There is a hammer."}
    hammer.pick_up_text = {"default": "You pick up the hammer."}
    hammer.use_text = {"default": "Thunk!",
                       "ROCK": "You carefully aim the hammer and strike the rock.  KABLOOEY!  You smash the rock into a fine dust."}
    hammer.drop_text = {"default": "You place the hammer down."}
    hammer.go_to_text = {"default": "You approach the hammer.  It does not respond."}
    gs.object_dictionary[hammer.name] = hammer

    #add special verbs that can only be used if you have a certain object.  The dictionary returns the object name.
    # The user must provide the target.
    gs.special_verbs["HAMMER"] = "HAMMER" #Now "Hammer door" is translated as "Use hammer on door"
    gs.special_verbs["SMASH"] = "HAMMER"
    gs.special_verbs["HIT"] = "HAMMER"

    #other examples
    gs.special_verbs["LIGHT"] = "MATCHES"
    gs.special_verbs["ATTACK"] = "SWORD"

    return gs