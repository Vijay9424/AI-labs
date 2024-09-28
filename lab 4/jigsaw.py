import numpy as np
import random


goal_state = np.array([[1, 2, 3, 4],
                        [5, 6, 7, 8],
                        [9, 10, 11, 12],
                        [13, 14, 15, 0]])  


initial_state = np.array([[1, 2, 3, 4],
                           [5, 6, 7, 8],
                           [0, 10, 11, 12],
                           [9, 13, 14, 15]])

def calculate_cost(state):
    """Calculate the number of misplaced tiles."""
    return np.sum(state != goal_state) - (state[3, 3] != goal_state[3, 3])  

def get_successors(state):
    """Generate successor states by swapping empty space with adjacent tiles."""
    successors = []
    zero_pos = np.argwhere(state == 0)[0]
    x, y = zero_pos[0], zero_pos[1]
    
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        if 0 <= x + dx < state.shape[0] and 0 <= y + dy < state.shape[1]:
            new_state = state.copy()
            
            new_state[x, y], new_state[x + dx, y + dy] = new_state[x + dx, y + dy], new_state[x, y]
            successors.append(new_state)
    
    return successors
    
def simulated_annealing(initial_state, initial_temp, cooling_rate):
    current_state = initial_state
    current_cost = calculate_cost(current_state)
    temperature = initial_temp

    while current_cost > 0 and temperature > 1e-10:  
        successors = get_successors(current_state)
        next_state = random.choice(successors)
        next_cost = calculate_cost(next_state)
        
        if next_cost < current_cost:
            current_state = next_state
            current_cost = next_cost
        else:
            
            if temperature > 0:
                acceptance_probability = np.exp((current_cost - next_cost) / temperature)
                if random.random() < acceptance_probability:
                    current_state = next_state
                    current_cost = next_cost
        
        
        temperature *= cooling_rate
        
    return current_state


if __name__ == "__main__":
    initial_temp = 1000
    cooling_rate = 0.99
    final_state = simulated_annealing(initial_state, initial_temp, cooling_rate)
    
    print("Final State:")
    print(final_state)
    print("Cost:", calculate_cost(final_state))
