def hill_climbing(problem):
    current = problem.initial_state()
    
    while True:
        neighbors = current.get_neighbors()
        if not neighbors:
            break
        
        next_state = max(neighbors, key=lambda state: heuristic(state))
        if heuristic(next_state) <= heuristic(current):
            break  
        
        current = next_state
    
    return current
