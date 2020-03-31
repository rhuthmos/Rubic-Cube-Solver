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
            #idx = visited_nodes.find(v)
            # if v is a white node
            if not(v in visited_nodes):
                visited_nodes.append(v)
                status.append(False)    # make v a gray naode
                parent.append(visited_nodes.index(u))    # insert parent
                move_taken.append(list(moves))    # insert taken move from u to v
                queue.append(v)
        status[visited_nodes.index(u)] = True    # make u a black node
        if (u == end):
            break
    
    ans = []
    #retrace the moves
    idx = visited_nodes.index(end)
    curr_parent = parent[idx]
    ans.append(move_taken[idx])
   # print("ans: ", ans)
    while (curr_parent != None and parent[curr_parent] != None):
        ans.append(move_taken[curr_parent])
        curr_parent = parent[curr_parent]
    #print (ans)
    return ans[::-1]
    #raise NotImplementedError

def shortest_path_optmized(start, end):
    """
    For Question 2, using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    # simultaneous bfs from both the ends and maintain visted_nodes_1 and 2.
    # when node is discovered while bfs of start check if it is present in visite_nodes_2 and vice versa to check meeting point
    raise NotImplementedError

if __name__ == "__main__":
    ender = rubik.I
    starter = rubik.perm_apply(rubik.F,rubik.L)
    starter = rubik.perm_apply(starter,rubik.U)
    starter = rubik.perm_apply(starter,rubik.F)
   # starter = rubik.perm_apply(starter,rubik.I)
   # starter = rubik.perm_apply(starter,rubik.I)
    instr = shortest_path(starter,ender)
    #print(instr)
    for item in instr:
        starter = rubik.perm_apply(item,starter)
    print(starter)