import heapq

class AStarSimplePath:

    def __init__(self, neighbors):
        """
            Class representing the A* algorithm without modification

            ----------
            attributes
            ----------
            : neighbors (list): list of the possible moves
            ----------
              methods
            ----------
            : outside_the_map(int, int, (int, int)): check if the coordinates
            are outisde of the map
            : heuristic (int, int): calcul heuristic between two coordinates
            : calcul_path ((int, int), (int, int), list, int, int):
            calul the shortest between two coordinates
        """
        self.neighbors = neighbors


    def outside_the_map(self, size, coord):
        """
            -> Check if a point is outside of the map surface

            ----------
            parameters
            ----------
            : width (int): width of the map
            : height (int): height of the map
            : coord (int, int): coordinates of the point
            ----------
              return
            ----------
            : boolean: True if the point is inside the map else False
        """
        x, y = coord
        # in the map, check the coordinates with the size of the map
        return x >= size or x < 0 or y >= size or y < 0

    @staticmethod
    def manhattan_distance(coord1, coord2):
        """
            -> Calcul the distance of manhattan between two coordinates

            ----------
            parameters
            ----------
            : coord1 (int, int): coordinates
            : coord1 (int, int): coordinates
            ----------
              return
            ----------
            : int: manhattan's distance between a and b
        """
        x1, y1 = coord1
        x2, y2 = coord2
        return abs(x2-x1) + abs(y2-y1)

    @classmethod
    def heuristic(cls, coord1, coord2):
        """
            -> Calcul the heuristic between two coordinates

            ----------
            parameters
            ----------
            : coord1 (int, int): coordinates
            : coord1 (int, int): coordinates
            ----------
              return
            ----------
            : int: manhattan's distance between a and b
        """
        return AStarSimplePath.manhattan_distance(coord1, coord2)

    def calcul_path(self, start, goal, obstacles, size):
        """
            -> Calcul the shortest path from a start point to a goal point

            ----------
            parameters
            ----------
            : start (int, int): coordinates of the start point
            : goal (int, int): coordinates of the goal point
            : obstacles (list): list of the coordinates corresponding to the obstacles
            : size (int): size of the map
            ----------
              return
            ----------
            -> if path exists:
            : list: shortest path from start to goal
            -> else:
            : False: no path exists
        """
        # init the parameter
        closed_nodes = set()
        came_from = {}
        gscore = {start:0}
        fscore = {start:AStarSimplePath.heuristic(start, goal)}
        open_nodes = []

        # start with the exploration of the start node
        heapq.heappush(open_nodes, (fscore[start], start))

        # while there is nodes to explore
        while open_nodes:

            current = heapq.heappop(open_nodes)[1]

            if current == goal:
                data = []
                # go through every coordinates we visited to arrive to the goal
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                # reverse the list to have the path from the start to the goal
                return data[::-1]

            closed_nodes.add(current)

            for i, j in self.neighbors:
                # new coordinates of the neighbor
                neighbor = current[0] + i, current[1] + j
                # skip the coordinates if its an obstacle or outisde the map
                if neighbor in obstacles or self.outside_the_map(size, neighbor):
                    continue
                # calcul new score
                tentative_g_score = gscore[current] + AStarSimplePath.heuristic(current, neighbor)
                if neighbor in closed_nodes and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                # node not visited yet or better score than before for these coordinates
                # update the variables
                if  tentative_g_score < gscore.get(neighbor, 0) or\
                 neighbor not in [i[1]for i in open_nodes]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + AStarSimplePath.heuristic(neighbor, goal)
                    # continue to explore this path
                    heapq.heappush(open_nodes, (fscore[neighbor], neighbor))
        # no path found
        return False
