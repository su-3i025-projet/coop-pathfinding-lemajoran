import heapq
from AStarSimplePath import AStarSimplePath

class BackWardSearch(AStarSimplePath):

    NEIGHBORS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, start, goal, wallStates, map_size):
        """
            Class representing the A* algorithm using the manhattan distance as
            heuristic

            Attributes
            ----------
            neighbors : *args
                list of the possible move
            start : tuple of int
                coordinates of the start point
            goal : tuple of int
                coordinates of the goal point
            wallStates : *args
                list of the coordinates of the walls
            closed_nodes : set()
                set of the closed nodes
            came_from : *kwargs
                the predecessors of the nodes
            gscore : *kwargs
                the g score of the nodes
            fscore:
                the f score of the nodes
            open_nodes:
                list of the open nodes

        Methods
        -------
        outside_the_map(size, coord)
            check if coord are outside of the map
        heuristic (coord1, coord2)
            calcul heuristic between two coordinates
        calcul_path(start, goal, obstacles, size)
            calcul the shortest path between two coordinates
        """
        self.start = start
        self.goal = goal
        self.wallStates = wallStates
        self.map_size = map_size
        self.closed_nodes = set()
        self.came_from = {}
        self.gscore = {start: 0}
        self.fscore = {start: self.heuristic(start, goal)}
        self.open_nodes = []

        # start with the exploration of the start node
        heapq.heappush(self.open_nodes, (self.fscore[start], start))

    def g_value_from_goal(self, coord):
        """
            Calcul the g score value of a node from the start point

            Parameters
            ----------
            coord : tuple of int
                coordinates of the point

            Returns
            -------
            int
                g score of the coordinates
        """
        # while there is nodes to explore
        while not coord in self.closed_nodes:
            
            current = heapq.heappop(self.open_nodes)[1]
            self.closed_nodes.add(current)

            for i, j in self.NEIGHBORS:

                # new coordinates of the neighbor
                neighbor = current[0] + i, current[1] + j

                # skip the coordinates if its an obstacle or outisde the map
                if neighbor in self.wallStates or\
                 self.outside_the_map(self.map_size, neighbor):
                    continue

                # calcul new score
                tentative_g_score = self.gscore[current] + \
                    BackWardSearch.heuristic(current, neighbor)

                if neighbor in self.closed_nodes and\
                tentative_g_score >= self.gscore.get(neighbor, 0):
                    continue

                # node not visited yet or better score than before for these coordinates
                # update the variables
                if tentative_g_score < self.gscore.get(neighbor, 0) or\
                        neighbor not in [i[1]for i in self.open_nodes]:
                    self.came_from[neighbor] = current
                    self.gscore[neighbor] = tentative_g_score
                    self.fscore[neighbor] = tentative_g_score + \
                        BackWardSearch.heuristic(neighbor, coord)

                    # continue to explore this path
                    heapq.heappush(self.open_nodes, (self.fscore[neighbor], neighbor))
        return self.gscore[coord]
