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

import numpy as np
import pygame

import glo
from AStarSimplePath import AStarSimplePath
from gameclass import Game, check_init_game_done
from method1 import Collision as cl
from ontology import Ontology
from players import Player
from sprite import MovingSprite
from spritebuilder import SpriteBuilder

# ---------------------------------


game = Game()

##################################
######## Init Game Board #########
##################################


def init(_boardname=None):
    global player, game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer1'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

##################################
######### Main Function ##########
##################################


def main():

    # for arg in sys.argv:
    iterations = 50  # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print("Iterations: ")
    print(iterations)

    init()

    #-----------------------------------#
    #--------- Initialisation ----------#
    #-----------------------------------#

    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0] * nbPlayers
    map_size = 20

    # get initial position of every players
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print("Init states:", initStates)

    # get position of every objects
    #goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    goalStates = []

    # get position of every walls
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)

    #-----------------------------------#
    #-- Init Potion's position random --#
    #-----------------------------------#

    for o in game.layers['ramassable']:
        x = random.randint(0, map_size - 1)
        y = random.randint(0, map_size - 1)
        while (x, y) in wallStates:
            x = random.randint(0, map_size - 1)
            y = random.randint(0, map_size - 1)
        goalStates.append((x, y))
        o.set_rowcol(x, y)
        game.layers['ramassable'].add(o)
    game.mainiteration()
    print("Goal states:", goalStates)

    #-----------------------------------#
    #--- Creation of the initial path --#
    #-----------------------------------#

    possible_neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    a_star = AStarSimplePath(possible_neighbors)
    players_step = [1 for i in range(nbPlayers)]
    players_path = []

    # initStates = [(1,0), (6, 3), (3,3)]
    # goalStates = [(0,5),(3, 5), (6,3)]
    # k=0
    # for i in game.layers['joueur']:
    #     i.set_rowcol(initStates[k][0], initStates[k][1])
    #     k += 1
    # game.mainiteration()
    #while True: pass

    for i in range(nbPlayers):
        start = initStates[i]
        goal = goalStates[i]
        path_i = cl.create_new_path(a_star, start, goal, wallStates, map_size)[0]
        players_path.append(path_i)

    print('Initial Path created')
    #print('players path', "\n".join(map(str, players_path)))

    #-----------------------------------#
    #-------- Players movements --------#
    #-----------------------------------#

    posPlayers = deepcopy(initStates)

    winner = False

    while not winner:

        for j in range(nbPlayers):

            # detect collision
            while cl.detect_collision(j, players_path, players_step):
                print("collision detected")
                cl.manage_collision(j, players_path, players_step,
                 wallStates, a_star)

            new_row, new_col = players_path[j][players_step[j]]
            # udate path information
            players[j].set_rowcol(new_row, new_col)
            posPlayers[j] = new_row, new_col
            # one step forward in the path of the player
            players_step[j] += 1

            # player reach the potion
            if posPlayers[j] == goalStates[j]:
                # problem if both player got the same goal and there is no more
                # goalstates for them after this one => they stay on the same
                # case
                # players_step[j] -= 1
                o = players[j].ramasse(game.layers)
                print("Objet trouvé par le joueur ", j)
                # increase the score of player j
                score[j] += 1

                # first player with 100 point win
                # end of the game
                if score[j] > 99:
                    winner = True
                    break

                # create new random coordinates for the new potion inside the map
                pot_x = random.randint(0, 5 - 1)
                pot_y = random.randint(0, 5 - 1)
                # if the potion appears in a wall generate new ones
                while (pot_x, pot_y) in wallStates:
                    pot_x = random.randint(0, 5 - 1)
                    pot_y = random.randint(0, 5 - 1)

                # set new coordinates to the potion
                o.set_rowcol(pot_x, pot_y)
                # set new coordinates for the goal
                goalStates[j] = (pot_x, pot_y)
                game.layers['ramassable'].add(o)

                #-----------------------------------#
                #-------- New Path Creation --------#
                #-----------------------------------#

                start = posPlayers[j]
                goal = (pot_x, pot_y)
                players_path[j], players_step[j] =\
                    cl.create_new_path(a_star, start, goal, wallStates, map_size, time)
                players_path[j] = [start] + players_path[j]
                players_step[j] += 1
                print(score)

            # previous path was an empty path
            # player reach the end of its path but its not the goal yet
            elif len(players_path[j]) == players_step[j]:

                start = posPlayers[j]
                players_path[j], players_step[j] =\
                    cl.create_new_path(a_star, start,
                     goalStates[j], wallStates, map_size, time)
                players_path[j] = [start] + players_path[j]
                players_step[j] += 1

        game.mainiteration()

    print("scores:", score)
    pygame.quit()


if __name__ == '__main__':
    main()
