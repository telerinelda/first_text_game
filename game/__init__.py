# this allows you to import Place as game.Place, rather than game.nouns.Place, etc.
# if this level of indirection is not desirable, then get rid of this file, and 
# import it the way you want to.
from .nouns import Place, Thing, Pathway
from .game_state_setup import gameState