import heapq
import random


EMPTY_SLOT = 0
MARBLE = 1


class MarbleSolitaireState:
    def __init__(self, board, moves=0):
        self.board = board
        self.moves = moves
        self.empty_position = self.board.index(EMPTY_SLOT)  
        self.goal_state = self.create_goal_state()
    
    def create_goal_state(self):
        
        goal = [MARBLE] * len(self.board)
        goal[len(goal) // 2] = EMPTY_SLOT  
        return goal

    def is_goal(self):
        return self.board == self.goal_state

    def get_successors(self):
        successors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
        for direction in directions:
            new_board = self.move(direction)
            if new_board:
                successors.append(new_board)
        return successors

    def move(self, direction):
        y = self.empty_position // 7  
        x = self.empty_position % 7
        
        
        dy, dx = direction
        marble_y, marble_x = y + dy, x + dx
        landing_y, landing_x = y + 2 * dy, x + 2 * dx

        if self.is_valid_move(marble_x, marble_y, landing_x, landing_y):
            new_board = self.board[:]
            new_board[self.empty_position], new_board[marble_y * 7 + marble_x], new_board[landing_y * 7 + landing_x] = new_board[landing_y * 7 + landing_x], MARBLE, EMPTY_SLOT
            return MarbleSolitaireState(new_board, self.moves + 1)
        return None

    def is_valid_move(self, marble_x, marble_y, landing_x, landing_y):
        
        if 0 <= marble_x < 7 and 0 <= marble_y < 7 and 0 <= landing_x < 7 and 0 <= landing_y < 7:
            return (self.board[marble_y * 7 + marble_x] == MARBLE and
                    self.board[landing_y * 7 + landing_x] == EMPTY_SLOT)
        return False

    def __lt__(self, other):
        return self.moves < other.moves



def priority_queue_search(initial_state):
    pq = []
    heapq.heappush(pq, (0, initial_state))  
    closed_set = set()

    while pq:
        current_priority, current_state = heapq.heappop(pq)
        if current_state.is_goal():
            return current_state  

        closed_set.add(tuple(current_state.board))

        for successor in current_state.get_successors():
            if tuple(successor.board) not in closed_set:
                heapq.heappush(pq, (successor.moves, successor))

    return None  



def heuristic_marbles_remaining(state):
    return sum(1 for cell in state.board if cell == MARBLE)

def heuristic_distance_to_goal(state):
    
    distance = 0
    for index, value in enumerate(state.board):
        if value == MARBLE:
            target_position = len(state.board) // 2  
            distance += abs(target_position // 7 - index // 7) + abs(target_position % 7 - index % 7)
    return distance



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



def solve_marble_solitaire():
    initial_board = [1] * 49  
    initial_board[24] = EMPTY_SLOT  

    initial_state = MarbleSolitaireState(initial_board)
    print("Solving Marble Solitaire...")

    
    print("Priority Queue Search Solution:")
    solution = priority_queue_search(initial_state)
    print("Moves:", solution.moves) if solution else print("No solution found!")

    print("\nBest-First Search Solution:")
    solution = best_first_search(initial_state, heuristic_distance_to_goal)
    print("Moves:", solution.moves) if solution else print("No solution found!")

    print("\nA* Search Solution:")
    solution = a_star(initial_state, heuristic_distance_to_goal)
    print("Moves:", solution.moves) if solution else print("No solution found!")



def generate_k_sat(k, m, n):
    clauses = set()
    
    while len(clauses) < m:
        clause = random.sample(range(1, n + 1), k)
        
        clause = [x if random.choice([True, False]) else -x for x in clause]
        clauses.add(tuple(sorted(clause)))

    return list(clauses)



def generate_and_solve_k_sat():
    k = 3  
    m = 5  
    n = 10  
    
    sat_problem = generate_k_sat(k, m, n)
    print("Generated k-SAT Problem:")
    for clause in sat_problem:
        print(clause)


if __name__ == "__main__":
    solve_marble_solitaire()
    generate_and_solve_k_sat()
