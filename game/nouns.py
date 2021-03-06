# this class is the generic data structure of an object or location in the game.
class Thing:
    def __init__(self, obj_name):
        self.name = obj_name

        self.location = "nowhere"
        self.sublocation = [] #takes two values:  the object that owns the sublocation, and the preposition
        self.can_pick_up = False
        self.is_transitive = False  # does it need a direct object to be used?
        self.is_location = False  # is this thing the room itself?

        # a thing needs response texts for when it is addressed by a command.  This is a dictionary where there
        # is a "default" text and other texts can be stored for use according the progress indicator.
        self.look_text = {"default": "Default Look Text."}
        self.room_look_text = {"default": "Default object in room text."}
        self.pick_up_text = {"default": "default pick up text."}
        self.use_text = {"default": "default use text."}
        self.dropa_text = {"default": "default drop text."}
        self.go_to_text = {"default": "default go to"}

        #other objects may be able to be located in, on, or under this object.  So we can set up a sublocation: (sublocation programming is incomplete)
        #self.num_sublocations = 0 #should always equal len of the two below strings
        self.sublocation_preposition = [] #values like "UNDER" or "ON" that the user can use
        self.sublocation_text = [] #values like "Under the bed" for building phrases about the place. start with capital.
        self.sublocation_hidden = [] #booleans True if you can't see the sublocation just by gazing on the object itself.

    def num_sublocations(self): #dynamically return the number of sublocations an object has.
        return len(self.sublocation_text)

    def in_sublocation(self): #boolean to check location of this object
        if len(self.sublocation):
            return True
        else:
            return False

    def add_sublocation(self,preposition, text, hidden):
        self.sublocation_preposition = preposition
        self.sublocation_text = text
        self.sublocation_hidden = hidden

    def sublocation_index(self,preposition):
        for i in range(self.num_sublocations()):
            if self.sublocation_preposition == preposition:
                return i
        else:
            raise Exception

    def is_hidden(self,gs):
        #return true if the object is located in a still-hidden sublocation
        if self.sublocation == []:
            return False
        else:
            sub_owner = gs.object_dictionary[self.sublocation[0]]
            prep = self.sublocation[1]
            sub_i = sub_owner.sublocation_index(prep)
            return sub_owner.sublocation_hidden

# here's a subclass that is for locations (ie rooms).
class Place(Thing):
    def __init__(self, obj_name):
        super().__init__(obj_name)
        self.location = self.name
        self.is_location = True
        self.room_look_text = {"default":""}

# here's a subclass that is for pathways connecting rooms: doorways, hallways that don't need to be locations.
class Pathway(Thing):
    def __init__(self, obj_name):
        super().__init__(obj_name)
        self.location2 = "NOWHERE" #this variable will always be the room the player is NOT in (they swap when he moves)
        self.pathway_open = True #can you pass through?
        self.look_thru_text = dict() #If the player tries to peer through the pathway to the next room or location.

    def switch(self):
        #this is a method for reversing the locations when you enter the room.  location2 is always the "other" location.
        self.location, self.location2 = self.location2, self.location
