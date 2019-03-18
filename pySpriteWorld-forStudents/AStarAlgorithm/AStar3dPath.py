import heapq
import AStarSimplePath as assp

class AStar3dPath(assp.AStarSimplePath):

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
        self.reservation_table = {}

    def calcul_path(self, start, goal, obstacles, size, time):
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
        print("time", time)
        # init the parameter
        closed_nodes = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: AStar3dPath.heuristic(start, goal)}
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
                # calcul new g score
                tentative_g_score = gscore[current] + \
                    AStar3dPath.heuristic(current, neighbor)

                if neighbor in closed_nodes and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                row, col = neighbor

                if (row, col, time+tentative_g_score) in self.reservation_table:
                    print(row, col, time+tentative_g_score)
                    continue

                # node not visited yet or better score than before for these coordinates
                # update the variables
                if tentative_g_score < gscore.get(neighbor, 0) or\
                        neighbor not in [i[1]for i in open_nodes]:
                    print("=>", row, col, time+gscore[current])
                    self.reservation_table[(row, col, time+gscore[current])] = True
                    self.reservation_table[(row, col, time+tentative_g_score)] = True
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + \
                        AStar3dPath.heuristic(neighbor, goal)
                    # continue to explore this path
                    heapq.heappush(open_nodes, (fscore[neighbor], neighbor))
        # no path found
        return False
