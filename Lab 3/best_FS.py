def best_first_search(initial_state, heuristic):
    pq = []
    heapq.heappush(pq, (heuristic(initial_state), initial_state))  
    closed_set = set()

    while pq:
        current_priority, current_state = heapq.heappop(pq)
        if current_state.is_goal():
            return current_state

        closed_set.add(tuple(current_state.board))

        for successor in current_state.get_successors():
            if tuple(successor.board) not in closed_set:
                heapq.heappush(pq, (heuristic(successor), successor))

    return None  
