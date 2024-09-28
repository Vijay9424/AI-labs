

import heapq

def levenshtein_distance(s1, s2):
    """Calculates the Levenshtein distance between two strings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    return dp[m][n]

def a_star_search(start, goal, heuristic, document1, document2):
    """Performs A* search to find the optimal alignment."""
    open_list = [(0, 0, 0, start)]  
    closed_set = set()
    parent_dict = {}

    while open_list:
        f_cost, g_cost, h_cost, current_state = heapq.heappop(open_list)

        if current_state == goal:
            return reconstruct_path(parent_dict, current_state)

        closed_set.add(current_state)

        for neighbor in get_neighbors(current_state, document1, document2):
            neighbor_g_cost = g_cost + cost_to_neighbor(current_state, neighbor, document1, document2)
            neighbor_h_cost = heuristic(neighbor, goal)
            neighbor_f_cost = neighbor_g_cost + neighbor_h_cost

            if neighbor not in closed_set:
                parent_dict[neighbor] = current_state
                heapq.heappush(open_list, (neighbor_f_cost, neighbor_g_cost, neighbor_h_cost, neighbor))

    return None

def reconstruct_path(parent_dict, current_state):
    """Reconstructs the path from the start to the goal state."""
    path = [current_state]
    while current_state in parent_dict:
        current_state = parent_dict[current_state]
        path.insert(0, current_state)
    return path

def get_neighbors(state, document1, document2):
    """Generates possible neighbor states from the given state."""
    neighbors = []

    
    if state[0] < len(document1) and state[1] < len(document2):
        neighbors.append((state[0] + 1, state[1] + 1))

    
    if state[0] < len(document1):
        neighbors.append((state[0] + 1, state[1]))

    
    if state[1] < len(document2):
        neighbors.append((state[0], state[1] + 1))

    return neighbors

def cost_to_neighbor(state1, state2, document1, document2):
    """Calculates the cost of transitioning from state1 to state2."""
    if state2[0] <= len(document1) and state2[1] <= len(document2):
        doc1_sentence2 = document1[state2[0] - 1] if state2[0] > 0 else ""
        doc2_sentence2 = document2[state2[1] - 1] if state2[1] > 0 else ""
        return levenshtein_distance(doc1_sentence2, doc2_sentence2)
    else:
        return float('inf')  

def heuristic(state, goal):
    """Estimates the cost of reaching the goal from the given state."""
    remaining_sentences_doc1 = len(document1) - state[0]
    remaining_sentences_doc2 = len(document2) - state[1]
    return remaining_sentences_doc1 + remaining_sentences_doc2

def preprocess_text(text):
    """Preprocesses the text by tokenizing and normalizing."""
    sentences = text.split('.')
    normalized_sentences = [sentence.lower().strip() for sentence in sentences]
    return normalized_sentences

def main():
    global document1, document2  

    
    with open(r'\document1.txt', 'r') as f:
        document1 = preprocess_text(f.read())
    with open(r'\document2.txt', 'r') as f:
        document2 = preprocess_text(f.read())

    
    start_state = (1, 1)
    goal_state = (len(document1), len(document2))

    
    alignment_path = a_star_search(start_state, goal_state, heuristic, document1, document2)

    
    if alignment_path is not None:
        for state in alignment_path:
            doc1_sentence = document1[state[0] - 1] if state[0] > 0 else ""
            doc2_sentence = document2[state[1] - 1] if state[1] > 0 else ""
            print(f"Document 1: {doc1_sentence}")
            print(f"Document 2: {doc2_sentence}")
            print()
    else:
        print("No valid alignment path found.")

if __name__ == '__main__':
    main()
