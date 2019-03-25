# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals

import random
import sys
from copy import deepcopy
from itertools import chain

sys.path.append('../Utils')
sys.path.append('../MethodPlayer')
sys.path.append('../AStarAlgorithm')
sys.path.append('../Tools')

import numpy as np
import pygame

import glo
from AStarSimplePath import AStarSimplePath
from method2 import *
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
    game.fps = 500  # frames per second
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

    players_step = [0 for i in range(nbPlayers)]
    players_path = [None for i in range(nbPlayers)]

    # get initial position of every players
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print("Init states:", initStates)
    posPlayers = deepcopy(initStates)

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

    for i in range(nbPlayers):
        start = posPlayers[i]
        goal = goalStates[i]
        path = AStarSimplePath.calcul_path(start, goal, wallStates, map_size)
        players_path[i] = path

    print('Initial Path created')
    print('\n\n'.join(map(str, players_path)))

    #-----------------------------------#
    #-------- Players movements --------#
    #-----------------------------------#

    grouped_path = CoopPath.organize_groups(players_path)

    iteration_before_next_wave =\
    CoopPath.number_of_move_before_next_group(players_path, grouped_path)

    step = 0

    while not Tools.finished(score, 100):

        for j in range(nbPlayers):

            # the player can move if it's its turn (= in the first group)
            if j in grouped_path[0]:
                can_move = True
            else: can_move = False

            if not can_move: continue

            # next position
            new_row, new_col = players_path[j][players_step[j]]

            # update player position
            players[j].set_rowcol(new_row, new_col)
            posPlayers[j] = new_row, new_col

            # one step forward in the path of the player
            players_step[j] += 1

            # player reach the potion
            # it wait until every player of the wave have reach their goal
            if posPlayers[j] == goalStates[j]:
                players_step[j] -= 1
                continue

        # every player of the wave have finished its path
        if iteration_before_next_wave == 0:

            # remove first group
            finished_path = grouped_path.pop(0)

            # loop trhough the player that have finished their path
            for i in finished_path:

                # take the potion
                o = players[i].ramasse(game.layers)
                print("Objet trouvé par le joueur ", j)

                # increase the score of player j
                score[i] += 1

                # create new random coordinates for the new potion inside the map
                pot_x, pot_y = Tools.random_potion(o, wallStates, map_size, posPlayers)

                # update coordinate of the potion
                goalStates[i] = (pot_x, pot_y)
                game.layers['ramassable'].add(o)

                # calcul the new path to reach the goal
                players_path[i] = AStarSimplePath.calcul_path(posPlayers[i],
                 goalStates[i], wallStates, map_size)

                # insert the player in a group without collision
                CoopPath.put_path_in_group(i, players_path, grouped_path)
                # with the other players
                #CoopPath.put_path_in_group(i, players_path, grouped_path)
                players_step[i] = 0

            # players of other group as obstacles are considered as obstacles
            obstacles = [posPlayers[i] for i in range(nbPlayers)\
             if i not in grouped_path[0]]

            # calcul new path
            for i in grouped_path[0]:
                players_path[i] = AStarSimplePath.calcul_path(posPlayers[i],
                goalStates[i], wallStates+obstacles, map_size)

            # reorganize the groups
            grouped_path = CoopPath.reorganize_groups(players_path, grouped_path)

            # number of step before next wave
            iteration_before_next_wave =\
            CoopPath.number_of_move_before_next_group(players_path, grouped_path)

        step += 1
        iteration_before_next_wave -= 1
        game.mainiteration()

        print("scores:", score)
        print('total step', step)
    pygame.quit()


if __name__ == '__main__':
    main()
