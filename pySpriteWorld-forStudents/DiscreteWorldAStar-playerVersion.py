# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random
import numpy as np
import sys

from AStarAlgorithm import a_star
# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player

def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()



    #-------------------------------
    # Building the matrix
    #-------------------------------


    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)

    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)

    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)

    start = initStates[0]
    goal =goalStates[0]
    #row2,col2 = (5,5)

    map_width = 20
    map_height = 20

    print(map_width, map_height)

    # calcul the shortest path
    a_start_path = a_star(start, goal, wallStates, map_width, map_height)

    for coord in a_start_path:
        next_row, next_col = coord
        player.set_rowcol(next_row,next_col)
        print ("pos 1:",next_row,next_col)
        game.mainiteration()

    # the play has found the object
    o = game.player.ramasse(game.layers)
    game.mainiteration()
    print ("Objet trouvé!", o)
    '''
        #x,y = game.player.get_pos()
    '''

    pygame.quit()





if __name__ == '__main__':
    main()
