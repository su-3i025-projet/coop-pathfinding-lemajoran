import sys

sys.path.append('../AStarAlgorithm')

class Search3D:

    def __init__(self):
        self.a_star = AStarSimplePath2([(1,0), (-1,0), (0,1), (0,-1)])

    def backward_search(self, start, goal, wallStates, map_size):
        path = self.a_star.calcul_path(goal, start, wall, wallStates, map_size)
        return path
