import random
import sys

sys.path.append('../AStarAlgorithm')

from AStarSimplePath import AStarSimplePath as assp

class Collision:

    @staticmethod
    def detect_collision(pos_players, players_path, players_step):
        """Detect collision between the players

            Parameters
            ----------
            pos_players : *args
                coordinates of the players
            player1 : int
                number of the player
            players_path : *args
                path of the players
            players_step : *args
                step of the players

            Returns
            -------
            bool
                True if collision False otherwise
        """
        for i in range(len(players_path)):

            # information of player i
            path_i = players_path[i]
            step_player_i = players_step[i]
            pos_player_i = pos_players[i]
            next_pos_player_i = path_i[step_player_i]

            for j in range(len(players_path)):

                # same player
                if i == j: continue

                # information of player j
                path_j = players_path[j]
                step_player_j = players_step[j]
                pos_player_j = pos_players[j]
                next_pos_player_j = path_j[step_player_j]

                # next position is the same for both player
                if next_pos_player_i == next_pos_player_j:
                    return i

                # face to face collision
                elif pos_player_i == next_pos_player_j and\
                 pos_player_j == next_pos_player_i:
                    return i
        return False

    @classmethod
    def is_valid_coordinates(cls, coord, map_size, obstacles):
        """Check if some coordinates are valid

            Parameters
            ----------
            coord : tuple of int
                coordinates to verify
            map_size : int
                size of the map
            obstacles : *args
                coordinates of the obstacles

            Returns
            -------
            bool
                True if the coordinates are valid False otherwise
        """
        x, y = coord
        # inside the map
        if x < 0 or x > 19 or y < 0 or y > 19:
            return False
        # not a wall
        if coord in obstacles:
            return False
        return True

    @classmethod
    def random_move(cls, obstacles, player, players_path, players_step, pos_players):
        """Get a valid random move from a player

            Parameters
            ----------
            obstacles : *args
                coordinates of the obstacles
            player : int
                number of the player
            players_path : *args
                paths of the players
            players_step : *args
                steps of the players
            pos_players : *args
                coordinates of the players

            Returns
            -------
            tuple of int
                coordinates of the random move
        """
        row, col = pos_players[player]
        random_move = (row, col)
        for r, c in random.sample([(1,0),(-1,0),(0,1),(0,-1)], 4):
            next_coord = row+r, col+c
            if Collision.is_valid_coordinates(next_coord, 20, obstacles):
                random_move = next_coord
                break
        return random_move


    @staticmethod
    def manage_collision(player, players_path, players_step,
     pos_players, wallStates, again=False):
        """Modify the path of the player to evoid a collision

            Parameters
            ----------
            player : int
                number of the player
            players_path : *args
                paths of the players
            players_step : *args
                steps of the players
            pos_players : *args
                coordinates of the players
            wallStates : *args
                coordinates of the walls
        """
        # information of the player
        current_pos = pos_players[player]
        current_step = players_step[player]
        next_pos = players_path[player][current_step]

        # evoid collision on the next pos
        # consider it as an obstacle
        obstacles = wallStates + [next_pos]

        # next position is goal
        if current_step == len(players_path[player])-1:

            # remove the goal coordinates
            del players_path[player][-1]

            # make a random move, next iteration it'll calcul a path to the goal
            players_path[player].append(Collision.random_move(obstacles, player,
             players_path, players_step, pos_players))

        else:

            new_path = []

            # start is current pos
            start = current_pos
            # goal is the coordinates two steps later in the path
            goal = players_path[player][current_step+1]

            #calcul path from start to goal
            new_slice = assp.calcul_path(start, goal, obstacles, 20)

            # if there is no path to the wanted coordinates
            if again or new_slice is False:
                # add a random move
                new_path.append(Collision.random_move(obstacles, player,
                 players_path, players_step, pos_players))
                # remove the end of the path to add the random coordinates
                del players_path[player][current_step:]

                players_path[player] += new_path

            else:
                new_path += new_slice
                # remove the coordinates of the collision
                del players_path[player][current_step]
                # insert the new alternative slice into the path
                for i in range(len(new_path)-1):
                    players_path[player].insert(players_step[player]+i, new_path[i])
