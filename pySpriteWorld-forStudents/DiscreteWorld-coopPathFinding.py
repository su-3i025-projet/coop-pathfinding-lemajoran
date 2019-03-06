# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from AStar_algorithm.AStarCooperative import AStarCooperativePath
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

def main():

    #for arg in sys.argv:
    iterations = 50 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()


    #-------------------------------
    # Initialisation
    #-------------------------------

    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers


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
    # Placement aleatoire des fioles
    #-------------------------------


    # on donne a chaque joueur une fiole a ramasser
    # en essayant de faire correspondre les couleurs pour que ce soit plus simple à suivre


    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------

    # A star algorithm calcul the path for each player

    posPlayers = initStates
    map_width = map_height = 20

    a_star = AStarCooperativePath([(0,1),(0,-1),(1,0),(-1,0)])
    path = []

    # associate each start point to a goal point
    for i in range(3):
        path.append(a_star.calcul_path(posPlayers[i], goalStates[i], wallStates,
        map_width, map_height, deepcopy(path)))

    # memorize step current step of each player in their path
    path_step = [0]*3
    goals = [i for i in goalStates]
    print(path)

    # no winner at the beginning
    winner = False

    while not winner:

        for j in range(3):
            # update coordinates of the j player
            print("=>", j, path[j], path_step[j])
            if path[j] == []: continue
            next_row, next_col = path[j][path_step[j]]
            players[j].set_rowcol(next_row,next_col)
            path_step[j] += 1

            col=next_col
            row=next_row
            posPlayers[j]=(row,col)

            # player reach the potion
            if (row,col) == goals[j]:
                o = players[j].ramasse(game.layers)
                print ("Objet trouvé par le joueur ", j)
                goalStates.remove((row,col))
                score[j]+=1

                # first player with 3 point win
                # end of the game
                if score[j] > 100:
                    winner = True
                    break

                # create new random coordinates for the object
                x = random.randint(10,12)
                y = random.randint(10,12)
                while (x,y) in wallStates:
                    x = random.randint(10,12)
                    y = random.randint(10,12)
                o.set_rowcol(x,y)
                # on ajoute ce nouveau goalState
                goalStates.append((x,y))
                game.layers['ramassable'].add(o)

                # create new path from the current position to the
                # new pos of the object
                temp_path = deepcopy(path)
                if j == 0:
                    temp_path[1] = temp_path[1][path_step[1]:]
                    temp_path[2] = temp_path[2][path_step[2]:]
                elif j == 1:
                    temp_path[0] = temp_path[0][path_step[0]:]
                    temp_path[2] = temp_path[2][path_step[2]:]
                else:
                    temp_path[0] = temp_path[0][path_step[0]:]
                    temp_path[1] = temp_path[1][path_step[1]:]
                temp_path.pop(j)
                path_step[j] = 0
                path[j] = a_star.calcul_path((row, col), (x, y), wallStates,
                map_width, map_height, temp_path)
                if path[j] == []:
                    path[j] = [(x, y)]
                if path[j] is False:
                    path[j] = [(x, y)]
                goals[j] = x, y
                print("->",j, path[j], path_step[j], goals)
                # new path, reinitialize step
        game.mainiteration()
    print ("scores:", score)
    pygame.quit()





if __name__ == '__main__':
    main()
