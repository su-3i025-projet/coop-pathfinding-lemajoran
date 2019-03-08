# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals

import sys

sys.path.append('../AStarAlgorithm')
sys.path.append('../Utils')

import numpy as np
import random

import glo
import pygame

from AStarSimplePath import AStarSimplePath
from gameclass import Game,check_init_game_done
from itertools import chain
from ontology import Ontology
from players import Player
from sprite import MovingSprite
from spritebuilder import SpriteBuilder





#---------------------------------


game = Game()

##################################
######## Init Game Board #########
##################################

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player

##################################
######### Main Function ##########
##################################

def main():

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

    #-------------------------------
    # Building the best path with A*
    #-------------------------------

    possible_neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
    a_star = AStarSimplePath(possible_neighbors)
    start = initStates[0]
    goal = goalStates[0]
    map_size = 20

    path = a_star.calcul_path(start, goal, wallStates, map_size)

    #-------------------------------
    # Moving along the path
    #-------------------------------

    for coord in path:

        player.set_rowcol(*coord)
        print ("pos 1:", coord)
        game.mainiteration()

        col,row = coord

        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break

    pygame.quit()



if __name__ == '__main__':
    main()
