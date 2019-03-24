import heapq

class AStarSimplePath:

    """
        Class representing the A* algorithm using manhattan distance as
        heuristic

        Attributes
        ----------
        neighbors : *args
            list of the possible moves

        Methods
        -------
        outside_the_map(size, coord)
            check if coord are outside of the map
        heuristic (coord1, coord2)
            calcul heuristic between two coordinates
        calcul_path(start, goal, obstacles, size)
            calcul the shortest path between two coordinates
    """

    NEIGHBORS= [(0, 1), (0, -1), (1, 0), (-1, 0)]

    @classmethod
    def outside_the_map(cls, size, coord):
        """
            Check if a point is outside of the map surface

            Parameters
            ----------
            size : int
                width of the map
            coord : tuple of int
                coordinates of the point

            Returns
            -------
            bool
                True if the point is outside of the map otherwise False
        """
        x, y = coord
        # in the map, check the coordinates with the size of the map
        return x >= size or x < 0 or y >= size or y < 0

    @staticmethod
    def manhattan_distance(coord1, coord2):
        """
            Calcul the distance of manhattan between two coordinates

            Parameters
            ----------
            coord1 : tuple of int
                coordinates of the first point
            coord2 : tuple of int
                coordinates of the second point

            Returns
            ----------
            int
                manhattan's distance between a and b
        """
        x1, y1 = coord1
        x2, y2 = coord2
        return abs(x2 - x1) + abs(y2 - y1)

    @classmethod
    def heuristic(cls, coord1, coord2):
        """
            Calcul the heuristic between two coordinates

            Parameters
            ----------
            coord1 : tuple of int
                coordinates of the first point
            coord2 : tuple of int
                coordinates of the second point

            Returns
            -------
            int
                heuristic between a and b
        """
        return AStarSimplePath.manhattan_distance(coord1, coord2)

    @staticmethod
    def calcul_path(start, goal, obstacles, map_size):
        """
            Calcul the shortest path between two coordinates

            Parameters
            ----------
            start : tuple of int
                coordinates of the start point
            goal : tuple of int
                coordinates of the goal point
            obstacles : *args
                list of the coordinates of the obstacles
            map_size : int
                size of the map

            Returns
            -------
            *args
                shortest path from start to goal
            bool
                no path exists
        """
        # init the parameter
        closed_nodes = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: AStarSimplePath.heuristic(start, goal)}
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

            for i, j in AStarSimplePath.NEIGHBORS:
                # new coordinates of the neighbor
                neighbor = current[0] + i, current[1] + j
                # skip the coordinates if its an obstacle or outisde the map
                if neighbor in obstacles or\
                 AStarSimplePath.outside_the_map(map_size, neighbor):
                    continue
                # calcul new score
                tentative_g_score = gscore[current] + \
                    AStarSimplePath.heuristic(current, neighbor)
                if neighbor in closed_nodes and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                # node not visited yet or better score than before for these coordinates
                # update the variables
                if tentative_g_score < gscore.get(neighbor, 0) or\
                        neighbor not in [i[1]for i in open_nodes]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + \
                        AStarSimplePath.heuristic(neighbor, goal)
                    # continue to explore this path
                    heapq.heappush(open_nodes, (fscore[neighbor], neighbor))
        # no path found
        return False
