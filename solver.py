from __future__ import print_function
import rubik

def shortest_path(start, end):
    """
    For Question 1, using BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves.

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """

    visited_nodes = []
    status = []
    parent = []
    move_taken = []

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
    while (curr_parent != None and parent[curr_parent] != None):
        ans.append(move_taken[curr_parent])
        curr_parent = parent[curr_parent]

    # cube = start[:]
    # for move in ans[::-1]:
    #     cube = rubik.perm_apply(move, cube)
    # assert cube == end

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

    # INITIALISATION
    # returned list of moves
    result_path = []
    # bfs distance and recovery dictionaries
    dist_front , recover_front = {} , {}
    dist_back  , recover_back  = {} , {}
    # bfs queues, using deque instead of list to have O(1) removal of 1st element
    q_front = __import__('collections').deque()
    q_back  = __import__('collections').deque()

    # SETTING UP
    # setting up bfs from front
    q_front.append(start)
    dist_front[start] = 0
    recover_front[start] = (None,None)
    # setting up bfs from back
    q_back.append(end)
    dist_back[end] = 0
    recover_back[end] = (None,None)

    # BFS LOOP - runs till both bfs intersect
    done = False
    #
    while not done:
        # state to act on in front bfs
        curr = q_front.popleft()

        # visiting all neighbours
        for move in rubik.quarter_twists:
            # find neighbour by applying move
            neighbour = rubik.perm_apply(move, curr)
            # if this has not been explored yet
            if neighbour not in dist_front:
                dist_front[neighbour]    = dist_front[curr] + 1
                recover_front[neighbour] = (curr, move)
                q_front.append(neighbour)
            # if this has been explored from back, then intersection
            if neighbour in dist_back:
                intersection_pt = neighbour
                done = True
                break

        # no need to continue back bfs if intersection found
        if done: break

        # state to act on in back bfs
        curr = q_back.popleft()

        # visiting all neighbours
        for move in rubik.quarter_twists:
            # find neighbour by applying move
            neighbour = rubik.perm_apply(move, curr)
            # if this has not been explored yet
            if neighbour not in dist_back:
                dist_back[neighbour]    = dist_back[curr] + 1
                recover_back[neighbour] = (curr, move)
                q_back.append(neighbour)
            # if this has been explored from front, then intersection
            if neighbour in dist_front:
                intersection_pt = neighbour
                done = True
                break

    # BACKTRACKING
    # recover moves from start to current state
    #         using recovery list of front bfs
    ptr = intersection_pt
    while ptr != start:
        result_path.append(recover_front[ptr][1])
        ptr = recover_front[ptr][0]
    result_path = result_path[::-1]
    # recover moves from current state to end
    #         using recovery list of back bfs
    ptr = intersection_pt
    while ptr != end:
        result_path.append(rubik.perm_inverse(recover_back[ptr][1]))
        ptr = recover_back[ptr][0]

    # SANITY CHECK
    cube = start[:]
    for move in result_path:
        cube = rubik.perm_apply(move, cube)
    assert cube == end

    return result_path
    # raise NotImplementedError

if __name__ == "__main__":

    no_of_scrambling_moves = int(input("Enter how many times to scramble: "))
    start , end = rubik.I , rubik.I
    for _ in range(no_of_scrambling_moves):
        move = __import__('random').choice(rubik.quarter_twists)
        end  = rubik.perm_apply(move, end)

    timer = __import__('timeit').default_timer

    start_t = timer()
    fast_path = shortest_path_optmized(start,end)
    end_t = timer()
    print("Minimum number of moves needed to solve is:", len(fast_path))

    print("Optimised version took", end_t-start_t, "seconds.")

    start_t = timer()
    path = shortest_path(start,end)
    end_t = timer()

    print("Non-optimised version took", end_t-start_t, "seconds.")

    assert len(path) == len(fast_path), "One of the functions reports a longer path than the other."
