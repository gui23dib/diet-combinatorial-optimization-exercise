import numpy as np
from ant_colony.nutrition_dataframe import NutritionDataFrame

class ACO:
    def __init__(self, problem, n_ants, n_iterations, evaporation_rate, pheromone_initial, alpha=1, beta=1):
        self.problem: NutritionDataFrame = problem
        self.n_ants: int = n_ants
        self.n_iterations: int = n_iterations
        self.evaporation_rate: float = evaporation_rate
        self.pheromones: float = np.full(len(problem.foodlist), pheromone_initial)
        self.alpha: float = alpha
        self.beta: float = beta
        self.best_solution: float = None
        self.best_value: float = 0
        self.best_values: list[int] = []
        self.best_cal_values: list[int] = []

    def _construct_solution(self):
        """Construct a solution probabilistically under constraints."""
        visited = set()
        solution = []
        total_cost = 0
        while len(solution) < len(self.problem.foodlist):
            probabilities = np.array([
                (self.pheromones[i] ** self.alpha) * (1 / (self.problem.foodlist[i].calories + 1)) ** self.beta
                if i not in visited else 0
                for i in range(len(self.problem.foodlist))
            ])
            probabilities /= probabilities.sum() if probabilities.sum() > 0 else 1
            next_city = np.random.choice(range(len(self.problem.foodlist)), p=probabilities)
            
            # Check calories constraint
            next_cost = total_cost + self.problem.foodlist[next_city].calories
            if next_cost <= self.problem.max_calories:
                solution.append(next_city)
                visited.add(next_city)
                total_cost = next_cost
            else:
                break  # Stop adding foodlist if calories exceeds the budget
            
            # Stop if protein collected meet or exceed the target
            if sum(self.problem.foodlist[city].protein for city in solution) >= self.problem.target_macro:
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
            self.best_cal_values.append(sum(self.problem.foodlist[food].calories for food in self.best_solution))

        return self.best_solution, self.best_value, self.best_values, self.best_cal_values