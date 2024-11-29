def a_star(initial_state, heuristic):
    pq = []
    heapq.heappush(pq, (0 + heuristic(initial_state), initial_state))
    cost_so_far = {tuple(initial_state.board): 0}
    closed_set = set()

    while pq:
        current_priority, current_state = heapq.heappop(pq)
        if current_state.is_goal():
            return current_state

        closed_set.add(tuple(current_state.board))

        for successor in current_state.get_successors():
            new_cost = cost_so_far[tuple(current_state.board)] + 1  

            if tuple(successor.board) not in cost_so_far or new_cost < cost_so_far[tuple(successor.board)]:
                cost_so_far[tuple(successor.board)] = new_cost
                priority = new_cost + heuristic(successor)
                heapq.heappush(pq, (priority, successor))

    return None  
