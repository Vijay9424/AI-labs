import heapq

class MarbleSolitaireState:
    def __init__(self, board, moves=0):
        self.board = board
        self.moves = moves
        self.empty_position = self.board.index(0)  
        self.goal_state = self.create_goal_state()
    
    def create_goal_state(self):
        
        goal = [1] * len(self.board)
        goal[len(goal)//2] = 0  
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
        
        
        pass

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
