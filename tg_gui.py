from appJar import gui
def setup_gui(game_name,help_text,about_text,game_func):
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
        #global command_list
        #global command_counter
        if button == "   Exit   ":
            tg.stop()
        elif button == "   Help   ":
            # help stuff here.
            tg.setMessage("console", help_text)
            #tg_play_sound("neutral")
            tg.setFocus("input")
        elif button == "   About   ":
            tg.setMessage("console", about_text)
            #tg_play_sound("neutral")
        elif button == "   Submit   ":
            tg.setMessage("console",game_func(tg.getEntry("input")))
            tg.setEntry("input", "")
            tg.setFocus("input")
        else:
            print("this shouldn't happen")

    def ent():
        press("   Submit   ")
    tg.enableEnter(ent)

    tg.addButtons(["   Submit   ", "   Help   ", "   About   ", "   Exit   "], press)
    tg.setFocus("input")
    # this bit makes the Submit button get activated if you press the enter key

    return tg

def play_sound(tg,sound_type = "neutral"):
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
    if sound_file != "":
        tg.playSound(sound_file)
