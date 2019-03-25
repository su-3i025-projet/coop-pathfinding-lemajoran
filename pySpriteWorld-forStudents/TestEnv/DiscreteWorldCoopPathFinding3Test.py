# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals

import random
import sys
from copy import deepcopy
from itertools import chain

sys.path.append('../AStarAlgorithm')
sys.path.append('../Utils')
sys.path.append('../MethodPlayer')
sys.path.append('../Tools')

import numpy as np
import pygame

import glo
from AStar3dPath import AStar3dPath as as3d
from AStarSimplePath import AStarSimplePath
from gameclass import Game, check_init_game_done
from method1 import Collision as cl
from ontology import Ontology
from players import Player
from sprite import MovingSprite
from spritebuilder import SpriteBuilder
from tools import Tools
from method1 import Collision

# ---------------------------------


game = Game()

##################################
######## Init Game Board #########
##################################


def init(_boardname=None):
    global player, game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer4'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 500   # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

##################################
######### Main Function ##########
##################################


def main(nb_pickups):

    init()

    #-----------------------------------#
    #--------- Initialisation ----------#
    #-----------------------------------#


    
    map_size = 20
    time = 0

    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0] * nbPlayers
    
     #data for plotting
    ceil_iterations = [0 for i in range (len(players))]
    total_iterations = 0

    players = [o for o in game.layers['joueur']]
    players_path = [None for i in range(nbPlayers)]
    players_step = [0 for i in range(nbPlayers)]

    # get initial position of every players
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print("Init states:", initStates)
    posPlayers = deepcopy(initStates)

    # get position of every objects
    goalStates = []

    # get position of every walls
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]

    #-- Init Potion's position random --#

    for o in game.layers['ramassable']:
        x, y = Tools.random_potion(o, wallStates, map_size, posPlayers)
        game.layers['ramassable'].add(o)
        goalStates.append((x, y))
    game.mainiteration()

    print("Goal states:", goalStates)

    #--- Creation of the initial path --#

    for i in range(nbPlayers):
        start = posPlayers[i]
        goal = goalStates[i]
        players_path[i] = as3d.calcul_path(start, goal, wallStates,
         map_size, time, i)
        ceil_iterations[i] =len(players_path[i]) 
        

    print(as3d.reservation)
    print("\n".join(map(str, players_path)))

    print('Initial Path created')

    #-----------------------------------#
    #-------- Players movements --------#
    #-----------------------------------#

    posPlayers = deepcopy(initStates)

    winner = False

    while time < nb_pickups:

        for j in range(nbPlayers):

            # new position
            new_row, new_col = players_path[j][players_step[j]]

            # udate path information
            players[j].set_rowcol(new_row, new_col)
            posPlayers[j] = new_row, new_col

            # one step forward in the path of the player
            players_step[j] += 1

            # player reach the potion
            if posPlayers[j] == goalStates[j]:

                # end of the game
                if score[j] > 999:
                    # players_path[j] = as3d.pause(start, j, time, wallStates)
                    start = posPlayers[j]
                    players_path[j] =\
                        as3d.calcul_path(start, start, wallStates, map_size, time+1, j)
                    players_step[j] = 0
                    continue

                # bring the potion
                o = players[j].ramasse(game.layers)
                print("Objet trouvé par le joueur ", j)

                # increase the score of player j
                score[j] += 1

                # create new random coordinates for the new potion inside the map
                pot_x, pot_y = Tools.random_potion(o, wallStates, map_size,
                 posPlayers)

                # update coordinate of the potion
                goalStates[j] = (pot_x, pot_y)
                game.layers['ramassable'].add(o)

                #-------- New Path Creation --------#

                start = posPlayers[j]
                goal = (pot_x, pot_y)

                players_path[j] =\
                    as3d.calcul_path(start, goal, wallStates, map_size, time+1, j)
                players_step[j] = 0
                
                print ('chemin :', len(players_path[j]))   
                ceil_iterations[j] += len(players_path[j])
                print(score)

            if players_step[j] == len(players_path[j]):
                start = posPlayers[j]
                goal = goalStates[j]
                players_path[j] =\
                    as3d.calcul_path(start, goal, wallStates, map_size, time+1, j)
                players_step[j] = 0
                print ('chemin :', len(players_path[j]))   
                ceil_iterations[j] += len(players_path[j])
                
        time += 1
        game.mainiteration()

    print(time)
    print("scores:", score)
    print("temps estimés: ",ceil_iterations)
    pygame.quit()
    return sum(score),sum(ceil_iterations), time, max(ceil_iterations)


#if __name__ == '__main__':
#   main(100)
