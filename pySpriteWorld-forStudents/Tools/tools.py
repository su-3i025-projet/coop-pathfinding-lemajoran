import random
import sys

sys.path.append('../MethodPlayer')
sys.path.append('../AStarAlgorithm')

from method1 import Collision as cl
from AStarSimplePath import AStarSimplePath as assp

class Tools:

    @staticmethod
    def random_potion(potion, wallStates, map_size, posPlayers):
        """Place a potion inside the map with random coordinates

            Parameters
            ----------
            potion : Object
                object to place
            wallStates : *args
                list of the coordinates of the walls
            map_size : int
                size of the map
            posPlayers : *args
                list of the coordinates of the players

            Returns
            -------
            tuple of int
                coordinates of the potion
        """
        x = random.randint(0,map_size - 1)
        y = random.randint(0,map_size - 1)
        while (x, y) in wallStates or (x, y) in posPlayers:
            x = random.randint(0, map_size - 1)
            y = random.randint(0, map_size - 1)
        potion.set_rowcol(x, y)
        return x, y

    @staticmethod
    def finished(score, n):
        """Check if the number of potion required by every player
            has been reached

            Parameters
            ----------
            score : *args
                list of the scores
            n : int
                number to reach

            Returns
            -------
            bool
                True if the number has been reached by every player
                otherwise False
        """
        for i in score:
            if i < n:
                return False
        return True
