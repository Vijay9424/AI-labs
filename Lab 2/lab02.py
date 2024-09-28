import random
import copy
import time
import heapq

class Puzzle8:
    def __init__(self, board):
        self.board = board  
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  
        self.parent = None
        self.action = None

    def is_goal(self):
        return self.board == self.goal

    def get_blank(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    return (i, j)

    def actions(self):
        actions = []
        i, j = self.get_blank()

        if i > 0: actions.append('UP')
        if i < 2: actions.append('DOWN')
        if j > 0: actions.append('LEFT')
        if j < 2: actions.append('RIGHT')

        return actions

    def result(self, action):
        i, j = self.get_blank()
        new_board = [row[:] for row in self.board]

        if action == 'UP':
            new_board[i][j], new_board[i-1][j] = new_board[i-1][j], new_board[i][j]
        elif action == 'DOWN':
            new_board[i][j], new_board[i+1][j] = new_board[i+1][j], new_board[i][j]
        elif action == 'LEFT':
            new_board[i][j], new_board[i][j-1] = new_board[i][j-1], new_board[i][j]
        elif action == 'RIGHT':
            new_board[i][j], new_board[i][j+1] = new_board[i][j+1], new_board[i][j]

        child = Puzzle8(new_board)
        child.parent = self
        child.action = action
        return child

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

def bfs(problem):
    queue = [problem]
    explored = set()

    while queue:
        state = queue.pop(0)
        if state.is_goal():
            return state
        explored.add(tuple(map(tuple, state.board)))  

        for action in state.actions():
            child = state.result(action)
            if tuple(map(tuple, child.board)) not in explored:
                queue.append(child)

    return None

def dfs(problem):
    stack = [problem]
    explored = set()

    while stack:
        state = stack.pop()
        if state.is_goal():
            return state
        explored.add(tuple(map(tuple, state.board)))

        for action in state.actions():
            child = state.result(action)
            if tuple(map(tuple, child.board)) not in explored:
                stack.append(child)

    return None

def a_star(problem, heuristic):
    class HeapQueue:
        def __init__(self):
            self.elems = []
            self.index = 0

        def put(self, elem, priority):
            heapq.heappush(self.elems, (priority, self.index, elem))
            self.index += 1

        def get(self):
            return heapq.heappop(self.elems)[2]

        def empty(self):
            return not self.elems

    hq = HeapQueue()
    hq.put(problem, 0)
    cost = {tuple(map(tuple, problem.board)): 0}

    while not hq.empty():
        state = hq.get()
        if state.is_goal():
            return state

        for action in state.actions():
            child = state.result(action)
            new_cost = cost[tuple(map(tuple, state.board))] + 1  

            if tuple(map(tuple, child.board)) not in cost or new_cost < cost[tuple(map(tuple, child.board))]:
                cost[tuple(map(tuple, child.board))] = new_cost
                priority = new_cost + heuristic(child)
                hq.put(child, priority)

    return None

def heuristic_misplaced_tiles(state):
    return sum(1 for i in range(3) for j in range(3) if state.board[i][j] != state.goal[i][j] and state.board[i][j] != 0)

def backtrack(state):
    path = []
    while state.parent is not None:
        path.append(state.action)  
        state = state.parent
    return path[::-1]  

def generate_puzzle8(goal, depth):
    puzzle = Puzzle8(goal)
    for _ in range(depth):
        actions = puzzle.actions()
        puzzle = puzzle.result(random.choice(actions))
    return puzzle

if __name__ == '__main__':
    
    initial_board = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]  
    puzzle = Puzzle8(initial_board)

    print("Initial State:")
    print(puzzle)

    
    print("\nBFS Solution:")
    solution = bfs(puzzle)
    if solution:
        print(solution)
        print("Path:", backtrack(solution))
    else:
        print("No solution found!")

    
    print("\nDFS Solution:")
    solution = dfs(puzzle)
    if solution:
        print(solution)
        print("Path:", backtrack(solution))
    else:
        print("No solution found!")

    
    print("\nA* Solution with Misplaced Tiles Heuristic:")
    solution = a_star(puzzle, heuristic_misplaced_tiles)
    if solution:
        print(solution)
        print("Path:", backtrack(solution))
    else:
        print("No solution found!")

    
    depth = 10  
    generated_puzzle = generate_puzzle8(initial_board, depth)
    print("\nGenerated Puzzle at depth", depth, ":")
    print(generated_puzzle)
