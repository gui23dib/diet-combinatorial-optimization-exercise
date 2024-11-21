import numpy as np

class AntColonyOptimization:
    def __init__(self, problem, num_ants, num_iterations, alpha, beta, evaporation_rate, solution_max_size = 15):
        self.problem = problem
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.solution_max_size = solution_max_size
        self.pheromones = np.ones(len(problem.foodlist))
        self.best_solution = None
        self.best_value = float('-inf')
        self.best_values = []
        self.best_cal_values = []

    def _construct_solution(self):
        visited = set()
        visit_counts = {}
        solution = []
        total_cost = 0
        
        while len(solution) < self.solution_max_size:
            probabilities = np.array([
                (self.pheromones[i] ** self.alpha) * (1 / (self.problem.foodlist[i].calories + 1)) ** self.beta if i not in visited or visit_counts.get(i, 0) < 5 else 0
                for i in range(len(self.problem.foodlist))
            ])
            probabilities /= probabilities.sum() if probabilities.sum() > 0 else 1
            next_city = np.random.choice(range(len(self.problem.foodlist)), p=probabilities)
            
            next_cost = total_cost + self.problem.foodlist[next_city].calories
            if next_cost <= self.problem.max_calories:
                solution.append(next_city)
                visit_counts[next_city] = visit_counts.get(next_city, 0) + 1
                if visit_counts[next_city] >= 5:
                    visited.add(next_city)
                total_cost = next_cost
            else:
                break 
            
            # if sum(self.problem.foodlist[city].protein for city in solution) >= self.problem.target_macro:
            #     break
    
        return solution

    def _update_pheromones(self, solutions, values):
        self.pheromones *= (1 - self.evaporation_rate)  # Evaporation
        for solution, value in zip(solutions, values):
            for city in solution:
                self.pheromones[city] += value

    def run(self):
        for _ in range(self.num_iterations):
            solutions = []
            values = []
            for _ in range(self.num_ants):
                solution = self._construct_solution()
                value = self.problem.evaluate(solution)
                solutions.append(solution)
                values.append(value)
                if value > self.best_value:
                    self.best_value = value
                    self.best_solution = solution
            self._update_pheromones(solutions, values)
            self.best_values.append(self.best_value)
            self.best_cal_values.append(sum(self.problem.foodlist[city].calories for city in self.best_solution))
            
        print(self.best_solution)
        return self.best_solution, self.best_value, self.best_values, self.best_cal_values