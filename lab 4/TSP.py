import numpy as np
import random
import math


locations = {
    "Jaipur": (26.9124, 75.7873),
    "Udaipur": (24.5718, 73.6782),
    "Jodhpur": (26.2389, 73.5486), 
    "Jaisalmer": (26.9157, 70.9160),
    "Ajmer": (26.4520, 74.6399),
    "Pushkar": (26.4862, 74.5605),
    "Bikaner": (28.0228, 73.3178),
    "Mount Abu": (24.5920, 72.6780),
    "Chittorgarh": (24.8790, 74.6294),
    "Alwar": (27.5506, 76.6002),
    "Ranthambore": (26.0157, 76.4818),
    "Sawai Madhopur": (26.0201, 76.3604),
    "Kota": (25.2138, 75.8647),
    "Tonk": (26.0632, 75.7799),
    "Sikar": (27.6098, 75.1398),
    "Jhunjhunu": (28.1144, 75.5297),
    "Nagaur": (27.2040, 73.7360),
    "Barmer": (25.7496, 71.4339),
    "Dausa": (26.9292, 75.4098),
    "Bundi": (25.4483, 75.6284)
}


def calculate_distance(loc1, loc2):
    lat1, lon1 = loc1
    lat2, lon2 = loc2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


def create_distance_matrix(locations):
    loc_names = list(locations.keys())
    n = len(loc_names)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            distance_matrix[i][j] = calculate_distance(locations[loc_names[i]], locations[loc_names[j]])
    
    return distance_matrix, loc_names


def simulated_annealing(distance_matrix, loc_names, initial_temp=1000, cooling_rate=0.995, num_iterations=1000):
    current_solution = list(range(len(loc_names)))  
    current_distance = calculate_total_distance(current_solution, distance_matrix)
    best_solution = current_solution[:]
    best_distance = current_distance

    temperature = initial_temp

    for iteration in range(num_iterations):
        
        new_solution = current_solution[:]
        i, j = random.sample(range(len(loc_names)), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

        new_distance = calculate_total_distance(new_solution, distance_matrix)
        
        if acceptance_probability(current_distance, new_distance, temperature) > random.random():
            current_solution = new_solution
            current_distance = new_distance

        
        if current_distance < best_distance:
            best_solution = current_solution[:]
            best_distance = current_distance

        
        temperature *= cooling_rate

    return best_solution, best_distance


def calculate_total_distance(solution, distance_matrix):
    total_distance = 0
    for i in range(len(solution)):
        total_distance += distance_matrix[solution[i]][solution[(i + 1) % len(solution)]]
    return total_distance


def acceptance_probability(current_distance, new_distance, temperature):
    if new_distance < current_distance:
        return 1.0
    return math.exp((current_distance - new_distance) / temperature)


def main():
    distance_matrix, loc_names = create_distance_matrix(locations)
    best_solution, best_distance = simulated_annealing(distance_matrix, loc_names)

    
    print("Best Tour: ")
    for index in best_solution:
        print(loc_names[index], end=" -> ")
    print(loc_names[best_solution[0]])  
    print(f"Total Distance: {best_distance:.2f}")

if __name__ == "__main__":
    main()
