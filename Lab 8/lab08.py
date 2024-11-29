import numpy as np
from scipy.stats import poisson

# Problem Constants
MAX_BIKES = 20  # Max bikes at each location
MAX_TRANSFER = 5  # Max bikes that can be transferred
PARKING_LIMIT = 10  # Limit for free parking
FREE_TRANSFER = 1  # Number of bikes transferred for free

# Transition probabilities (simplified as deterministic for this example)
def poisson_rental(rate):
    return poisson.rvs(rate)  # Sample a Poisson random variable for rentals

def poisson_return(rate):
    return poisson.rvs(rate)  # Sample a Poisson random variable for returns

# Rewards calculation
def calculate_reward(s1, s2, action, rentals_s1, rentals_s2, returns_s1, returns_s2):
    # Bike rental reward (INR 10 per bike rented out)
    rental_reward = 10 * min(s1, rentals_s1) + 10 * min(s2, rentals_s2)

    # Cost of transferring bikes (INR 2 per bike moved)
    if action > 0:  # Moving bikes from Location 1 to Location 2
        transfer_cost = (action - FREE_TRANSFER) * 2 if action > FREE_TRANSFER else 0
    else:  # Moving bikes from Location 2 to Location 1
        transfer_cost = abs(action) * 2

    # Parking cost if more than 10 bikes are kept overnight
    parking_cost = (4 if s1 > PARKING_LIMIT else 0) + (4 if s2 > PARKING_LIMIT else 0)

    return rental_reward - transfer_cost - parking_cost

# Policy Iteration Algorithm
def policy_iteration():
    # State space: all combinations of bikes at location 1 and location 2
    states = [(s1, s2) for s1 in range(MAX_BIKES+1) for s2 in range(MAX_BIKES+1)]
    actions = range(-MAX_TRANSFER, MAX_TRANSFER+1)  # Actions range from -5 to 5
    
    # Initializing policy and value functions
    policy = np.zeros((MAX_BIKES+1, MAX_BIKES+1), dtype=int)  # Policy: action to take for each state
    value = np.zeros((MAX_BIKES+1, MAX_BIKES+1))  # Value function for each state

    # Policy Evaluation
    def policy_evaluation():
        # Value function update based on current policy
        epsilon = 1e-3
        gamma = 0.9  # Discount factor
        delta = float('inf')
        while delta > epsilon:
            delta = 0
            new_value = np.copy(value)
            for s1 in range(MAX_BIKES+1):
                for s2 in range(MAX_BIKES+1):
                    action = policy[s1, s2]
                    # Get rentals and returns for both locations
                    rentals_s1 = poisson_rental(3)  # Example: 3 expected rentals at Location 1
                    rentals_s2 = poisson_rental(4)  # Example: 4 expected rentals at Location 2
                    returns_s1 = poisson_return(3)  # Example: 3 expected returns at Location 1
                    returns_s2 = poisson_return(2)  # Example: 2 expected returns at Location 2

                    # Apply action and calculate new state
                    new_s1 = min(MAX_BIKES, max(0, s1 - action + returns_s1))  # New state at Location 1
                    new_s2 = min(MAX_BIKES, max(0, s2 + action + returns_s2))  # New state at Location 2

                    # Reward for taking the action
                    reward = calculate_reward(s1, s2, action, rentals_s1, rentals_s2, returns_s1, returns_s2)
                    # Bellman update for value function
                    new_value[s1, s2] = reward + gamma * value[new_s1, new_s2]
                    delta = max(delta, abs(new_value[s1, s2] - value[s1, s2]))
            value[:] = new_value
            return value
    
    # Policy Improvement
    def policy_improvement():
        stable = True
        for s1 in range(MAX_BIKES+1):
            for s2 in range(MAX_BIKES+1):
                old_action = policy[s1, s2]
                # Find the best action for current state (greedy policy)
                best_action = None
                best_value = float('-inf')
                for action in actions:
                    # Get rentals and returns for both locations
                    rentals_s1 = poisson_rental(3)  # Example: 3 expected rentals at Location 1
                    rentals_s2 = poisson_rental(4)  # Example: 4 expected rentals at Location 2
                    returns_s1 = poisson_return(3)  # Example: 3 expected returns at Location 1
                    returns_s2 = poisson_return(2)  # Example: 2 expected returns at Location 2

                    # Apply action and calculate new state
                    new_s1 = min(MAX_BIKES, max(0, s1 - action + returns_s1))  # New state at Location 1
                    new_s2 = min(MAX_BIKES, max(0, s2 + action + returns_s2))  # New state at Location 2

                    # Reward for taking the action
                    reward = calculate_reward(s1, s2, action, rentals_s1, rentals_s2, returns_s1, returns_s2)
                    # Calculate the expected value
                    expected_value = reward + 0.9 * value[new_s1, new_s2]
                    if expected_value > best_value:
                        best_value = expected_value
                        best_action = action
                # Update policy
                policy[s1, s2] = best_action
                if old_action != best_action:
                    stable = False
        return stable

    # Run Policy Iteration
    iteration = 0
    while True:
        print(f"Iteration {iteration}:")
        policy_evaluation()
        if policy_improvement():
            print("Policy stable, stopping iteration.")
            break
        iteration += 1

    return policy, value

# Run Policy Iteration
policy, value = policy_iteration()

# Output the optimal policy and value function
print("Optimal Policy:")
print(policy)
print("Optimal Value Function:")
print(value)
