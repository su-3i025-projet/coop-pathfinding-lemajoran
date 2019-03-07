# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from AStar_algorithm.AStarPathSplicing import AStarPathSplicing
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
from copy import deepcopy
import pygame
import glo

import random
import numpy as np
import sys


# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer1'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

def placer_fiole_alea():
    pass

def main():

    #for arg in sys.argv:
    iterations = 50 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    #--------------------------#
    #----- Initialisation -----#
    #--------------------------#

    init()

    # get player informations
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers

    # map size
    map_width = map_height = 20

    # initial position of the players
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)

    # initial goal of the players
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)

    # get coordinates of every walls
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]

    #--------------------------------#
    #----- Potion init position -----#
    #--------------------------------#

    # on donne a chaque joueur une fiole a ramasser
    # en essayant de faire correspondre les couleurs pour que ce soit plus simple à suivre
    posPlayers = deepcopy(initStates)

    # create an A* algorithm to calcul the path for each player
    # using slice splicing
    a_star = AStarPathSplicing([(0,1),(0,-1),(1,0),(-1,0)])

    # memorize the current step of each player in their path
    path_step = [0 for i in range(nbPlayers)]

    # memorize path of each player
    path_players = []

    # calculate the path for each player with A* from their start point
    # to their goal point
    for i in range(nbPlayers):
        path_players.append(a_star.calcul_path(initStates[i], goalStates[i], wallStates,
        map_width, map_height, deepcopy(path_players)))

    # no winner at the beginning
    winner = False

    while not winner:

        for j in range(nbPlayers):

            # update coordinates of the j player
            new_row, new_col = path_players[j][path_step[j]]
            players[j].set_rowcol(new_row,new_col)
            posPlayers[j] = (new_row, new_col)
            # player has advanced of one step in its path
            path_step[j] += 1

            # player reach the potion
            if (new_row, new_col) == goalStates[j]:

                o = players[j].ramasse(game.layers)
                print ("Objet trouvé par le joueur ", j)
                # increase the score of player j
                score[j]+=1

                # first player with 100 point win
                # end of the game
                if score[j] > 99:
                    winner = True
                    break

                # create new random coordinates for the new potion inside map
                # coordinates
                x = random.randint(0,map_width-1)
                y = random.randint(0,map_height-1)
                # if the potion appears in the coordinates of a wall
                # generate a new position for it
                while (x,y) in wallStates:
                    x = random.randint(0,map_width-1)
                    y = random.randint(0,map_height-1)

                # set new coordinates to the potion
                o.set_rowcol(x,y)
                # set new coordinates for the goal
                goalStates[j] = x, y
                game.layers['ramassable'].add(o)

                #-----------------------------#
                #----- New path creation -----#
                #-----------------------------#

                # copy the path of every player
                temp_path = deepcopy(path_players)

                # keep only the part of the path that hasn't been executed yet
                temp_path = [temp_path[k][path_step[k]:] for k in range(nbPlayers)]
                # remove the path of the current player
                temp_path.pop(j)

                # create a new path in function of the path of the other players
                path_players[j] = a_star.calcul_path((new_row, new_col), (x, y), wallStates,
                map_width, map_height, temp_path)
                # new path, no step executed yet
                path_step[j] = 0

                # start coordiantes and goal coordinates are the same
                # no valid path from start coordinates to the goal coordinates
                # next turn it will calcul a path again -> elif condition
                if path_players[j] == [] or path_players[j] is False:
                    path_players[j] = [(new_row, new_col)]

                print(score)

            # previous path was an empty path
            # player reach the end of its path but its not the goal yet
            elif len(path_players[j]) == path_step[j]:

                # copy the path of every player
                temp_path = deepcopy(path_players)

                #the goal hasn't changed
                x, y = goalStates[j]

                # keep only the part of the path that hasn't been executed yet
                temp_path = [temp_path[k][path_step[k]:] for k in range(nbPlayers)]
                # remove the path of the current player
                temp_path.pop(j)

                # create a new path in function of the path of the other players
                path_players[j] = a_star.calcul_path((new_row, new_col), (x, y), wallStates,
                map_width, map_height, temp_path)

                # new path, no step executed yet
                path_step[j] = 0

                #start coordinates and goal coordinates are the same
                # no valid path from start coordinates to the goal coordinates
                if path_players[j] == [] or path_players[j] is False:
                    path_players[j] = [(new_row, new_col)]

        game.mainiteration()

    print ("scores:", score)
    pygame.quit()





if __name__ == '__main__':
    main()
