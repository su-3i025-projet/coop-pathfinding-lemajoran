from copy import deepcopy

class CoopPath:

    @classmethod
    # test if there is a collision between player1 and another player
    def detect_collision(cls, path1, path2):
        """Detect a collision between two paths

            Parameters
            ----------
            path1 : *args
                list of the coord. for the first path
            path2 : *args
                list of the coord. for the second path

            Returns
            -------
            bool
                True if collision False otherwise
        """
        if path1 is False or path2 is False:
            return True

        if len(path1) > len(path2):
            min_path = path2
            max_path = path1
        else:
            min_path = path1
            max_path = path2

        for i in range(len(min_path)):
            # they are on the same case at the same moment
            if path1[i] == path2[i]:
                return True
            # horizontal colision with 2 separate cases
            if len(path1[i:]) > 1 and len(path2[i:]) > 1:
                if path1[i] == path2[i+1] and path2[i] == path1[i+1]:
                 return True

        if min_path[-1] in max_path[len(min_path)-1:]:
            return True

        return False

    @staticmethod
    def put_path_in_group(index, paths, path_group):
        """Add a path in a list of groups, evoid collision

            Parameters
            ----------
            index : int
                index of the path to add
            paths : *args
                list of every paths
            path_group: *args
                list of the groups
        """
        if len(path_group) == 0:
            path_group.append([index])
        else:
            for l in path_group[::-1]:
                # check for collision between all the paths of the group
                for i in l:
                    # detect a collision between the path  and the paths in the group
                    if CoopPath.detect_collision(paths[index], paths[i]):
                        break
                else:
                    l.append(index)
                    break
            else:
                # no convenient group for the paths index
                path_group.append([index])

    @staticmethod
    def organize_groups(paths):
        """Organize the different groups from a list of paths

            Parameters
            ----------
            paths: *args
                list of the paths to group

            Returns
            -------
            *args
                list of the groups
        """
        res = []
        already_placed = []

        # stop when every path have a group
        while len(already_placed) < len(paths):
            # compare every path with the other ones
            for i in range(len(paths)):
                # if the path already has a group continue
                if i in already_placed: continue
                # mark the path as visited
                already_placed.append(i)
                # put the path in a group
                CoopPath.put_path_in_group(i, paths, res)
        return CoopPath.reorganize_groups(paths, res)

    @staticmethod
    def number_of_move_before_next_group(paths, grouped_path):
        """Calcul the number of move before the next group of path
            has to start

            Parameters
            ----------
            paths : *args
                list of every path
            grouped_path : *args
                list of the group of paths

            Returns
            -------
            int
                number of move before the next group has to start
        """
        longuest_path_index = max(grouped_path[0], key=lambda x: len(paths[x]))
        return len(paths[longuest_path_index])

    @staticmethod
    def reorganize_groups(paths, path_group):
        """Reorganize a list of groups

            Parameters
            ----------
            paths : *args
                list of the paths
            path_group : *args
                list of the groups

            Returns
            -------
            *args
                A reorganized list of groups
        """
        new_grouped_path = []
        # go through every group of path
        for group in path_group:
            for i in group:
                CoopPath.put_path_in_group(i, paths, new_grouped_path)
        # remove empty path from the group 0
        res = deepcopy(new_grouped_path)
        for i in new_grouped_path[0]:
            if paths[i] is False:
                res.append([i])
                res[0].remove(i)
        # remove the group 0 if it's empty
        while res[0] == []:
            res.pop(0)
        return res
