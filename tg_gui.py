from appJar import gui

def setup_gui(game_name):
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
    tg.addButtons(["   Submit   ", "   Help   ", "   About   ", "   Exit   "], press)
    tg.setFocus("input")
    # this bit makes the Submit button get activated if you press the enter key
    tg.enableEnter(press("   Submit   "))

    return tg


def press(button):
    if button == "   Exit   ":
        tg.stop()
    elif button == "   Help   ":
        # help stuff here.
        tg.setMessage("console", "set up help text later")
        tg_play_sound("neutral")
        tg.setFocus("input")
    elif button == "   About   ":
        tg.setMessage("console", "set up about text later")
        tg_play_sound("neutral")
    elif button == "   Submit   ":
        user_input = tg.getEntry("input")
        #command_counter += 1
        #command_list = user_input.upper().replace(".","").replace(",","").split()
        #command_list[:] = [x for x in command_list if x not in ["A","THE"]] #remove fluff
        #game()  # this function call evaluates the input and reacts to it.
        tg.setEntry("input", "")
        tg.setFocus("input")
    else:
        print("this shouldn't happen")

# Here's a function that makes it slightly easier to display text in the main message location
def tgprint(print_text):
    #prev = tg.getMessage("console")
    #tg.setMessage("console", prev + "\n\n" + print_text)
    tg.setMessage("console", print_text)

def tg_play_sound(sound_type = "neutral"):
    sound_file = ""
    if sound_type == "neutral":
        sound_file = "sounds/neutral" + choice(["1","2","3"]) + ".Wav"
    elif sound_type == "unsuccessful":
        sound_file = "sounds/unsuccessful" + choice(["1","2","3"]) + ".Wav"
    elif sound_type == "success":
        sound_file = "sounds/success1.Wav"
    elif sound_type == "zelda":
        sound_file = "sounds/Zeldasound.Wav"
    elif sound_type == "death":
        sound_file = "sounds/death.Wav"
    elif sound_type == "victory":
        sound_file = "sounds/victory.Wav"
    if sound_file != "" and sound_toggle:
        tg.playSound(sound_file)
#tg_play_sound("zelda")