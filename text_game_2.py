import tg_gui
help_text = "help text here"
about_text = "about text here"
game_name = "test game name"

def game_func(command_input):
    #print("received: "+command_input)
    return "game func output"

tg = tg_gui.setup_gui(game_name,help_text,about_text,game_func)

tg_gui.play_sound(tg,"zelda")
#
#
# leave this command last:
tg.go()
