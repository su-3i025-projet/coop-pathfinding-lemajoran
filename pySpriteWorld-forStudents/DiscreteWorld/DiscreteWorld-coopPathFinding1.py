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
from AStarSimplePath import AStarSimplePath as assp
from gameclass import Game, check_init_game_done
from method1 import Collision as cl
from ontology import Ontology
from players import Player
from sprite import MovingSprite
from spritebuilder import SpriteBuilder
from tools import Tools

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
    game.fps = 200 # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

##################################
######### Main Function ##########
##################################


def main():

    init()

    #-----------------------------------#
    #--------- Initialisation ----------#
    #-----------------------------------#

    map_size = 20

    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0] * nbPlayers

    players = [o for o in game.layers['joueur']]
    players_path = [None for i in range(nbPlayers)]
    players_step = [0 for i in range(nbPlayers)]

    # get initial position of every players
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print("Init states:", initStates)
    # initStates = [(0,2), (0,1), (0,3)]
    posPlayers = deepcopy(initStates)

    goalStates = []

    # get position of every walls
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]

    #-- Init Potion's position random --#

    for o in game.layers['ramassable']:
        x, y = Tools.random_potion(o, wallStates, map_size, posPlayers)
        game.layers['ramassable'].add(o)
        goalStates.append((x, y))

    # goalStates = [(0,6),(0, 6), (0,0)]
    #
    # k=0
    # for i in game.layers['joueur']:
    #     i.set_rowcol(initStates[k][0], initStates[k][1])
    #     k += 1
    game.mainiteration()

    print("Goal states:", goalStates)

    #--- Creation of the initial paths --#

    for i in range(nbPlayers):
        start = posPlayers[i]
        goal = goalStates[i]
        players_path[i] = assp.calcul_path(start, goal, wallStates,
         map_size)

    print('Initial Path created')
    print('players path', "\n".join(map(str, players_path)))

    #-----------------------------------#
    #-------- Players movements --------#
    #-----------------------------------#

    step = 0

    while not Tools.finished(score, 1000):

        again = False
        # detect collision
        player = cl.detect_collision(posPlayers, players_path, players_step)
        while player is not False:
            # manage collision
            cl.manage_collision(player, players_path, players_step,
             posPlayers, wallStates, again)
            again = True
            player = cl.detect_collision(posPlayers, players_path, players_step)

        for j in range(nbPlayers):

            # new position
            new_row, new_col = players_path[j][players_step[j]]

            # udpdate player position
            players[j].set_rowcol(new_row, new_col)
            posPlayers[j] = new_row, new_col

            # one step forward in the path of the player
            players_step[j] += 1

            # player reach the goal
            if posPlayers[j] == goalStates[j]:

                # if it already has the number of potion
                # it does nothing
                if score[j] > 999:
                    players_step[j] -= 1
                    continue

                # take the potion
                o = players[j].ramasse(game.layers)
                print("Objet trouvé par le joueur ", j)

                # increase the score of player j
                score[j] += 1

                # create new random coordinates for the new potion inside the map
                pot_x, pot_y = Tools.random_potion(o, wallStates, map_size, posPlayers)

                # update coordinate of the potion
                goalStates[j] = (pot_x, pot_y)
                game.layers['ramassable'].add(o)

                #-------- New Path Creation --------#

                start = posPlayers[j]
                goal = goalStates[j]

                players_path[j] = assp.calcul_path(start, goal, wallStates,
                 map_size)
                players_step[j] = 0
                print(score)

            # player reach the end of its path but its not the goal yet
            # no possible path at the current moment
            elif len(players_path[j]) == players_step[j]:
                start = posPlayers[j]
                goal = goalStates[j]
                players_path[j] = assp.calcul_path(start, goal, wallStates,
                 map_size)
                players_step[j] = 0

        step += 1
        game.mainiteration()

    print('total step', step)
    print("scores:", score)
    pygame.quit()

###############################################
# no termination if the a player that has already finished is staying on a
# potion of someone else
###############################################


if __name__ == '__main__':
    main()
