
class Collision:
    """docstring for Collision."""

    def __init__(self, Lpaths):
        super(Collision, self).__init__()
        self.Lpaths = Lpaths
        self.collisionPointers  = [[] for i in range(len(Lpaths))]
        self.waiting = [True for  i in range (len(Lpaths))]


    def init_collisionPointers(self):
        """
        init the values of the collisionPointers matrix that keeps track of conflicts
        init the steps_free array that keeps the number of free turns left for the agent
        """
        for i in range(len(Lpaths)):
            for j in range(i,len(Lpaths)):
                if i!=j:
                    if crossing_paths(Lpaths[i], Lpaths[j]):
                        collisionPointers[i].append(j)
                        collisionPointers[j].append(i)

        for i in range(len(Lpaths)):
            init_permit(i)


    def crossing_paths(path1, path2):
        """
        looks for possible crossings between two paths
        """
        for i in range(len(path1)):
            for j in range(len(path2)):
                if path2[i]== path1[i]:
                    return True
        return False

    def new_conflicts(player_number):
        """
        deletes old conflits involving player_number
        updates matrix based on new pathing
        heuristic : new_pathed player gives priority to formerly conflicted players
        """
        for j in collisionPointers(player_number):
            self.collisionPointers[j].remove(player_number)
        for i in range(len(Lpaths)):
            if i!= player_number:
                if crossing_paths(Lpaths[i],Lpaths[player_number]):

                    if not can_walk(i):
                        self.collisionPointers[i].append(player_number)

                    self.collisionPointers[player_number].append(i)

    def can_walk(player_number):
        """
        true if no conflict involving the player, false otherwise
        """
        return collisionPointers[player_number]== []

    def create_new_path(player_number,start, goal, wallStates, map_size):
        """
        creates new path for this player
        deletes the former conflict that existed on the provious path of the player
        looks for new conflicts on the pathing
        handles conflicts bases on the defined policy (ethic,FIFO,random)
        """
        Lpaths[player_number] = a_star.calcul_path(start, goal, wallStates, map_size)
        new_conflicts(player_number)
