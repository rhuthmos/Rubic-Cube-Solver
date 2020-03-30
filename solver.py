import rubik
import copy

visited_nodes = []
status = []
parent = []
move_taken = []

def shortest_path(start, end):
    """
    For Question 1, using BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves.

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    # initialize
    visited_nodes.append(start)
    status.append(False)
    parent.append(None)
    move_taken.append(None)

    queue = [start]
    while (len(queue)>0):
        u = queue.pop(0)
        # all neighbours of u
        for moves in rubik.quarter_twists:
            v = rubik.perm_apply(moves, u)
            idx = visited_nodes.find(v)
            # if v is a white node
            if (idx == -1):
                visited_nodes.append(v)
                status.append(False)    # make v a gray naode
                parent.append(visited_nodes.find(u))    # insert parent
                move_taken.append(rubik.quarter_twists_names[moves])    # insert taken move from u to v
                queue.append(v)
        status[visited_nodes.find(u)] = True    # make u a black node
        if (u == end):
            break
    
    ans = []
    #retrace the moves
    idx = visited_nodes.find(end)
    curr_parent = parent[idx]
    ans.append(move_taken[idx])
    while (curr_parent != None):
        idx = visited_nodes.find(curr_parent)
        curr_parent = parent[idx]
        ans.append(move_taken[idx])
    
    return ans[::-1]
    #raise NotImplementedError

def shortest_path_optmized(start, end):
    """
    For Question 2, using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    raise NotImplementedError
