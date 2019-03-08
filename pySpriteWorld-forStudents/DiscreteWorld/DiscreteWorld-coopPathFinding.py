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
from copy import deepcopy
from itertools import chain
from gameclass import Game,check_init_game_done
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
########### Functions ############
##################################

def create_new_path(a_star, start, goal, wallStates, map_size):

    # create new path to the the new coordinates of the potion
    # use basic A* algorithm
    new_path = a_star.calcul_path(start, goal, wallStates, map_size)

    # start coordiantes and goal coordinates are the same
    # no valid path from start coordinates to the goal coordinates
    # next turn it will calcul a path again -> elif condition
    if new_path == [] or new_path is False:
         new_path = [start]

    # new path, no step executed yet
    return new_path, 0

def detect_direction(L):
    if len(L) == 1:
        return 'STATIC'
    x1, y1 = L[0]
    x2, y2 = L[1]
    if x1 - x2 < 0:
        return 'EAST'
    elif x1 - x2 < 0:
        return 'WEST'
    elif y1 - y2 > 0:
        return 'NORTH'
    elif y1 - y2 < 0:
        return 'SOUTH'
    else:
        return 'STATIC'

def opposite_direction(dir1, dir2):
    if (dir1 == 'EAST' and dir2 == 'WEST') or (dir1 == 'WEST' and dir2 == 'EAST')\
    or (dir1 == 'NORTH' and dir2 == 'SOUTH') or (dir1 == 'SOUTH' and dir2 == 'NORTH'):
        return True
    return False

def perpendicular_direction(dir1, dir2):
    if (dir1 == 'EAST' and dir2 == 'NORTH') or (dir1 == 'EAST' and dir2 == 'SOUTH')\
    or (dir1 == 'WEST' and dir2 == 'NORTH') or (dir1 == 'WEST' and dir2 == 'SOUTH')\
    or (dir1 == 'NORTH' and dir2 == 'EAST') or (dir1 == 'NORTH' and dir2 == 'WEST')\
    or (dir1 == 'SOUTH' and dir2 == 'EAST') or (dir1 == 'SOUTH' and dir2 == 'WEST'):
        return True
    return False

def move_static(dir1, dir2):
    if (dir1 == 'STATIC' and dir2 != 'STATIC') or\
     (dir1 != 'STATIC' and dir2 == 'STATIC'):
        return True
    return False

def detect_collision(player1, players_path, players_step):
    step1 = players_step[player1]
    path1 = players_path[player1].copy()[step1:]
    dir1 = detect_direction(path1)
    # check if there is a colliision with each player of the map
    for player2 in range(len(players_path)):
        if player1 != player2:
            step2 = players_step[player2]
            path2 = players_path[player2].copy()[step2:]
            dir2 = detect_direction(path2)
            # # two static players
            # if dir1 == 'STATIC' and dir2 == 'STATIC':
            #     return False
            # face to face collision
            if opposite_direction(dir1, dir2) and\
             (path1[1] == path2[0] and path2[1] == path1[0]):
                return True
            # perpendiculaire collision
            if perpendicular_direction(dir1, dir2):
                if path1[1] == path2[1]:
                    return True
            if move_static(dir1, dir2):
                if (len(path1) > 1 and path1[1] == path2[0]) or\
                 (len(path2) > 1 and path2[1] == path1[0]):
                    return True
    return False

##################################
######### Main Function ##########
##################################

def main():

    #for arg in sys.argv:
    iterations = 50 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()

    #-----------------------------------#
    #--------- Initialisation ----------#
    #-----------------------------------#

    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    map_size = 20

    # get initial position of every players
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)


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
        x = random.randint(0, map_size-1)
        y = random.randint(0, map_size-1)
        while (x, y) in wallStates:
            x = random.randint(0, map_size-1)
            y = random.randint(0, map_size-1)
        goalStates.append((x, y))
        o.set_rowcol(x, y)
        game.layers['ramassable'].add(o)
    game.mainiteration()
    print ("Goal states:", goalStates)

    #-----------------------------------#
    #--- Creation of the initial path --#
    #-----------------------------------#

    possible_neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
    a_star = AStarSimplePath(possible_neighbors)
    players_step = [0 for i in range(nbPlayers)]
    players_path = []

    for i in range(nbPlayers):
        start = initStates[i]
        goal = goalStates[i]
        path_i = create_new_path(a_star, start, goal, wallStates, map_size)[0]
        players_path.append(path_i)

    print('Initial Path created')
    #print('players path', players_path)

    #-----------------------------------#
    #-------- Players movements --------#
    #-----------------------------------#

    posPlayers = deepcopy(initStates)

    winner = False

    while not winner:

        for j in range(nbPlayers):

            curr_row, curr_col = posPlayers[j]

            # TODO # reaction to a collision
            while detect_collision(j, players_path, players_step):
                # current position
                start = curr_row, curr_col
                # next step collision
                path_step = players_step[j]
                obstacle = players_path[j][path_step]
                # calcul new path to evoid collision
                goal = players_path[j][path_step+1]
                # add the collision into the wallStates
                print('start', start)
                print('path step', path_step)
                print('obstacle', obstacle)
                print('goal', goal)
                new_path = a_star.calcul_path(start, goal, wallStates+[obstacle],
                 map_size)

                if not new_path:
                    new_path = [(curr_row, curr_col)]
                print("new calculated path", new_path)
                # remove the collision from the current path
                players_path[j].remove(obstacle)
                # add each step of the alternative path into the current path
                for c in range(len(new_path)):
                    players_path[j].insert(path_step+c, new_path[c])


            # udate path information
            path_step = players_step[j]
            new_row, new_col = players_path[j][path_step]
            players[j].set_rowcol(new_row, new_col)
            posPlayers[j] = new_row, new_col
            # one step forward in the path of the player
            players_step[j] += 1


            # player reach the potion
            if posPlayers[j] == goalStates[j]:

                o = players[j].ramasse(game.layers)
                print("Objet trouvé par le joueur ", j)
                # increase the score of player j
                score[j]+=1

                # first player with 100 point win
                # end of the game
                if score[j] > 99:
                    winner = True
                    break

                # create new random coordinates for the new potion inside the map
                pot_x = random.randint(0, 5-1)
                pot_y = random.randint(0, 5-1)
                # if the potion appears in a wall generate new ones
                while (pot_x, pot_y) in wallStates:
                    pot_x = random.randint(0, 5-1)
                    pot_y = random.randint(0, 5-1)

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
                players_path[j], players_step[j] = create_new_path(a_star,
                start, goal, wallStates, map_size)
                print(score)

            # previous path was an empty path
            # player reach the end of its path but its not the goal yet
            elif len(players_path[j]) == players_step[j]:

                start = posPlayers[j]
                players_path[j], players_step[j] = create_new_path(a_star,
                start, goalStates[j], wallStates, map_size)

        game.mainiteration()

    print ("scores:", score)
    pygame.quit()


if __name__ == '__main__':
    main()
