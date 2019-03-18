import random

class Collision:

    @staticmethod
    def create_new_path(a_star, start, goal, wallStates, map_size):

        # create new path to the the new coordinates of the potion
        # use basic A* algorithm
        new_path = a_star.calcul_path(start, goal, wallStates, map_size)

        # start coordiantes and goal coordinates are the same
        # no valid path from start coordinates to the goal coordinates
        # next turn it will calcul a path again -> elif condition
        if new_path == [] or new_path is False:
            new_path = [start]

        # new path, no step executed yet
        return new_path, 0

    @staticmethod
    # test if there is a collision between player1 and another player
    def detect_collision(player1, players_path, players_step):
        next_coord = players_path[player1][players_step[player1]]
        for player2 in range(player1):
            player2_coord = players_path[player2][players_step[player2]-1]
            # next case if the same for both player
            if next_coord == player2_coord:
                return True
            # horizontal colision with 2 separate cases
            player1_current_coord = players_path[player1][players_step[player1]-1]
            if players_step[player2] > 1:
                player2_previous_coord = players_path[player2][players_step[player2]-2]
                if player1_current_coord == player2_coord and\
                 next_coord == player2_previous_coord:
                 return True
        return False

    @classmethod
    # test if the coord are valid coordinates
    def is_possible(cls, coord, wallStates):
        x, y = coord
        # inside the map
        if x < 0 or x > 19 or y < 0 or y > 19:
            return False
        # not a wall
        if coord in wallStates:
            return False
        return True

    @classmethod
    def random_move(cls, player1, players_path, players_step, wallStates):
        row, col = players_path[player1][players_step[player1]-1]
        random_move = (row, col)
        for r, c in random.sample([(1,0),(-1,0),(0,1),(0,-1)], 4):
            next_coord = row+r, col+c
            if Collision.is_possible(next_coord, wallStates):
                random_move = next_coord
                break
        return random_move

    @staticmethod
    # create new path for player1 after the detection of a collision
    def manage_collision(player1, players_path, players_step, wallStates, a_star):
        new_path = []
        # get the position of the players that have already moved
        pos_player = [players_path[i][players_step[i]-1] for i in range(player1)]
        current_pos_player1 = players_path[player1][players_step[player1]-1]
        # next case is the goal
        if players_step[player1] == len(players_path[player1])-1:
            # make a random move to avoid the collision
            new_path.append(Collision.random_move(player1,
             players_path, players_step, wallStates+pos_player))
            # create a new path from the random coord to the goal
            goal_player1 = players_path[player1][-1]
            new = Collision.create_new_path(a_star, new_path[0],
             goal_player1, wallStates + pos_player, 20)[0]
            new_path += new
            # add the new slice of path to the path
            for i in range(len(new_path)):
                players_path[player1].insert(players_step[player1]+i, new_path[i])
        else:
            # next case after the collision
            next_case = players_path[player1][players_step[player1]+1]
            new_path = Collision.create_new_path(a_star, current_pos_player1,
             next_case, wallStates + pos_player, 20)[0]
            # remove the coord. of the collision from the player's path
            del players_path[player1][players_step[player1]]
            # add the new slice of path to the path
            for i in range(len(new_path)-1):
                players_path[player1].insert(players_step[player1]+i, new_path[i])
        # infinite collision by the current path
        # create new path from the pos to the goal
        if Collision.detect_collision(player1, players_path, players_step):
            # make a random move to avoid the collision
            new_path = [Collision.random_move(player1,
             players_path, players_step, wallStates+pos_player)]
            # create a new path from the random coord to the goal
            # whith the position of other players in the wallStates
            goal_player1 = players_path[player1][-1]
            new = Collision.create_new_path(a_star, new_path[0],
             goal_player1, wallStates + pos_player, 20)[0]
            new_path += new
            # replace the path of the player with the new one
            players_path[player1] = [current_pos_player1] + new_path
            players_step[player1] = 1
