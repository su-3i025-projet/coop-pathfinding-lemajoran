import heapq
import AStarSimplePath as assp
from BackWardSearch import BackWardSearch

class AStar3dPath(assp.AStarSimplePath):
    """
        Class representing the A* algorithm using true distance as
        heuristic

        Attributes
        ----------
        neighbors : *args
            list of the possible move to reach a neighbor
        reservation : *kwargs
            reservation table to stock tuple (coord, time)

        Methods
        -------
        heuristic (coord1, coord2)
            calcul heuristic between two coordinates
        calcul_path(start, goal, obstacles, size)
            calcul the shortest path between two coordinates
    """
    NEIGHBORS = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
    reservation = {}
    STEP_NUMBER = 8

    @classmethod
    def heuristic(cls, coord, backward):
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
        return backward.g_value_from_goal(coord)

    # @staticmethod
    # def pause(coord, player, time, wallStates):
    #     print("pause")
    #     if ((coord, time) in AStar3dPath.reservation and\
    #         AStar3dPath.reservation[(coord, time)] != player):
    #         row, col = coord
    #         for r, c in AStar3dPath.NEIGHBORS:
    #             if ((row+r, col+r), time) not in AStar3dPath.reservation and\
    #              (row+r, col+r) not in wallStates and row+r < 20 and row+r >-1\
    #              and col+c<20 and col+c>-1:
    #                 AStar3dPath.reservation[((row+r, col+r), time)] = player
    #                 return [(row+r, col+r)]
    #         else:
    #             print("pas de case possible")
    #             while True: pass
    #     AStar3dPath.reservation[(coord, time)] = player
    #     return [coord]

    @classmethod
    def remove_elt_from_dict(cls, player):
        """
            Remove reservations from the reservation table

            Parameters
            ----------
            player : int
                number of the player
        """
        elt_to_remove = []

        for k in AStar3dPath.reservation.keys():
            if AStar3dPath.reservation[k] == player:
                elt_to_remove.append(k)
        for i in elt_to_remove:
            del AStar3dPath.reservation[i]

    @staticmethod
    def calcul_path(start, goal, obstacles, size, time, player):
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
        # run it from goal to start
        backward = BackWardSearch(goal, start, obstacles, size)

        # init the parameter
        closed_nodes = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: AStar3dPath.heuristic(start, backward)}
        open_nodes = []

        # start with the exploration of the start node
        heapq.heappush(open_nodes, (fscore[start], start))

        # while there is nodes to explore
        while open_nodes:

            current = heapq.heappop(open_nodes)[1]

            if gscore[current] > AStar3dPath.STEP_NUMBER:
                continue

            closed_nodes.add(current)

            for i, j in AStar3dPath.NEIGHBORS:

                # new coordinates of the neighbor
                neighbor = current[0] + i, current[1] + j

                # skip the coordinates if its an obstacle or outisde the map
                if neighbor in obstacles or AStar3dPath.outside_the_map(size, neighbor):
                    continue

                # calcul new distance from start coordinates
                if neighbor != current:
                    tentative_g_score = gscore[current] + 1
                else: tentative_g_score = gscore[current]

                # already visited with a g value lower than the current one
                if neighbor in closed_nodes and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                # coordinates already reserved by a player
                if (neighbor, time+gscore[current]) in AStar3dPath.reservation and\
                AStar3dPath.reservation[(neighbor, time+gscore[current])] != player:
                    continue

                # coordinates already reserved by a player
                if (neighbor, time+tentative_g_score) in AStar3dPath.reservation and\
                AStar3dPath.reservation[(neighbor, time+tentative_g_score)] != player:
                    continue

                # node not visited yet or better score than before for these coordinates
                # update the variables
                if tentative_g_score < gscore.get(neighbor, 0) or\
                        neighbor not in [i[1]for i in open_nodes]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + \
                        AStar3dPath.heuristic(neighbor, backward)
                    # continue to explore this path
                    heapq.heappush(open_nodes, (fscore[neighbor], neighbor))

        best_node = None
        best_h = float('inf')

        for node in closed_nodes:
            
            if gscore[node] == AStar3dPath.STEP_NUMBER:
                temp_h = AStar3dPath.heuristic(node, backward)
                if best_node is None or temp_h < best_h:
                    best_node = node
                    best_h = temp_h

        data = []

        while best_node in came_from:
            data.append(best_node)
            best_node = came_from[best_node]

        data = data[::-1]

        AStar3dPath.remove_elt_from_dict(player)

        # reservation of the coordinates
        AStar3dPath.reservation[(start, time)] = player
        time += 1
        for coord in data:
            AStar3dPath.reservation[(coord, time)] = player
            time += 1
        return data
