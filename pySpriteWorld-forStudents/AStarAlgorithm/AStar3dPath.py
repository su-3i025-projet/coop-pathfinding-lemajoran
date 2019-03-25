import heapq
import AStarSimplePath as assp
from BackWardSearch import BackWardSearch

class AStar3dPath(assp.AStarSimplePath):
    """Class representing the A* algorithm using true distance as
        heuristic

        Attributes
        ----------
        neighbors : *args
            list of the possible move to reach a neighbor
        reservation : *kwargs
            reservation table to stock tuple (coord, time)

        Methods
        -------
        heuristic(coord1, coord2)
            calcul heuristic between two coordinates
        calcul_path(start, goal, obstacles, size)
            calcul the shortest path between two coordinates
    """
    NEIGHBORS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    reservation = {}
    STEP_NUMBER = 8

    @classmethod
    def heuristic(cls, coord, backward):
        """Calcul the heuristic between two coordinates

            Parameters
            ----------
            coord : tuple of int
                coordinates of the point
            backward : BackWardSearch
                backward object for heuristic

            Returns
            -------
            int
                True Distance between a and b
        """
        return backward.g_value_from_goal(coord)

    @classmethod
    def random_move(cls, coord, player, time, wallStates):
        """Make a valid random move

            Parameters
            ----------
            coord : tuple of int
                coordinates of the player
            player : int
                number of the player
            time : int
                time of the move
            wallStates : *args
                coordinates of the walls

            Returns
            -------
            tuple of int
                random valid move
        """
        row, col = coord
        # search valid coordinates among the neighbors
        for r, c in AStar3dPath.NEIGHBORS:
            neighbor = row+r, col+c
            if (neighbor, time) in AStar3dPath.reservation and\
            AStar3dPath.reservation[(neighbor, time)] != player:
                continue
            if (neighbor, time-1) in AStar3dPath.reservation and\
            AStar3dPath.reservation[(neighbor, time-1)] != player:
                continue
            if neighbor in wallStates or\
             AStar3dPath.outside_the_map(20, neighbor):
                continue
            return neighbor
        return coord

    @classmethod
    def remove_elt_from_dict(cls, player):
        """Remove reservations from the reservation table

            Parameters
            ----------
            player : int
                number of the player
        """
        elt_to_remove = []
        # get key to remove
        for k in AStar3dPath.reservation.keys():
            if AStar3dPath.reservation[k] == player:
                elt_to_remove.append(k)
        # remove elements from dictionnary
        for i in elt_to_remove:
            del AStar3dPath.reservation[i]

    @classmethod
    def final_path(cls, came_from, closed_nodes, backward, start, player, wallStates, time):
        """Calcul final path for a player

            Parameters
            ----------
            came_from : *kwargs
                predecessors of the nodes
            closed_nodes : *kwargs
                closed nodes
            backward : BackWardSearch
                backward object
            start : tuple of int
                initial position of the player
            player : int
                number of the player
            obstacles : *args
                coordinate of the walls
            time : int
                time of the move

            Returns
            -------
            *args
                final path of the player
        """
        best_node = None
        best_h = float('inf')

        # get the best node to the partial path
        # search for the best heuristic
        for node in closed_nodes:

            temp_h = AStar3dPath.heuristic(node, backward)
            if best_node is None or temp_h < best_h:
                    best_node = node
                    best_h = temp_h

        data = []

        # get all the node of the path
        while best_node in came_from:
            data.append(best_node)
            best_node = came_from[best_node]

        # reverse the path to have it in the right way
        data = data[::-1]
        # remove previous reservation of the player
        AStar3dPath.remove_elt_from_dict(player)
        # assert new reservation for the coordinates of the path
        AStar3dPath.reservation[(start, time)] = player
        time += 1

        # empty path
        if data == []:

            # another player at the current position next step
            if (best_node, time) in AStar3dPath.reservation and\
                AStar3dPath.reservation[(best_node, time)] != player:
                # make random move
                data = [AStar3dPath.random_move(start, player,
                 time, wallStates)]
            # stay on the current pos
            else: data = [best_node]
            AStar3dPath.reservation[(data[0], time)] = player

        else:

            for coord in data:
                # make a reservation for each coordinates of the path
                AStar3dPath.reservation[(coord, time)] = player
                time += 1

        return data


    @staticmethod
    def calcul_path(start, goal, obstacles, size, time, player):
        """Calcul the shortest path between two coordinates

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
                partial path from start to goal
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

            closed_nodes.add(current)

            if gscore[current] > AStar3dPath.STEP_NUMBER:
                continue

            for i, j in AStar3dPath.NEIGHBORS:

                # new coordinates of the neighbor
                neighbor = current[0] + i, current[1] + j

                # skip the coordinates if its an obstacle or outisde the map
                if neighbor in obstacles or AStar3dPath.outside_the_map(size, neighbor):
                    continue

                # calcul new distance from start coordinates
                tentative_g_score = gscore[current] + 1

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

        return AStar3dPath.final_path(came_from, closed_nodes, backward, start, player, obstacles, time)
