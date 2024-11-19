import numpy as np
import matplotlib.pyplot as plt

class TravelerProblem:
    def __init__(self, n_cities, star_range=(0, 25), cost_range=(100, 1000)):
        """Initialize the problem with cities, stars, and costs."""
        self.n_cities = n_cities
        self.stars = [20, 30, 30, 10, 15, 20, 60, 80, 10, 45]  #np.random.randint(star_range[0], star_range[1] + 1, size=n_cities)
        self.costs = [400, 200, 300, 100, 100, 100, 900, 230, 320, 400] #np.random.randint(cost_range[0], cost_range[1] + 1, size=n_cities)
        self.target_stars = 100
        self.max_budget = 5000

    def evaluate(self, solution):
        """Evaluate a solution based on stars and cost constraints."""
        total_stars = sum(self.stars[city] for city in solution)
        total_cost = sum(self.costs[city] for city in solution)
        if total_cost > self.max_budget:
            return 0  # Invalid solution
        return total_stars

class ACOTraveler:
    def __init__(self, problem, n_ants, n_iterations, evaporation_rate, pheromone_initial, alpha=1, beta=1):
        self.problem = problem
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.evaporation_rate = evaporation_rate
        self.pheromones = np.full(problem.n_cities, pheromone_initial)
        self.alpha = alpha
        self.beta = beta
        self.best_solution = None
        self.best_value = 0
        self.best_values = []

    def _construct_solution(self):
        """Construct a solution probabilistically under constraints."""
        visited = set()
        solution = []
        total_cost = 0
        while len(solution) < self.problem.n_cities:
            probabilities = np.array([
                (self.pheromones[i] ** self.alpha) * (1 / (self.problem.costs[i] + 1)) ** self.beta
                if i not in visited else 0
                for i in range(self.problem.n_cities)
            ])
            probabilities /= probabilities.sum() if probabilities.sum() > 0 else 1
            next_city = np.random.choice(range(self.problem.n_cities), p=probabilities)
            
            # Check cost constraint
            next_cost = total_cost + self.problem.costs[next_city]
            if next_cost <= self.problem.max_budget:
                solution.append(next_city)
                visited.add(next_city)
                total_cost = next_cost
            else:
                break  # Stop adding cities if cost exceeds the budget
            
            # Stop if stars collected meet or exceed the target
            if sum(self.problem.stars[city] for city in solution) >= self.problem.target_stars:
                break
        return solution

    def _update_pheromones(self, solutions, values):
        """Update pheromones based on solutions and their values."""
        self.pheromones *= (1 - self.evaporation_rate)  # Evaporation
        for solution, value in zip(solutions, values):
            for city in solution:
                self.pheromones[city] += value

    def optimize(self):
        """Run the ACO algorithm."""
        for _ in range(self.n_iterations):
            solutions = [self._construct_solution() for _ in range(self.n_ants)]
            values = [self.problem.evaluate(sol) for sol in solutions]
            
            max_value = max(values)
            if max_value > self.best_value:
                self.best_value = max_value
                self.best_solution = solutions[np.argmax(values)]
            
            self._update_pheromones(solutions, values)
            self.best_values.append(self.best_value)

        return self.best_solution, self.best_value, self.best_values

# Problem definition
n_cities = 10  # Number of cities
problem = TravelerProblem(n_cities)

print("Stars in each city:", problem.stars)
print("Costs in each city:", problem.costs)

# Define ACO parameters and solve
aco = ACOTraveler(problem, n_ants=20, n_iterations=100, evaporation_rate=0.1, pheromone_initial=1.0)
best_solution, best_value, best_values = aco.optimize()

# Results
print("Best Solution (Cities):", best_solution)
print("Stars Collected:", best_value)
print("Total Cost:", sum(problem.costs[city] for city in best_solution))

# Visualization
plt.figure(figsize=(12, 5))

# Convergence plot
plt.subplot(1, 2, 1)
plt.plot(best_values, marker='o', color='blue')
plt.title("Convergence of ACO")
plt.xlabel("Iteration")
plt.ylabel("Best Stars Collected")

# Pheromone levels
plt.subplot(1, 2, 2)
plt.bar(range(problem.n_cities), aco.pheromones, color='green', alpha=0.7)
plt.title("Pheromone Levels for Cities")
plt.xlabel("City")
plt.ylabel("Pheromone Strength")
plt.xticks(range(problem.n_cities), [f"City {i+1}" for i in range(problem.n_cities)])

plt.tight_layout()
plt.show()
