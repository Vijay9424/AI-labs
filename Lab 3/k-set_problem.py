import random

def generate_k_sat(k, m, n):
    clauses = set()
    
    while len(clauses) < m:
        clause = random.sample(range(1, n + 1), k)
        
        clause = [x if random.choice([True, False]) else -x for x in clause]
        clauses.add(tuple(sorted(clause)))

    return list(clauses)

if __name__ == "__main__":
    k = 3  
    m = 5  
    n = 10  
    
    sat_problem = generate_k_sat(k, m, n)
    print("Generated k-SAT Problem:")
    for clause in sat_problem:
        print(clause)
